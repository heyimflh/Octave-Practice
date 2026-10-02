from fractions import Fraction
import copy

A_DEFAULT = [
    [2,  1, -1],
    [4,  3,  1],
    [-2, 1,  2],
]
B_DEFAULT = [3, 9, 4]

def to_fraction(value):
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        return Fraction(value).limit_denominator(10**9)
    if isinstance(value, str):
        value = value.strip()
        if '/' in value:
            parts = value.split('/')
            if len(parts) == 2:
                return Fraction(int(parts[0]), int(parts[1]))
        return Fraction(value)
    raise ValueError(f"Tidak dapat mengonversi nilai: {value!r}")

def copy_matrix(matrix):
    return [[elem for elem in row] for row in matrix]

def matrix_to_fraction(matrix):
    return [[to_fraction(x) for x in row] for row in matrix]

def vector_to_fraction(vec):
    return [to_fraction(x) for x in vec]

def format_fraction(val):
    if not isinstance(val, Fraction):
        val = Fraction(val)
    if val.denominator == 1:
        return str(val.numerator)
    return f"{val.numerator}/{val.denominator}"

def format_fraction_with_decimal(val):
    frac_str = format_fraction(val)
    dec_val = float(val)
    dec_str = f"{dec_val:.10g}"
    if frac_str == dec_str:
        return frac_str
    return f"{frac_str}  ({dec_str})"

def _col_width(val_str):
    return max(len(val_str), 4)

SEPARATOR_60 = "=" * 60
SEPARATOR_DASH = "-" * 60

def print_matrix(matrix, title=None, augmented=False):
    n = len(matrix)
    if n == 0:
        return

    str_matrix = []
    for row in matrix:
        str_matrix.append([format_fraction(x) for x in row])

    m = len(str_matrix[0])

    col_widths = []
    for j in range(m):
        w = max(len(str_matrix[i][j]) for i in range(n))
        col_widths.append(w)

    if title:
        print(f"\n{title}")

    for i, row in enumerate(str_matrix):
        parts = []
        for j, val in enumerate(row):
            if augmented and j == m - 1:
                parts.append("| " + val.rjust(col_widths[j]))
            else:
                parts.append(val.rjust(col_widths[j]))
        print("  [ " + "  ".join(parts) + " ]")
    print()

def print_vector(vec, name="y"):
    vals = [format_fraction(x) for x in vec]
    w = max(len(v) for v in vals)
    for i, v in enumerate(vals):
        print(f"  [ {v.rjust(w)} ]")
    print()

def forward_elimination(aug, n, verbose=True, record_multipliers=False):
    multipliers = {}

    for k in range(n - 1):  # pivot pada kolom k
        pivot = aug[k][k]

        if pivot == Fraction(0):
            raise ValueError(
                f"Error: pivot bernilai 0 pada kolom {k + 1}. "
                "Eliminasi langsung tidak dapat dilanjutkan."
            )

        if verbose:
            print(f"  [Langkah {k + 1}]")
            print(f"  Pivot = {format_fraction(pivot)}")
            print()

        for i in range(k + 1, n):
            if aug[i][k] == Fraction(0):
                continue

            m_ik = aug[i][k] / pivot
            multipliers[(i, k)] = m_ik

            if verbose:
                m_str = format_fraction(m_ik)
                m_sign = "-" if m_ik >= 0 else "+"
                m_abs = format_fraction(abs(m_ik))
                print(f"  m{i+1}{k+1} = {format_fraction(aug[i][k])} / {format_fraction(pivot)} = {m_str}")
                if m_ik >= 0:
                    print(f"  Operasi: R{i+1} <- R{i+1} - {m_abs}·R{k+1}")
                else:
                    print(f"  Operasi: R{i+1} <- R{i+1} - ({m_str})·R{k+1}")
                print()

            for j in range(k, n + 1):
                aug[i][j] = aug[i][j] - m_ik * aug[k][j]

        if verbose:
            print_matrix(aug, title="  Matriks setelah langkah ini:", augmented=True)

    return aug, multipliers

