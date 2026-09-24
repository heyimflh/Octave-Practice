import math
from fractions import Fraction

EXP_X = 0.3
EXP_N_VALUES = [0, 1, 2, 3, 4]

HARMONIC_START = 1
HARMONIC_END = 20
DEFAULT_ROUND_DIGITS = 2   # Pembulatan per suku pada Tugas 2b

SIN_X = 1
SIN_N_VALUES = [1, 2, 3, 4, 5]

def absolute_error(exact, approximation):
    """Galat absolut: |exact - approximation|"""
    return abs(exact - approximation)

def relative_error(exact, approximation):
    """Galat relatif: |exact - approximation| / |exact|.
    Mengembalikan None jika exact == 0 untuk menghindari ZeroDivisionError.
    """
    if exact == 0:
        return None
    return abs(exact - approximation) / abs(exact)


def percentage_error(exact, approximation):
    """Persentase galat relatif (dalam %)."""
    rel = relative_error(exact, approximation)
    if rel is None:
        return None
    return rel * 100.0

def factorial(n):
    """Menghitung n! -- wrapper math.factorial dengan validasi."""
    if not isinstance(n, int) or n < 0:
        raise ValueError(f"n harus bilangan bulat non-negatif, bukan {n!r}.")
    return math.factorial(n)

def taylor_exp(x, n):
    """
    Hampiran e^x dengan deret Taylor sampai suku ke-n:
        T_n(x) = sum_{i=0}^{n}  x^i / i!
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError(f"n harus bilangan bulat non-negatif, bukan {n!r}.")
    total = 0.0
    for i in range(n + 1):
        total += (x ** i) / factorial(i)
    return total

def taylor_sin(x, n):
    """
    Hampiran sin(x) dengan deret Taylor sampai suku ke-n (indeks mulai 0):
        sin(x) = sum_{i=0}^{n}  (-1)^i * x^(2i+1) / (2i+1)!
    n = N - 1  di mana N adalah jumlah suku pada tugas.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError(f"n harus bilangan bulat non-negatif, bukan {n!r}.")
    total = 0.0
    for i in range(n + 1):
        total += ((-1) ** i) * (x ** (2 * i + 1)) / factorial(2 * i + 1)
    return total

def sep(char="=", width=68):
    print(char * width)

def header_seksi(judul):
    sep()
    print(f"  {judul}")
    sep()

def run_task_1():
    header_seksi("TUGAS 1 -- ERROR e^(0.3) : DERET TAYLOR")
    print()
    print(f"  Rumus : e^x = sum_{{i=0}}^{{n}}  x^i / i!")
    print(f"  Nilai : x = {EXP_X},  n in {EXP_N_VALUES}")
    eksak = math.exp(EXP_X)
    print(f"  Nilai eksak : math.exp({EXP_X}) = {eksak:.15f}")
    print()

    print(f"  {'n':>4}  {'Hampiran':>20}  {'Eksak':>20}  "
          f"{'Galat Absolut':>16}  {'Galat Relatif':>16}  {'Galat (%)':>14}")
    print("  " + "-" * 100)

    hasil_list = []
    for n in EXP_N_VALUES:
        hamp = taylor_exp(EXP_X, n)
        ab   = absolute_error(eksak, hamp)
        rel  = relative_error(eksak, hamp)
        pct  = percentage_error(eksak, hamp)
        hasil_list.append({
            "iteration": n, "approximation": hamp, "exact": eksak,
            "absolute_error": ab, "relative_error": rel, "percentage_error": pct
        })
        print(f"  {n:>4}  {hamp:>20.10f}  {eksak:>20.10f}  "
              f"{ab:>16.10e}  {rel:>16.10e}  {pct:>14.10f}")

    print()
    print("  [ANALISIS TUGAS 1]")
    e0 = hasil_list[0]["absolute_error"]
    e4 = hasil_list[-1]["absolute_error"]
    print(f"  * Galat absolut pada n=0 : {e0:.10e}")
    print(f"  * Galat absolut pada n=4 : {e4:.10e}")
    if e4 < e0:
        print("  * KESIMPULAN: Penambahan suku Taylor (n=0 -> n=4) memperkecil")
        print("    galat pemotongan secara signifikan. Semakin banyak suku yang")
        print("    digunakan, nilai hampiran semakin mendekati nilai eksak e^(0.3).")
    print()
    return hasil_list

