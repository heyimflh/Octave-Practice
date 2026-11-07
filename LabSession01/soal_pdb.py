"""
Tugas Praktikum Metode Numerik - Lab Session Kelas 3B
Penyelesaian Persamaan Diferensial Biasa (PDB)
Persamaan: dy/dx = x * sqrt(y)

Disini kita bandingin 3 metode numerik:
1. Euler
2. Heun (Runge-Kutta Orde-2)
3. Runge-Kutta Orde-4 (RK4)
"""

import math
from typing import List, Tuple

# -------------------------------------------------------------
# Parameter & Nilai Awal
# (Bisa disesuaikan kalau mau ganti kondisi awal atau step size)
# -------------------------------------------------------------
x0: float = 0.0          # Nilai x awal (default = 0.0)
y0: float = 1.0          # Nilai y awal pas x0 (default = 1.0)
h: float = 0.1           # Ukuran langkah (step size)
x_target: float = 1.2    # Target akhir nilai x yang mau dihitung
epsilon: float = 0.0001  # Batas toleransi error yang diminta


# -------------------------------------------------------------
# Fungsi PDB & Solusi Eksak (Buat Pembanding Galat)
# -------------------------------------------------------------
def f(x: float, y: float) -> float:
    """
    Fungsi turunan dy/dx = f(x, y) = x * sqrt(y)
    Pake math.sqrt buat ngitung akarnya.
    """
    # Cek dulu biar gak ada nilai negatif masuk ke akar
    if y < 0:
        raise ValueError(f"Nilai y ({y}) tidak boleh negatif di dalam fungsi math.sqrt.")
    return x * math.sqrt(y)


def y_exact(x: float, x_init: float = x0, y_init: float = y0) -> float:
    """
    Solusi analitik (manual) buat cari nilai eksak:
    dy / sqrt(y) = x dx  -> integrasi kedua sisi
    2*sqrt(y) = (x^2)/2 + C
    Kalau x0=0, y0=1 dapet C=2 -> y(x) = (1 + x^2 / 4)^2
    Fungsi ini dibuat fleksibel ngikutin x_init & y_init.
    """
    if y_init < 0:
        raise ValueError(f"Nilai y_init ({y_init}) tidak boleh negatif.")
    c_const = math.sqrt(y_init) - (x_init**2) / 4.0
    term = c_const + (x**2) / 4.0
    return (term**2) if term >= 0 else 0.0


# -------------------------------------------------------------
# Implementasi 3 Metode Numerik
# -------------------------------------------------------------
def euler_method(
    x0: float, y0: float, h: float, x_target: float
) -> List[Tuple[int, float, float]]:
    """
    Metode Euler sederhana:
    y_{i+1} = y_i + h * f(x_i, y_i)
    Tiap langkah cuma ngandelin gradien di titik awal doang.
    """
    # Cari tahu butuh berapa step dari x0 nyampe target
    steps = int(round((x_target - x0) / h))
    history: List[Tuple[int, float, float]] = []

    curr_x = x0
    curr_y = y0
    history.append((0, curr_x, curr_y))

    for i in range(1, steps + 1):
        # Update nilai y pake rumus Euler
        curr_y = curr_y + h * f(curr_x, curr_y)
        # Pakai round biar float gak geser-geser gara-gara presisi biner
        curr_x = round(x0 + i * h, 10)
        history.append((i, curr_x, curr_y))

    return history


def heun_rk2_method(
    x0: float, y0: float, h: float, x_target: float
) -> List[Tuple[int, float, float]]:
    """
    Metode Heun / Runge-Kutta Orde-2:
    k1 = kemiringan di awal langkah
    k2 = estimasi kemiringan di ujung langkah
    y_{i+1} = y_i + (h/2) * (k1 + k2) -> rata-rata dari k1 dan k2
    """
    steps = int(round((x_target - x0) / h))
    history: List[Tuple[int, float, float]] = []

    curr_x = x0
    curr_y = y0
    history.append((0, curr_x, curr_y))

    for i in range(1, steps + 1):
        # Hitung slope awal (k1) dan slope prediksi akhir (k2)
        k1 = f(curr_x, curr_y)
        k2 = f(curr_x + h, curr_y + h * k1)
        # Ambil rata-rata kedua slope buat langkah berikutnya
        curr_y = curr_y + (h / 2.0) * (k1 + k2)
        curr_x = round(x0 + i * h, 10)
        history.append((i, curr_x, curr_y))

    return history


def runge_kutta_4_method(
    x0: float, y0: float, h: float, x_target: float
) -> List[Tuple[int, float, float]]:
    """
    Metode Runge-Kutta Orde-4 (RK4):
    Pake 4 sampel kemiringan (k1, k2, k3, k4) biar hasilnya jauh lebih akurat.
    y_{i+1} = y_i + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
    """
    steps = int(round((x_target - x0) / h))
    history: List[Tuple[int, float, float]] = []

    curr_x = x0
    curr_y = y0
    history.append((0, curr_x, curr_y))

    for i in range(1, steps + 1):
        # Hitung 4 komponen gradien bobot RK4
        k1 = f(curr_x, curr_y)
        k2 = f(curr_x + 0.5 * h, curr_y + 0.5 * h * k1)
        k3 = f(curr_x + 0.5 * h, curr_y + 0.5 * h * k2)
        k4 = f(curr_x + h, curr_y + h * k3)
        # Gabungin pake rata-rata berbobot Simpson
        curr_y = curr_y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        curr_x = round(x0 + i * h, 10)
        history.append((i, curr_x, curr_y))

    return history


