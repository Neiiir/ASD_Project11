import os

FILE_NAME = "antrian_klinik.txt"


# =========================
# NODE & LINKED LIST
# =========================
class Node:
    def __init__(self, nomor, nama, umur, keluhan):
        self.nomor = nomor
        self.nama = nama
        self.umur = umur
        self.keluhan = keluhan
        self.next = None


class AntrianLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, nama, umur, keluhan):
        """Tambah pasien di belakang — O(1)"""
        self.size += 1
        node_baru = Node(self.size, nama, umur, keluhan)

        if self.tail is None:       # antrian kosong
            self.head = node_baru
            self.tail = node_baru
        else:
            self.tail.next = node_baru  # sambung ke node terakhir
            self.tail = node_baru       # tail pindah ke node baru

    def dequeue(self):
        """Ambil pasien dari depan — O(1)"""
        if self.head is None:
            return None

        pasien = self.head
        self.head = self.head.next  # head maju ke node berikutnya

        if self.head is None:       # antrian jadi kosong
            self.tail = None

        self.size -= 1
        self._renumber()
        return pasien

    def update(self, nomor, nama_baru, umur_baru, keluhan_baru):
        """Cari dan update pasien — O(n)"""
        current = self.head
        while current:
            if current.nomor == nomor:
                current.nama = nama_baru
                current.umur = umur_baru
                current.keluhan = keluhan_baru
                return True
            current = current.next
        return False

    def hapus(self, nomor):
        """Hapus pasien di tengah — O(n)"""
        current = self.head
        prev = None

        while current:
            if current.nomor == nomor:
                if prev is None:            # hapus di head
                    self.head = current.next
                else:
                    prev.next = current.next  # bypass node ini

                if current.next is None:    # hapus di tail
                    self.tail = prev

                self.size -= 1
                self._renumber()
                return True
            prev = current
            current = current.next
        return False

    def _renumber(self):
        """Nomor ulang semua pasien setelah ada perubahan"""
        current = self.head
        nomor = 1
        while current:
            current.nomor = nomor
            nomor += 1
            current = current.next

    def tampilkan(self):
        """Traverse dari head ke tail — O(n)"""
        if self.head is None:
            print("Antrian kosong.")
            return

        print("\n=== DAFTAR ANTRIAN ===")
        current = self.head
        while current:
            print(f"No: {current.nomor} | Nama: {current.nama} | "
                  f"Umur: {current.umur} | Keluhan: {current.keluhan}")
            current = current.next

    def is_empty(self):
        return self.head is None


# =========================
# FILE HANDLING
# =========================
antrian = AntrianLinkedList()

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 4:
                    _, nama, umur, keluhan = parts
                    antrian.enqueue(nama, umur, keluhan)


def save_data():
    with open(FILE_NAME, "w") as file:
        current = antrian.head
        while current:
            file.write(f"{current.nomor}|{current.nama}|{current.umur}|{current.keluhan}\n")
            current = current.next


# =========================
# CRUD
# =========================
def tambah_pasien():
    nama = input("Nama Pasien: ")
    umur = input("Umur: ")
    keluhan = input("Keluhan: ")
    antrian.enqueue(nama, umur, keluhan)
    save_data()
    print("Pasien berhasil ditambahkan ke antrian!")


def lihat_antrian():
    antrian.tampilkan()


def panggil_pasien():
    if antrian.is_empty():
        print("Tidak ada pasien dalam antrian.")
        return

    pasien = antrian.dequeue()
    save_data()
    print(f"\nMemanggil Pasien:")
    print(f"Nama: {pasien.nama} | Umur: {pasien.umur} | Keluhan: {pasien.keluhan}")


def update_pasien():
    lihat_antrian()
    try:
        nomor = int(input("Masukkan nomor antrian yang ingin diupdate: "))
    except ValueError:
        print("Input tidak valid.")
        return

    nama_baru = input("Nama Baru: ")
    umur_baru = input("Umur Baru: ")
    keluhan_baru = input("Keluhan Baru: ")

    if antrian.update(nomor, nama_baru, umur_baru, keluhan_baru):
        save_data()
        print("Data pasien berhasil diupdate!")
    else:
        print("Nomor antrian tidak ditemukan.")


def hapus_pasien():
    lihat_antrian()
    try:
        nomor = int(input("Masukkan nomor antrian yang ingin dihapus: "))
    except ValueError:
        print("Input tidak valid.")
        return

    if antrian.hapus(nomor):
        save_data()
        print("Pasien berhasil dihapus dari antrian!")
    else:
        print("Nomor antrian tidak ditemukan.")


# =========================
# MENU
# =========================
def menu():
    load_data()

    while True:
        print("\n=== SISTEM ANTRIAN KLINIK ===")
        print("1. Tambah Pasien")
        print("2. Lihat Antrian")
        print("3. Panggil Pasien Berikutnya")
        print("4. Update Data Pasien")
        print("5. Hapus Pasien")
        print("6. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_pasien()
        elif pilihan == "2":
            lihat_antrian()
        elif pilihan == "3":
            panggil_pasien()
        elif pilihan == "4":
            update_pasien()
        elif pilihan == "5":
            hapus_pasien()
        elif pilihan == "6":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid.")


menu()