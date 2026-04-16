import os

FILE_NAME = "antrian_klinik.txt"
antrian = []

# =========================
# FILE HANDLING
# =========================
def load_data():
    global antrian
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()
            antrian = [line.strip().split("|") for line in lines]


def save_data():
    with open(FILE_NAME, "w") as file:
        for pasien in antrian:
            file.write("|".join(pasien) + "\n")


# =========================
# CRUD
# =========================
def tambah_pasien():
    nama = input("Nama Pasien: ")
    umur = input("Umur: ")
    keluhan = input("Keluhan: ")

    nomor_antrian = str(len(antrian) + 1)

    pasien = [nomor_antrian, nama, umur, keluhan]
    antrian.append(pasien)

    save_data()
    print("Pasien berhasil ditambahkan ke antrian!")


def lihat_antrian():
    if not antrian:
        print("Antrian kosong.")
        return

    print("\n=== DAFTAR ANTRIAN ===")
    for pasien in antrian:
        print(f"No: {pasien[0]} | Nama: {pasien[1]} | Umur: {pasien[2]} | Keluhan: {pasien[3]}")


def panggil_pasien():
    if not antrian:
        print("Tidak ada pasien dalam antrian.")
        return

    pasien = antrian.pop(0)

    for i in range(len(antrian)):
        antrian[i][0] = str(i + 1)

    save_data()

    print("\nMemanggil Pasien:")
    print(f"Nama: {pasien[1]} | Umur: {pasien[2]} | Keluhan: {pasien[3]}")


def update_pasien():
    lihat_antrian()
    nomor = input("Masukkan nomor antrian yang ingin diupdate: ")

    for pasien in antrian:
        if pasien[0] == nomor:
            pasien[1] = input("Nama Baru: ")
            pasien[2] = input("Umur Baru: ")
            pasien[3] = input("Keluhan Baru: ")

            save_data()
            print("Data pasien berhasil diupdate!")
            return

    print("Nomor antrian tidak ditemukan.")


def hapus_pasien():
    lihat_antrian()
    nomor = input("Masukkan nomor antrian yang ingin dihapus: ")

    for pasien in antrian:
        if pasien[0] == nomor:
            antrian.remove(pasien)

            for i in range(len(antrian)):
                antrian[i][0] = str(i + 1)

            save_data()
            print("Pasien berhasil dihapus dari antrian!")
            return

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