"""
Tugas Praktikum Metode Numerik - Lab Session Kelas 3B
Penyelesaian Sistem Persamaan Non-Linear (SPNL)
Persamaan: f(x) = cos(x) - x = 0

Di sini kita bandingin 2 metode pencarian akar:
1. Fixed-Point Iteration (Iterasi Titik Tetap)
2. Newton-Raphson
"""

import math
from typing import List, Optional, Tuple

# -------------------------------------------------------------
# Parameter & Tebakan Awal
# (Bisa diatur di sini, syarat dari soal: 0 < x0 < 1.4)
# -------------------------------------------------------------
x0: float = 0.5          # Tebakan awal x0 (default = 0.5)
tol: float = 0.0001      # Toleransi error |f(x)| < 0.0001
max_iter: int = 100      # Batas maks iterasi biar gak looping tanpa henti


# -------------------------------------------------------------
# Definisi Fungsi Utama dan Turunannya
# -------------------------------------------------------------
def f(x: float) -> float:
    """
    Fungsi utama yang mau dicari akarnya:
    f(x) = cos(x) - x
    """
    return math.cos(x) - x


def f_prime(x: float) -> float:
    """
    Turunan pertama dari f(x) buat metode Newton-Raphson:
    f'(x) = -sin(x) - 1
    """
    return -math.sin(x) - 1.0


def g(x: float) -> float:
    """
    Fungsi iterasi titik tetap (pindah ruas dari f(x) = 0):
    x = cos(x)  =>  g(x) = cos(x)
    """
    return math.cos(x)


def g_prime(x: float) -> float:
    """
    Turunan pertama dari g(x) buat ngecek syarat konvergensi:
    g'(x) = -sin(x)
    """
    return -math.sin(x)


# -------------------------------------------------------------
# Metode 1: Fixed-Point Iteration (Iterasi Titik Tetap)
# -------------------------------------------------------------
def fixed_point_iteration(
    x_start: float, tol_err: float, max_steps: int = 100
) -> Optional[List[Tuple[int, float, float, float]]]:
    """
    Pencarian akar pake Fixed-Point Iteration:
    x_{i+1} = g(x_i) = cos(x_i)
    Wajib lolos syarat mutlak konvergensi: |g'(x0)| < 1 sebelum iterasi.
    """
    print("\n" + "=" * 65)
    print(" METODE 1: FIXED-POINT ITERATION (ITERASI TITIK TETAP)")
    print("=" * 65)

    # Cek syarat mutlak konvergensi terlebih dahulu
    g_prime_val = abs(g_prime(x_start))
    print(f"[*] Pengecekan Syarat Awal Konvergensi:")
    print(f"    |g'(x0)| = |-sin({x_start})| = {g_prime_val:.6f}")

    if g_prime_val < 1.0:
        print("    -> Syarat konvergensi terpenuhi: |g'(x0)| < 1. Iterasi dilanjutkan!")
    else:
        print("    -> [ERROR] Syarat konvergensi TIDAK terpenuhi (|g'(x0)| >= 1).")
        print("    -> Iterasi tidak boleh dilanjutkan!")
        return None

    # Masuk ke proses iterasi
    history: List[Tuple[int, float, float, float]] = []
    curr_x = x_start
    i = 0

    # Simpan iterasi awal (i = 0)
    fx = f(curr_x)
    err = abs(fx)
    history.append((i, curr_x, fx, err))

    # Looping sampai error lebih kecil dari toleransi atau kena batas maksimal
    while err >= tol_err and i < max_steps:
        curr_x = g(curr_x)
        i += 1
        fx = f(curr_x)
        err = abs(fx)
        history.append((i, curr_x, fx, err))

    return history


# -------------------------------------------------------------
# Metode 2: Newton-Raphson
# -------------------------------------------------------------
def newton_raphson(
    x_start: float, tol_err: float, max_steps: int = 100
) -> Optional[List[Tuple[int, float, float, float]]]:
    """
    Pencarian akar pake Newton-Raphson:
    x_{i+1} = x_i - f(x_i) / f'(x_i)
    Wajib lolos syarat mutlak: f'(x0) != 0 sebelum iterasi.
    """
    print("\n" + "=" * 65)
    print(" METODE 2: NEWTON-RAPHSON")
    print("=" * 65)

    # Cek syarat mutlak: turunan awal gak boleh nol (biar gak pembagian dengan nol)
    f_prime_val = f_prime(x_start)
    print(f"[*] Pengecekan Syarat Awal:")
    print(f"    f'(x0) = -sin({x_start}) - 1 = {f_prime_val:.6f}")

    if abs(f_prime_val) > 1e-12:
        print("    -> Syarat terpenuhi: f'(x0) != 0. Iterasi dilanjutkan!")
    else:
        print("    -> [ERROR] f'(x0) = 0! Pembagian dengan nol terjadi.")
        print("    -> Iterasi dihentikan.")
        return None

    # Masuk ke proses iterasi
    history: List[Tuple[int, float, float, float]] = []
    curr_x = x_start
    i = 0

    # Simpan iterasi ke-0
    fx = f(curr_x)
    err = abs(fx)
    history.append((i, curr_x, fx, err))

    # Looping iterasi Newton-Raphson
    while err >= tol_err and i < max_steps:
        dfx = f_prime(curr_x)
        if abs(dfx) < 1e-12:
            print(f"    -> [STOP] Turunan f'(x) mendekati nol di iterasi ke-{i}.")
            break
        curr_x = curr_x - (fx / dfx)
        i += 1
        fx = f(curr_x)
        err = abs(fx)
        history.append((i, curr_x, fx, err))

    return history


