# Panduan Pengguna
## Rik0Sec CTF Quick Launcher v1.1.0

Panduan ini ditujukan untuk mahasiswa dan pemula yang ingin menggunakan launcher dalam CTF, praktikum, atau lab keamanan siber yang memiliki izin. Baca perintah yang ditampilkan sebelum menyetujuinya.

## 1. Mengenal CTF Quick Launcher

CTF (*Capture The Flag*) adalah latihan keamanan siber berbasis tantangan. Peserta dapat diminta menganalisis file, trafik jaringan, encoding, konfigurasi Linux, log, atau aplikasi untuk menemukan bukti dan flag.

Rik0Sec CTF Quick Launcher membantu:
- memilih kategori pemeriksaan;
- mengecek ketersediaan executable pendukung;
- menampilkan perintah yang akan dijalankan;
- meminta persetujuan sebelum menjalankan perintah tertentu.

**Launcher bukan auto-solver dan tidak menjamin flag ditemukan.** Pengguna tetap perlu memahami soal dan menafsirkan hasil.

## 2. Persiapan

### Persyaratan dasar

- Python 3.9 atau lebih baru.
- Linux direkomendasikan, terutama Kali Linux.
- Tools eksternal sesuai kategori yang ingin digunakan. Tidak semua tools wajib tersedia.
- Tidak diperlukan package Python pihak ketiga.

Periksa Python:

```bash
python3 --version
```

Jika perintah tidak ditemukan, instal Python melalui package manager distro.

## 3. Memilih lingkungan

Ada tiga cara umum menggunakan launcher.

### A. Kali Linux atau Ubuntu secara langsung

Pada Kali/Ubuntu, buka terminal dan jalankan:

```bash
sudo apt update
sudo apt install -y python3 git
git clone https://github.com/rik0sec/rik0sec-ctf-quick-launcher.git
cd rik0sec-ctf-quick-launcher
python3 ctf_quick_launcher.py
```

 Jika repository diunduh sebagai ZIP, ekstrak terlebih dahulu, lalu `cd` ke folder hasil ekstraksi.

### B. Windows melalui WSL2

WSL2 memungkinkan menjalankan distro Linux dari Windows tanpa VM desktop penuh.

1. Buka PowerShell atau Windows Terminal sebagai Administrator.
2. Jalankan:

   ```powershell
   wsl --install -d Ubuntu
   ```

3. Restart jika Windows meminta.
4. Buka Ubuntu dari Start Menu, lalu buat username dan password Linux.
5. Di terminal Ubuntu:

   ```bash
   sudo apt update
   sudo apt install -y python3 git
   git clone https://github.com/rik0sec/rik0sec-ctf-quick-launcher.git
   cd rik0sec-ctf-quick-launcher
   python3 ctf_quick_launcher.py
   ```

Jika WSL sudah terpasang, lewati instalasi WSL dan langsung gunakan distro Linux yang tersedia. Pengguna dapat memilih Ubuntu sebagai awal yang sederhana atau memasang distro Kali melalui panduan resmi Kali Linux.

**Catatan batasan WSL:** WSL cocok untuk menjalankan CLI dan mempelajari banyak fitur launcher. Namun, akses capture jaringan, interface, system journal, firewall, dan GUI dapat berbeda dari Linux penuh. Pemeriksaan firewall di WSL bukan pemeriksaan firewall Windows. Untuk eksperimen jaringan dan fitur yang memerlukan akses sistem lebih lengkap, VM biasanya lebih mudah dipisahkan dari host.

### C. VirtualBox dengan Kali Linux atau Ubuntu

VirtualBox direkomendasikan jika ingin lingkungan lab Linux yang lebih terisolasi dan konsisten.

1. Instal Oracle VirtualBox.
2. Unduh ISO Kali Linux atau Ubuntu dari situs resminya.
3. Buat VM baru dan instal sistem operasi.
4. Jalankan VM, buka terminal, lalu instal kebutuhan dasar:

   ```bash
   sudo apt update
   sudo apt install -y python3 git
   ```

