#!/usr/bin/env python3
"""
Unit Test Komprehensif untuk Backend REST API Buku Tamu Digital Kampus
Mata Kuliah: Cloud Computing (Ujian Chunin UTS)
"""

import os
import json
import shutil
import tempfile
import unittest
import threading
from http.server import HTTPServer
import urllib.request
import urllib.error
import urllib.parse

# Impor komponen dari app.py
import app


class TestGuestbookAPI(unittest.TestCase):
    """Test suite untuk menguji seluruh fungsionalitas REST API app.py."""

    @classmethod
    def setUpClass(cls):
        """Menyiapkan server pengujian di port dinamis dengan direktori temporary."""
        cls.test_dir = tempfile.mkdtemp(prefix="test_guestbook_")
        cls.test_file = os.path.join(cls.test_dir, "guestbook.json")

        # Set environment variable untuk tes
        app.DATA_DIR = cls.test_dir
        app.DATA_FILE = cls.test_file

        # Gunakan port 0 agar OS memilih port yang kosong otomatis
        cls.server = HTTPServer(("127.0.0.1", 0), app.GuestbookRequestHandler)
        cls.port = cls.server.server_address[1]
        cls.base_url = f"http://127.0.0.1:{cls.port}"

        # Jalankan server di background thread
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        """Mematikan server dan membersihkan direktori temporary."""
        cls.server.shutdown()
        cls.server.server_close()
        shutil.rmtree(cls.test_dir, ignore_errors=True)

    def setUp(self):
        """Reset berkas database JSON ke array kosong sebelum setiap tes."""
        app.write_entries_atomic([])

    def _request(self, method, path, data=None, headers=None):
        """Helper untuk mengirimkan HTTP request dan membaca hasilnya."""
        url = self.base_url + path
        req_headers = headers if headers is not None else {}
        body = None
        if data is not None:
            if isinstance(data, dict):
                body = json.dumps(data).encode("utf-8")
                if "Content-Type" not in req_headers:
                    req_headers["Content-Type"] = "application/json"
            elif isinstance(data, (bytes, str)):
                body = data if isinstance(data, bytes) else data.encode("utf-8")

        req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                resp_body = resp.read().decode("utf-8")
                return resp.status, json.loads(resp_body) if resp_body else None, resp.headers
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            return e.code, json.loads(err_body) if err_body else None, e.headers

    def test_01_health_check(self):
        """Verifikasi endpoint GET /health mengembalikan 200 OK dan status UP."""
        status, payload, _ = self._request("GET", "/health")
        self.assertEqual(status, 200)
        self.assertEqual(payload["status"], "UP")
        self.assertEqual(payload["service"], "guestbook-backend")
        self.assertTrue(payload["storage_writable"])

    def test_02_get_empty_messages(self):
        """Verifikasi GET /messages pada kondisi database kosong mengembalikan total 0."""
        status, payload, _ = self._request("GET", "/messages")
        self.assertEqual(status, 200)
        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["total"], 0)
        self.assertEqual(payload["messages"], [])

    def test_03_post_valid_message(self):
        """Verifikasi POST /messages dengan data valid menghasilkan 201 Created."""
        data = {
            "name": "Budi Santoso",
            "institution": "Telkom University",
            "purpose": "Menghadiri Seminar Cloud Computing"
        }
        status, payload, _ = self._request("POST", "/messages", data=data)
        self.assertEqual(status, 201)
        self.assertEqual(payload["status"], "success")
        self.assertIn("data", payload)
        self.assertEqual(payload["data"]["name"], "Budi Santoso")
        self.assertEqual(payload["data"]["index"], 0)
        self.assertTrue(len(payload["data"]["id"]) > 20)  # Valid UUID
        self.assertTrue(payload["data"]["created_at"].endswith("Z"))

    def test_04_get_messages_with_data(self):
        """Verifikasi GET /messages mengembalikan daftar dan kalkulasi index yang benar."""
        # Masukkan 2 entri
        self._request("POST", "/messages", {"name": "Tamu 1", "institution": "Telkom", "purpose": "Acara 1"})
        self._request("POST", "/messages", {"name": "Tamu 2", "institution": "ITB", "purpose": "Acara 2"})

        status, payload, _ = self._request("GET", "/messages")
        self.assertEqual(status, 200)
        self.assertEqual(payload["total"], 2)
        self.assertEqual(payload["messages"][0]["index"], 0)
        self.assertEqual(payload["messages"][0]["name"], "Tamu 1")
        self.assertEqual(payload["messages"][1]["index"], 1)
        self.assertEqual(payload["messages"][1]["name"], "Tamu 2")

    def test_05_post_validation_empty_or_whitespace(self):
        """Verifikasi POST ditolak dengan 400 Bad Request jika field kosong atau hanya spasi."""
        test_cases = [
            {"name": "   ", "institution": "Telkom", "purpose": "Seminar"},
            {"name": "Budi", "institution": "", "purpose": "Seminar"},
            {"name": "Budi", "institution": "Telkom", "purpose": "   "}
        ]
        for tc in test_cases:
            status, payload, _ = self._request("POST", "/messages", data=tc)
            self.assertEqual(status, 400)
            self.assertEqual(payload["status"], "error")
            self.assertEqual(payload["error"]["code"], "VALIDATION_ERROR")

    def test_06_post_validation_length_exceeded(self):
        """Verifikasi POST ditolak dengan 400 jika field melebihi panjang maksimum."""
        data = {
            "name": "A" * 101,  # max 100
            "institution": "Telkom",
            "purpose": "Seminar"
        }
        status, payload, _ = self._request("POST", "/messages", data=data)
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"]["code"], "VALIDATION_ERROR")

    def test_07_post_unsupported_media_type(self):
        """Verifikasi POST ditolak dengan 415 jika Content-Type bukan application/json."""
        headers = {"Content-Type": "text/plain"}
        status, payload, _ = self._request("POST", "/messages", data="plain text data", headers=headers)
        self.assertEqual(status, 415)
        self.assertEqual(payload["error"]["code"], "UNSUPPORTED_MEDIA_TYPE")

    def test_08_delete_valid_message_and_index_shift(self):
        """Verifikasi DELETE /messages?index=X berhasil 200 dan menggeser indeks sisa."""
        # Masukkan 3 entri
        self._request("POST", "/messages", {"name": "Tamu 0", "institution": "A", "purpose": "P0"})
        self._request("POST", "/messages", {"name": "Tamu 1", "institution": "B", "purpose": "P1"})
        self._request("POST", "/messages", {"name": "Tamu 2", "institution": "C", "purpose": "P2"})

        # Hapus index 1 ("Tamu 1")
        status, payload, _ = self._request("DELETE", "/messages?index=1")
        self.assertEqual(status, 200)
        self.assertEqual(payload["deleted"]["name"], "Tamu 1")
        self.assertEqual(payload["total"], 2)

        # Verifikasi urutan index baru saat GET
        status, get_payload, _ = self._request("GET", "/messages")
        self.assertEqual(get_payload["total"], 2)
        self.assertEqual(get_payload["messages"][0]["name"], "Tamu 0")
        self.assertEqual(get_payload["messages"][0]["index"], 0)
        self.assertEqual(get_payload["messages"][1]["name"], "Tamu 2")
        self.assertEqual(get_payload["messages"][1]["index"], 1)

    def test_09_delete_negative_index(self):
        """Verifikasi DELETE dengan index negatif ditolak dengan 400 Bad Request."""
        status, payload, _ = self._request("DELETE", "/messages?index=-1")
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"]["code"], "INVALID_INDEX")

    def test_10_delete_non_integer_index(self):
        """Verifikasi DELETE dengan index bukan angka ditolak dengan 400 Bad Request."""
        status, payload, _ = self._request("DELETE", "/messages?index=abc")
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"]["code"], "INVALID_INDEX")

    def test_11_delete_out_of_range(self):
        """Verifikasi DELETE dengan index di luar jangkauan mengembalikan 404 Not Found."""
        status, payload, _ = self._request("DELETE", "/messages?index=99")
        self.assertEqual(status, 404)
        self.assertEqual(payload["error"]["code"], "INDEX_OUT_OF_RANGE")

    def test_12_route_not_found(self):
        """Verifikasi pemanggilan route tidak dikenal menghasilkan 404 ROUTE_NOT_FOUND."""
        status, payload, _ = self._request("GET", "/unknown-route")
        self.assertEqual(status, 404)
        self.assertEqual(payload["error"]["code"], "ROUTE_NOT_FOUND")

    def test_13_cors_preflight(self):
        """Verifikasi OPTIONS /messages mengembalikan 204 No Content dengan header CORS."""
        req = urllib.request.Request(self.base_url + "/messages", method="OPTIONS")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 204)
            self.assertEqual(resp.headers.get("Access-Control-Allow-Origin"), "*")
            self.assertIn("DELETE", resp.headers.get("Access-Control-Allow-Methods"))


if __name__ == "__main__":
    unittest.main()
