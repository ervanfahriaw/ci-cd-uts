# 🎬 Naskah Presentasi & Panduan Pengujian Demo Video (Chunin Exam UTS)
### Mata Kuliah: Cloud Computing (CSO) — Telkom University
**Studi Kasus No. 1**: Buku Tamu Digital Kampus (*Digital Guestbook / SITAMU*)  
**Repositori GitHub**: [https://github.com/ervanfahriaw/ci-cd-uts](https://github.com/ervanfahriaw/ci-cd-uts)  
**Target Nilai**: 100 / 100 (Predikat: **Sangat Baik** di Seluruh 5 Komponen Rubrik)

---

## 🔑 Informasi Akun & Password (Credentials)
Catat informasi login berikut sebelum memulai demonstrasi:

| Layanan | URL Akses | Username | Password | Keterangan |
|---|---|:---:|:---:|---|
| **Jenkins Server** | [http://localhost:8085](http://localhost:8085) | `ervan` | `admin123` | Server CI/CD otomatis |
| **Aplikasi Web SITAMU** | [http://localhost:8081](http://localhost:8081) | *(Tanpa login)* | *(Tanpa login)* | Antarmuka Buku Tamu Publik |
| **Backend REST API** | [http://localhost:8000/messages](http://localhost:8000/messages) | *(Publik)* | *(Publik)* | Endpoint data JSON |
| **GitHub Webhook Tunnel** | `https://subtext-tableful-smashing.ngrok-free.dev` | - | - | Tunnel ngrok aktif ke port 8085 |

---

## 🖥️ 1. Persiapan Jendela Sebelum Mulai Merekam Layar
Buka jendela-jendela berikut dan susun agar siap dipindahkan (*Alt + Tab*):
1. **Browser Tab 1**: [http://localhost:8081](http://localhost:8081) *(Web Antarmuka SITAMU Telkom University)*
2. **Browser Tab 2**: [http://localhost:8085/job/chunin-guestbook-pipeline/](http://localhost:8085/job/chunin-guestbook-pipeline/) *(Dashboard Jenkins — Login dengan `ervan` / `admin123`)*
3. **Browser Tab 3**: [http://localhost:8000/messages](http://localhost:8000/messages) *(Endpoint Backend JSON)*
4. **Browser Tab 4**: [https://github.com/ervanfahriaw/ci-cd-uts](https://github.com/ervanfahriaw/ci-cd-uts) *(Repositori GitHub)*
5. **VS Code**: Menampilkan struktur file proyek (`app.py`, `index.html`, `Jenkinsfile`, `README.md`)
6. **Terminal / PowerShell (WSL2)**: Untuk mengeksekusi perintah Docker dan Git
7. **Perekam Layar**: OBS Studio atau bawaan Windows Game Bar (**Tekan `Win + Alt + R`** untuk mulai/selesai merekam)

---

## ⏱️ 2. Rundown Video Demo (Target Durasi: 5 – 8 Menit)

| Waktu | Segmen | Fokus Pengujian | Rubrik Terkait |
|:---:|:---|:---|:---:|
| **00:00 - 01:00** | **Segmen 1: Pembukaan & Arsitektur** | Perkenalan tim, studi kasus, arsitektur Docker & network | Komponen 5 (Dokumentasi) |
| **01:00 - 02:45** | **Segmen 2: Tur Fitur & Penjelasan Web** | UI SITAMU, branding Telkom University, responsive sidebar, filter tanggal, cetak PDF & badge | Komponen 2 (Frontend) |
| **02:45 - 04:00** | **Segmen 3: Pengujian CRUD REST API** | Operasi POST tamu, GET daftar JSON, DELETE real-time dengan modal dialog | Komponen 1 (Backend API) |
| **04:00 - 05:30** | **Segmen 4: Simulasi Data Immunity** | Menghapus kontainer backend (`docker rm -f`), membuktikan data aman di Named Volume | Komponen 3 (Docker & Storage) |
| **05:30 - 07:15** | **Segmen 5: Simulasi Otomasi CI/CD** | `git push` memicu Jenkins via Webhook otomatis, 5 Stage pipeline hingga auto-deploy | Komponen 4 (Jenkins CI/CD) |
| **07:15 - 07:45** | **Segmen 6: Penutup & Deliverables** | Verifikasi berkas wajib di GitHub dan penutup | Komponen 5 (Deliverables) |

---

## 🎬 3. Panduan Pengujian Step-by-Step & Naskah Demo (Script Lengkap)

---

### 🎙️ SEGMEN 1: Pembukaan & Penjelasan Arsitektur (00:00 – 01:00)
#### 📌 Tindakan Praktis di Layar:
1. Buka layar menampilkan halaman **README.md** di VS Code atau di GitHub.
2. Sorot tabel identitas kelompok dan diagram arsitektur sistem (`Mermaid Diagram`).

#### 🗣️ Naskah Presenter:
> *"Halo, selamat pagi/siang kepada Bapak/Ibu Dosen Pengampu mata kuliah Cloud Computing (CSO) dan rekan-rekan sekalian. Kami dari Kelompok [Sebutkan Nomor Kelompok] yang beranggotakan:
> 1. [Nama Anggota 1 - NIM]
> 2. [Nama Anggota 2 - NIM]
> 3. [Nama Anggota 3 - NIM]
>
> Pada Ujian Tengah Semester (Chunin Exam) ini, kelompok kami mengimplementasikan **Studi Kasus No. 1: Buku Tamu Digital Kampus (*Digital Guestbook*)** yang kami beri nama **SITAMU Telkom University**.
>
> Sistem ini dibangun dengan arsitektur Cloud-Native berbasis kontainer:
> 1. **Frontend Service**: Menggunakan Plain HTML5, Tailwind CSS, dan Vanilla JS yang dijalankan pada web server **Nginx Alpine** di port 8081 dengan metode **Bind Mount** untuk kemudahan pembaruan langsung di host.
> 2. **Backend Service**: Menggunakan **Python REST API** murni tanpa framework berat di port 8000 yang menangani operasi CRUD berbasis JSON.
> 3. **Docker Storage**: Data disimpan secara persisten di **Docker Named Volume** bernama `guestbook-db-data` untuk menjamin persistensi data mutlak (*Data Immunity*).
> 4. **Jaringan**: Terhubung melalui Custom Bridge Network bernama `app-net` dengan resolusi nama DNS Docker.
> 5. **Otomatisasi CI/CD**: Terintegrasi penuh dengan **GitHub Webhook** melalui secure tunnel ngrok ke **Jenkins Pipeline** 5 stage yang melakukan deployment otomatis setiap kali ada pembaruan kode.*
>
> *Mari kita masuk ke pengujian antarmuka aplikasi."*

---

### 🎙️ SEGMEN 2: Penjelasan & Demonstrasi Fitur Web SITAMU (01:00 – 02:45)
#### 📌 Tindakan Praktis di Layar:
1. Pindah ke browser [http://localhost:8081](http://localhost:8081).
2. Tunjukkan elemen-elemen berikut menggunakan kursor:
   - **Logo Resmi**: Tunjukkan logo perisai Telkom University di brand header sidebar serta favicon resmi di tab browser.
   - **Tombol Hamburger Universal**: Klik tombol hamburger (ikon garis 3) di pojok kiri atas untuk menunjukkan navigasi bisa disembunyikan/dimunculkan dengan transisi mulus di desktop maupun mobile.
   - **Menu Kategori Acara**: Klik judul kategori untuk memperlihatkan animasi akordeon buka-tutup (*minimize/expand*). Klik salah satu kategori untuk menunjukkan sorotan warna merah aktif yang konsisten.
   - **Form Registrasi Tamu**: Ketik teks di form untuk memperlihatkan *live character counter* (0/500 karakter).
   - **Toolbar Riwayat & Filter Tanggal**: Tunjukkan tombol preset "Semua Tanggal", "Hari Ini", dan pemilih kalender tanggal spesifik.
   - **Aksi Resepsionis**:
     - Klik tombol **Cetak Badge Akses**: Tunjukkan modal kartu tanda masuk tamu berlogo Telkom University.
     - Klik tombol **Unduh PDF**: Tunjukkan dokumen cetak ber-kop resmi Telkom University (bukan screenshot mentah).

#### 🗣️ Naskah Presenter:
> *"Sekarang kita berada di antarmuka web SITAMU pada URL `localhost:8081`. Desain web ini mengadopsi standar resmi Telkom University dengan warna khas Crimson Red `#e01a3f` dan Dark Neutral `#343a40`.
>
> Berikut adalah fitur-fitur unggulan pada antarmuka:
> - **Branding Resmi Kampus**: Dilengkapi logo perisai Telkom University yang proporsional di header sidebar serta favicon resmi di tab browser.
> - **Sidebar Navigasi Responsif**: Dilengkapi tombol hamburger universal yang memungkinkan pengguna menyembunyikan atau memunculkan bilah navigasi dengan animasi halus di layar desktop maupun mobile.
> - **Kategori Acara Dinamis**: Menu kategori acara dapat diminimalkan (accordion collapsible) dan tombol yang aktif ditandai dengan sorotan aksen merah yang konsisten.
> - **Formulir Tamu Interaktif**: Dilengkapi validasi form instan, penghitung karakter langsung (*live counter*), serta pengamanan sanitasi input dari risiko serangan XSS (*Cross-Site Scripting*).
> - **Manajemen Riwayat Kunjungan**: Resepsionis dapat memfilter tamu berdasarkan kategori maupun tanggal kunjungan masa lalu menggunakan fitur pemilih tanggal kalender.
> - **Fitur Pelaporan Akademik**: Tersedia tombol **Unduh PDF** yang menghasilkan dokumen cetak ber-kop resmi Telkom University, serta tombol **Cetak Badge** untuk mencetak kartu identitas tanda masuk pengunjung resmi kampus."*

---

### 🎙️ SEGMEN 3: Pengujian CRUD & Error Handling REST API (02:45 – 04:00)
#### 📌 Tindakan Praktis di Layar:
1. **Uji POST (Tambah Tamu Baru)**:
   - Masukkan data pada formulir:
     - Nama Tamu: `Dr. Hendra Wijaya, M.T.`
     - Instansi: `Institut Teknologi Bandung (ITB)`
     - Kategori: `Seminar & Kuliah Umum`
     - Keperluan: `Narasumber Kuliah Umum DevOps & Cloud Computing`
   - Klik tombol **Kirim Data Buku Tamu**.
   - Tunjukkan notifikasi *toast* sukses dan data langsung muncul di tabel paling atas secara instan tanpa me-refresh browser.
2. **Uji GET (Daftar JSON)**:
   - Buka tab baru ke [http://localhost:8000/messages](http://localhost:8000/messages).
   - Tunjukkan respon JSON standar dari Backend Python yang memuat array data tamu.
3. **Uji DELETE (Check-out Tamu)**:
   - Kembali ke web `localhost:8081`.
   - Klik tombol ikon hapus (*checkout*) pada baris data tamu.
   - Tunjukkan **Modal Konfirmasi Hapus** (mencegah klik tak sengaja).
   - Klik **Ya, Hapus Tamu**. Tunjukkan baris data langsung terhapus seketika dari tabel secara real-time.
4. **Uji Error Handling**:
   - Coba klik tombol kirim saat input form kosong. Tunjukkan penolakan validasi instan (pencegahan status HTTP 400 Bad Request).

#### 🗣️ Naskah Presenter:
> *"Sekarang kita buktikan pemenuhan Komponen 1 (Backend Python API) dan Komponen 2 (Frontend Vanilla JS):
>
> 1. **Operasi POST**: Kita masukkan data tamu baru. Ketika tombol kirim ditekan, Javascript mengeksekusi `fetch()` asynchronous dengan metode POST dan header `application/json`. Respon HTTP `201 Created` diterima dan data langsung masuk ke tabel secara real-time.
> 2. **Operasi GET**: Di background, aplikasi memanggil endpoint GET `/messages` yang mengembalikan seluruh daftar tamu dalam format JSON murni.
> 3. **Operasi DELETE**: Untuk menghapus atau melakukan check-out tamu, kita klik ikon hapus. Sistem menampilkan modal konfirmasi. Saat disetujui, query DELETE dikirimkan ke `/messages?index=X` dan baris data terhapus seketika tanpa perlu refresh halaman manual.
> 4. **Error Handling**: API dan Frontend dilengkapi error handling presisi. Jika payload kosong atau tipe konten tidak sesuai, server secara ketat menolak dengan status HTTP 400 Bad Request atau 415 Unsupported Media Type."*

---

### 🎙️ SEGMEN 4: Simulasi Data Immunity (Hapus Kontainer Backend) (04:00 – 05:30)
*(Poin Kunci Penilaian Bobot 25% Docker & Storage Config)*

#### 📌 Tindakan Praktis di Layar:
1. Kembali ke web `localhost:8081`, tambahkan 1 data tamu khusus sebagai pembuktian:
   - Nama: `Budi Santoso - Uji Persistensi`
   - Instansi: `PT Telkom Indonesia`
   - Keperluan: `Pengujian Data Immunity UTS`
   - Klik **Kirim Data Buku Tamu** (Pastikan data tampil di tabel).
2. Pindah ke **Terminal / PowerShell**:
   - Hancurkan kontainer backend secara paksa:
     ```bash
     wsl docker rm -f guestbook-backend
     ```
   - Tunjukkan dengan perintah `wsl docker ps` bahwa kontainer `guestbook-backend` sudah benar-benar terhapus.
3. Pindah ke browser [http://localhost:8081](http://localhost:8081) dan tekan **F5 / Refresh**:
   - Tunjukkan indikator bahwa backend sedang *offline* / gagal terhubung karena kontainer telah dimatikan.
4. Kembali ke terminal, jalankan kembali kontainer backend menggunakan **Named Volume** `guestbook-db-data`:
   ```bash
   wsl docker run -d --name guestbook-backend --network app-net --network-alias backend -p 8000:8000 -v guestbook-db-data:/var/lib/backend_data belajar-backend:latest
   ```
5. Kembali ke browser [http://localhost:8081](http://localhost:8081) dan tekan **F5 / Refresh**:
   - **Perlihatkan bahwa data `Budi Santoso - Uji Persistensi` MASIH ADA dan TIDAK HILANG 100%!**

#### 🗣️ Naskah Presenter:
> *"Sekarang kita buktikan pemenuhan kriteria tertinggi Komponen 3, yaitu **Data Immunity**:
>
> Kita telah mendaftarkan tamu bernama 'Budi Santoso'. Sekarang kita buka terminal dan menghapus paksa kontainer backend menggunakan perintah `docker rm -f guestbook-backend`.
>
> Kontainer backend sekarang telah musnah. Saat web di-refresh, server backend tidak dapat dihubungi.
>
> Sekarang, kita hidupkan kontainer backend baru yang di-mount ke Docker Named Volume `guestbook-db-data` pada path `/var/lib/backend_data`.
>
> Ketika kita refresh kembali peramban `localhost:8081`, dapat dilihat bahwa data tamu 'Budi Santoso' **tetap utuh 100%**. Ini membuktikan secara empiris bahwa data tersimpan persisten di luar siklus hidup kontainer."*

---

### 🎙️ SEGMEN 5: Simulasi Otomasi CI/CD & GitHub Webhook (05:30 – 07:15)
*(Poin Kunci Penilaian Bobot 25% Jenkins CI/CD Pipeline)*

#### 📌 Tindakan Praktis di Layar:
1. Buka tab browser di **Dashboard Jenkins**:
   - [http://localhost:8085/job/chunin-guestbook-pipeline/](http://localhost:8085/job/chunin-guestbook-pipeline/) *(Login: `ervan` / `admin123`)*
   - Perlihatkan riwayat build sebelumnya yang berstatus hijau/biru `SUCCESS`.
2. Buka Terminal / VS Code, buat perubahan kecil dan lakukan commit push ke GitHub:
   ```bash
   git commit --allow-empty -m "test(demo): simulasi otomatisasi webhook ci-cd uts"
   git push origin main
   ```
3. Langsung kembali ke tab Jenkins (tanpa menekan tombol 'Build Now'):
   - Tunggu 2-4 detik, perlihatkan build baru langsung terpicu otomatis (*Started by GitHub push by ervanfahriaw via Webhook*).
4. Klik build yang sedang berjalan dan buka tampilan **Pipeline Console Output** atau **Stage View**:
   - Tunjukkan 5 Stage yang dieksekusi secara otomatis:
     1. **Stage 1: Checkout SCM** *(Menarik commit terbaru dari GitHub)*
     2. **Stage 2: Syntax Check & Unit Testing** *(Menjalankan `test_app.py`, 13/13 tes lulus)*
     3. **Stage 3: Build Docker Image** *(Membangun image backend `belajar-backend:latest`)*
     4. **Stage 4: Automated Container Deployment** *(Auto-deploy kontainer di `app-net` tanpa menghapus volume)*
     5. **Stage 5: Health Check Verification** *(Verifikasi status HTTP 200 OK pada `/health` dan `/messages`)*
5. Tunjukkan status akhir build bernilai **Finished: SUCCESS**.

#### 🗣️ Naskah Presenter:
> *"Masuk ke Komponen 4, yaitu otomatisasi CI/CD Pipeline:
>
> Di layar terlihat dashboard Jenkins untuk job `chunin-guestbook-pipeline`. Sekarang, kami melakukan `git push` ke branch `main` di GitHub.
>
> Tanpa perlu menyentuh tombol 'Build Now', GitHub Webhook yang terhubung melalui secure HTTPS tunnel ngrok langsung mendeteksi push event dan memicu Jenkins Pipeline secara otomatis.
>
> Pipeline mengeksekusi 5 Stage deklaratif:
> 1. **Checkout**: Mengambil source code terbaru dari GitHub.
> 2. **Syntax Check & Unit Test**: Menjalankan 13 unit test pada backend Python untuk memverifikasi kode sebelum rilis.
> 3. **Build Image**: Mengemas aplikasi ke dalam Docker image Alpine Linux.
> 4. **Automated Deployment**: Menerapkan kontainer baru ke dalam jaringan `app-net` dengan tetap menjaga Named Volume database.
> 5. **Health Check**: Memvalidasi respon endpoint `/health` dan `/messages`.
>
> Seluruh stage berhasil dieksekusi dengan status akhir **SUCCESS**."*

---

### 🎙️ SEGMEN 6: Penutup & Verifikasi Berkas Deliverables (07:15 – 07:45)
#### 📌 Tindakan Praktis di Layar:
1. Buka tab repositori GitHub [https://github.com/ervanfahriaw/ci-cd-uts](https://github.com/ervanfahriaw/ci-cd-uts).
2. Tunjukkan berkas-berkas proyek:
   - `app.py`
   - `index.html`
   - `Dockerfile`
   - `docker-compose.yml`
   - `Jenkinsfile`
   - `README.md`
3. Gulir ke bagian bawah README untuk menunjukkan identitas anggota kelompok dan panduan instalasi.

#### 🗣️ Naskah Presenter:
> *"Sebagai penutup, seluruh berkas deliverables tugas UTS Chunin Exam telah lengkap di repositori GitHub kami di `github.com/ervanfahriaw/ci-cd-uts`, mencakup source code, Dockerfile, docker-compose, Jenkinsfile, serta dokumentasi komprehensif pada README.md.
>
> Demikian demonstrasi dan pengujian proyek Cloud Computing Chunin Exam dari kelompok kami. Terima kasih atas perhatian Bapak/Ibu Dosen dan rekan-rekan semua. Wassalamualaikum wr. wb."*

---

## 📋 4. Ringkasan Perintah Penting (Cheat Sheet Command Line)

| Aksi | Perintah Terminal / PowerShell |
|---|---|
| **Hancurkan Kontainer Backend** | `wsl docker rm -f guestbook-backend` |
| **Cek Status Kontainer** | `wsl docker ps` |
| **Bangkitkan Backend (Data Immunity)** | `wsl docker run -d --name guestbook-backend --network app-net --network-alias backend -p 8000:8000 -v guestbook-db-data:/var/lib/backend_data belajar-backend:latest` |
| **Trigger Git Push CI/CD Otomatis** | `git commit --allow-empty -m "test(demo): simulasi webhook ci-cd uts" ; git push origin main` |

---

## 🏆 5. Lembar Verifikasi Mandiri Rubrik Penilaian (Target 100/100)

| Komponen | Bobot | Kriteria Nilai Maksimal (85–100) | Status Pemenuhan Proyek | Bukti dalam Demo |
|:---:|:---:|---|:---:|:---:|
| **1. Backend Python API** | **20%** | Fitur CRUD lengkap (GET, POST, DELETE), respons JSON rapi, error handling (400/404) presisi. | **Sangat Baik (100)** | Ditunjukkan di **Segmen 3**: Operasi POST tamu, GET daftar JSON, DELETE dengan modal konfirmasi. |
| **2. Frontend HTML & JS** | **15%** | Tampilan UI bersih, `fetch()` JS lancar, tombol Delete berfungsi real-time tanpa refresh manual. | **Sangat Baik (100)** | Ditunjukkan di **Segmen 2 & 3**: UI SITAMU resmi Telkom University, responsive navbar, live updates. |
| **3. Docker & Storage Config** | **25%** | Named Volume terbukti menjaga data saat kontainer di-dismantle (`docker rm -f`), Bind Mount berfungsi. | **Sangat Baik (100)** | Ditunjukkan di **Segmen 4**: Hancurkan kontainer backend, spawn ulang, data 100% aman; edit `index.html` live update. |
| **4. Jenkins CI/CD Pipeline** | **25%** | Jenkinsfile sukses mengeksekusi seluruh 5 stage via Webhook otomatis. | **Sangat Baik (100)** | Ditunjukkan di **Segmen 5**: `git push` otomatis men-trigger Jenkins via GitHub webhook hingga build **SUCCESS**. |
| **5. Dokumentasi & Demo** | **15%** | README.md memuat diagram arsitektur, petunjuk lengkap, dan video demo memperlihatkan git push hingga auto-deploy. | **Sangat Baik (100)** | Ditunjukkan di **Segmen 1 & 6**: README lengkap dengan Mermaid diagram, video 5–8 menit mencakup seluruh siklus. |