def backward_substitution(U, rhs, n, verbose=True):
    x = [Fraction(0)] * n

    for i in range(n - 1, -1, -1):
        if U[i][i] == Fraction(0):
            raise ValueError(
                "Error: diagonal utama bernilai 0. "
                "SPL tidak memiliki solusi tunggal (matriks singular)."
            )
        s = Fraction(0)
        for j in range(i + 1, n):
            s += U[i][j] * x[j]
        x[i] = (rhs[i] - s) / U[i][i]

        if verbose:
            print(f"  x{i+1} = {format_fraction_with_decimal(x[i])}")

    return x

def eliminasi_gauss(A, b):
    n = len(A)
    A_frac = matrix_to_fraction(A)
    b_frac = vector_to_fraction(b)
    aug = [A_frac[i] + [b_frac[i]] for i in range(n)]

    print(SEPARATOR_60)
    print("                    ELIMINASI GAUSS")
    print(SEPARATOR_60)
    print_matrix(aug, title="Matriks Augmented Awal [A | b]:", augmented=True)

    print("  ── Forward Elimination ──")
    print()

    aug, _ = forward_elimination(aug, n, verbose=True)
    print_matrix(aug, title="  Matriks Segitiga Atas:", augmented=True)

    U = [aug[i][:n] for i in range(n)]
    rhs = [aug[i][n] for i in range(n)]

    print("  ── Backward Substitution ──")
    print()
    x = backward_substitution(U, rhs, n, verbose=True)

    print()
    print(f"  {'─'*46}")
    print("  SOLUSI (Eliminasi Gauss):")
    for i, xi in enumerate(x):
        print(f"    x{i+1} = {format_fraction_with_decimal(xi)}")
    print()

    return x, aug

def gauss_jordan_from_upper(aug_upper, n, verbose=True):
    aug = [row[:] for row in aug_upper]

    if verbose:
        print("  ── Backward Elimination & Normalisasi ──")
        print()

    for k in range(n - 1, -1, -1):
        pivot = aug[k][k]
        if pivot == Fraction(0):
            raise ValueError(
                "Error: pivot bernilai 0 pada Gauss-Jordan. "
                "Matriks singular."
            )

        pivot_str = format_fraction(pivot)
        if verbose:
            print(f"  Normalisasi R{k+1}: R{k+1} <- R{k+1} / {pivot_str}")

        for j in range(k, n + 1):
            aug[k][j] = aug[k][j] / pivot

        if verbose:
            print_matrix(aug, title=f"  Setelah normalisasi R{k+1}:", augmented=True)

        for i in range(k - 1, -1, -1):
            if aug[i][k] == Fraction(0):
                continue
            factor = aug[i][k]
            factor_str = format_fraction(factor)
            if verbose:
                print(f"  Eliminasi: R{i+1} <- R{i+1} - ({factor_str})·R{k+1}")

            for j in range(k, n + 1):
                aug[i][j] = aug[i][j] - factor * aug[k][j]

        if verbose:
            if k > 0:
                print_matrix(aug, title="  Matriks saat ini:", augmented=True)

    x = [aug[i][n] for i in range(n)]
    return aug, x

def gauss_jordan(A, b):
    n = len(A)

    A_frac = matrix_to_fraction(A)
    b_frac = vector_to_fraction(b)
    aug = [A_frac[i] + [b_frac[i]] for i in range(n)]

    print(SEPARATOR_60)
    print("                    GAUSS-JORDAN")
    print(SEPARATOR_60)
    print_matrix(aug, title="Matriks Augmented Awal [A | b]:", augmented=True)

    print("  ── Forward Elimination ──")
    print()
    aug, _ = forward_elimination(aug, n, verbose=True)

    print_matrix(aug, title="  Hasil Forward Elimination (Segitiga Atas):", augmented=True)

    aug_rref, x = gauss_jordan_from_upper(aug, n, verbose=True)

    print_matrix(aug_rref, title="  Matriks RREF Akhir [I | x]:", augmented=True)

    print(f"  {'─'*46}")
    print("  SOLUSI (Gauss-Jordan):")
    for i, xi in enumerate(x):
        print(f"    x{i+1} = {format_fraction_with_decimal(xi)}")
    print()

    return x

