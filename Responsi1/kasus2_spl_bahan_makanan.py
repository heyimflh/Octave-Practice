import itertools

import numpy as np

KONVERSI_KE_KG = {"kg": 1.0, "hg": 0.1, "dag": 0.01, "g": 0.001}

BAHAN = ["Beras", "Telur", "Tepung", "Ayam"]

DATA = {
    "Adel": ([(2.5, "kg"), (1500, "g"), (5, "kg"), (500, "g")], 161000),
    "Briza": ([(40, "hg"), (0.75, "kg"), (1000, "g"), (2, "kg")], 149000),
    "Caca": ([(2000, "g"), (15, "hg"), (50, "dag"), (6000, "g")], 251500),
    "Dinda": ([(1, "kg"), (4250, "g"), (20, "hg"), (9, "hg")], 173000),
}

TOLERANSI = 1e-10
MAKS_ITERASI = 1000


def ke_kg(nilai, satuan):
    return nilai * KONVERSI_KE_KG[satuan]


def bentuk_matriks():
    baris = []
    total = []
    for belanja, harga in DATA.values():
        baris.append([ke_kg(n, s) for n, s in belanja])
        total.append(harga)
    return np.array(baris, dtype=float), np.array(total, dtype=float)


def dominan_diagonal(A):
    diag = np.abs(np.diag(A))
    luar = np.sum(np.abs(A), axis=1) - diag
    return bool(np.all(diag > luar))


def cari_urutan_dominan(A):
    for perm in itertools.permutations(range(A.shape[0])):
        if dominan_diagonal(A[list(perm), :]):
            return list(perm)
    return None


def jari_jari_spektral_gs(A):
    L = np.tril(A)
    U = A - L
    T = -np.linalg.solve(L, U)
    return float(np.max(np.abs(np.linalg.eigvals(T))))


def gauss_seidel(A, b, toleransi=TOLERANSI, maks_iterasi=MAKS_ITERASI):
    n = len(b)
    x = np.zeros(n)
    riwayat = [x.copy()]
    for iterasi in range(1, maks_iterasi + 1):
        x_lama = x.copy()
        for i in range(n):
            jumlah = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i + 1:], x_lama[i + 1:])
            x[i] = (b[i] - jumlah) / A[i, i]
        riwayat.append(x.copy())
        if np.max(np.abs(x - x_lama)) < toleransi:
            return x, iterasi, riwayat
    return x, maks_iterasi, riwayat


def gauss_jordan(A, b):
    n = len(b)
    M = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
    for k in range(n):
        pivot = k + np.argmax(np.abs(M[k:, k]))
        if abs(M[pivot, k]) < 1e-15:
            raise ValueError("Matriks singular, SPL tidak punya solusi tunggal")
        M[[k, pivot]] = M[[pivot, k]]
        M[k] = M[k] / M[k, k]
        for i in range(n):
            if i != k:
                M[i] = M[i] - M[i, k] * M[k]
    return M[:, -1]


def cetak_matriks(A, b):
    for i in range(A.shape[0]):
        isi = "  ".join("%8.3f" % v for v in A[i])
        print("[ %s ] | %12.2f" % (isi, b[i]))


