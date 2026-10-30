import math

import matplotlib.pyplot as plt
import numpy as np

V_BOLA = 300.0
TOLERANSI = 1e-8
MAKS_ITERASI = 100


def f(r):
    return (4.0 / 3.0) * math.pi * r ** 3 - V_BOLA


def cari_selang_awal(fungsi, batas_bawah=0.0, batas_atas=10.0, langkah=1.0):
    selang = []
    a = batas_bawah
    while a < batas_atas:
        b = a + langkah
        if fungsi(a) * fungsi(b) < 0:
            selang.append((a, b))
        a = b
    return selang


def biseksi(fungsi, a, b, toleransi=TOLERANSI, maks_iterasi=MAKS_ITERASI):
    if fungsi(a) * fungsi(b) >= 0:
        raise ValueError("f(a) dan f(b) harus berbeda tanda")
    tabel = []
    c_lama = a
    for i in range(1, maks_iterasi + 1):
        c = (a + b) / 2.0
        fc = fungsi(c)
        galat = abs(c - c_lama) if i > 1 else float("nan")
        tabel.append((i, a, b, c, fc, galat))
        if abs(fc) < toleransi or (i > 1 and galat < toleransi):
            return c, tabel
        if fungsi(a) * fc < 0:
            b = c
        else:
            a = c
        c_lama = c
    return c, tabel


def regula_falsi(fungsi, a, b, toleransi=TOLERANSI, maks_iterasi=MAKS_ITERASI):
    if fungsi(a) * fungsi(b) >= 0:
        raise ValueError("f(a) dan f(b) harus berbeda tanda")
    tabel = []
    c_lama = a
    for i in range(1, maks_iterasi + 1):
        fa, fb = fungsi(a), fungsi(b)
        c = (a * fb - b * fa) / (fb - fa)
        fc = fungsi(c)
        galat = abs(c - c_lama) if i > 1 else float("nan")
        tabel.append((i, a, b, c, fc, galat))
        if abs(fc) < toleransi or (i > 1 and galat < toleransi):
            return c, tabel
        if fa * fc < 0:
            b = c
        else:
            a = c
        c_lama = c
    return c, tabel


def cetak_tabel(tabel, maks_baris=12):
    print("%-5s %-12s %-12s %-14s %-14s %-12s" % ("Iter", "a", "b", "c", "f(c)", "Galat"))
    tampil = tabel if len(tabel) <= maks_baris else tabel[:maks_baris - 1] + [tabel[-1]]
    for i, (k, a, b, c, fc, galat) in enumerate(tampil):
        if len(tabel) > maks_baris and i == len(tampil) - 1:
            print("%-5s" % "...")
        g = "-" if math.isnan(galat) else "%.3e" % galat
        print("%-5d %-12.6f %-12.6f %-14.8f %-14.3e %-12s" % (k, a, b, c, fc, g))