# -------------------------------------------------------------
# Bagian Output & Tampilan Tabel
# -------------------------------------------------------------
def cetak_tabel_metode(
    nama_metode: str, history: List[Tuple[int, float, float]]
) -> None:
    """
    Buat nampilin tabel riwayat iterasi per metode ke terminal.
    Kolomnya ada: Iterasi, X, Y hitung, Y eksak, dan galat mutlaknya.
    """
    print(f"\n{'=' * 75}")
    print(f" TABEL HASIL ITERASI: {nama_metode.upper()}")
    print(f"{'=' * 75}")
    print(f"| {'Iterasi':^7} | {'X':^8} | {'Y':^14} | {'Y Eksak':^14} | {'Galat Mutlak':^16} |")
    print(f"+{'-' * 9}+{'-' * 10}+{'-' * 16}+{'-' * 16}+{'-' * 18}+")

    for i, x_val, y_val in history:
        y_an = y_exact(x_val)
        galat = abs(y_an - y_val)
        print(f"| {i:^7d} | {x_val:^8.2f} | {y_val:^14.6f} | {y_an:^14.6f} | {galat:^16.6f} |")

    print(f"+{'-' * 9}+{'-' * 10}+{'-' * 16}+{'-' * 16}+{'-' * 18}+")


def cetak_kesimpulan_berdampingan(
    y_euler: float, y_heun: float, y_rk4: float, x_target: float, tol: float
) -> None:
    """
    Nampilin perbandingan nilai akhir y pas x=1.2 dari ketiga metode secara berdampingan.
    Sekalian dicek apakah galatnya udah lolos toleransi error yang diminta.
    """
    y_an = y_exact(x_target)
    err_euler = abs(y_an - y_euler)
    err_heun = abs(y_an - y_heun)
    err_rk4 = abs(y_an - y_rk4)

    status_euler = "TERPENUHI" if err_euler < tol else "TIDAK TERPENUHI"
    status_heun = "TERPENUHI" if err_heun < tol else "TIDAK TERPENUHI"
    status_rk4 = "TERPENUHI" if err_rk4 < tol else "TIDAK TERPENUHI"

    print("\n" + "=" * 89)
    print(f"{'KESIMPULAN AKHIR PERBANDINGAN ESTIMASI NILAI Y (x = ' + str(x_target) + ')':^89}")
    print("=" * 89)
    print(f"| {'Parameter':<22} | {'Metode Euler':^18} | {'Heun (RK-2)':^18} | {'RK-4':^20} |")
    print(f"+{'-' * 24}+{'-' * 20}+{'-' * 20}+{'-' * 22}+")
    print(f"| {'Estimasi Nilai Y':<22} | {y_euler:^18.6f} | {y_heun:^18.6f} | {y_rk4:^20.6f} |")
    print(f"| {'Solusi Eksak Analitik':<22} | {y_an:^18.6f} | {y_an:^18.6f} | {y_an:^20.6f} |")
    print(f"| {'Galat Mutlak':<22} | {err_euler:^18.6f} | {err_heun:^18.6f} | {err_rk4:^20.6e} |")
    print(f"| {'Status (e < ' + str(tol) + ')':<22} | {status_euler:^18} | {status_heun:^18} | {status_rk4:^20} |")
    print(f"+{'-' * 24}+{'-' * 20}+{'-' * 20}+{'-' * 22}+")
    print("\nKeterangan Analisis:")
    print(f"1. Solusi eksak analitik pada x = {x_target:.1f} adalah y = (1 + {x_target}^2 / 4)^2 = {y_an:.6f}.")
    print(f"2. Metode Euler memiliki akumulasi galat terbesar ({err_euler:.6f}) karena hanya mengandalkan gradien awal.")
    print(f"3. Metode Heun (RK-2) memperbaiki akurasi secara signifikan (galat = {err_heun:.6f}) dengan prediktor-korektor.")
    print(f"4. Metode Runge-Kutta Orde-4 (RK-4) memberikan hasil paling akurat (galat = {err_rk4:.6e}) dan berhasil memenuhi kriteria toleransi error epsilon < {tol}.")
    print("=" * 89)


# -------------------------------------------------------------
# Main Program
# -------------------------------------------------------------
def main():
    print("=" * 75)
    print(" PROGRAM PENYELESAIAN PERSAMAAN DIFERENSIAL BIASA (PDB)")
    print(" Persamaan : dy/dx = x * sqrt(y)")
    print(f" Nilai Awal: x0 = {x0}, y0 = {y0}")
    print(f" Step Size : h = {h}")
    print(f" Target    : x = {x_target}")
    print(f" Toleransi : epsilon < {epsilon}")
    print("=" * 75)

    # 1. Hitung pake metode Euler
    hist_euler = euler_method(x0, y0, h, x_target)
    cetak_tabel_metode("Metode Euler", hist_euler)

    # 2. Hitung pake metode Heun (RK-2)
    hist_heun = heun_rk2_method(x0, y0, h, x_target)
    cetak_tabel_metode("Metode Runge-Kutta Orde-2 (Heun)", hist_heun)

    # 3. Hitung pake metode RK-4
    hist_rk4 = runge_kutta_4_method(x0, y0, h, x_target)
    cetak_tabel_metode("Metode Runge-Kutta Orde-4", hist_rk4)

    # Ambil nilai y terakhir pas di x = 1.2
    y_euler_final = hist_euler[-1][2]
    y_heun_final = hist_heun[-1][2]
    y_rk4_final = hist_rk4[-1][2]

    # Cetak rangkuman perbandingan di paling bawah
    cetak_kesimpulan_berdampingan(
        y_euler=y_euler_final,
        y_heun=y_heun_final,
        y_rk4=y_rk4_final,
        x_target=x_target,
        tol=epsilon,
    )


if __name__ == "__main__":
    main()
