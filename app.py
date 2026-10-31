#!/usr/bin/env python3
"""
Buku Tamu Digital Kampus (Digital Guestbook) - Backend Service
Mata Kuliah: Cloud Computing (Ujian Chunin UTS) - Telkom University
Sesuai Dokumen Panduan: Pilihan Studi Kasus No. 1
"""

import os
import sys
import json
import uuid
import threading
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ==========================================
# Konfigurasi Lingkungan & Penyimpanan
# ==========================================
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")

# Menentukan lokasi direktori data:
# - Dalam kontainer Docker: default ke /var/lib/backend_data (Named Volume guestbook-db-data)
# - Pada lingkungan host/pengembangan lokal: fallback aman ke direktori ./data
DEFAULT_DATA_DIR = "/var/lib/backend_data" if os.name != "nt" else os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DATA_DIR = os.getenv("DATA_DIR", DEFAULT_DATA_DIR)
DATA_FILE = os.getenv("DATA_FILE", os.path.join(DATA_DIR, "guestbook.json"))

# Kunci konkurensi untuk thread-safety penulisan data JSON
storage_lock = threading.Lock()

# Batas maksimum ukuran payload (16 KiB)
MAX_PAYLOAD_SIZE = 16 * 1024


def init_storage():
    """Menginisialisasi direktori dan berkas guestbook.json dengan aman."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
            with open(DATA_FILE + ".tmp", "w", encoding="utf-8") as f:
                json.dump([], f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(DATA_FILE + ".tmp", DATA_FILE)
            print(f"[STORAGE] Inisialisasi berkas database baru: {DATA_FILE}")
        else:
            # Validasi keterbacaan JSON
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("Root JSON bukan bertipe array/list")
            print(f"[STORAGE] Berkas database terverifikasi ({len(data)} entri): {DATA_FILE}")
    except Exception as e:
        print(f"[STORAGE ERROR] Gagal menginisialisasi penyimpanan di {DATA_FILE}: {e}", file=sys.stderr)
        raise e


def read_entries():
    """Membaca seluruh entri tamu dari guestbook.json di bawah proteksi thread lock."""
    with storage_lock:
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Format berkas database rusak (bukan array)")
            return data


def write_entries_atomic(entries):
    """Menulis seluruh entri tamu ke file sementara lalu menggantinya secara atomik."""
    with storage_lock:
        os.makedirs(DATA_DIR, exist_ok=True)
        tmp_file = DATA_FILE + ".tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        # Penggantian atomik (menjamin file tidak pernah korup jika sistem crash)
        os.replace(tmp_file, DATA_FILE)


class GuestbookRequestHandler(BaseHTTPRequestHandler):
    """Handler HTTP Request untuk layanan REST API Buku Tamu Digital."""

    server_version = "CampusGuestbook/1.0"

    def _set_cors_headers(self):
        """Menambahkan header CORS lengkap untuk interoperabilitas."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")

    def _send_json(self, status_code, payload):
        """Mengirimkan respons HTTP dengan payload berformat JSON."""
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, status_code, error_code, message):
        """Mengirimkan respons error terstandar sesuai spesifikasi PRD."""
        self._send_json(status_code, {
            "status": "error",
            "error": {
                "code": error_code,
                "message": message
            }
        })

    def do_OPTIONS(self):
        """Menangani permintaan CORS preflight."""
        self.send_response(204)
        self._set_cors_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        """Menangani permintaan HTTP GET untuk /messages dan /health."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path.rstrip("/")

        # Normalisasi path untuk mendukung akses langsung atau via proxy /api/*
        if path in ("/health", "/api/health"):
            self.handle_health()
        elif path in ("/messages", "/api/messages"):
            self.handle_get_messages()
        else:
            self._send_error_json(404, "ROUTE_NOT_FOUND", f"Endpoint '{self.path}' tidak ditemukan pada server.")

    def do_POST(self):
        """Menangani permintaan HTTP POST untuk menambahkan tamu baru ke /messages."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path.rstrip("/")

        if path in ("/messages", "/api/messages"):
            self.handle_post_messages()
        else:
            self._send_error_json(404, "ROUTE_NOT_FOUND", f"Endpoint '{self.path}' tidak ditemukan pada server.")

    def do_DELETE(self):
        """Menangani permintaan HTTP DELETE untuk menghapus entri tamu berbasis index."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path.rstrip("/")

        if path in ("/messages", "/api/messages"):
            self.handle_delete_messages(parsed_url.query)
        else:
            self._send_error_json(404, "ROUTE_NOT_FOUND", f"Endpoint '{self.path}' tidak ditemukan pada server.")

    def handle_health(self):
        """Handler endpoint Health Check (/health) untuk Docker & Jenkins."""
        try:
            entries = read_entries()
            self._send_json(200, {
                "status": "UP",
                "service": "guestbook-backend",
                "storage_path": DATA_FILE,
                "storage_writable": os.access(DATA_DIR, os.W_OK),
                "total_entries": len(entries),
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            })
        except Exception as e:
            self._send_error_json(500, "STORAGE_ERROR", f"Pemeriksaan kesehatan sistem gagal: {str(e)}")

    def handle_get_messages(self):
        """Handler endpoint GET /messages untuk menampilkan daftar seluruh tamu."""
        try:
            entries = read_entries()
            # Hitung index sementara (0..N-1) secara dinamis sesuai posisi array
            messages_with_index = []
            for idx, item in enumerate(entries):
                entry_copy = dict(item)
                entry_copy["index"] = idx
                messages_with_index.append(entry_copy)

            self._send_json(200, {
                "status": "success",
                "total": len(messages_with_index),
                "messages": messages_with_index
            })
        except Exception as e:
            self._send_error_json(500, "STORAGE_ERROR", f"Gagal membaca data buku tamu: {str(e)}")

    def handle_post_messages(self):
        """Handler endpoint POST /messages untuk registrasi tamu baru."""
        # 1. Validasi Header Content-Type
        content_type = self.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            self._send_error_json(
                415,
                "UNSUPPORTED_MEDIA_TYPE",
                "Header 'Content-Type' harus bernilai 'application/json'."
            )
            return

        # 2. Validasi Ukuran Payload (Content-Length)
        content_length_header = self.headers.get("Content-Length")
        if not content_length_header:
            self._send_error_json(411, "LENGTH_REQUIRED", "Header 'Content-Length' wajib disertakan.")
            return

        try:
            content_length = int(content_length_header)
        except ValueError:
            self._send_error_json(400, "INVALID_CONTENT_LENGTH", "Header 'Content-Length' tidak valid.")
            return

        if content_length > MAX_PAYLOAD_SIZE:
            self._send_error_json(
                413,
                "PAYLOAD_TOO_LARGE",
                f"Ukuran payload ({content_length} bytes) melebihi batas maksimum 16 KiB."
            )
            return

        # 3. Baca dan Parsing Body JSON
        try:
            body_bytes = self.rfile.read(content_length)
            payload = json.loads(body_bytes.decode("utf-8"))
        except json.JSONDecodeError as err:
            self._send_error_json(400, "INVALID_JSON", f"Format body request bukan JSON yang valid: {str(err)}")
            return
        except Exception as err:
            self._send_error_json(400, "REQUEST_READ_ERROR", f"Gagal membaca body request: {str(err)}")
            return

        if not isinstance(payload, dict):
            self._send_error_json(400, "INVALID_PAYLOAD", "Payload JSON harus berupa sebuah Object {}.")
            return

        # 4. Validasi Nilai Field Wajib (name, institution, purpose)
        name = payload.get("name")
        institution = payload.get("institution")
        purpose = payload.get("purpose")

        if not isinstance(name, str) or not name.strip():
            self._send_error_json(
                400,
                "VALIDATION_ERROR",
                "Field 'name' wajib diisi berupa teks nama pengunjung (1-100 karakter)."
            )
            return

        name = name.strip()
        if len(name) > 100:
            self._send_error_json(
                400,
                "VALIDATION_ERROR",
                f"Field 'name' terlalu panjang ({len(name)} karakter, maksimum 100 karakter)."
            )
            return

        if not isinstance(institution, str) or not institution.strip():
            self._send_error_json(
                400,
                "VALIDATION_ERROR",
                "Field 'institution' wajib diisi (1-150 karakter, gunakan 'Umum' bila hadir secara pribadi)."
            )
            return

        institution = institution.strip()
        if len(institution) > 150:
            self._send_error_json(
                400,
                "VALIDATION_ERROR",
                f"Field 'institution' terlalu panjang ({len(institution)} karakter, maksimum 150 karakter)."
            )
            return

        if not isinstance(purpose, str) or not purpose.strip():
            self._send_error_json(
                400,
                "VALIDATION_ERROR",
                "Field 'purpose' wajib diisi dengan keperluan/tujuan kunjungan (1-300 karakter)."
            )
            return

        purpose = purpose.strip()
        if len(purpose) > 300:
            self._send_error_json(
                400,
                "VALIDATION_ERROR",
                f"Field 'purpose' terlalu panjang ({len(purpose)} karakter, maksimum 300 karakter)."
            )
            return

        # 5. Pembuatan Entri Baru
        new_entry = {
            "id": str(uuid.uuid4()),
            "name": name,
            "institution": institution,
            "purpose": purpose,
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        # 6. Simpan secara Atomik ke File JSON di Named Volume
        try:
            entries = read_entries()
            assigned_index = len(entries)
            entries.append(new_entry)
            write_entries_atomic(entries)

            response_data = dict(new_entry)
            response_data["index"] = assigned_index

            self._send_json(201, {
                "status": "success",
                "message": "Entri buku tamu berhasil ditambahkan.",
                "data": response_data
            })
        except Exception as e:
            self._send_error_json(500, "STORAGE_ERROR", f"Gagal menyimpan data tamu ke volume: {str(e)}")

    def handle_delete_messages(self, query_string):
        """Handler endpoint DELETE /messages?index=X untuk menghapus entri tamu."""
        # 1. Ekstraksi Query Parameter 'index'
        params = parse_qs(query_string)
        if "index" not in params or not params["index"][0].strip():
            self._send_error_json(
                400,
                "MISSING_INDEX",
                "Parameter 'index' wajib disertakan pada query URL (contoh: DELETE /messages?index=0)."
            )
            return

        index_raw = params["index"][0].strip()

        # 2. Validasi Format Index (Harus Bilangan Bulat Non-Negatif)
        try:
            target_index = int(index_raw)
        except ValueError:
            self._send_error_json(
                400,
                "INVALID_INDEX",
                f"Parameter 'index' harus berupa bilangan bulat valid, bukan '{index_raw}'."
            )
            return

        if target_index < 0:
            self._send_error_json(
                400,
                "INVALID_INDEX",
                "Parameter 'index' tidak boleh bernilai negatif."
            )
            return

        # 3. Lakukan Penghapusan di Bawah Lock
        try:
            entries = read_entries()
            total_current = len(entries)

            if target_index >= total_current:
                self._send_error_json(
                    404,
                    "INDEX_OUT_OF_RANGE",
                    f"Entri tamu pada index {target_index} tidak ditemukan (total entri saat ini: {total_current})."
                )
                return

            deleted_item = entries.pop(target_index)
            write_entries_atomic(entries)

            self._send_json(200, {
                "status": "success",
                "message": f"Entri tamu pada index {target_index} berhasil dihapus.",
                "deleted": deleted_item,
                "total": len(entries)
            })
        except Exception as e:
            self._send_error_json(500, "STORAGE_ERROR", f"Gagal memproses penghapusan data tamu: {str(e)}")

    def log_message(self, format, *args):
        """Kustomisasi format log server agar rapi dan informatif."""
        sys.stdout.write(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"{self.address_string()} - {format % args}\n"
        )
        sys.stdout.flush()


def run_server(server_class=HTTPServer, handler_class=GuestbookRequestHandler):
    """Menjalankan HTTP server."""
    init_storage()
    server_address = (HOST, PORT)
    httpd = server_class(server_address, handler_class)
    print("=" * 65)
    print(f" Buku Tamu Digital Kampus — Backend REST API")
    print(f" URL Server      : http://{HOST}:{PORT}")
    print(f" Storage Path    : {DATA_FILE}")
    print(" Siap menerima koneksi (GET, POST, DELETE, /health)...")
    print("=" * 65)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server dimatikan oleh pengguna.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    run_server()