def main():
    print("=" * 70)
    print("KASUS 3 - PERSAMAAN NONLINEAR (JARI-JARI BOLA DALAM TABUNG)")
    print("=" * 70)

    print("\n1. Perumusan persamaan nonlinear")
    print("-" * 70)
    print("Tinggi tabung t = 2r, jadi bola menyentuh alas, tutup, dan dinding tabung.")
    print("V bola   = (4/3) pi r^3 = %.0f cm^3" % V_BOLA)
    print("V tabung = pi r^2 t = 2 pi r^3")
    print("V bola : V tabung = (4/3) pi r^3 : 2 pi r^3 = 2 : 3")
    print("V tabung = (3/2) x %.0f = %.0f cm^3" % (V_BOLA, 1.5 * V_BOLA))
    print("V tabung di luar bola = %.0f - %.0f = %.0f cm^3" % (1.5 * V_BOLA, V_BOLA, 0.5 * V_BOLA))
    print("\nPersamaan nonlinear: f(r) = (4/3) pi r^3 - 300 = 0")

    print("\n2. Metode grafik untuk menentukan nilai awal")
    print("-" * 70)
    selang = cari_selang_awal(f)
    print("Perubahan tanda f(r) ditemukan pada selang:", selang)
    a0, b0 = selang[0]
    print("Nilai awal dipakai: a = %g, b = %g" % (a0, b0))
    print("f(a) = %.4f, f(b) = %.4f" % (f(a0), f(b0)))

    print("\n3. Metode Biseksi")
    print("-" * 70)
    r_bis, tab_bis = biseksi(f, a0, b0)
    cetak_tabel(tab_bis)
    print("Akar biseksi        : r = %.10f cm (%d iterasi)" % (r_bis, len(tab_bis)))

    print("\n4. Metode Regula-Falsi")
    print("-" * 70)
    r_rf, tab_rf = regula_falsi(f, a0, b0)
    cetak_tabel(tab_rf)
    print("Akar regula-falsi   : r = %.10f cm (%d iterasi)" % (r_rf, len(tab_rf)))

    r_eksak = (3.0 * V_BOLA / (4.0 * math.pi)) ** (1.0 / 3.0)

    print("\n5. Perbandingan dan verifikasi")
    print("-" * 70)
    print("%-16s %-18s %-12s %-16s" % ("Metode", "r (cm)", "Iterasi", "Galat vs eksak"))
    print("%-16s %-18.10f %-12d %-16.3e" % ("Biseksi", r_bis, len(tab_bis), abs(r_bis - r_eksak)))
    print("%-16s %-18.10f %-12d %-16.3e" % ("Regula-falsi", r_rf, len(tab_rf), abs(r_rf - r_eksak)))
    print("%-16s %-18.10f" % ("Analitik", r_eksak))

    r = r_bis
    v_bola = (4.0 / 3.0) * math.pi * r ** 3
    t = 2 * r
    v_tabung = math.pi * r ** 2 * t
    v_luar = v_tabung - v_bola
    v_rumus = (2.0 / 3.0) * math.pi * r ** 3

    print("\n6. Hasil akhir (memakai akar biseksi)")
    print("-" * 70)
    print("Jari-jari bola dan tabung (r) : %.6f cm" % r)
    print("Tinggi tabung (t = 2r)        : %.6f cm" % t)
    print("Volume bola                   : %.6f cm^3" % v_bola)
    print("Volume tabung                 : %.6f cm^3" % v_tabung)
    print("Volume tabung di luar bola    : %.6f cm^3" % v_luar)
    print("Cek V = (2/3) pi r^3          : %.6f cm^3" % v_rumus)

    rr = np.linspace(0, 10, 500)
    ff = (4.0 / 3.0) * np.pi * rr ** 3 - V_BOLA

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    ax1.plot(rr, ff, "b-", linewidth=2, label="f(r)")
    ax1.axhline(0, color="k", linewidth=1)
    ax1.axvspan(a0, b0, color="orange", alpha=0.25, label="selang awal [%g, %g]" % (a0, b0))
    ax1.plot(r, 0, "ro", label="akar r = %.4f" % r)
    ax1.set_title("Metode Grafik: f(r) = (4/3)πr³ - 300")
    ax1.set_xlabel("r (cm)")
    ax1.set_ylabel("f(r)")
    ax1.grid(True)
    ax1.legend()

    rz = np.linspace(a0, b0, 200)
    fz = (4.0 / 3.0) * np.pi * rz ** 3 - V_BOLA
    ax2.plot(rz, fz, "b-", linewidth=2, label="f(r)")
    ax2.axhline(0, color="k", linewidth=1)
    ax2.plot([c for _, _, _, c, _, _ in tab_bis[:6]], [fc for _, _, _, _, fc, _ in tab_bis[:6]],
             "go", label="tebakan biseksi")
    ax2.plot([c for _, _, _, c, _, _ in tab_rf[:6]], [fc for _, _, _, _, fc, _ in tab_rf[:6]],
             "m^", label="tebakan regula-falsi")
    ax2.plot(r, 0, "ro", label="akar")
    ax2.set_title("Zoom pada selang awal")
    ax2.set_xlabel("r (cm)")
    ax2.set_ylabel("f(r)")
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.savefig("grafik_kasus3.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    main()