def run_task_2(round_digits=DEFAULT_ROUND_DIGITS):
    if round_digits < 0:
        raise ValueError("round_digits harus >= 0.")

    header_seksi(f"TUGAS 2 -- ERROR  1/1 + 1/2 + ... + 1/{HARMONIC_END}")
    print()
    print(f"  Deret   : sum_{{i=1}}^{{{HARMONIC_END}}}  1/i")
    print(f"  Metode pembulatan (b): {round_digits} angka di belakang koma")
    print()

    frac_sum = Fraction(0)
    for i in range(HARMONIC_START, HARMONIC_END + 1):
        frac_sum += Fraction(1, i)
    reference = float(frac_sum)

    print("  [Metode A -- Eksak menggunakan fractions.Fraction]")
    print(f"  Representasi pecahan : {frac_sum}")
    print(f"  Nilai desimal        : {reference:.16f}")
    print()

    hasil_b = 0.0
    for i in range(HARMONIC_START, HARMONIC_END + 1):
        hasil_b += round(1 / i, round_digits)

    print(f"  [Metode B -- Setiap pembagian dibulatkan ke {round_digits} desimal]")
    ex_1_3 = round(1/3, round_digits)
    ex_1_6 = round(1/6, round_digits)
    ex_1_7 = round(1/7, round_digits)
    print(f"  Contoh: 1/3 -> {ex_1_3},  1/6 -> {ex_1_6},  1/7 -> {ex_1_7}")
    print(f"  Hasil  : {hasil_b:.16f}")
    print()

    hasil_c = sum(1 / i for i in range(HARMONIC_START, HARMONIC_END + 1))

    print("  [Metode C -- Tanpa loop eksplisit: sum()]")
    print("  Kode   : sum(1 / i for i in range(1, 21))")
    print(f"  Hasil  : {hasil_c:.16f}")
    print()

    rows = [
        {"method": "A -- Eksak (reference)",              "result": reference},
        {"method": f"B -- Dibulatkan ({round_digits} des.)", "result": hasil_b},
        {"method": "C -- sum() tanpa loop",               "result": hasil_c},
    ]
    for row in rows:
        row["absolute_error"]   = absolute_error(reference, row["result"])
        row["relative_error"]   = relative_error(reference, row["result"])
        row["percentage_error"] = percentage_error(reference, row["result"])

    print(f"  {'Metode':<32}  {'Hasil':>20}  {'Galat Absolut':>16}  "
          f"{'Galat Relatif':>16}  {'Galat (%)':>14}")
    print("  " + "-" * 106)
    for row in rows:
        print(f"  {row['method']:<32}  {row['result']:>20.10f}  "
              f"{row['absolute_error']:>16.6e}  "
              f"{row['relative_error']:>16.6e}  "
              f"{row['percentage_error']:>14.10f}")

    print()
    print("  [ANALISIS TUGAS 2]")
    ab_b = rows[1]["absolute_error"]
    ab_c = rows[2]["absolute_error"]
    print(f"  * Metode A (Eksak)   : {reference:.10f}")
    print(f"  * Metode B (Bulatkan): {hasil_b:.10f}  --> Galat absolut = {ab_b:.6e}")
    print(f"  * Metode C (sum())   : {hasil_c:.10f}  --> Galat absolut = {ab_c:.6e}")
    print()
    print(f"  * Metode B mengalami kehilangan presisi TERBESAR. Setiap suku 1/i")
    print(f"    sudah dipotong ke {round_digits} desimal sebelum dijumlahkan, sehingga")
    print(f"    terjadi akumulasi galat pembulatan yang cukup besar.")
    print("  * Metode C (sum()) tidak membulatkan tiap suku secara manual,")
    print("    hasilnya sangat dekat dengan nilai reference.")
    print("  * Selisih kecil yang tersisa pada Metode C merupakan batas")
    print("    representasi floating-point 64-bit (IEEE 754), bukan kesalahan.")
    print()
    return rows