5. Clone dan jalankan project:

   ```bash
   git clone https://github.com/rik0sec/rik0sec-ctf-quick-launcher.git
   cd rik0sec-ctf-quick-launcher
   python3 ctf_quick_launcher.py
   ```

Untuk koneksi internet biasa, NAT umumnya cukup. Untuk lab antar-VM, pertimbangkan Host-only atau Internal Network. Jangan gunakan Bridged Adapter untuk eksperimen yang berisiko menjangkau jaringan nyata kecuali memang diperlukan dan diizinkan.

## 4. Menjalankan project dari ZIP

Jika mengunduh ZIP dari GitHub, pindah ke folder Downloads dan ekstrak:

```bash
cd ~/Downloads
unzip rik0sec-ctf-quick-launcher.zip
cd rik0sec-ctf-quick-launcher
python3 ctf_quick_launcher.py
```

Nama folder hasil ekstraksi dapat berbeda sesuai nama ZIP yang diunduh. Sesuaikan perintah `cd` dengan nama folder sebenarnya.

Alternatif:

```bash
chmod +x ctf_quick_launcher.py
./ctf_quick_launcher.py
```

Perintah `chmod` bersifat opsional; menjalankan dengan `python3` sudah cukup.

## 5. Memahami menu utama

Menu utama menyediakan kategori berikut:

| Menu | Pilih saat soal membahas... |
|---|---|
| 1. Network & PCAP | File `.pcap`/`.pcapng`, HTTP, DNS, FTP, SMTP, TCP |
| 2. Cryptography | Base64, Hex, XOR, RSA sederhana, JWT/hash |
| 3. Web & API (manual) | Website, endpoint, request/response, cookie, JWT |
| 4. Linux & SUID | Permission Linux, SUID, capabilities |
| 5. Forensics & files | File misterius, metadata, strings, signature |
| 6. Logs & incident response | Log login, aktivitas sistem, indikasi insiden |
| 7. Firewall & ACL | Aturan firewall dan Linux File ACL |
| 8. Cek semua tools | Memeriksa executable pendukung di PATH |
| 0. Keluar | Menutup launcher |

Menu 8 hanya memeriksa apakah executable ditemukan di PATH. Status `[OK]` bukan jaminan bahwa semua fungsi tool tersebut berjalan atau bahwa hak akses sudah mencukupi.

## 6. Konfirmasi sebelum menjalankan

Untuk perintah eksternal, launcher menampilkan perintah dan prompt:

```text
Jalankan? [y/N]:
```

- Ketik `y` lalu Enter untuk menyetujui.
- Tekan Enter atau ketik `n` untuk membatalkan.

Periksa nama file, path, target, dan opsi perintah terlebih dahulu. Launcher memanggil program sebagai daftar argumen proses, bukan melalui shell, tetapi perintah yang dijalankan tetap dapat membaca data atau berinteraksi dengan sistem sesuai fungsinya.

## 7. Panduan setiap kategori

### A. Network & PCAP

Gunakan jika soal menyediakan file capture jaringan.

Pilihan:
1. Ringkasan PCAP.
2. Statistik protokol.
3. HTTP request.
4. DNS query.
5. TCP stream.
6. Nmap service scan untuk target CTF/lab yang diizinkan.

Contoh mencari DNS:
1. Pilih menu `1`, lalu `4`.
2. Masukkan path PCAP, misalnya `/home/kali/Downloads/capture.pcap`.
3. Periksa perintah yang ditampilkan.
4. Setujui dengan `y`.
5. Analisis nama domain yang muncul.

Jika tidak ada baris DNS, bisa jadi capture memang tidak berisi paket DNS. Itu tidak otomatis menandakan fitur gagal.

