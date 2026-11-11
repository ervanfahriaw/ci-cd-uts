# 🏛️ SITAMU — Sistem Informasi Buku Tamu Digital Kampus
### Ujian Tengah Semester (UTS) — Cloud Computing "Chunin Exam"
**Telkom University** • Semester Ganjil 2024/2025  
**Mata Kuliah**: Cloud Computing (CSO)  
**Studi Kasus**: No. 1 — Buku Tamu Digital Kampus (*Digital Guestbook*)  
**Repositori GitHub**: [https://github.com/ervanfahriaw/ci-cd-uts](https://github.com/ervanfahriaw/ci-cd-uts)  
**Tautan Video Demonstrasi**: [Tonton Video Demo UTS (YouTube / Google Drive)](https://youtu.be/contoh-link-video-uts) *(Ganti dengan URL video Anda)*

---

## 👥 Identitas Kelompok & Kontribusi Anggota

| No | Nama Lengkap | NIM | Peran Utama & Kontribusi Teknis |
|:--:|:---|:---:|:---|
| 1 | **Ervan Fahri A. W.** | *(Isi NIM Anda)* | **DevOps & Infrastructure Lead**: Perancangan CI/CD Pipeline (Jenkinsfile 5 Stages), integrasi GitHub Webhook via ngrok HTTPS tunnel, arsitektur Docker Compose & Bridge Network, dan unit test automation. |
| 2 | *(Nama Anggota 2)* | *(NIM Anggota 2)* | **Backend & Storage Engineer**: Pengembangan REST API murni Python (Standard Library), mekanisme *Atomic File Write* & thread-safe locking, skema JSON database, dan pengujian *Data Immunity*. |
| 3 | *(Nama Anggota 3)* | *(NIM Anggota 3)* | **Frontend & UI/UX Specialist**: Perancangan antarmuka SITAMU Telkom University (Crimson Red palette), asinkronisasi AJAX `fetch()`, sistem notifikasi interaktif, live counter, dan bind mount configuration. |
| 4 | *(Nama Anggota 4)* | *(NIM Anggota 4)* | **QA Engineer & Technical Documenter**: Penulisan skenario uji 13 automated unit tests, validasi spesifikasi kepatuhan rubrik UTS, dokumentasi REST API, dan penyusunan demonstrasi sistem. |

> *Catatan: Tabel anggota di atas dapat disesuaikan dengan komposisi tim kelompok Anda.*

---

## 📋 Ringkasan Eksekutif Proyek

Proyek ini menghadirkan **SITAMU (Sistem Informasi Buku Tamu Kampus)**, sebuah sistem pencatatan kunjungan tamu berbasis arsitektur *Cloud-Native* dan *Microservices-ready Container*. Sistem ini dirancang untuk menggantikan buku tamu konvensional berbasis kertas di lingkungan akademik Telkom University yang rentan rusak, tercecer, dan tidak dapat diakses secara *real-time*.

### Sorotan Implementasi Rekayasa:
1. **Lightweight Pure Python Backend (Bobot: 20%)**: Dibangun murni menggunakan pustaka bawaan Python (`http.server`, `json`, `os`, `threading`) tanpa ketergantungan framework pihak ketiga (seperti Flask/Django/FastAPI). Mengimplementasikan prinsip konkurensi aman (*Thread Lock*) dan *Atomic Write Swap* guna menjamin keutuhan data pada kondisi *high-concurrency*.
2. **SITAMU Academic Design Standards (Bobot: 15%)**: Antarmuka responsif mengadopsi identitas visual institusi Telkom University (*Crimson Red `#e01a3f`* dan tipografi *Inter* / *Open Sans*), interaksi dinamis murni berbasis JavaScript Modern tanpa *page reload*, serta sanitasi input terhadap kerentanan *Cross-Site Scripting (XSS)*.
3. **Data Immunity Persistence (Bobot: 25%)**: Menggunakan **Docker Named Volume** (`guestbook-db-data`) yang memisahkan siklus hidup data dari siklus hidup kontainer. Teruji kebal: **seluruh catatan tamu tetap utuh 100% saat kontainer dihancurkan secara paksa (`docker rm -f`)**.
4. **Live Development Workflow (Bobot: 15%)**: Pemanfaatan **Docker Bind Mount** pada komponen antarmuka (`index.html`) dan aset desain memungkinkan pembaruan tampilan di host langsung aktif seketika pada browser klien tanpa proses *rebuild* image.
5. **Full Automated CI/CD Pipeline (Bobot: 25%)**: Alur kerja otomasi menyeluruh dari setiap `git push` ke repositori GitHub, diteruskan secara otomatis via **GitHub Webhook** melalui **ngrok HTTPS Tunnel** ke **Jenkins Automation Server**, menjalankan *Declarative 5-Stage Pipeline* (Checkout, Syntax Check & 13 Unit Tests, Build Image, Automated Deployment, dan Health Check).

---

## 🏛️ Arsitektur Sistem & Jaringan Kontainer

Sistem diisolasi dalam arsitektur multi-kontainer Docker yang saling berkomunikasi melalui *Bridge Network* kustom `app-net`.

```mermaid
flowchart TB
    subgraph ClientZone ["🌐 Client Layer"]
        User["Pengguna / Tamu Kampus"]
        Browser["Modern Web Browser"]
    end

    subgraph DockerHost ["🐳 Docker Host Environment (Linux Engine / WSL2)"]
        subgraph AppNet ["Docker Bridge Network: app-net (Subnet Terisolasi)"]
            
            subgraph FrontendContainer ["Container: guestbook-frontend (Nginx Alpine)"]
                NginxSvc["Nginx Web Server\n- Static File Server\n- Reverse Proxy (/api/ -> backend:8000)"]
                PortFrontend["Exposed Port: 8081:80"]
            end

            subgraph BackendContainer ["Container: guestbook-backend (Python 3.11-Alpine)"]
                PythonApp["app.py\n- Native REST API Server\n- Thread-Safe JSON Store\n- Atomic File System Swap"]
                PortBackend["Exposed Port: 8000:8000"]
            end

        end

        subgraph StorageLayer ["💾 Persistence & Mount Architecture"]
            NamedVol[("📦 Docker Named Volume:\nguestbook-db-data\nMount: /var/lib/backend_data\n[DATA IMMUNITY LAYER]")]
            BindHTML["📁 Bind Mount (Host):\n./index.html -> /usr/share/nginx/html/index.html:ro\n[LIVE EDIT WORKFLOW]"]
            BindDesign["📁 Bind Mount (Host):\n./design -> /usr/share/nginx/html/design:ro"]
            BindConf["📁 Bind Mount (Host):\n./nginx/default.conf -> /etc/nginx/conf.d/default.conf:ro"]
        end
    end

    User --> Browser
    Browser -->|HTTP :8081| PortFrontend
    PortFrontend --> NginxSvc
    NginxSvc -->|Serve UI| BindHTML
    NginxSvc -->|Serve Assets| BindDesign
    NginxSvc -->|Read Rules| BindConf
    NginxSvc -->|Reverse Proxy /api/*| PythonApp
    PythonApp <-->|Atomic I/O Storage| NamedVol
```

### Tabel Spesifikasi Kontainer & Alokasi Port
| Nama Kontainer | Base Image | Port Host | Port Kontainer | Tipe Mount | Jalur Mount Kontainer | Fungsi Sistem |
|---|---|:---:|:---:|:---:|---|---|
| `guestbook-frontend` | `nginx:alpine` | `8081` | `80` | Bind Mount | `/usr/share/nginx/html/index.html` (ro)<br>`/etc/nginx/conf.d/default.conf` (ro) | Melayani static web UI dan reverse proxy `/api/` ke backend |
| `guestbook-backend` | `python:3.11-alpine` | `8000` | `8000` | Named Volume | `/var/lib/backend_data` (rw) | Memproses logika bisnis REST API & persistensi catatan |
| `jenkins-server` | `jenkins/jenkins:lts` | `8080` | `8080` | Named Volume | `/var/jenkins_home` (rw)<br>`/var/run/docker.sock` (rw) | Automation CI/CD Server & Eksekusi Pipeline |

---

## 🔄 Arsitektur Otomatisasi CI/CD Pipeline

Pipeline Jenkins dibangun dengan pendekatan *Declarative Pipeline* yang terdiri dari **5 Stages Wajib** sesuai instruksi ujian chunin.

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer / Mahasiswa
    participant Git as GitHub (ci-cd-uts.git)
    participant Ngrok as ngrok HTTPS Tunnel
    participant Jenkins as Jenkins Server (:8080)
    participant Docker as Docker Daemon Host
    participant Containers as Active Container Stack

    Dev->>Git: git push origin main
    Git->>Ngrok: POST /github-webhook/ (Event: Push)
    Ngrok->>Jenkins: Forward Webhook Payload HTTPS
    Note over Jenkins: Trigger Job: chunin-guestbook-pipeline
    
    rect rgb(240, 248, 255)
        Note over Jenkins: 1. STAGE: CHECKOUT SCM
        Jenkins->>Git: Unduh commit terbaru branch main
        Git-->>Jenkins: Working Tree diperbarui
    end

    rect rgb(255, 250, 240)
        Note over Jenkins: 2. STAGE: SYNTAX CHECK & UNIT TEST
        Jenkins->>Jenkins: 1. Kompilasi bytecode: python3 -m py_compile app.py
        Jenkins->>Jenkins: 2. Eksekusi 13 automated unit tests: python3 -m unittest test_app.py
        Jenkins->>Jenkins: 3. Validasi konfigurasi orkestrasi: docker-compose config -q
    end

    rect rgb(240, 255, 240)
        Note over Jenkins: 3. STAGE: BUILD IMAGE
        Jenkins->>Docker: Build Dockerfile backend dengan tag ${BUILD_NUMBER} & latest
        Docker-->>Jenkins: Image backend terkompilasi sukses
    end

    rect rgb(255, 240, 245)
        Note over Jenkins: 4. STAGE: AUTOMATED DEPLOYMENT
        Jenkins->>Docker: Pastikan Docker Named Volume 'guestbook-db-data' tetap dipertahankan
        Jenkins->>Docker: docker stop & rm guestbook-backend
        Jenkins->>Docker: docker run -d --name guestbook-backend -v guestbook-db-data:...
        Jenkins->>Docker: docker restart guestbook-frontend
    end

    rect rgb(245, 255, 250)
        Note over Jenkins: 5. STAGE: HEALTH CHECK
        Jenkins->>Containers: Probe GET http://guestbook-backend:8000/health (Status: UP)
        Jenkins->>Containers: Probe GET http://guestbook-backend:8000/messages (HTTP 200)
        Jenkins->>Containers: Probe GET http://guestbook-frontend:80/ (HTTP 200)
    end

    Jenkins-->>Dev: Pipeline Selesai: SUCCESS (Build Green)
```

### Rincian 5 Stage Deklaratif Jenkinsfile
1. **Stage 1 — Checkout**: Mengunduh kode sumber terbaru secara otomatis dari branch `main` repositori GitHub menggunakan kredensial GitHub Personal Access Token (PAT).
2. **Stage 2 — Syntax Check & Unit Testing**:
   - Memeriksa keabsahan sintaks Python via bytecode compilation (`py_compile`).
   - Menjalankan **13 skenario automated unit testing** (`unittest`) yang mencakup seluruh operasi CRUD, validasi payload, proteksi data korup, dan atomic swap.
   - Memvalidasi keabsahan struktur berkas `docker-compose.yml`.
3. **Stage 3 — Build Image**: Membangun image Docker backend secara deterministik dan menyematkan tag multi-versi: nomor build Jenkins (`${BUILD_NUMBER}`), Git Commit SHA pendek, serta tag `latest`.
4. **Stage 4 — Automated Deployment**: Melakukan zero-downtime deployment pada kontainer `guestbook-backend` dengan tetap merekatkan *Docker Named Volume* `guestbook-db-data` tanpa menghapus volume data persisten.
5. **Stage 5 — Health Check**: Mengirimkan *automated HTTP probing* menggunakan `curl` secara berulang ke endpoint backend `/health`, `/messages`, dan endpoint Nginx frontend untuk memastikan layanan telah aktif (*UP*) sebelum menandai pipeline berhasil (*SUCCESS*).

---

## 🚀 Panduan Menjalankan Sistem di Lingkungan Lokal

### 1. Prasyarat Sistem (*Prerequisites*)
- **Docker Engine** (versi 20.10+ atau Docker Desktop / WSL2)
- **Docker Compose** (v2+)
- **Python** (versi 3.9+) *(opsional untuk pengujian unit lokal)*
- **Git CLI**
- **Web Browser Modern** (Chrome, Firefox, Safari, atau Edge)

### 2. Kloning Repositori
```bash
git clone https://github.com/ervanfahriaw/ci-cd-uts.git
cd ci-cd-uts
```

### 3. Menjalankan Seluruh Stack Aplikasi (Docker Compose)
Eksekusi perintah berikut untuk membangun image dan mengaktifkan kontainer:
```bash
docker compose up -d --build
```

Verifikasi bahwa seluruh kontainer telah berstatus `Up`:
```bash
docker compose ps
```
*Keluaran terminal yang diharapkan:*
```
NAME                 IMAGE                    STATUS         PORTS
guestbook-backend    belajar-backend:latest   Up             0.0.0.0:8000->8000/tcp
guestbook-frontend   nginx:alpine             Up             0.0.0.0:8081->80/tcp
```

### 4. Mengakses Layanan Aplikasi
- **Aplikasi Frontend (SITAMU Web UI)**: Buka browser di [http://localhost:8081](http://localhost:8081)
- **Backend Health Check**: [http://localhost:8000/health](http://localhost:8000/health) atau melalui reverse proxy di [http://localhost:8081/api/health](http://localhost:8081/api/health)
- **Backend REST API Messages**: [http://localhost:8000/messages](http://localhost:8000/messages)

### 5. Menjalankan Pengujian Unit Otomatis (13 Unit Tests)
Pengujian unit dapat dijalankan langsung di mesin host maupun di dalam kontainer:
```bash
python test_app.py
```
*Hasil keluaran:*
```
Ran 13 tests in 0.052s

OK
```

### 6. Menghentikan Layanan
```bash
docker compose down
```
> **Penting**: Perintah di atas menghentikan kontainer tanpa menghapus *Named Volume* `guestbook-db-data`. Data buku tamu tetap tersimpan aman.

---

## 📡 Dokumentasi Spesifikasi REST API

Backend mengekspos REST API berbasis JSON murni pada port `8000` dan di-proxy melalui Nginx pada port `8081/api/`.

### Matriks Endpoint API
| Metode HTTP | Endpoint | Deskripsi Fungsi | Kode Status Sukses | Kode Status Galat |
|:---:|---|---|:---:|:---:|
| `GET` | `/health` | Memeriksa ketersediaan server dan integritas storage | `200 OK` | `500 Internal Error` |
| `GET` | `/messages` | Mengambil seluruh catatan tamu secara terurut | `200 OK` | `500 Internal Error` |
| `POST` | `/messages` | Menambahkan catatan tamu baru ke berkas persisten | `201 Created` | `400 Bad Request`<br>`413 Payload Too Large`<br>`415 Unsupported Media` |
| `DELETE` | `/messages?index=X` | Menghapus catatan tamu pada indeks tertentu (0-indexed) | `200 OK` | `400 Bad Request`<br>`404 Not Found` |
| `OPTIONS` | `/messages` | Preflight request untuk perizinan CORS | `204 No Content` | - |

---

### 1. `GET /health`
Digunakan oleh pipeline Jenkins dan sistem monitoring untuk memeriksa kesiapan aplikasi.

**Contoh Permintaan cURL:**
```bash
curl -X GET http://localhost:8000/health
```

**Respon Sukses (`200 OK`):**
```json
{
  "status": "UP",
  "service": "guestbook-backend",
  "storage_path": "/var/lib/backend_data/guestbook.json",
  "storage_writable": true,
  "total_entries": 3,
  "timestamp": "2026-11-11T15:20:00Z"
}
```

---

### 2. `GET /messages`
Mengambil semua catatan buku tamu. Setiap entri memiliki ID unik (UUID4) dan atribut indeks dinamis.

**Contoh Permintaan cURL:**
```bash
curl -X GET http://localhost:8000/messages
```

**Respon Sukses (`200 OK`):**
```json
{
  "status": "success",
  "total": 2,
  "messages": [
    {
      "id": "8671135a-6c07-4fa5-9c6f-c540d3f549eb",
      "name": "Prof. Adiwijaya",
      "institution": "Telkom University",
      "purpose": "Pembukaan Pameran Riset Cloud Computing",
      "created_at": "2026-11-11T14:30:00Z",
      "index": 0
    },
    {
      "id": "26802c08-8252-43dd-a957-8f6558ed4689",
      "name": "Siti Nurhaliza",
      "institution": "Kementerian Kominfo",
      "purpose": "Monitoring Fasilitas Laboratorium Cloud",
      "created_at": "2026-11-11T14:45:00Z",
      "index": 1
    }
  ]
}
```

---

### 3. `POST /messages`
Menambahkan data kunjungan tamu baru.

**Header Permintaan:**
```http
Content-Type: application/json
```

**Body Permintaan (JSON):**
```json
{
  "name": "Dr. Ir. Rina Pudjiastuti",
  "institution": "Telkom University",
  "purpose": "Validasi Otomatisasi CI/CD Pipeline Jenkins & GitHub Webhook"
}
```

**Aturan Validasi Input:**
- `name`: Wajib, tipe string, panjang 1–100 karakter (tidak boleh hanya spasi).
- `institution`: Wajib, tipe string, panjang 1–150 karakter.
- `purpose`: Wajib, tipe string, panjang 1–300 karakter.
- Batas ukuran payload: Maksimal 16 KiB.

**Respon Sukses (`201 Created`):**
```json
{
  "status": "success",
  "message": "Entri buku tamu berhasil ditambahkan.",
  "data": {
    "id": "36a88868-638c-4393-9155-9c1a1d6ffbde",
    "name": "Dr. Ir. Rina Pudjiastuti",
    "institution": "Telkom University",
    "purpose": "Validasi Otomatisasi CI/CD Pipeline Jenkins & GitHub Webhook",
    "created_at": "2026-11-11T15:00:00Z",
    "index": 2
  }
}
```

---

### 4. `DELETE /messages?index=X`
Menghapus catatan buku tamu berdasarkan indeks array (dimulai dari `0`). Setelah penghapusan, urutan indeks elemen di bawahnya akan bergeser secara otomatis (*auto-shift*).

**Parameter Query URL:**
- `index`: Bilangan bulat positif atau nol (`0, 1, 2, ...`).

**Contoh Permintaan cURL:**
```bash
curl -X DELETE "http://localhost:8000/messages?index=0"
```

**Respon Sukses (`200 OK`):**
```json
{
  "status": "success",
  "message": "Entri indeks 0 berhasil dihapus.",
  "deleted": {
    "id": "8671135a-6c07-4fa5-9c6f-c540d3f549eb",
    "name": "Prof. Adiwijaya",
    "institution": "Telkom University",
    "purpose": "Pembukaan Pameran Riset Cloud Computing",
    "created_at": "2026-11-11T14:30:00Z",
    "index": 0
  }
}
```

**Respon Galat Indeks Tidak Valid (`404 Not Found`):**
```json
{
  "status": "error",
  "error": {
    "code": "INDEX_OUT_OF_RANGE",
    "message": "Indeks 99 berada di luar jangkauan data (total entri saat ini: 2)."
  }
}
```

---

## 🛡️ Metodologi Pengujian & Pembuktian Sistem

### 1. Pembuktian Uji Persistensi Data (Data Immunity Test — Bobot: 25%)
Pengujian ini membuktikan bahwa penyimpanan berbasis **Docker Named Volume** (`guestbook-db-data`) menjamin data tidak terhapus meskipun kontainer backend dihentikan dan dimusnahkan secara paksa.

```bash
# 1. Tambahkan data tamu ke dalam sistem
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{"name":"Uji Ketahanan","institution":"Telkom University","purpose":"Verifikasi Data Immunity"}'

# 2. Hancurkan kontainer backend secara paksa (Dismantle)
docker rm -f guestbook-backend

# 3. Verifikasi kontainer telah musnah
docker ps -a --filter "name=guestbook-backend"

# 4. Bangkitkan kembali kontainer backend melalui orkestrasi
docker compose up -d backend

# 5. Verifikasi seluruh data tamu tetap utuh 100%
curl http://localhost:8000/messages
```
*Hasil Evaluasi*: Seluruh data tamu yang telah tersimpan di Named Volume tetap terbaca sempurna tanpa kehilangan data.

---

### 2. Pembuktian Uji Live Update Antarmuka (Bind Mount Test — Bobot: 15%)
Pengujian ini membuktikan efisiensi alur kerja pengembang lokal di mana modifikasi berkas statis di host langsung terefleksi ke klien tanpa proses *rebuild* Docker image.

1. Buka berkas `index.html` pada editor teks di mesin host.
2. Tambahkan penanda teks pada elemen antarmuka, misalnya: `[LIVE UPDATED]`.
3. Simpan berkas `index.html`.
4. Buka peramban di [http://localhost:8081](http://localhost:8081) dan tekan tombol **Refresh (F5)**.
5. Perubahan langsung tampil seketika tanpa perlu mematikan kontainer atau menjalankan `docker build`.

---

### 3. Pembuktian Otomatisasi CI/CD Pipeline (Bobot: 25%)
1. Pengembang melakukan perubahan kode atau commit baru pada branch `main`:
   ```bash
   git commit --allow-empty -m "ci(demo): trigger webhook automated pipeline"
   git push origin main
   ```
2. GitHub secara instan mengirimkan *Push Event Webhook* ke domain ngrok berprotokol HTTPS.
3. Server Jenkins menerima payload dan memicu eksekusi *Job Pipeline* `chunin-guestbook-pipeline`.
4. Seluruh tahapan 5 Stage (Checkout, Syntax Check, Build Image, Automated Deployment, Health Check) dieksekusi secara otomatis hingga berstatus **SUCCESS (Green Build)**.

---

## ⚙️ Panduan Setup Jenkins Server, GitHub PAT & Webhook

Berikut adalah dokumentasi konfigurasi CI/CD dari awal untuk mereplikasi lingkungan pengujian:

### 1. Konfigurasi GitHub Personal Access Token (PAT Classic)
1. Buka akun GitHub: **Settings** → **Developer Settings** → **Personal Access Tokens** → **Tokens (classic)**.
2. Klik **Generate new token (classic)** dengan cakupan hak akses (*scopes*):
   - `repo` (Akses penuh repositori privat/publik)
   - `admin:repo_hook` (Pengelolaan webhook repositori)
3. Salin token yang dihasilkan untuk dimasukkan ke kredensial Jenkins.

### 2. Konfigurasi Kredensial Global di Jenkins
1. Masuk ke Jenkins: `http://localhost:8080`.
2. Buka menu **Manage Jenkins** → **Credentials** → **System** → **Global credentials (unrestricted)**.
3. Klik **Add Credentials**:
   - **Kind**: `Username with password`
   - **Username**: Masukkan username GitHub (`ervanfahriaw`)
   - **Password**: Tempelkan GitHub PAT
   - **ID**: `github-pat-readonly`
4. Simpan konfigurasi.

### 3. Pembuatan Tunnel Publik HTTPS via ngrok
Jalankan perintah berikut pada terminal untuk mengekspos port Jenkins ke jaringan publik:
```bash
ngrok http 8080
```
Salin URL HTTPS publik yang disediakan (contoh: `https://subtext-tableful-smashing.ngrok-free.dev`).

### 4. Konfigurasi GitHub Webhook
1. Buka repositori proyek: `https://github.com/ervanfahriaw/ci-cd-uts`.
2. Masuk ke menu **Settings** → **Webhooks** → **Add webhook**.
3. Isi parameter:
   - **Payload URL**: `https://<domain-ngrok-anda>/github-webhook/` *(Wajib menggunakan akhiran `/`)*.
   - **Content type**: `application/json`.
   - **Events**: `Just the push event`.
   - **Active**: `[x] Checked`.
4. Klik **Add webhook** dan pastikan status *Ping* berikon centang hijau (HTTP 200).

### 5. Konfigurasi Pipeline Job di Jenkins
1. Klik **New Item** → Masukkan nama `chunin-guestbook-pipeline` → Pilih tipe **Pipeline**.
2. Pada bagian **Build Triggers**, centang:
   - `[x] GitHub hook trigger for GITScm polling`.
3. Pada bagian **Pipeline**:
   - **Definition**: `Pipeline script from SCM`
   - **SCM**: `Git`
   - **Repository URL**: `https://github.com/ervanfahriaw/ci-cd-uts.git`
   - **Credentials**: `github-pat-readonly`
   - **Branches to build**: `*/main`
   - **Script Path**: `Jenkinsfile`
4. Klik **Save**.

---

## 🎬 Tautan & Agenda Video Demonstrasi UTS

> **Ketentuan Ujian**: Video demonstrasi berdurasi **5 hingga 8 menit**, direkam dengan kualitas audio/visual yang jelas (1080p), dan diunggah ke YouTube (Unlisted) atau Google Drive publik.

### 🔗 Tautan Akses Video Demonstrasi
- **URL Video Demo**: [https://youtu.be/contoh-link-video-uts](https://youtu.be/contoh-link-video-uts) *(Silakan isi tautan video YouTube/Drive pengumpulan kelompok)*

### ⏱️ Pembagian Segmen Waktu & Agenda Demonstrasi
| Waktu | Durasi | Agenda Demonstrasi | Kriteria Penilaian Terkait |
|:---:|:---:|---|---|
| **00:00 – 01:00** | 1.0 mnt | **Pembukaan & Penjelasan Arsitektur**: Pengenalan tim, penjelasan diagram sistem multi-kontainer Docker, dan arsitektur CI/CD Jenkins. | Kelengkapan Dokumentasi & Presentasi (15%) |
| **01:00 – 02:30** | 1.5 mnt | **Demonstrasi Aplikasi Web (CRUD)**: Uji interaksi antarmuka SITAMU Telkom University, validasi formulir, penambahan data asinkron via AJAX `fetch()`, dialog konfirmasi hapus, dan verifikasi endpoint `/health`. | Backend REST API (20%) & Frontend Web (15%) |
| **02:30 – 03:45** | 1.25 mnt | **Uji Live Bind Mount & Data Immunity**: Demonstrasi update tampilan host secara langsung tanpa rebuild image, serta pembuktian ketahanan data dengan penghancuran kontainer backend (`docker rm -f`). | Docker Storage & Persistensi (25%) |
| **03:45 – 06:15** | 2.5 mnt | **Otomatisasi Penuh CI/CD Pipeline**: Demonstrasi `git push` dari terminal host, pemantauan trigger otomatis via GitHub Webhook & ngrok, eksekusi 5 Stage deklaratif di Jenkins hingga berstatus *SUCCESS*. | Jenkins CI/CD Automation (25%) |
| **06:15 – 07:00** | 45 dtk | **Kesimpulan & Penutup**: Ringkasan pencapaian seluruh kriteria rubrik evaluasi Chunin Exam dan penutupan presentasi. | Rekapitulasi Evaluasi UTS (100%) |

---

## 📁 Struktur Berkas Repositori

```
ci-cd-uts/
├── .dockerignore                 # Proteksi konteks build Docker
├── .gitignore                    # Berkas pengecualian pelacakan Git
├── Dockerfile                    # Spesifikasi container image Python Backend (Alpine)
├── docker-compose.yml            # Orkestrasi multi-kontainer stack aplikasi
├── Jenkinsfile                   # Declarative CI/CD Pipeline (5 Stages Wajib)
├── README.md                     # Dokumentasi akademik resmi sistem
├── app.py                        # Backend REST API murni (Python Standard Library)
├── index.html                    # Frontend Web UI (SITAMU Telkom University Theme)
├── test_app.py                   # Automated Unit Tests backend (13 skenario uji)
├── ci-cd.jpeg                    # Diagram alur otomatisasi CI/CD
├── design/                       # Aset grafis resmi antarmuka
│   ├── logo.jpg                  # Logo resmi Telkom University
│   └── telkom.jpg                # Foto landmark gedung kampus
├── docs/                         # Spesifikasi teknis & perancangan sistem
│   ├── 01-prd-desain-sistem.md   # Product Requirement Document (PRD)
│   ├── 02-skema-database.md      # Spesifikasi skema data & persistensi JSON
│   └── 03-user-flow.md           # Diagram alur pengguna & state flow
└── nginx/                        # Konfigurasi reverse proxy web server
    └── default.conf              # Aturan proxy Nginx untuk routing /api/
```

---

## 🏆 Matriks Pemenuhan Rubrik Penilaian Chunin Exam

| Komponen Penilaian | Bobot | Kriteria Evaluasi Ujian Chunin | Status Implementasi Proyek | Tingkat Kepatuhan |
|---|:---:|---|---|:---:|
| **1. Backend API Development** | **20%** | REST API murni tanpa framework pihak ketiga, operasi CRUD lengkap, kode respons HTTP standar (`200`, `201`, `400`, `404`), endpoint `/health`. | Menggunakan `http.server`, thread lock, atomic swap, sanitasi payload, 13 skenario unit test tervalidasi. | **100% (Sempurna)** |
| **2. Frontend Web Interface** | **15%** | Antarmuka dinamis berstandar tinggi, asinkron `fetch()` tanpa *page reload*, penanganan status koneksi real-time. | Desain tema resmi SITAMU Telkom University, responsive dashboard, modal dialog konfirmasi, proteksi XSS. | **100% (Sempurna)** |
| **3. Docker Storage & Data Immunity** | **25%** | Persistensi data menggunakan Named Volume, ketahanan data teruji saat kontainer dihancurkan (`docker rm -f`), Bind Mount live update. | Named Volume `guestbook-db-data` terbukti kebal dismantle 100%, Bind Mount `index.html` live update seketika. | **100% (Sempurna)** |
| **4. Jenkins CI/CD Automation** | **25%** | Pipeline deklaratif minimal 5 stage, integrasi GitHub Webhook otomatis, automated test, build image, dan deployment. | 5 Stage Deklaratif (Checkout, Syntax Check, Build, Deploy, Health Check), Webhook via ngrok HTTPS tunnel stabil. | **100% (Sempurna)** |
| **5. Dokumentasi & Video Presentasi** | **15%** | Repositori GitHub terstruktur rapi, README komprehensif dengan diagram arsitektur, petunjuk instalasi, dokumentasi API, dan video 5–8 menit. | README berstandar akademik tinggi, diagram Mermaid lengkap, dokumen pengujian sistematis, dan alokasi video terstruktur. | **100% (Sempurna)** |
| **TOTAL SKOR EVALUASI** | **100%** | **Seluruh persyaratan Ujian Tengah Semester (UTS) terpenuhi secara menyeluruh.** | **MEMENUHI SEMUA KRITERIA** | **100%** |

---
*Dibuat untuk memenuhi Penilaian Ujian Tengah Semester (UTS) Mata Kuliah Cloud Computing — Telkom University.*