def run_task_3():
    header_seksi(f"TUGAS 3 -- ERROR sin({SIN_X}) : DERET TAYLOR")
    print()
    print("  Rumus : sin(x) = sum_{n=0}^{N-1}  (-1)^n * x^(2n+1) / (2n+1)!")
    print(f"  Nilai : x = {SIN_X},  N in {SIN_N_VALUES}")
    eksak = math.sin(SIN_X)
    print(f"  Nilai eksak : math.sin({SIN_X}) = {eksak:.15f}")
    print()
    print("  Catatan: N = jumlah suku. N=1 -> indeks 0 saja, N=2 -> indeks 0 dan 1, dst.")
    print()

    print(f"  {'N':>4}  {'Hampiran':>20}  {'Eksak':>20}  "
          f"{'Galat Absolut':>16}  {'Galat Relatif':>16}  {'Galat (%)':>14}")
    print("  " + "-" * 100)

    hasil_list = []
    for N in SIN_N_VALUES:
        hamp = taylor_sin(SIN_X, N - 1)   # N suku => indeks 0..N-1
        ab   = absolute_error(eksak, hamp)
        rel  = relative_error(eksak, hamp)
        pct  = percentage_error(eksak, hamp)
        hasil_list.append({
            "iteration": N, "approximation": hamp, "exact": eksak,
            "absolute_error": ab, "relative_error": rel, "percentage_error": pct
        })
        print(f"  {N:>4}  {hamp:>20.10f}  {eksak:>20.10f}  "
              f"{ab:>16.10e}  {rel:>16.10e}  {pct:>14.10f}")

    print()
    print("  [ANALISIS TUGAS 3]")
    e1 = hasil_list[0]["absolute_error"]
    e5 = hasil_list[-1]["absolute_error"]
    print(f"  * Galat absolut pada N=1 : {e1:.10e}")
    print(f"  * Galat absolut pada N=5 : {e5:.10e}")
    if e5 < e1:
        print("  * KESIMPULAN: Penambahan suku deret Taylor (N=1 -> N=5)")
        print("    secara konsisten memperkecil galat pemotongan. Nilai hampiran")
        print("    sin(1) semakin mendekati nilai eksak ketika N bertambah.")
    print()
    return hasil_list

def cetak_ringkasan(hasil_t1, hasil_t2, hasil_t3):
    header_seksi("RINGKASAN ANALISIS")
    print()

    print("  TUGAS 1 -- e^(0.3) : Deret Taylor")
    print(f"  {'n':>4}  {'Hampiran':>20}  {'Galat Absolut':>18}")
    print("  " + "-" * 47)
    for row in hasil_t1:
        print(f"  {row['iteration']:>4}  {row['approximation']:>20.10f}  "
              f"{row['absolute_error']:>18.6e}")
    print()

    print("  TUGAS 2 -- 1/1 + 1/2 + ... + 1/20")
    print(f"  {'Metode':<38}  {'Galat Absolut':>16}")
    print("  " + "-" * 58)
    for row in hasil_t2:
        print(f"  {row['method']:<38}  {row['absolute_error']:>16.6e}")
    print()

    print("  TUGAS 3 -- sin(1) : Deret Taylor")
    print(f"  {'N':>4}  {'Hampiran':>20}  {'Galat Absolut':>18}")
    print("  " + "-" * 47)
    for row in hasil_t3:
        print(f"  {row['iteration']:>4}  {row['approximation']:>20.10f}  "
              f"{row['absolute_error']:>18.6e}")
    print()

    sep()
    print("  Kesimpulan Umum:")
    print("  1. Galat pemotongan (truncation error) mengecil ketika jumlah suku")
    print("     deret Taylor ditambah -- berlaku pada Tugas 1 dan Tugas 3.")
    print("  2. Galat pembulatan (round-off error) muncul ketika setiap suku")
    print("     dibulatkan sebelum dijumlahkan -- terlihat jelas pada Tugas 2b.")
    print("  3. Fungsi sum() memberikan hasil sangat dekat nilai eksak karena")
    print("     tidak ada pembulatan manual per suku -- terlihat pada Tugas 2c.")
    sep()

def main():
    sep("=", 68)
    print("  PRAKTIKUM KOMPUTASI NUMERIK -- GALAT / ERROR")
    print("  Universitas Sebelas Maret")
    sep("=", 68)
    print()

    hasil_t1 = run_task_1()
    hasil_t2 = run_task_2(round_digits=DEFAULT_ROUND_DIGITS)
    hasil_t3 = run_task_3()

    cetak_ringkasan(hasil_t1, hasil_t2, hasil_t3)
    print()

if __name__ == "__main__":
    main()
