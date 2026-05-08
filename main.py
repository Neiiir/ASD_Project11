import os

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
            file.write(f"{current.nomor}|{current.nama}|{current.umur}|{current.kelamin}|{bpjs_save}|{current.keluhan}\n")
            current = current.next

# =========================
# LOGIC & UI
# =========================
def input_boolean_bpjs():
    while True:
        pilihan = input("Apakah pasien BPJS? (y/n): ").lower()
        if pilihan == 'y': return True
        if pilihan == 'n': return False
        print("Input tidak valid, gunakan 'y' atau 'n'.")

def tambah_pasien():
    nama = input("Nama Pasien: ")
    umur = input("Umur: ")
    jk = input("Jenis Kelamin (L/P): ").upper()
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
        umur = input("Umur Baru: ")
        jk = input("JK Baru (L/P): ").upper()
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

def menu():
    load_data()
    while True:
        print("\n======= SISTEM KLINIK V2.1 =======")
        print("1. Tambah Pasien")
        print("2. Lihat Seluruh Antrian")
        print("3. Panggil Pasien Berikutnya")
        print("4. Cari Pasien")
        print("5. Update Data Pasien")
        print("6. Hapus Pasien dari Antrian")
        print("7. Keluar Program")
        
        pilih = input("\nPilih menu [1-7]: ")
        if pilih == "1": tambah_pasien()
        elif pilih == "2": antrian.tampilkan()
        elif pilih == "3": panggil_pasien()
        elif pilih == "4": cari_pasien()
        elif pilih == "5": update_pasien()
        elif pilih == "6": hapus_pasien()
        elif pilih == "7": 
            print("Program selesai.")
            break
        else: 
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    menu()