#!/usr/bin/env python3
"""Rik0Sec CTF Quick Launcher — authorized CTF/lab helper. Python 3.9+, stdlib only."""
import base64, binascii, json, shutil, subprocess
from pathlib import Path

VERSION = "1.1.0"
TOOLS = {
    "Network & PCAP": ["tshark", "capinfos", "wireshark", "tcpdump", "nmap"],
    "Cryptography": ["python3", "openssl", "hashcat", "john"],
    "Web & API (manual)": ["burpsuite", "curl", "firefox"],
    "Linux & SUID": ["find", "stat", "getcap", "namei", "grep"],
    "Forensics & files": ["file", "exiftool", "binwalk", "strings", "xxd"],
    "Logs & incident response": ["grep", "awk", "journalctl", "last", "ss"],
    "Firewall & ACL": ["iptables", "nft", "ufw", "getfacl"],
}

def header(title):
    print("\n" + "=" * 60 + "\n " + title + "\n" + "=" * 60)

def pause():
    input("\nTekan Enter untuk kembali...")

def toolcheck():
    header("PEMERIKSAAN TOOLS")
    for group, names in TOOLS.items():
        print("\n" + group)
        for name in names:
            path = shutil.which(name)
            print(f"  [{'OK' if path else '--'}] {name:<12} {path or 'tidak ditemukan'}")
    print("\nOK berarti executable ditemukan, bukan jaminan semua fiturnya berjalan.")

def existing_file():
    raw = input("Path file (kosong untuk batal): ").strip()
    if not raw:
        return None
    p = Path(raw).expanduser()
    if not p.is_file():
        print("File tidak ditemukan atau bukan file biasa.")
        return None
    return str(p.resolve())


def existing_path():
    """Minta path file/direktori yang sudah ada untuk pemeriksaan read-only."""
    raw = input("Path file/direktori (kosong untuk batal): ").strip()
    if not raw:
        return None
    p = Path(raw).expanduser()
    if not p.exists():
        print("Path tidak ditemukan.")
        return None
    return str(p.resolve())

def run(args, desc, timeout=120):
    print(f"\n{desc}\n$ " + " ".join(map(str, args)))
    if input("Jalankan? [y/N]: ").strip().lower() != "y":
        print("Dibatalkan.")
        return
    try:
        subprocess.run(list(args), check=False, timeout=timeout)
    except FileNotFoundError:
        print("Executable tidak ditemukan:", args[0])
    except subprocess.TimeoutExpired:
        print("Melewati batas waktu.")
    except KeyboardInterrupt:
        print("\nDihentikan pengguna.")

def network():
    header("NETWORK & PCAP")
    print("1 Ringkasan PCAP\n2 Statistik protokol\n3 HTTP request\n4 DNS query\n5 TCP stream\n6 Nmap service scan (target lab berizin)\n0 Kembali")
    c = input("Pilih: ").strip()
    if c == "6":
        nmap = shutil.which("nmap")
        target = input("IP/hostname target CTF/lab yang diizinkan: ").strip()
        if nmap and target and not target.startswith("-") and not any(x.isspace() for x in target):
            print("Hanya scan target yang secara eksplisit diizinkan.")
            run([nmap, "-sV", "-oN", "nmap-result.txt", target], "Nmap service scan", 300)
        else:
            print("Target tidak valid atau Nmap tidak tersedia.")
        return
    if c not in {"1","2","3","4","5"}: return
    p = existing_file()
    tshark = shutil.which("tshark")
    if not p or not tshark:
        print("File tidak dipilih atau tshark tidak tersedia."); return
    base = [tshark, "-r", p]
    if c == "1":
        cap = shutil.which("capinfos")
        run([cap, p] if cap else base + ["-c","30"], "Ringkasan capture")
    elif c == "2": run(base + ["-q","-z","io,phs"], "Statistik protokol")
    elif c == "3": run(base + ["-Y","http.request","-T","fields","-e","frame.number","-e","ip.src","-e","http.host","-e","http.request.uri"], "HTTP request")
    elif c == "4": run(base + ["-Y","dns","-T","fields","-e","frame.number","-e","ip.src","-e","dns.qry.name"], "DNS query")
    else:
        stream = input("Nomor TCP stream [0]: ").strip() or "0"
        if stream.isdigit(): run(base + ["-q","-z",f"follow,tcp,ascii,{stream}"], "TCP stream")
        else: print("Nomor stream harus angka.")