def main():
    print("=" * 70)
    print("KASUS 2 - SPL METODE LANGSUNG / TIDAK LANGSUNG")
    print("=" * 70)

    print("\n1. Konversi satuan ke kilogram")
    print("-" * 70)
    for nama, (belanja, harga) in DATA.items():
        rincian = ", ".join(
            "%s %g %s = %g kg" % (BAHAN[i], n, s, ke_kg(n, s))
            for i, (n, s) in enumerate(belanja)
        )
        print("%s: %s | Rp %s" % (nama, rincian, format(harga, ",.0f")))

    A, b = bentuk_matriks()

    print("\n2. Bentuk SPL (x1 = beras, x2 = telur, x3 = tepung, x4 = ayam, per kg)")
    print("-" * 70)
    for (nama, _), baris, harga in zip(DATA.items(), A, b):
        suku = " + ".join("%gx%d" % (v, j + 1) for j, v in enumerate(baris))
        print("%-6s: %s = %s" % (nama, suku, format(harga, ".0f")))

    print("\nBentuk matriks A.x = b :")
    cetak_matriks(A, b)

    print("\n3. Analisis kelayakan metode tidak langsung (Gauss-Seidel)")
    print("-" * 70)
    print("det(A) = %.6f" % np.linalg.det(A))

    dominan_asli = dominan_diagonal(A)
    rho_asli = jari_jari_spektral_gs(A)
    print("Urutan asli dominan diagonal secara ketat : %s" % ("Ya" if dominan_asli else "Tidak"))
    print("Jari-jari spektral iterasi Gauss-Seidel   : %.6f (%s)" % (
        rho_asli, "konvergen" if rho_asli < 1 else "divergen"
    ))

    A_pakai, b_pakai = A.copy(), b.copy()
    urutan = list(range(len(b)))
    metode_tidak_langsung = dominan_asli or rho_asli < 1

    if not dominan_asli:
        perm = cari_urutan_dominan(A)
        if perm is not None:
            urutan = perm
            A_pakai, b_pakai = A[perm, :], b[perm]
            metode_tidak_langsung = True
            nama_baris = list(DATA.keys())
            print("\nSetelah baris ditukar menjadi urutan: %s" % ", ".join(nama_baris[i] for i in perm))
            print("matriks menjadi dominan diagonal secara ketat:")
            cetak_matriks(A_pakai, b_pakai)
            print("Jari-jari spektral setelah penukaran baris : %.6f" % jari_jari_spektral_gs(A_pakai))
        else:
            metode_tidak_langsung = False

    if metode_tidak_langsung:
        print("\nKesimpulan: SPL dapat diselesaikan dengan metode numerik (Gauss-Seidel).")
        print("\n4. Penyelesaian dengan Gauss-Seidel (tebakan awal 0, toleransi %g)" % TOLERANSI)
        print("-" * 70)
        x, iterasi, riwayat = gauss_seidel(A_pakai, b_pakai)
        print("%-6s %-14s %-14s %-14s %-14s" % ("Iter", "x1", "x2", "x3", "x4"))
        tampil = list(range(0, min(6, len(riwayat))))
        if len(riwayat) > 6:
            tampil += [len(riwayat) - 1]
        for k in tampil:
            print("%-6d %-14.6f %-14.6f %-14.6f %-14.6f" % ((k,) + tuple(riwayat[k])))
        print("Konvergen setelah %d iterasi" % iterasi)
        metode = "Gauss-Seidel"
    else:
        print("\nKesimpulan: SPL tidak dapat diselesaikan dengan metode numerik.")
        print("Digunakan metode langsung Gauss-Jordan.")
        print("\n4. Penyelesaian dengan Gauss-Jordan")
        print("-" * 70)
        x = gauss_jordan(A, b)
        metode = "Gauss-Jordan"

    print("\n5. Hasil akhir (%s)" % metode)
    print("-" * 70)
    for nama, harga in zip(BAHAN, x):
        print("Harga %-7s per kg : Rp %s" % (nama, format(harga, ",.2f")))

    print("\n6. Verifikasi")
    print("-" * 70)
    selisih = np.max(np.abs(x - np.linalg.solve(A, b)))
    residu = np.max(np.abs(A @ x - b))
    print("Selisih maksimum dengan numpy.linalg.solve : %.3e" % selisih)
    print("Residu maksimum |A.x - b|                  : %.3e" % residu)
    for (nama, (belanja, harga)), baris in zip(DATA.items(), A):
        print("%-6s total hitung Rp %s | total soal Rp %s" % (
            nama, format(float(baris @ x), ",.2f"), format(harga, ",.2f")
        ))


if __name__ == "__main__":
    main()