def lu_decomposition(A, verbose=True):
    n = len(A)
    A_frac = matrix_to_fraction(A)

    L = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    U = copy_matrix(A_frac)

    multipliers = {}

    for k in range(n - 1):
        pivot = U[k][k]

        if pivot == Fraction(0):
            raise ValueError(
                f"Error: pivot U[{k}][{k}] = 0. "
                "Dekomposisi LU tanpa pertukaran baris tidak dapat dilanjutkan."
            )

        for i in range(k + 1, n):
            if U[i][k] == Fraction(0):
                continue

            m_ik = U[i][k] / pivot
            multipliers[(i, k)] = m_ik

            L[i][k] = m_ik

            for j in range(k, n):
                U[i][j] = U[i][j] - m_ik * U[k][j]

    return L, U, multipliers

def forward_substitution(L, b, n, verbose=True):
    y = [Fraction(0)] * n

    for i in range(n):
        s = Fraction(0)
        for j in range(i):
            s += L[i][j] * y[j]
        y[i] = (b[i] - s) / L[i][i]

        if verbose:
            print(f"  y{i+1} = {format_fraction_with_decimal(y[i])}")

    return y

def mat_mul(A, B):
    m = len(A)
    k = len(A[0])
    nc = len(B[0])
    C = [[Fraction(0)] * nc for _ in range(m)]
    for i in range(m):
        for p in range(k):
            for j in range(nc):
                C[i][j] += A[i][p] * B[p][j]
    return C

def mat_vec_mul(A, x):
    n = len(A)
    b = [Fraction(0)] * n
    for i in range(n):
        for j in range(n):
            b[i] += A[i][j] * x[j]
    return b

def verify_ax_eq_b(A, x, b_original):
    A_frac = matrix_to_fraction(A)
    x_frac = [to_fraction(xi) for xi in x]
    b_frac = vector_to_fraction(b_original)

    Ax = mat_vec_mul(A_frac, x_frac)
    berhasil = all(Ax[i] == b_frac[i] for i in range(len(b_frac)))
    return berhasil, Ax

def verify_lu(A_original, L, U):
    A_frac = matrix_to_fraction(A_original)
    LU = mat_mul(L, U)
    berhasil = all(
        LU[i][j] == A_frac[i][j]
        for i in range(len(A_frac))
        for j in range(len(A_frac[0]))
    )
    return berhasil, LU

def dekomposisi_lu(A, b):
    n = len(A)
    b_frac = vector_to_fraction(b)

    print(SEPARATOR_60)
    print("                   DEKOMPOSISI LU")
    print(SEPARATOR_60)

    print_matrix(matrix_to_fraction(A), title="Matriks A:")
    print("  b =")
    print_vector(b_frac, "b")

    L, U, multipliers = lu_decomposition(A, verbose=False)

    print("  ── Multiplier ──")
    print()
    if multipliers:
        for (i, k), m_val in sorted(multipliers.items()):
            print(f"  m{i+1}{k+1} = {format_fraction(m_val)}")
    else:
        print("  (Tidak ada multiplier — matriks sudah segitiga atas)")
    print()

    print_matrix(L, title="  Matriks L:")
    print_matrix(U, title="  Matriks U:")

    lu_ok, LU = verify_lu(A, L, U)
    status_lu = "BERHASIL ✓" if lu_ok else "GAGAL ✗"
    print(f"  Verifikasi L × U = A  :  {status_lu}")
    if not lu_ok:
        print_matrix(LU, title="  L × U =")
    print()

    print("  ── Penyelesaian Ly = b (Forward Substitution) ──")
    print()
    y = forward_substitution(L, b_frac, n, verbose=True)
    y_str = ", ".join(format_fraction(yi) for yi in y)
    print()
    print(f"  y = [{y_str}]")
    print()

    print("  ── Penyelesaian Ux = y (Backward Substitution) ──")
    print()
    x = backward_substitution(U, y, n, verbose=True)
    print()
    ax_ok, Ax = verify_ax_eq_b(A, x, b)
    status_ax = "BERHASIL ✓" if ax_ok else "GAGAL ✗"
    print(f"  Verifikasi A × x = b  :  {status_ax}")
    print()

    print(f"  {'─'*46}")
    print("  SOLUSI (Dekomposisi LU):")
    for i, xi in enumerate(x):
        print(f"    x{i+1} = {format_fraction_with_decimal(xi)}")
    print()

    return x, L, U, y