# -------------------------------------------------------------
# Fungsi Buat Cetak Tabel ASCII
# -------------------------------------------------------------
def cetak_tabel(nama_metode: str, history: List[Tuple[int, float, float, float]]) -> None:
    """
    Cetak tabel iterasi rapi dengan kolom: Iterasi, x, f(x), dan Error (|f(x)|)
    Biar gampang di-copy atau screenshot ke laporan praktikum.
    """
    print(f"\nTabel Iterasi {nama_metode}:")
    print(f"+{'-' * 9}+{'-' * 14}+{'-' * 16}+{'-' * 18}+")
    print(f"| {'Iterasi':^7} | {'x':^12} | {'f(x)':^14} | {'Error (|f(x)|)':^16} |")
    print(f"+{'-' * 9}+{'-' * 14}+{'-' * 16}+{'-' * 18}+")

    for step, x_val, fx_val, err_val in history:
        print(f"| {step:^7d} | {x_val:^12.6f} | {fx_val:^14.6f} | {err_val:^16.6f} |")

    print(f"+{'-' * 9}+{'-' * 14}+{'-' * 16}+{'-' * 18}+")


# -------------------------------------------------------------
# Fungsi Buat Cetak Kesimpulan Perbandingan
# -------------------------------------------------------------
def cetak_kesimpulan(
    hist_fpi: Optional[List[Tuple[int, float, float, float]]],
    hist_nr: Optional[List[Tuple[int, float, float, float]]],
    tol_err: float,
) -> None:
    """
    Cetak tabel kesimpulan perbandingan hasil akar dan jumlah iterasi
    antara Fixed-Point Iteration dan Newton-Raphson.
    """
    print("\n" + "=" * 79)
    print(f"{'KESIMPULAN PERBANDINGAN METODE PENCARIAN AKAR':^79}")
    print("=" * 79)
    print(f"| {'Parameter':<28} | {'Fixed-Point Iteration':^22} | {'Newton-Raphson':^20} |")
    print(f"+{'-' * 30}+{'-' * 24}+{'-' * 22}+")

    # Ambil data akhir FPI
    if hist_fpi:
        iter_fpi = hist_fpi[-1][0]
        x_fpi = hist_fpi[-1][1]
        fx_fpi = hist_fpi[-1][2]
        err_fpi = hist_fpi[-1][3]
        status_fpi = "TERPENUHI" if err_fpi < tol_err else "BELUM"
    else:
        iter_fpi, x_fpi, fx_fpi, err_fpi, status_fpi = "-", "-", "-", "-", "GAGAL"

    # Ambil data akhir Newton-Raphson
    if hist_nr:
        iter_nr = hist_nr[-1][0]
        x_nr = hist_nr[-1][1]
        fx_nr = hist_nr[-1][2]
        err_nr = hist_nr[-1][3]
        status_nr = "TERPENUHI" if err_nr < tol_err else "BELUM"
    else:
        iter_nr, x_nr, fx_nr, err_nr, status_nr = "-", "-", "-", "-", "GAGAL"

    print(f"| {'Tebakan Awal (x0)':<28} | {x0:^22.4f} | {x0:^20.4f} |")
    print(f"| {'Akar x Ditemukan':<28} | {x_fpi:^22.6f} | {x_nr:^20.6f} |")
    print(f"| {'Nilai f(x) Terakhir':<28} | {fx_fpi:^22.6f} | {fx_nr:^20.6f} |")
    print(f"| {'Error Akhir (|f(x)|)':<28} | {err_fpi:^22.6f} | {err_nr:^20.6f} |")
    print(f"| {'Jumlah Iterasi':<28} | {str(iter_fpi) + ' iterasi':^22} | {str(iter_nr) + ' iterasi':^20} |")
    print(f"| {'Status (|f(x)| < ' + str(tol_err) + ')':<28} | {status_fpi:^22} | {status_nr:^20} |")
    print(f"+{'-' * 30}+{'-' * 24}+{'-' * 22}+")

    print("\nCatatan Analisis Mahasiswa:")
    print(f"1. Kedua metode berhasil nemuin akar di sekitar x = {x_nr:.6f} dengan error < {tol_err}.")
    print(f"2. Newton-Raphson jauh lebih kenceng (cuma butuh {iter_nr} iterasi) dibanding Fixed-Point ({iter_fpi} iterasi).")
    print("3. Hal ini wajar karena Newton-Raphson punya konvergensi kuadratik, sedangkan Fixed-Point cuma linear.")
    print("=" * 79)


# -------------------------------------------------------------
# Main Program
# -------------------------------------------------------------
def main():
    print("=" * 65)
    print(" PROGRAM PENYELESAIAN SISTEM PERSAMAAN NON-LINEAR (SPNL)")
    print(" Persamaan : f(x) = cos(x) - x = 0")
    print(f" Tebakan   : x0 = {x0} (Syarat: 0 < x0 < 1.4)")
    print(f" Toleransi : |f(x)| < {tol}")
    print("=" * 65)

    # 1. Jalankan Fixed-Point Iteration
    hist_fpi = fixed_point_iteration(x0, tol, max_iter)
    if hist_fpi:
        cetak_tabel("Fixed-Point Iteration", hist_fpi)

    # 2. Jalankan Newton-Raphson
    hist_nr = newton_raphson(x0, tol, max_iter)
    if hist_nr:
        cetak_tabel("Newton-Raphson", hist_nr)

    # 3. Cetak perbandingan di paling bawah
    cetak_kesimpulan(hist_fpi, hist_nr, tol)


if __name__ == "__main__":
    main()