def crypto():
    header("CRYPTOGRAPHY")
    print("1 Base64 decode\n2 Hex decode\n3 Reverse -> Hex -> Base64\n4 RSA textbook (p,q,e,c)\n5 XOR repeating key\n6 Referensi Hashcat JWT HS256\n0 Kembali")
    c = input("Pilih: ").strip()
    try:
        if c == "1":
            print(base64.b64decode(input("Base64: ").strip(), validate=True).decode(errors="replace"))
        elif c == "2":
            print(bytes.fromhex(input("Hex: ").strip()))
        elif c == "3":
            s = input("String Hex (boleh diawali data: ): ").strip()
            if s.lower().startswith("data:"): s = s.split(":",1)[1].strip()
            print(base64.b64decode(bytes.fromhex(s[::-1]), validate=True).decode(errors="replace"))
        elif c == "4":
            p=int(input("p: ")); q=int(input("q: ")); e=int(input("e: ")); cipher=int(input("c: "))
            n=p*q; phi=(p-1)*(q-1); d=pow(e,-1,phi); m=pow(cipher,d,n)
            print("Plaintext:", m.to_bytes(max(1,(m.bit_length()+7)//8),"big"))
        elif c == "5":
            data=bytes.fromhex(input("Ciphertext Hex: ")); key=input("Key: ").encode()
            if not key: print("Key kosong.")
            else:
                out=bytes(b ^ key[i%len(key)] for i,b in enumerate(data))
                print("Bytes:",out); print("Text:",out.decode(errors="replace"))
        elif c == "6":
            print("Untuk token/wordlist CTF yang diizinkan:\n  hashcat -m 16500 <jwt_file> <wordlist>")
    except (ValueError, binascii.Error) as e: print("Input/decoding tidak valid:", e)

def web():
    header("WEB & API — MANUAL")
    print("1 Template curl GET\n2 Template curl POST\n3 Decode JWT header/payload\n4 Checklist manual\n5 Buka Burp Suite\n0 Kembali")
    c=input("Pilih: ").strip()
    if c=="1": print("curl -i 'https://<HOST_LAB>/<PATH>'")
    elif c=="2": print("curl -i -X POST 'https://<HOST_LAB>/<PATH>' -H 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'key=value'")
    elif c=="3":
        try:
            parts=input("JWT: ").strip().split(".")
            if len(parts)!=3: raise ValueError("JWT harus punya tiga bagian.")
            def dec(s): return json.loads(base64.urlsafe_b64decode(s + "="*(-len(s)%4)))
            print("Header:",json.dumps(dec(parts[0]),indent=2)); print("Payload:",json.dumps(dec(parts[1]),indent=2))
            print("Decode bukan verifikasi signature/token.")
        except Exception as e: print("JWT tidak valid:",e)
    elif c=="4":
        print("""- Pastikan host masuk scope CTF/lab berizin.
- Petakan endpoint, parameter, method, cookie, dan header.
- Uji satu perubahan input per percobaan di Burp Repeater.
- Bandingkan respons normal dan respons yang diubah.
- Periksa autentikasi, otorisasi, validasi input, dan kontrol akses.
- Validasi bukti sebelum mengirim flag.
- Jangan gunakan scanner otomatis kecuali aturan lab mengizinkan.""")
    elif c=="5":
        burp=shutil.which("burpsuite")
        if burp: run([burp],"Membuka Burp Suite")
        else: print("Burp Suite tidak ditemukan.")

def linux():
    header("LINUX & SUID")
    print("1 Daftar file SUID lokal\n2 Periksa permission file\n3 Cari capabilities\n4 Periksa permission path\n0 Kembali")
    c=input("Pilih: ").strip()
    if c=="1":
        f=shutil.which("find")
        if f: run([f,"/","-type","f","-perm","-4000","-ls"],"Audit SUID lokal",300)
    elif c in {"2","4"}:
        p=existing_file()
        if p:
            tool=shutil.which("stat" if c=="2" else "namei")
            if tool: run([tool,p] if c=="2" else [tool,"-l",p],"Periksa permission")
    elif c=="3":
        g=shutil.which("getcap")
        if g: run([g,"-r","/"],"Audit capabilities lokal",300)
        else: print("getcap tidak ditemukan.")

def forensics():
    header("FORENSICS & FILES")
    print("1 file type\n2 ExifTool metadata\n3 strings\n4 Binwalk\n5 Hex dump\n0 Kembali")
    c=input("Pilih: ").strip()
    mapping={"1":("file",[]),"2":("exiftool",[]),"3":("strings",["-n","6"]),"4":("binwalk",[]),"5":("xxd",[])}
    if c not in mapping:return
    p=existing_file()
    if not p:return
    name,args=mapping[c]; exe=shutil.which(name)
    if exe:run([exe]+args+[p],f"Analisis {Path(p).name}")
    else:print(name,"tidak ditemukan.")

def logs():
    header("LOGS & INCIDENT RESPONSE")
    print("1 Cari pola dalam file log\n2 Riwayat login\n3 Listening sockets\n4 Journal terbaru\n0 Kembali")
    c=input("Pilih: ").strip()
    if c=="1":
        p=existing_file(); pattern=input("Kata/pola regex: ").strip()
        exe=shutil.which("grep")
        if p and pattern and exe:run([exe,"-inE","--",pattern,p],"Cari pola log")
    elif c=="2":
        exe=shutil.which("last")
        if exe:run([exe,"-a"],"Riwayat login")
    elif c=="3":
        exe=shutil.which("ss")
        if exe:run([exe,"-tulpn"],"Socket/listening")
    elif c=="4":
        exe=shutil.which("journalctl")
        if exe:run([exe,"-n","100","--no-pager"],"Journal terbaru")

def firewall():
    header("FIREWALL & ACL — READ ONLY")
    print("Pemeriksaan tidak mengubah aturan atau permission sistem.\n")
    print("1 Lihat aturan iptables (IPv4)\n2 Lihat ruleset nftables\n3 Lihat status UFW\n4 Periksa Linux File ACL (getfacl)\n0 Kembali")
    c = input("Pilih: ").strip()

    mapping = {
        "1": ("iptables", ["-L", "-n", "-v", "--line-numbers"], "Membaca aturan iptables"),
        "2": ("nft", ["list", "ruleset"], "Membaca ruleset nftables"),
        "3": ("ufw", ["status", "verbose"], "Membaca status UFW"),
    }
    if c in mapping:
        name, args, description = mapping[c]
        exe = shutil.which(name)
        if exe:
            print("Info: perintah ini hanya menampilkan konfigurasi yang sedang aktif.")
            run([exe] + args, description)
        else:
            print(f"{name} tidak ditemukan. Periksa instalasi tool dan PATH.")
    elif c == "4":
        print("Linux File ACL menunjukkan user/group mana yang mendapat izin pada file atau direktori.")
        print("Catatan: Linux File ACL berbeda dari Network ACL pada firewall/router.")
        path = existing_path()
        if not path:
            return
        exe = shutil.which("getfacl")
        if exe:
            print("Info: getfacl hanya membaca entri ACL; tidak mengubah permission.")
            run([exe, "-p", "--", path], "Memeriksa Linux File ACL")
        else:
            print("getfacl tidak ditemukan. Tool ini biasanya tersedia melalui paket acl.")
    elif c != "0":
        print("Pilihan tidak valid.")

def main():
    menus={"1":("Network & PCAP",network),"2":("Cryptography",crypto),"3":("Web & API (manual)",web),
           "4":("Linux & SUID",linux),"5":("Forensics & files",forensics),
           "6":("Logs & incident response",logs),"7":("Firewall & ACL",firewall)}
    while True:
        header(f"RIK0SEC CTF QUICK LAUNCHER v{VERSION}")
        print("Kali Linux | UAS Sistem Keamanan Jaringan")
        for k,(name,_) in menus.items():print(f"  {k}. {name}")
        print("  8. Cek semua tools\n  0. Keluar")
        c=input("\nPilih kategori: ").strip()
        if c=="0":print("Terima kasih. Gunakan hanya pada CTF/lab berizin.");break
        if c=="8":toolcheck();pause()
        elif c in menus:
            try:menus[c][1]()
            except KeyboardInterrupt:print("\nDibatalkan.")
            pause()
        else:print("Pilihan tidak valid.");pause()

if __name__=="__main__":
    try:main()
    except (KeyboardInterrupt,EOFError):print("\nKeluar dari launcher.")