def tampilkan_perbandingan(x_gauss, x_gj, x_lu, A=None, b=None, L=None, U=None, y_lu=None):
    n = len(x_gauss)

    print(SEPARATOR_60)
    print("              PERBANDINGAN SEMUA METODE")
    print(SEPARATOR_60)
    print()

    col = 15
    header = f"  {'Variabel':<10} {'Gauss':^{col}} {'Gauss-Jordan':^{col}} {'LU':^{col}}"
    print(header)
    print("  " + "-" * (10 + col * 3 + 6))

    for i in range(n):
        sg = format_fraction(x_gauss[i])
        sj = format_fraction(x_gj[i])
        sl = format_fraction(x_lu[i])
        print(f"  {'x' + str(i+1):<10} {sg:^{col}} {sj:^{col}} {sl:^{col}}")

    print("  " + "-" * (10 + col * 3 + 6))
    print()

    konsisten = all(x_gauss[i] == x_gj[i] == x_lu[i] for i in range(n))
    status_konsisten = "BERHASIL ✓" if konsisten else "TIDAK KONSISTEN ✗"

    if A is not None and b is not None:
        ax_ok_g, _ = verify_ax_eq_b(A, x_gauss, b)
        ax_ok_j, _ = verify_ax_eq_b(A, x_gj, b)
        ax_ok_l, _ = verify_ax_eq_b(A, x_lu, b)
        ax_ok = ax_ok_g and ax_ok_j and ax_ok_l
        status_ax = "BERHASIL ✓" if ax_ok else "GAGAL ✗"
        print(f"  Verifikasi A × x = b        :  {status_ax}")

    if A is not None and L is not None and U is not None:
        lu_ok, _ = verify_lu(A, L, U)
        status_lu = "BERHASIL ✓" if lu_ok else "GAGAL ✗"
        print(f"  Verifikasi A = L × U        :  {status_lu}")
    if y_lu is not None:
        y_str = ", ".join(format_fraction(yi) for yi in y_lu)
        print(f"  Vektor y (LU) = [{y_str}]")

    print(f"  Konsistensi ketiga metode   :  {status_konsisten}")
    print()

    if konsisten:
        print("  [OK] Ketiga metode menghasilkan solusi SPL yang sama.")
    else:
        print("  [!]  Hasil ketiga metode tidak konsisten — periksa implementasi.")
    print()

def tampilkan_ringkasan_akhir(x_gauss, x_gj, x_lu, L, U, y_lu, A, b):
    n = len(x_gauss)
    col = 10

    print(SEPARATOR_60)
    print("                  HASIL AKHIR SPL")
    print(SEPARATOR_60)
    print()

    header = f"  {'Metode':<16} {'x1':^{col}} {'x2':^{col}} {'x3':^{col}}"
    print(header)
    print("  " + "-" * (16 + col * 3 + 4))

    sg = [format_fraction(x) for x in x_gauss]
    sj = [format_fraction(x) for x in x_gj]
    sl = [format_fraction(x) for x in x_lu]

    print(f"  {'Gauss':<16} {sg[0]:^{col}} {sg[1]:^{col}} {sg[2]:^{col}}")
    print(f"  {'Gauss-Jordan':<16} {sj[0]:^{col}} {sj[1]:^{col}} {sj[2]:^{col}}")
    print(f"  {'LU':<16} {sl[0]:^{col}} {sl[1]:^{col}} {sl[2]:^{col}}")
    print("  " + "-" * (16 + col * 3 + 4))
    print()

    y_str = ", ".join(format_fraction(yi) for yi in y_lu)
    print(f"  y (LU) = [{y_str}]")
    print()
    print_matrix(L, title="  Matriks L:")
    print_matrix(U, title="  Matriks U:")

    lu_ok, _ = verify_lu(A, L, U)
    ax_ok, _ = verify_ax_eq_b(A, x_lu, b)
    konsisten = all(x_gauss[i] == x_gj[i] == x_lu[i] for i in range(n))

    print(f"  Verifikasi A = LU           : {'BERHASIL ✓' if lu_ok else 'GAGAL ✗'}")
    print(f"  Verifikasi A × x = b        : {'BERHASIL ✓' if ax_ok else 'GAGAL ✗'}")
    print(f"  Konsistensi ketiga metode   : {'BERHASIL ✓' if konsisten else 'GAGAL ✗'}")
    print()