**Nmap:** masukkan hanya IP/hostname target yang secara eksplisit termasuk scope dan diizinkan. Hindari pemindaian rentang jaringan luas. Hasil scan disimpan sebagai `nmap-result.txt` pada working directory saat launcher dijalankan.

### B. Cryptography

Gunakan untuk encoding atau latihan kriptografi sederhana.

- **Base64 decode:** masukkan string Base64.
- **Hex decode:** masukkan string hexadecimal.
- **Reverse → Hex → Base64:** jalankan transformasi berurutan sesuai format soal.
- **RSA textbook:** masukkan nilai `p`, `q`, `e`, dan `c` yang diberikan soal. Ditujukan untuk contoh RSA sederhana, bukan memecahkan enkripsi modern.
- **XOR repeating key:** masukkan ciphertext dalam format Hex dan key teks.
- **Referensi Hashcat JWT HS256:** menampilkan contoh command untuk latihan yang diizinkan; launcher tidak menjalankan cracking otomatis.

Hasil decode yang tidak terbaca dapat berarti urutan transformasi berbeda atau data bukan teks biasa.

### C. Web & API (manual)

Menu ini bersifat manual, bukan scanner atau exploit otomatis. Fitur:
- template `curl` GET dan POST;
- decode header dan payload JWT;
- checklist pengujian manual;
- membuka Burp Suite jika tersedia.

Contoh template:

```bash
curl -i 'https://<HOST_LAB>/<PATH>'
```

Ganti placeholder dengan host dan path yang diberikan platform CTF. Jangan menguji sistem publik tanpa izin.

**JWT:** decoder hanya membaca header dan payload. Ini tidak memverifikasi signature, masa berlaku, maupun penerimaan token oleh server.

### D. Linux & SUID

Gunakan untuk memeriksa konfigurasi sistem Linux lokal:
1. Daftar file SUID lokal.
2. Periksa permission file.
3. Cari Linux capabilities.
4. Periksa permission path.

Pemindaian seluruh filesystem dapat memerlukan waktu dan menampilkan `Permission denied` pada direktori tertentu. Itu tidak otomatis berarti ada kerentanan. File SUID atau capability juga tidak otomatis rentan; analisis konteks dan permission secara hati-hati.

### E. Forensics & files

Gunakan jika soal menyediakan file untuk dianalisis.

Pilihan:
- `file`: identifikasi tipe file;
- `exiftool`: membaca metadata;
- `strings`: menampilkan teks yang dapat dibaca;
- `binwalk`: mengenali signature/struktur file;
- `xxd`: menampilkan hexadecimal dump.

Masukkan path file yang benar, misalnya:

```text
/home/kali/Downloads/suspicious.bin
```

Hasil `strings` tidak selalu menampilkan metadata terkompresi atau data biner. Gunakan beberapa metode dan cocokkan dengan petunjuk soal.

### F. Logs & incident response

Pilihan:
1. Cari pola dalam file log.
2. Riwayat login.
3. Listening sockets.
4. Journal terbaru (100 entri).

Contoh pencarian:
1. Pilih `6`, lalu `1`.
2. Masukkan path file log.
3. Masukkan pola seperti `failed`.
4. Periksa hasil dan konteks timestamp, username, alamat IP, serta pesan log.

Ketersediaan `last` berbeda antar distro/versi. Pada beberapa sistem, perintah tersebut dapat disediakan oleh paket `wtmpdb`. Jika tidak ditemukan, pasang paket yang sesuai untuk distro atau lewati fitur tersebut.

### G. Firewall & ACL

Menu ini menyediakan pemeriksaan **read-only**:

| Pilihan | Fungsi | Perintah |
|---|---|---|
| 1 | Aturan iptables IPv4 | `iptables -L -n -v --line-numbers` |
| 2 | Ruleset nftables | `nft list ruleset` |
| 3 | Status UFW | `ufw status verbose` |
| 4 | Linux File ACL pada path yang dipilih | `getfacl -p <path>` |

