import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
FILE_NAME = "antrian_klinik.txt"

# =========================
# NODE & LINKED LIST
# =========================
class Node:
    def __init__(self, nomor, nama, umur, kelamin, is_bpjs, keluhan):
        self.nomor = nomor
        self.nama = nama
        self.umur = umur
        self.kelamin = kelamin
        self.is_bpjs = bool(is_bpjs)
        self.keluhan = keluhan
        self.next = None

class AntrianLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, nama, umur, kelamin, is_bpjs, keluhan):
        self.size += 1
        node_baru = Node(self.size, nama, umur, kelamin, is_bpjs, keluhan)
        if self.tail is None:
            self.head = self.tail = node_baru
        else:
            self.tail.next = node_baru
            self.tail = node_baru

    def dequeue(self):
        if self.head is None: return None
        pasien = self.head
        self.head = self.head.next
        if self.head is None: self.tail = None
        self._renumber()
        return pasien

    def update(self, nomor, nama, umur, kelamin, is_bpjs, keluhan):
        current = self.head
        while current:
            if current.nomor == nomor:
                current.nama, current.umur = nama, umur
                current.kelamin, current.is_bpjs = kelamin, is_bpjs
                current.keluhan = keluhan
                return True
            current = current.next
        return False

    def cari_nama(self, nama_cari):
        """Mencari pasien dan mengembalikan list berisi objek Node"""
        hasil = []
        current = self.head
        while current:
            if nama_cari.lower() in current.nama.lower():
                hasil.append(current)
            current = current.next
        return hasil

    def hapus(self, nomor):
        current = self.head
        prev = None
        while current:
            if current.nomor == nomor:
                if prev is None: self.head = current.next
                else: prev.next = current.next
                if current.next is None: self.tail = prev
                self._renumber()
                return True
            prev = current
            current = current.next
        return False

    def _renumber(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current.nomor = count
            current = current.next
        self.size = count

    def tampilkan(self):
        if self.head is None:
            print("\n[!] Antrian masih kosong.")
            return
        self._print_header()
        current = self.head
        while current:
            self._print_pasien(current)
            current = current.next
        print("╚" + "═" * 93 + "╝\n")

    def _print_header(self):
        print("\n╔" + "═"*93 + "╗")
        print(f"║{'No':<3} | {'Nama':<20} | {'Umur':<4} | {'JK':<3} | {'Tipe':<8} | {'Keluhan':<40}║")
        print("╠" + "═" * 93 + "╣")

    def _print_pasien(self, p):
        tipe_txt = "BPJS" if p.is_bpjs else "Umum"
        print(f"║{p.nomor:<3} | {p.nama:<20} | {p.umur:<4} | {p.kelamin:<3} | {tipe_txt:<8} | {p.keluhan:<40}║")

# =========================
# FILE HANDLING (UTF-8)
# =========================
antrian = AntrianLinkedList()

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 6:
                    _, nama, umur, jk, bpjs_val, keluhan = parts
                    antrian.enqueue(nama, umur, jk, bpjs_val == "1", keluhan)

def save_data():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        current = antrian.head

        while current:
            bpjs_save = "1" if current.is_bpjs else "0"

            file.write(
                f"{current.nomor}|"
                f"{current.nama}|"
                f"{current.umur}|"
                f"{current.kelamin}|"
                f"{bpjs_save}|"
                f"{current.keluhan}\n"
            )

            current = current.next

    print("[DEBUG] Data berhasil disimpan ke TXT")

# =========================
# CETAK PDF SURAT ANTRIAN
# =========================
def buat_pdf_pasien(pasien):
    nama_file = f"surat_antrian_{pasien.nomor}.pdf"

    pdf = canvas.Canvas(nama_file, pagesize=letter)
    width, height = letter

# =========================
# HEADER
# =========================

    # Logo
    logo_path = "logo_ipb.png"

    if os.path.exists(logo_path):

        pdf.drawImage(
            logo_path,
            45,                 # posisi kiri
            height - 95,        # posisi atas
            width=75,
            height=75,
            preserveAspectRatio=True,
            mask='auto'
        )

    # Nama Klinik
    pdf.setFont("Helvetica-Bold", 22)

    pdf.drawCentredString(
        width / 2,
        height - 50,
        "Klinik SV IPB University"
    )

    # Alamat
    pdf.setFont("Helvetica", 11)

    pdf.drawCentredString(
        width / 2,
        height - 72,
        "Jl. Kumbang No.14, RT.02/RW.06, Babakan,"
    )

    pdf.drawCentredString(
        width / 2,
        height - 88,
        "Kecamatan Bogor Tengah, Kota Bogor, Jawa Barat 16128"
    )

    # Garis pemisah
    pdf.line(
        40,
        height - 110,
        width - 40,
        height - 110
    )

    # =========================
    # JUDUL
    # =========================

    pdf.setFont("Helvetica-Bold", 20)

    pdf.drawCentredString(
        width / 2,
        height - 150,
        "Nomor Antrian Anda"
    )

    # =========================
    # NOMOR BESAR
    # =========================

    nomor_antrian = f"{pasien.nomor:03}"

    pdf.setFont("Helvetica-Bold", 100)

    pdf.drawCentredString(
        width / 2,
        height - 320,
        nomor_antrian
    )

    # =========================
    # DATA PASIEN
    # =========================
    status = "BPJS" if pasien.is_bpjs else "Umum"

    pdf.setFont("Helvetica", 13)

    data = [
        ("Nama Pasien", pasien.nama),
        ("Umur", pasien.umur),
        ("Jenis Kelamin", pasien.kelamin),
        ("Tipe Pasien", status),
        ("Keluhan", pasien.keluhan),
        ("Tanggal Daftar",
         datetime.now().strftime("%d-%m-%Y %H:%M"))
    ]

    # Posisi tabel
    x_label = 170
    x_titikdua = 320
    x_value = 340

    y = height - 500

    for label, value in data:
        pdf.drawString(x_label, y, label)
        pdf.drawString(x_titikdua, y, ":")
        pdf.drawString(x_value, y, str(value))
        y -= 30

    # =========================
    # FOOTER
    # =========================
    pdf.setFont("Helvetica-Oblique", 10)

    pdf.drawCentredString(
        width / 2,
        70,
        "* Harap menunggu hingga nomor dipanggil *"
    )

    pdf.save()

    print(f"\n[V] PDF berhasil dibuat: {nama_file}")

# =========================
# LOGIC & UI
# =========================
def input_boolean_bpjs():
    RED = "\033[31m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"

    while True:
        pilihan = input(f"{BOLD}{GREEN}➔{RESET} Apakah pasien BPJS? (y/n): ").lower()
        if pilihan == 'y': return True
        if pilihan == 'n': return False
        print(f"\n{BOLD}{RED}================ INVALID ==============={RESET}")
        print(f"{RED}Input tidak valid, gunakan 'y' atau 'n'.{RESET}\n")

def input_jenis_kelamin():
    RED = "\033[31m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"

    while True:
        jk = input(f"{BOLD}{GREEN}➔{RESET} Jenis Kelamin (L/P): ").upper()

        if jk in ["L", "P"]:
            return jk
        print(f"\n{BOLD}{RED}================= INVALID ================{RESET}")
        print(f"{RED}Input tidak valid! Gunakan hanya L atau P {RESET}\n")
    
def input_umur():
    RED = "\033[31m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"

    while True:
        umur = input(f"{BOLD}{GREEN}➔{RESET} Umur: ")

        if umur.isdigit():

            umur_int = int(umur)

            if umur_int > 0 and umur_int <= 120:
                return umur
        print(f"\n{BOLD}{RED}============ INVALID ==========={RESET}")
        print(f"{RED}Input umur harus berupa angka valid!{RESET}\n")

def tambah_pasien():
    RED = "\033[31m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"

    nama = input(f"{BOLD}{GREEN}➔{RESET} Nama Pasien: ")
    umur = input_umur()
    jk = input_jenis_kelamin()
    is_bpjs = input_boolean_bpjs()
    keluhan = input(f"{BOLD}{GREEN}➔{RESET} Keluhan: ")

    antrian.enqueue(nama, umur, jk, is_bpjs, keluhan)
    save_data()

    print(f"\n{BOLD}{GREEN}============= SUCCESS ============{RESET}")
    print(f"{GREEN}[V] Pasien berhasil masuk antrian!{RESET}\n")

def cari_pasien():
    RED = "\033[31m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"

    nama = input(f"{BOLD}{GREEN}➔{RESET} Masukkan nama pasien yang dicari: ")
    hasil = antrian.cari_nama(nama)
    
    if not hasil:
        print(f"\n{BOLD}{RED}============== ERROR ============={RESET}")
        print(f"{RED}[!] Pasien dengan nama '{nama}' tidak ditemukan.{RESET}\n")
    else:
        print("╔" + "═"*31 + f" HASIL PENCARIAN ({len(hasil)} ditemukan) " + "═"*31 + "╗")
        print(f"║{'No':<3} | {'Nama':<20} | {'Umur':<4} | {'JK':<3} | {'Tipe':<8} | {'Keluhan':<40}║")
        print("╠" + "═" * 93 + "╣")
        for p in hasil:
            status = "BPJS" if p.is_bpjs else "Umum"
            print(f"║{p.nomor:<3} | {p.nama:<20} | {p.umur:<4} | {p.kelamin:<3} | {status:<8} | {p.keluhan:<40}║")
        print("╚" + "═" * 93 + "╝\n")

def panggil_pasien():
    YELLOW = "\033[33m" 
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"

    pasien = antrian.dequeue()
    if pasien:
        save_data()
        status = "BPJS" if pasien.is_bpjs else "Umum"
        print(f"\n{BOLD}{YELLOW}>>> MEMANGGIL PASIEN BERIKUTNYA [!]:{RESET}")
        print(f"    Nama    : {pasien.nama}")
        print(f"    Tipe    : {status}")
        print(f"    Keluhan : {pasien.keluhan}\n")
    else:
        print(f"\n{BOLD}{RED}================ ERROR ==============={RESET}")
        print(f"{RED}[!] Tidak ada antrian untuk dipanggil.{RESET}\n")

def update_pasien():
    antrian.tampilkan()
    RED = "\033[31m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    
    try:
        nomor = int(input(f"\n{BOLD}{GREEN}➔{RESET} Nomor antrian yang diupdate: "))
        nama = input(f"{BOLD}{GREEN}➔{RESET} Nama Baru: ")
        umur = input_umur()
        jk = input_jenis_kelamin()
        is_bpjs = input_boolean_bpjs()
        keluhan = input(f"{BOLD}{GREEN}➔{RESET} Keluhan Baru: ")
        if antrian.update(nomor, nama, umur, jk, is_bpjs, keluhan):
            save_data()
            print(f"\n{BOLD}{GREEN}============== SUCCESS ============={RESET}")
            print(f"{GREEN}[V] Data pasien berhasil diperbarui.{RESET}\n")
        else:
            print(f"\n{BOLD}{RED}============== ERROR ============={RESET}")
            print(f"{RED}[!] Nomor antrian tidak ditemukan.{RESET}\n")
    except ValueError:
        print(f"\n{BOLD}{RED}=========== INVALID =========={RESET}")
        print(f"{RED}[!] Masukkan nomor yang valid.{RESET}\n")

def hapus_pasien():
    antrian.tampilkan()
    RED = "\033[31m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"

    try:
        nomor = int(input(f"{BOLD}{GREEN}➔{RESET} Nomor pasien yang akan dihapus: "))
        if antrian.hapus(nomor):
            save_data()
            print(f"\n{BOLD}{GREEN}========== SUCCESS ========={RESET}")
            print(f"{GREEN}[V] Pasien berhasil dihapus.{RESET}\n")
        else:
            print(f"\n{BOLD}{RED}========== ERROR ========={RESET}")
            print(f"{RED}[!] Nomor tidak ditemukan.{RESET}\n")
    except ValueError:
        print(f"\n{BOLD}{RED}======== ERROR ======={RESET}")
        print(f"{RED}[!] Input tidak valid.{RESET}\n")

def reset_data():
    antrian.tampilkan()
    RED = "\033[31m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m" 

    print(f"{BOLD}{YELLOW}================ PERINGATAN [!] ================{RESET}")
    konfirmasi = input(
        f"{YELLOW}Yakin ingin menghapus SEMUA data antrian? (y/n):{RESET} "
    ).lower()

    if konfirmasi == "y":

        # Reset linked list
        antrian.head = None
        antrian.tail = None
        antrian.size = 0    

        # Kosongkan file
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            pass
        
        save_data()
        print(f"\n{BOLD}{GREEN}================ SUCCESS ==============={RESET}")
        print(f"{GREEN}[V] Semua data antrian berhasil direset.{RESET}\n")

    else:
        print("\n[!] Reset dibatalkan.\n")

def cetak_pdf_pasien():
    RED = "\033[31m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"

    if antrian.head is None:
        print(f"\n{BOLD}{RED}========== ERROR ========={RESET}")
        print(f"{RED}[!] Tidak ada data pasien.{RESET}\n")
        return

    antrian.tampilkan()

    try:
        nomor = int(input("\nMasukkan nomor antrian yang ingin dicetak: "))

        current = antrian.head

        while current:
            if current.nomor == nomor:

                buat_pdf_pasien(current)

                print(f"\n{BOLD}{GREEN}============== SUCCESS ============{RESET}")
                print(f"{BOLD}{GREEN}[V] Surat antrian berhasil dicetak.{RESET}\n")
                return

            current = current.next
        print(f"\n{BOLD}{RED}============== ERROR ============={RESET}")
        print(f"{RED}[!] Nomor antrian tidak ditemukan.{RESET}\n")

    except ValueError:
        print(f"\n{BOLD}{RED}=========== ERROR =========={RESET}")
        print(f"{RED}[!] Input nomor harus angka.{RESET}\n")

def menu():
    load_data()

    # Color
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    NAVY = "\033[38;5;19m"
    TEAL = "\033[38;5;30m"


    while True:
        # ==+ LOGO ===
        print(f"{NAVY}          ▄▄▄███████▄▄▄          {RESET}")
        print(f"{NAVY}       ▄█████████████████▄       {RESET}")
        print(f"{NAVY}     ▄█████████████████████▄     {RESET}")
        print(f"{NAVY}    ██████████▀   ▀██████████    {RESET}{GREEN}             ▄▄▄▄▄▄▄      {RESET}")
        print(f"{NAVY}   ████████▀{RESET}   ▄█▄   {NAVY}▀████████   {RESET}{GREEN}             ███████      {RESET}")
        print(f"{NAVY}  ████████{RESET}   ▀█████▀   {NAVY}████████  {RESET}{GREEN}      ▄▄▄▄▄▄▄███████▄▄▄▄▄▄▄{RESET}")
        print(f"{NAVY}  ████████{RESET} ▀█████████▀ {NAVY}████████  {RESET}{GREEN}      █████████████████████{RESET}")
        print(f"{NAVY}  ████████{RESET}  ▀███████▀  {NAVY}████████  {RESET}{GREEN}      ▀▀▀▀▀▀▀███████▀▀▀▀▀▀▀{RESET}")
        print(f"{NAVY}  ████████▄{RESET}  ▄ █ █ ▄  {NAVY}▄████████  {RESET}{GREEN}             ███████      {RESET}")
        print(f"{NAVY}   █████████▄{RESET} ▀▀▀▀▀ {NAVY}▄█████████   {RESET}{GREEN}             ▀▀▀▀▀▀▀      {RESET}")
        print(f"{NAVY}    █████████████████████████    {RESET}")
        print(f"{NAVY}     ▀█████████████████████▀     {RESET}")
        print(f"{NAVY}       ▀█████████████████▀       {RESET}")
        print(f"{NAVY}          ▀▀▀███████▀▀▀          {RESET}")
        print(f"   {BOLD}I P B  U N I V E R S I T Y{RESET}    |    {BOLD}{GREEN}K L I N I K  V O K A S I{RESET}\n")

        # === Title ===
        print(f"{TEAL}╔════════════════════════════════════════════════════════╗{RESET}")
        print(f"{TEAL}║{RESET} {BOLD}{NAVY}         + SISTEM KLINIK SV IPB UNIVERSITY            {RESET} {TEAL}║{RESET}")
        print(f"{TEAL}╠═══╗════════════════════════════════════════════════════╣{RESET}")

        # ==== Daftar Menu ====
        print(f"{TEAL}║{RESET} 1 {TEAL}║{RESET} Tambah Pasien                                      {RESET}{TEAL}║{RESET}")
        print(f"{TEAL}║---║----------------------------------------------------║{RESET}")
        print(f"{TEAL}║{RESET} 2 {TEAL}║{RESET} Lihat Seluruh Antrian                              {RESET}{TEAL}║{RESET}")
        print(f"{TEAL}║---║----------------------------------------------------║{RESET}")
        print(f"{TEAL}║{RESET} 3 {TEAL}║{RESET} Panggil Pasien Berikutnya                          {RESET}{TEAL}║{RESET}")
        print(f"{TEAL}║---║----------------------------------------------------║{RESET}")
        print(f"{TEAL}║{RESET} 4 {TEAL}║{RESET} Cari Pasien                                        {RESET}{TEAL}║{RESET}")
        print(f"{TEAL}║---║----------------------------------------------------║{RESET}")
        print(f"{TEAL}║{RESET} 5 {TEAL}║{RESET} Update Data Pasien                                 {RESET}{TEAL}║{RESET}")
        print(f"{TEAL}║---║----------------------------------------------------║{RESET}")
        print(f"{TEAL}║{RESET} 6 {TEAL}║{RESET} Hapus Pasien dari Antrian                          {RESET}{TEAL}║{RESET}")
        print(f"{TEAL}║---║----------------------------------------------------║{RESET}")
        print(f"{TEAL}║{RESET} 7 {TEAL}║{RESET} Cetak Surat Antrian PDF                            {RESET}{TEAL}║{RESET}")
        print(f"{TEAL}║---║----------------------------------------------------║{RESET}")
        print(f"{TEAL}║{RESET} 8 {TEAL}║{RESET} Reset Semua Data                                   {RESET}{TEAL}║{RESET}")
        print(f"{TEAL}║---║----------------------------------------------------║{RESET}")
        print(f"{TEAL}║{RESET} 9 {TEAL}║{RESET} Keluar Program                                     {RESET}{TEAL}║{RESET}")
        print(f"{TEAL}╚═══╝════════════════════════════════════════════════════╝{RESET}")

        # === Logic Menu ===

        pilih = input(f"\n{BOLD}{GREEN}➔{RESET} Pilih menu [1-9]: ")


        if pilih == "1": tambah_pasien()
        elif pilih == "2": antrian.tampilkan()
        elif pilih == "3": panggil_pasien()
        elif pilih == "4": cari_pasien()
        elif pilih == "5": update_pasien()
        elif pilih == "6": hapus_pasien()
        elif pilih == "7": cetak_pdf_pasien()
        elif pilih == "8": reset_data()
        elif pilih == "9": 
            print(f"{GREEN}╔═════╣{RESET}{MAGENTA}Terima Kasih Master, See You{RESET} {MAGENTA}{BOLD}Tomorow!{RESET}{GREEN}╠═════╗{RESET}")
            print(f"{BOLD}{GREEN}➔{RESET}                {TEAL}{BOLD}Program selesai...{RESET}               {GREEN}║{RESET}")
            print(f"{GREEN}╚═════════════════════════════════════════════════╝{RESET}")
            break
        else: 
            print(f"\n{RED}{BOLD}======== ERROR ========{RESET}")
            print(f"{BOLD}{RED}➔{RESET} Pilihan tidak valid.\n")

if __name__ == "__main__":
    menu()
