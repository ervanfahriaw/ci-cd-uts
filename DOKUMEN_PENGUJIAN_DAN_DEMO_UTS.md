# 📋 Panduan Skenario Pengujian & Naskah Demo Video (Chunin Exam UTS)
### Mata Kuliah: Cloud Computing (CSO) — Telkom University
**Studi Kasus No. 1**: Buku Tamu Digital Kampus (*Digital Guestbook / SITAMU*)  
**Repositori GitHub**: [https://github.com/ervanfahriaw/ci-cd-uts](https://github.com/ervanfahriaw/ci-cd-uts)  
**Target Nilai**: 100 / 100 (Predikat: **Sangat Baik** di Seluruh 5 Komponen Rubrik)

---

## 🎯 Tujuan Dokumen
Dokumen ini disusun sebagai **panduan teknis step-by-step** dan **naskah presentasi (script video)** bagi kelompok mahasiswa untuk melakukan pengujian menyeluruh serta perekaman video demonstrasi proyek UTS Cloud Computing sesuai dengan instruksi resmi berkas `Cloud_computing_chunin_exam.pdf`.

---

## 🖥️ 1. Persiapan Awal Sebelum Perekaman / Pengujian
Pastikan aplikasi dan tab browser berikut sudah disiapkan dan dibuka sebelum memulai pengujian atau menyalakan tombol *Record*:

### A. Tab Browser (Disarankan menggunakan Google Chrome / Microsoft Edge)
1. **Tab 1 — Web Aplikasi Frontend**: [http://localhost:8081](http://localhost:8081)
2. **Tab 2 — Dashboard Jenkins**: [http://localhost:8085/job/chunin-guestbook-pipeline/](http://localhost:8085/job/chunin-guestbook-pipeline/)
3. **Tab 3 — Repositori GitHub**: [https://github.com/ervanfahriaw/ci-cd-uts](https://github.com/ervanfahriaw/ci-cd-uts)
4. **Tab 4 — Endpoint Backend**: [http://localhost:8000/messages](http://localhost:8000/messages) *(opsional untuk verifikasi JSON mentah)*

### B. Aplikasi Pendukung
1. **VS Code / Teks Editor**: Menampilkan struktur folder proyek (`app.py`, `index.html`, `Jenkinsfile`, `docker-compose.yml`, `README.md`).
2. **Terminal / PowerShell (WSL2)**: Untuk mengeksekusi perintah Docker dan Git.
3. **Aplikasi Perekam Layar**: OBS Studio atau bawaan Windows Game Bar (**Tombol `Win + Alt + R`** untuk mulai/berhenti rekam).

---

## ⏱️ 2. Rundown Video Demo (Target Durasi: 5 – 8 Menit)

| Menit | Segmen | Fokus Pengujian | Rubrik Terkait |
|:---:|:---|:---|:---:|
| **00:00 - 01:00** | **Segmen 1: Pembukaan & Arsitektur** | Perkenalan tim, studi kasus, dan arsitektur Docker | Komponen 5 (Dokumentasi) |
| **01:00 - 02:45** | **Segmen 2: Tur Fitur & Penjelasan Web** | UI/UX SITAMU, validasi form, filter tanggal, cetak PDF & badge | Komponen 2 (Frontend) |
| **02:45 - 04:00** | **Segmen 3: Pengujian CRUD REST API** | Operasi POST, GET, DELETE real-time, dan response JSON | Komponen 1 (Backend API) |
| **04:00 - 05:15** | **Segmen 4: Data Immunity & Bind Mount** | Simulasi hapus kontainer (`docker rm -f`) & live reload host | Komponen 3 (Docker & Storage) |
| **05:15 - 07:00** | **Segmen 5: Otomasi CI/CD & Webhook** | `git push` memicu Jenkins, 5 stage pipeline, auto-deploy | Komponen 4 (Jenkins CI/CD) |
| **07:00 - 07:45** | **Segmen 6: Penutup & Deliverables** | Verifikasi GitHub repo, berkas README.md, dan penutup | Komponen 5 (Deliverables) |

---

## 🎬 3. Panduan Pengujian Step-by-Step & Naskah Demo (Scripting)

---

### 🎙️ SEGMEN 1: Pembukaan & Penjelasan Arsitektur (00:00 - 01:00)
#### 📌 Tindakan Praktis:
1. Buka layar menampilkan halaman utama **README.md** di VS Code atau browser GitHub.
2. Tampilkan diagram arsitektur sistem.

#### 🗣️ Naskah / Contoh Kalimat Presenter:
> *"Halo, selamat pagi/siang kepada Bapak/Ibu Dosen Pengampu mata kuliah Cloud Computing (CSO) dan rekan-rekan sekalian. Kami dari Kelompok [Nama/Nomor Kelompok] yang beranggotakan [Sebutkan Nama & NIM Anggota Tim].*
>
> *Pada Ujian Tengah Semester (Chunin Exam) ini, kelompok kami mengimplementasikan **Studi Kasus No. 1: Buku Tamu Digital Kampus (Digital Guestbook)** yang kami beri nama **SITAMU Telkom University**.*
>
> *Sistem ini dibangun dengan arsitektur Cloud-Native berbasis kontainer:
> 1. **Frontend Service**: Menggunakan Plain HTML5, Tailwind CSS, dan Vanilla JS yang dijalankan pada web server **Nginx Alpine** di port 8081 dengan metode **Bind Mount**.
> 2. **Backend Service**: Menggunakan **Python REST API** murni (tanpa framework berat) di port 8000 yang menangani operasi CRUD berbasis JSON.
> 3. **Docker Storage**: Data disimpan secara persisten di **Docker Named Volume** bernama `guestbook-db-data` untuk menjamin persistensi data mutlak (*Data Immunity*).
> 4. **Jaringan**: Terhubung melalui Custom Bridge Network bernama `app-net` dengan resolusi nama DNS Docker.
> 5. **Otomatisasi CI/CD**: Terintegrasi penuh dengan **GitHub Webhook** dan **Jenkins Pipeline** 5 stage yang melakukan deployment otomatis setiap kali ada pembaruan kode.*
>
> *Mari kita masuk ke pengujian antarmuka aplikasi."*

---

### 🎙️ SEGMEN 2: Penjelasan & Demonstrasi Fitur Web SITAMU (01:00 - 02:45)
#### 📌 Tindakan Praktis:
1. Pindah layar ke browser: buka **[http://localhost:8081](http://localhost:8081)**.
2. Sorot elemen-elemen antarmuka secara teratur dengan kursor:
   - **Logo Resmi**: Tunjukkan logo Telkom University yang rapi di brand header dan favicon pada tab browser.
   - **Tombol Hamburger**: Klik tombol menu (hamburger) untuk menunjukkan fitur sembunyikan/tampilkan sidebar navigasi baik di desktop maupun mobile.
   - **Menu Kategori Acara**: Klik header kategori acara untuk memperlihatkan animasi akordeon buka-tutup (*minimize/expand*).
   - **Form Registrasi Tamu**: Tunjukkan *live character counter* (0/500 karakter), pilihan kategori acara, dan tombol submit.
   - **Toolbar Riwayat & Filter Tanggal**: Tunjukkan tombol preset "Semua Tanggal", "Hari Ini", dan pemilih kalender tanggal spesifik.
   - **Aksi Cetak**: Buka modal "Cetak Badge Akses" dan tombol "Unduh PDF".

#### 🗣️ Naskah / Contoh Kalimat Presenter:
> *"Sekarang kita berada di antarmuka web SITAMU pada URL `localhost:8081`. Desain web ini mengadopsi standar identitas resmi Telkom University dengan warna khas Crimson Red `#e01a3f` dan Dark Neutral `#343a40`.*
>
> *Berikut adalah fitur-fitur unggulan pada antarmuka:
> - **Branding Resmi**: Terdapat logo Telkom University yang proporsional di header sidebar serta favicon resmi di tab peramban.
> - **Sidebar Navigasi Responsif**: Dilengkapi tombol hamburger universal yang memungkinkan pengguna menyembunyikan atau memunculkan bilah navigasi dengan animasi halus, memberikan kenyamanan penuh di layar desktop maupun gawai mobile.
> - **Kategori Acara Dinamis**: Menu kategori acara dapat diminimalkan (accordion collapsible) dan tombol yang aktif ditandai dengan sorotan aksen merah yang konsisten.
> - **Form Registrasi Tamu Interaktif**: Dilengkapi validasi form instan, penghitung karakter langsung (*live character counter*), serta pengamanan sanitasi input dari risiko serangan XSS (*Cross-Site Scripting*).
> - **Manajemen Riwayat Kunjungan**: Pengguna resepsionis dapat memfilter data tamu berdasarkan kategori acara maupun tanggal kunjungan masa lalu menggunakan fitur pemilih tanggal kalender.
> - **Fitur Pelaporan Akademik**: Tersedia tombol **Unduh PDF** yang menghasilkan dokumen cetak ber-kop resmi Telkom University (bukan tangkapan layar mentah), serta tombol **Cetak Badge** untuk menghasilkan kartu identitas tanda masuk pengunjung resmi kampus."*

---

### 🎙️ SEGMEN 3: Pengujian CRUD & Error Handling REST API (02:45 - 04:00)
#### 📌 Tindakan Praktis:
1. **Uji CREATE (POST)**:
   - Isi form:
     - Nama Tamu: `Dr. Hendra Wijaya, M.T.`
     - Instansi / Lembaga: `Institut Teknologi Bandung (ITB)`
     - Kategori: `Seminar & Kuliah Umum`
     - Keperluan: `Narasumber Kuliah Umum Cloud Native & DevOps Architecture`
   - Klik tombol **Kirim Data Buku Tamu**.
   - Tunjukkan notifikasi *toast* sukses berwarna merah-putih dan data langsung muncul di tabel paling atas secara instan tanpa me-refresh browser.
2. **Uji READ (GET)**:
   - Buka tab baru ke `http://localhost:8000/messages` untuk memperlihatkan bahwa data tersimpan dalam format JSON REST API standar yang rapi.
3. **Uji DELETE**:
   - Kembali ke tabel tamu di `localhost:8081`.
   - Klik tombol ikon hapus (*checkout*) pada baris tamu yang baru dibuat.
   - Tunjukkan munculnya **Modal Konfirmasi Hapus** (mencegah klik tak sengaja).
   - Klik tombol konfirmasi **Ya, Hapus Tamu**.
   - Tunjukkan baris data langsung hilang secara real-time dari tabel dengan konfirmasi *toast*.
4. **Uji Error Handling**:
   - Coba klik tombol submit form dengan kondisi form kosong.
   - Tunjukkan sistem menolak pengiriman dan memberikan pesan validasi (HTTP 400 Bad Request prevention).

#### 🗣️ Naskah / Contoh Kalimat Presenter:
> *"Sekarang kita buktikan pemenuhan Komponen 1 (Backend Python API) dan Komponen 2 (Frontend Vanilla JS):
>
> 1. **Operasi POST**: Kita masukkan data tamu baru, Dr. Hendra Wijaya dari ITB untuk kegiatan Kuliah Umum. Ketika tombol kirim ditekan, Javascript mengeksekusi `fetch()` asynchronous dengan metode POST dan header `application/json`. Respon HTTP `201 Created` diterima dan data langsung masuk ke tabel secara real-time.
> 2. **Operasi GET**: Di background, aplikasi memanggil endpoint GET `/messages` yang mengembalikan seluruh daftar tamu dalam format JSON murni.
> 3. **Operasi DELETE**: Untuk menghapus atau melakukan check-out tamu, kita klik ikon hapus. Sistem menampilkan modal dialog konfirmasi demi keamanan data. Saat disetujui, query DELETE dikirimkan ke `/messages?index=X` dan baris data terhapus seketika tanpa perlu refresh halaman manual.
> 4. **Error Handling**: API dan Frontend dilengkapi error handling presisi. Jika payload kosong atau tipe konten tidak sesuai, server secara ketat menolak dengan status HTTP 400 Bad Request atau 415 Unsupported Media Type."*

---

### 🎙️ SEGMEN 4: Pengujian Data Immunity & Bind Mount (04:00 - 05:15)
*(Ini adalah poin pengujian berbobot tinggi: 25% Docker Storage Config + 15% Bind Mount).*

#### 📌 Tindakan Praktis 1 — Data Immunity (Docker Named Volume):
1. Input satu data tamu sebagai pembuktian:
   - Nama: `Budi Santoso - Uji Persistensi`
   - Instansi: `Telkom Regional III`
   - Keperluan: `Pengujian Data Immunity UTS`
2. Klik kirim dan pastikan data tampil di tabel.
3. Buka **Terminal / PowerShell**:
   - Jalankan perintah untuk melihat status kontainer:
     ```bash
     docker ps
     ```
   - Hancurkan kontainer backend secara paksa:
     ```bash
     docker rm -f guestbook-backend
     ```
   - Tunjukkan di terminal bahwa kontainer `guestbook-backend` sudah benar-benar terhapus:
     ```bash
     docker ps
     ```
4. Buka kembali browser `http://localhost:8081` dan refresh halaman:
   - Tunjukkan indikator koneksi di antarmuka berubah menjadi offline / server tidak merespons (karena backend sengaja kita matikan).
5. Kembali ke terminal dan hidupkan kembali kontainer backend dengan menghubungkannya ke **Named Volume** yang sama:
   ```bash
   docker run -d --name guestbook-backend --network app-net --network-alias backend -p 8000:8000 -v guestbook-db-data:/var/lib/backend_data belajar-backend:latest
   ```
6. Kembali ke browser dan refresh `http://localhost:8081`:
   - **Tunjukkan bahwa data `Budi Santoso - Uji Persistensi` MASIH ADA dan UTUH 100%!**

#### 📌 Tindakan Praktis 2 — Live Reload Bind Mount:
1. Buka file `index.html` di VS Code pada baris judul sub-header (sekitar baris 280):
   - Ubah teks:
     ```html
     <!-- Dari: -->
     <span class="text-xs text-[#6c757d]">Kampus Utama Telkom University Bandung</span>
     <!-- Menjadi: -->
     <span class="text-xs text-[#6c757d]">Kampus Utama Telkom University Bandung • Live Bind Mount Active</span>
     ```
2. Simpan file (`Ctrl + S`).
3. Kembali ke browser `http://localhost:8081` dan tekan `F5` / Refresh:
   - Tunjukkan teks langsung ter-update secara instan **tanpa perlu menjalankan `docker build`**.
   - Kembalikan teks ke semula dan simpan lagi.

#### 🗣️ Naskah / Contoh Kalimat Presenter:
> *"Pada Komponen 3, rubrik meminta pembuktian 'Data Immunity' menggunakan Docker Named Volume serta fungsi Bind Mount:
>
> 1. **Pengujian Data Immunity**: Kita telah memasukkan data tamu bernama 'Budi Santoso'. Sekarang kita buka terminal dan menghapus paksa kontainer backend menggunakan perintah `docker rm -f guestbook-backend`. Kontainer backend kini telah hancur dan status web sempat terputus.
> 
> Lalu, kita spawn kontainer baru yang dimount ke Named Volume `guestbook-db-data` pada direktori target `/var/lib/backend_data`. Ketika halaman di-refresh, dapat kita lihat bahwa data tamu 'Budi Santoso' tetap tersimpan dengan utuh 100%! Ini membuktikan bahwa penyimpanan data terisolasi sempurna di luar siklus hidup (*lifecycle*) kontainer.
>
> 2. **Pengujian Bind Mount**: Pada kontainer Frontend Nginx, file `index.html` dipetakan menggunakan host Bind Mount. Ketika kita mengubah teks di editor host lokal dan menyimpan perubahan, tampilan pada peramban langsung diperbarui seketika tanpa perlu melakukan build ulang Docker image."*

---

### 🎙️ SEGMEN 5: Pengujian Otomasi CI/CD & GitHub Webhook (05:15 - 07:00)
*(Ini adalah poin pengujian berbobot tinggi: 25% Jenkins CI/CD Pipeline).*

#### 📌 Tindakan Praktis:
1. Buka tab browser di **Dashboard Jenkins**:
   - `http://localhost:8085/job/chunin-guestbook-pipeline/`
   - Perlihatkan riwayat build yang ada saat ini (misal Build terakhir adalah #19 dengan status hijau/biru `SUCCESS`).
2. Buka terminal atau VS Code untuk membuat perubahan kecil yang memicu commit:
   - Buka `README.md` atau beri komentar kecil di `app.py`.
   - Jalankan perintah git:
     ```bash
     git add .
     git commit -m "test(demo): verifikasi otomatisasi pipeline ci-cd uts"
     git push origin main
     ```
3. Langsung kembali ke tab **Jenkins Dashboard**:
   - Tunggu 2-5 detik tanpa menekan tombol "Build Now".
   - Tunjukkan antrean build baru (misal Build #20) otomatis berjalan sendiri karena adanya sinyal push event dari GitHub Webhook via tunnel ngrok.
4. Klik build yang sedang berjalan dan buka tampilan **Pipeline Console Output** atau **Stage View**:
   - Tunjukkan kelima stage yang berhasil dieksekusi secara berurutan:
     1. **Stage 1: Checkout SCM** *(Mengambil kode terbaru dari branch `main`)*
     2. **Stage 2: Syntax Check & Unit Testing** *(Menjalankan `python test_app.py`, 13 dari 13 unit tests passed)*
     3. **Stage 3: Build Docker Image** *(Membangun image `belajar-backend:latest`)*
     4. **Stage 4: Automated Container Deployment** *(Me-restart dan memastikan kontainer `guestbook-backend` dan `guestbook-frontend` berjalan di `app-net`)*
     5. **Stage 5: Health Check & Verification** *(Memvalidasi endpoint `/health` dan `/messages` dengan status 200 OK)*
5. Tunjukkan status akhir build bernilai **Finished: SUCCESS**.
6. Buka kembali `http://localhost:8081` untuk memastikan aplikasi tetap berjalan normal setelah auto-deploy.

#### 🗣️ Naskah / Contoh Kalimat Presenter:
> *"Masuk ke Komponen 4, yaitu otomatisasi CI/CD Pipeline menggunakan Jenkins dan GitHub Webhook:
>
> Di layar terlihat dashboard Jenkins untuk job `chunin-guestbook-pipeline`. Sekarang, pengembang melakukan push kode ke branch `main` repositori GitHub. 
> 
> Tanpa perlu menyentuh tombol 'Build Now' di Jenkins, webhook GitHub yang dikonfigurasi melalui secure tunnel ngrok langsung memicu proses build secara instan.
>
> Pipeline ini mengeksekusi 5 Stage deklaratif:
> 1. **Checkout**: Mengambil kode sumber terbaru dari GitHub.
> 2. **Syntax Check & Unit Test**: Menjalankan 13 suite unit testing pada backend Python untuk memverifikasi seluruh respons status kode sebelum rilis.
> 3. **Build Image**: Mengemas aplikasi backend ke dalam Docker image berbasis Alpine Linux yang ringkas dan aman.
> 4. **Automated Deployment**: Menerapkan kontainer baru ke dalam jaringan `app-net` tanpa menghapus persistent volume database.
> 5. **Health Check**: Melakukan audit otomatis terhadap respon API lokal hingga memastikan status HTTP 200 OK.
>
> Seluruh stage berhasil dieksekusi dengan status akhir **SUCCESS**."*

---

### 🎙️ SEGMEN 6: Penutup & Verifikasi Berkas Pengumpulan (07:00 - 07:45)
#### 📌 Tindakan Praktis:
1. Buka halaman utama repositori GitHub kelompok:
   - [https://github.com/ervanfahriaw/ci-cd-uts](https://github.com/ervanfahriaw/ci-cd-uts)
2. Tunjukkan struktur berkas wajib:
   - `app.py`
   - `index.html`
   - `Dockerfile`
   - `docker-compose.yml`
   - `Jenkinsfile`
   - `README.md`
3. Gulir ke bawah halaman GitHub untuk memperlihatkan **README.md** yang memuat:
   - Identitas Anggota Kelompok lengkap (Nama & NIM)
   - Deskripsi Studi Kasus No. 1
   - Diagram Arsitektur Docker & Network
   - Panduan Instalasi Lokal & Jenkins

#### 🗣️ Naskah / Contoh Kalimat Presenter:
> *"Sebagai penutup, seluruh berkas deliverables tugas UTS Chunin Exam telah diunggah ke repositori GitHub publik kami di alamat `github.com/ervanfahriaw/ci-cd-uts`.
> 
> Berkas-berkas wajib mencakup:
> 1. Kode sumber Backend `app.py`, Frontend `index.html`, serta pengujian `test_app.py`.
> 2. Berkas kontainerisasi `Dockerfile` dan `docker-compose.yml`.
> 3. Skrip otomatisasi `Jenkinsfile` dengan 5 tahapan pipeline.
> 4. Dokumentasi komprehensif pada `README.md` yang memuat identitas kelompok, diagram arsitektur, dan petunjuk operasional lengkap.
>
> Demikian demonstrasi dan pengujian proyek Cloud Computing Chunin Exam dari kelompok kami. Terima kasih atas perhatian Bapak/Ibu Dosen Pengampu dan rekan-rekan semua. Wassalamualaikum wr. wb."*

---

## 📊 4. Lembar Verifikasi Mandiri Terhadap Rubrik Penilaian (CSO Rubric Checklist)

Gunakan tabel ini untuk memastikan seluruh kriteria penilaian maksimal tercapai sebelum mengumpulkan tautan video:

| No | Komponen Penilaian | Bobot | Kriteria Nilai Maksimal (85–100) | Status Pemenuhan Proyek | Bukti dalam Demo |
|:--:|:---|:---:|:---|:---:|:---|
| **1** | **Backend Python API** | **20%** | Fitur CRUD lengkap (GET, POST, DELETE), respons JSON rapi, error handling (400/404) presisi. | **Sangat Baik (100)** | Ditunjukkan di **Segmen 3**: Operasi POST tamu, GET daftar JSON, DELETE dengan modal, dan validasi form. |
| **2** | **Frontend HTML & JS** | **15%** | Tampilan UI bersih, fetch() JS lancar, tombol Delete berfungsi real-time tanpa reload. | **Sangat Baik (100)** | Ditunjukkan di **Segmen 2 & 3**: UI SITAMU resmi Telkom University, responsive navbar, live updates. |
| **3** | **Docker & Storage Config** | **25%** | Named Volume terbukti menjaga data saat kontainer di-dismantle (`docker rm -f`), Bind Mount berfungsi. | **Sangat Baik (100)** | Ditunjukkan di **Segmen 4**: Hancurkan kontainer backend, spawn ulang, data 100% aman; edit `index.html` live update. |
| **4** | **Jenkins CI/CD Pipeline** | **25%** | Jenkinsfile sukses mengeksekusi seluruh stage (Checkout, Test, Build, Deploy, Health Check) via Webhook. | **Sangat Baik (100)** | Ditunjukkan di **Segmen 5**: `git push` otomatis men-trigger Jenkins via GitHub webhook hingga build **SUCCESS**. |
| **5** | **Dokumentasi & Demo** | **15%** | README.md memuat diagram arsitektur, petunjuk lengkap, & video demo memperlihatkan git push hingga auto-deploy. | **Sangat Baik (100)** | Ditunjukkan di **Segmen 1 & 6**: README lengkap dengan Mermaid diagram, video 5–8 menit mencakup seluruh siklus. |

---

## 💡 5. Tips Teknis Perekaman Video Presentasi
1. **Resolusi Rekaman**: Rekam layar pada resolusi minimal 1080p (1920x1080) dengan framerate 30 fps atau 60 fps agar teks baris perintah dan antarmuka web terbaca jelas oleh dosen penilai.
2. **Audio Jernih**: Gunakan mikrofon headset atau mic eksternal dengan volume stabil dan tanpa noise latar belakang.
3. **Pembagian Suara Anggota**: Apabila seluruh anggota kelompok berbicara, bagi segmen di atas secara adil (misal Anggota 1 untuk Segmen 1 & 2, Anggota 2 untuk Segmen 3, Anggota 3 untuk Segmen 4, Anggota 4 untuk Segmen 5 & 6).
4. **Platform Pengunggahan Video**: Unggah video hasil rekaman ke **Google Drive** (pastikan akses diset ke *Anyone with the link can view / Siapa saja yang memiliki link dapat melihat*) atau **YouTube Unlisted**, kemudian cantumkan tautannya pada portal LMS pengumpulan UTS.