Perintah iptables, nftables, dan UFW dapat membutuhkan root. Jika muncul `Permission denied`, `Operation not permitted`, atau `You need to be root`, pemeriksaan belum memperoleh hak akses yang diperlukan. Jalankan pemeriksaan dengan hak akses yang sesuai secara sadar, misalnya dari terminal terpisah menggunakan `sudo` untuk satu perintah yang memang dipahami. Jangan menjalankan seluruh launcher sebagai root hanya untuk membaca firewall.

Linux File ACL berbeda dari Network ACL:
- Linux File ACL mengatur hak user/group pada file atau direktori.
- Firewall mengatur lalu lintas jaringan.

### H. Cek semua tools

Pilih `8` dari menu utama:
- `[OK]`: executable ditemukan di PATH.
- `[--]`: executable tidak ditemukan di PATH.

Tools bersifat opsional. Jika hanya menggunakan fitur Base64, misalnya, tidak perlu memasang Nmap atau Wireshark.

## 8. Instalasi tools tambahan (opsional)

Di Kali/Debian, beberapa paket umum dapat dipasang dengan `apt`. Nama paket dan ketersediaan dapat berbeda sesuai versi distro:

```bash
sudo apt update
sudo apt install -y tshark tcpdump nmap openssl hashcat john \
  curl exiftool binwalk acl nftables iptables ufw
```

Jangan memasang semuanya jika tidak diperlukan. Untuk Burp Suite, Wireshark, atau tools lain, ikuti dokumentasi paket/distro yang digunakan. `requirements.txt` tidak perlu dipasang karena launcher hanya menggunakan Python standard library.

## 9. Troubleshooting

| Kondisi | Penjelasan / tindakan |
|---|---|
| `python3: command not found` | Instal Python 3 melalui package manager distro. |
| Tool tidak ditemukan | Periksa menu 8 dan instal paket yang menyediakan executable tersebut jika dibutuhkan. |
| File tidak ditemukan | Periksa ejaan dan path; gunakan path lengkap. |
| `Permission denied` | Periksa izin file atau kebutuhan hak akses. Jangan langsung menjalankan seluruh launcher sebagai root. |
| Firewall meminta root | Jalankan hanya pemeriksaan terkait dengan hak akses yang sesuai dan pahami command-nya. |
| `last` tidak ditemukan | Ketersediaan berbeda antar distro; pada beberapa Kali/Debian dapat disediakan oleh paket `wtmpdb`. |
| Tidak ada hasil DNS/HTTP | Capture mungkin tidak berisi protokol/filter yang dicari. |
| `Invalid hex` | Pastikan input hanya berisi karakter hexadecimal yang valid. |
| Hasil decode tidak terbaca | Periksa kemungkinan encoding berlapis atau data biner. |
| WSL tidak menampilkan informasi sistem/jaringan yang diharapkan | WSL memiliki batas integrasi dengan host dan kernel; gunakan VM Linux untuk lab yang memerlukan lingkungan Linux penuh. |

## 10. Tips belajar dan keamanan

1. Baca deskripsi soal sebelum memilih kategori.
2. Jalankan satu pemeriksaan pada satu waktu.
3. Simpan output yang relevan dan catat proses analisis.
4. Validasi temuan dengan bukti, bukan tebakan.
5. Patuhi scope, aturan platform, dan batas percobaan.
6. Gunakan hanya untuk CTF, praktikum, sistem sendiri, atau lab yang memberi izin.
7. Jangan memasukkan password, token pribadi, private key, atau data rahasia.
8. Jangan mengunggah PCAP/log yang mengandung data pribadi atau flag yang dilarang dibagikan.

## 11. Keluar dari program

Pilih `0` pada menu utama. Untuk menghentikan proses yang sedang berjalan, tekan `Ctrl+C`.

Selamat belajar. Fokus pada pemahaman proses analisis, bukan hanya menemukan flag.
