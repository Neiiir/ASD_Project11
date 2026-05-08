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
        print("-" * 95)

    def _print_header(self):
        print("\n" + "="*95)
        print(f"{'No':<3} | {'Nama':<20} | {'Umur':<4} | {'JK':<3} | {'Tipe':<8} | {'Keluhan'}")
        print("-" * 95)

    def _print_pasien(self, p):
        tipe_txt = "BPJS" if p.is_bpjs else "Umum"
        print(f"{p.nomor:<3} | {p.nama:<20} | {p.umur:<4} | {p.kelamin:<3} | {tipe_txt:<8} | {p.keluhan}")

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
    while True:
        pilihan = input("Apakah pasien BPJS? (y/n): ").lower()
        if pilihan == 'y': return True
        if pilihan == 'n': return False
        print("Input tidak valid, gunakan 'y' atau 'n'.")

def input_jenis_kelamin():
    while True:
        jk = input("Jenis Kelamin (L/P): ").upper()

        if jk in ["L", "P"]:
            return jk

        print("Input tidak valid! Gunakan hanya L atau P.")
    
def input_umur():
    while True:
        umur = input("Umur: ")

        if umur.isdigit():

            umur_int = int(umur)

            if umur_int > 0 and umur_int <= 120:
                return umur

        print("Input umur harus berupa angka valid!")

def tambah_pasien():
    nama = input("Nama Pasien: ")
    umur = input_umur()
    jk = input_jenis_kelamin()
    is_bpjs = input_boolean_bpjs()
    keluhan = input("Keluhan: ")

    antrian.enqueue(nama, umur, jk, is_bpjs, keluhan)
    save_data()

    print("\n[V] Pasien berhasil masuk antrian!")

def cari_pasien():
    nama = input("Masukkan nama pasien yang dicari: ")
    hasil = antrian.cari_nama(nama)
    
    if not hasil:
        print(f"\n[!] Pasien dengan nama '{nama}' tidak ditemukan.")
    else:
        print(f"\n--- HASIL PENCARIAN ({len(hasil)} ditemukan) ---")
        print("=" * 95)
        print(f"{'No':<3} | {'Nama':<20} | {'Umur':<4} | {'JK':<3} | {'Tipe':<8} | {'Keluhan'}")
        print("-" * 95)
        for p in hasil:
            status = "BPJS" if p.is_bpjs else "Umum"
            print(f"{p.nomor:<3} | {p.nama:<20} | {p.umur:<4} | {p.kelamin:<3} | {status:<8} | {p.keluhan}")
        print("=" * 95)

def panggil_pasien():
    pasien = antrian.dequeue()
    if pasien:
        save_data()
        status = "BPJS" if pasien.is_bpjs else "Umum"
        print("\n>>> MEMANGGIL PASIEN BERIKUTNYA:")
        print(f"    Nama    : {pasien.nama}")
        print(f"    Tipe    : {status}")
        print(f"    Keluhan : {pasien.keluhan}")
    else:
        print("\n[!] Tidak ada antrian untuk dipanggil.")

def update_pasien():
    antrian.tampilkan()
    try:
        nomor = int(input("\nNomor antrian yang diupdate: "))
        nama = input("Nama Baru: ")
        umur = input_umur()
        jk = input_jenis_kelamin()
        is_bpjs = input_boolean_bpjs()
        keluhan = input("Keluhan Baru: ")
        if antrian.update(nomor, nama, umur, jk, is_bpjs, keluhan):
            save_data()
            print("[V] Data pasien berhasil diperbarui.")
        else:
            print("[!] Nomor antrian tidak ditemukan.")
    except ValueError:
        print("[!] Masukkan nomor yang valid.")

def hapus_pasien():
    antrian.tampilkan()
    try:
        nomor = int(input("\nNomor pasien yang akan dihapus: "))
        if antrian.hapus(nomor):
            save_data()
            print("[V] Pasien berhasil dihapus.")
        else:
            print("[!] Nomor tidak ditemukan.")
    except ValueError:
        print("[!] Input tidak valid.")

def reset_data():
    konfirmasi = input(
        "\nYakin ingin menghapus SEMUA data antrian? (y/n): "
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
        print("\n[V] Semua data antrian berhasil direset.")

    else:
        print("\n[!] Reset dibatalkan.")

def cetak_pdf_pasien():
    if antrian.head is None:
        print("\n[!] Tidak ada data pasien.")
        return

    antrian.tampilkan()

    try:
        nomor = int(input("\nMasukkan nomor antrian yang ingin dicetak: "))

        current = antrian.head

        while current:
            if current.nomor == nomor:

                buat_pdf_pasien(current)

                print("\n[V] Surat antrian berhasil dicetak.")
                return

            current = current.next

        print("[!] Nomor antrian tidak ditemukan.")

    except ValueError:
        print("[!] Input nomor harus angka.")

def menu():
    load_data()
    while True:
        print("\n======= SISTEM KLINIK SV IPB UNIVERSITY =======")
        print("1. Tambah Pasien")
        print("2. Lihat Seluruh Antrian")
        print("3. Panggil Pasien Berikutnya")
        print("4. Cari Pasien")
        print("5. Update Data Pasien")
        print("6. Hapus Pasien dari Antrian")
        print("7. Cetak Surat Antrian PDF")
        print("8. Reset Semua Data")
        print("9. Keluar Program")
        
        pilih = input("\nPilih menu [1-9]: ")
        if pilih == "1": tambah_pasien()
        elif pilih == "2": antrian.tampilkan()
        elif pilih == "3": panggil_pasien()
        elif pilih == "4": cari_pasien()
        elif pilih == "5": update_pasien()
        elif pilih == "6": hapus_pasien()
        elif pilih == "7": cetak_pdf_pasien()
        elif pilih == "8": reset_data()
        elif pilih == "9": 
            print("Program selesai.")
            break
        else: 
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    menu()