def tampilkan_soal(A, b):
    n = len(A)
    A_frac = matrix_to_fraction(A)
    b_frac = vector_to_fraction(b)

    print()
    print("  Sistem Persamaan Linear:")
    for i in range(n):
        terms = []
        for j in range(n):
            c = A_frac[i][j]
            c_str = format_fraction(c)
            var = f"x{j+1}"
            if j == 0:
                terms.append(f"{c_str}{var}")
            else:
                if c >= 0:
                    terms.append(f"+ {c_str}{var}")
                else:
                    c_abs = format_fraction(abs(c))
                    terms.append(f"- {c_abs}{var}")
        b_str = format_fraction(b_frac[i])
        print("    " + " ".join(terms) + f" = {b_str}")
    print()
    print("  Matriks A:")
    print_matrix(A_frac)
    print("  Vektor b:")
    print_vector(b_frac)

def menu(A, b):
    while True:
        print()
        print(SEPARATOR_60)
        print("           PROGRAM PENYELESAIAN SPL")
        print(SEPARATOR_60)
        tampilkan_soal(A, b)
        print(SEPARATOR_DASH)
        print("  1. Eliminasi Gauss")
        print("  2. Gauss-Jordan")
        print("  3. Dekomposisi LU")
        print("  4. Jalankan Semua Metode")
        print("  5. Keluar")
        print(SEPARATOR_DASH)

        pilihan = input("  Pilih menu [1-5]: ").strip()
        print()

        if pilihan == "1":
            try:
                x_gauss, _ = eliminasi_gauss(A, b)
            except ValueError as e:
                print(f"\n  {e}\n")

        elif pilihan == "2":
            try:
                x_gj = gauss_jordan(A, b)
            except ValueError as e:
                print(f"\n  {e}\n")

        elif pilihan == "3":
            try:
                x_lu, L, U, y_lu = dekomposisi_lu(A, b)
            except ValueError as e:
                print(f"\n  {e}\n")

        elif pilihan == "4":
            try:
                print("\n" + "=" * 60)
                print("         MENJALANKAN SEMUA METODE")
                print("=" * 60)

                x_gauss, _ = eliminasi_gauss(A, b)
                x_gj = gauss_jordan(A, b)
                x_lu, L, U, y_lu = dekomposisi_lu(A, b)

                tampilkan_perbandingan(x_gauss, x_gj, x_lu, A=A, b=b, L=L, U=U, y_lu=y_lu)
                tampilkan_ringkasan_akhir(x_gauss, x_gj, x_lu, L, U, y_lu, A, b)

            except ValueError as e:
                print(f"\n  {e}\n")

        elif pilihan == "5":
            print("  Program selesai. Terima kasih!")
            break

        else:
            print("  Pilihan tidak valid. Masukkan angka 1–5.")

        input("\n  [Tekan Enter untuk kembali ke menu...]\n")

def main():
    print()
    print(SEPARATOR_60)
    print("   PROGRAM PENYELESAIAN SISTEM PERSAMAAN LINEAR (SPL)")
    print("   Metode: Eliminasi Gauss | Gauss-Jordan | Dekomposisi LU")
    print("   Implementasi: Python 3 (fractions.Fraction)")
    print(SEPARATOR_60)
    print()
    print("  Menggunakan data soal default (3×3):")
    print("    2x1 +  x2 -  x3 = 3")
    print("    4x1 + 3x2 +  x3 = 9")
    print("   -2x1 +  x2 + 2x3 = 4")
    print()

    A = A_DEFAULT
    b = B_DEFAULT

    A = matrix_to_fraction(A)
    b = vector_to_fraction(b)

    menu(A, b)

if __name__ == "__main__":
    main()
