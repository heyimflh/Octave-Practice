# Program Penyelesaian Persamaan Diferensial Biasa (PDB) – Metode Numerik

Program Python modular dan komprehensif untuk menyelesaikan masalah nilai awal Persamaan Diferensial Biasa (PDB) orde-1 menggunakan metode analitik (eksak) serta tiga metode numerik: **Metode Euler**, **Metode Heun (Runge-Kutta Orde-2)**, dan **Metode Runge-Kutta Orde-4 (RK4)**.

Program ini dibuat untuk memenuhi **Tugas Praktikum Metode Numerik** (Universitas Sebelas Maret).

---

## 1. Masalah Matematika & Soal Tugas

Diberikan Persamaan Diferensial Biasa (PDB):
$$\frac{dy}{dx} = \frac{4x^3 - 2x + 1}{2 + y}, \quad y(0) = 1$$

Tugas:
1. Menentukan nilai **$y(2)$** menggunakan metode:
   - **Analitik (Eksak)**
   - **Euler** ($n = 15$)
   - **Heun** ($n = 15$)
   - **Runge-Kutta Orde-4 (RK4)** ($n = 15$)
2. Menghitung **galat absolut** dan **galat relatif** (serta persentasenya) dari masing-masing pendekatan numerik.

### Catatan Asumsi Istilah Galat
> **Pernyataan Asumsi:** Istilah *"galat abstrak"* pada teks soal tugas diasumsikan sebagai **galat absolut** (*absolute error*, $|y_{\text{eksak}} - y_{\text{aprok}}|$), sesuai dengan konvensi baku literatur metode numerik.

---

## 2. Penurunan Solusi Eksak (Analitik)

PDB merupakan persamaan terpisahkan (*separable ODE*):
$$(2 + y)\,dy = (4x^3 - 2x + 1)\,dx$$

Integralkan kedua ruas:
$$\int (2 + y)\,dy = \int (4x^3 - 2x + 1)\,dx$$
$$2y + \frac{1}{2}y^2 = x^4 - x^2 + x + C$$

Substitusikan kondisi awal $y(0) = 1$:
$$2(1) + \frac{1}{2}(1)^2 = 0 + C \implies C = \frac{5}{2}$$

Kalikan kedua ruas dengan 2 dan susun persamaan kuadrat dalam $y$:
$$y^2 + 4y = 2x^4 - 2x^2 + 2x + 5$$
$$(y + 2)^2 = 2x^4 - 2x^2 + 2x + 9$$
$$y(x) = -2 + \sqrt{2x^4 - 2x^2 + 2x + 9}$$

*(Akar positif dipilih agar memenuhi kondisi awal $y(0) = -2 + \sqrt{9} = 1$)*.

Nilai eksak di $x = 2$:
$$y(2) = -2 + \sqrt{2(16) - 2(4) + 2(2) + 9} = -2 + \sqrt{37} \approx 4.082762530298$$

---

## 3. Struktur Proyek

```text
TugasP10/
├── main.py                     # Entry point CLI program
├── ode/                        # Paket modular solver PDB
│   ├── __init__.py             # Inisialisasi paket ode
│   ├── problem.py              # Definisi fungsi f(x, y), solusi eksak, & validasi
│   ├── methods.py              # Algoritma Euler, Heun, dan RK4
│   ├── errors.py               # Perhitungan galat & pemformatan angka
│   ├── report.py               # Pelaporan terminal & ekspor CSV
│   └── plotting.py             # Visualisasi kurva & galat (Matplotlib)
├── tests/
│   ├── __init__.py
│   └── test_ode.py             # Unit test lengkap (13 test cases)
├── output/                     # Berkas keluaran (dibuat otomatis)
│   ├── ringkasan.csv           # Ringkasan hasil & galat
│   ├── iterasi_euler.csv       # Tabel langkah detail Euler
│   ├── iterasi_heun.csv        # Tabel langkah detail Heun
│   ├── iterasi_rk4.csv         # Tabel langkah detail RK4
│   ├── grafik_perbandingan.png # Visualisasi kurva solusi
│   └── grafik_galat.png        # Visualisasi galat langkah (skala log)
├── requirements.txt            # Dependensi opsional
├── README.md                   # Dokumentasi lengkap
└── PRD.md                      # Product Requirement Document
```

---

## 4. Instalasi dan Persyaratan Sistem

- **Python**: Versi $\ge 3.9$ (diuji pada Python 3.13)
- **Pustaka Wajib**: Pustaka standar bawaan Python (`math`, `argparse`, `csv`, `unittest`, `os`, `sys`). **Tidak membutuhkan instalasi paket tambahan untuk menjalankan solver.**
- **Pustaka Opsional** (untuk grafik visualisasi PNG):
  ```bash
  pip install -r requirements.txt
  ```
  *(Jika `matplotlib` tidak terpasang, program tetap berjalan normal dan melewati pembuatan grafik dengan pesan peringatan).*

---

## 5. Cara Menjalankan Program

### 5.1 Eksekusi Default (Sesuai Soal Tugas)
Jalankan perintah berikut di direktori `TugasP10`:
```bash
python main.py
```
Program akan menghitung $y(2)$ dengan $n = 15$, mencetak tabel iterasi dan ringkasan di terminal, serta mengekspor CSV dan grafik PNG ke folder `output/`.

### 5.2 Menjalankan dengan Argumen Tambahan (CLI)
Program mendukung berbagai opsi argumen:
```bash
# Mengubah jumlah langkah iterasi menjadi 30
python main.py --n 30

# Mengubah presisi tampilan desimal menjadi 10 digit
python main.py --precision 10

# Menentukan titik target integrasi dan kondisi awal yang berbeda
python main.py --x0 0.0 --y0 1.0 --b 3.0 --n 20

# Menjalankan tanpa membuat file grafik gambar
python main.py --no-plot

# Melihat seluruh bantuan argumen CLI
python main.py --help
```

---

## 6. Cara Menjalankan Pengujian (Unit Tests)

Jalankan test suite menggunakan modul `unittest` bawaan Python:
```bash
python -m unittest discover tests
```
Seluruh 13 pengujian mencakup:
- Nilai awal solusi eksak $y(0) = 1$ (T-01)
- Nilai target solusi eksak $y(2) = -2 + \sqrt{37}$ (T-02)
- Evaluasi turunan awal $f(0, 1) = 1/3$ (T-03)
- Nilai satu langkah metode Euler (T-04)
- Kesesuaian hasil aproksimasi dan galat Euler, Heun, RK4 dengan tabel acuan (T-05a, T-05b, T-05c)
- Pola galat: Galat Euler > Galat Heun > Galat RK4 (T-05d)
- Fungsi perhitungan galat absolut, relatif, dan persentase (T-06)
- Integritas panjang iterasi ($n + 1$ titik) dan titik akhir $x_n = 2.0$ tepat (T-07)
- Verifikasi analitik: turunan numerik $y_{\text{eksak}}$ memenuhi PDB (T-08)
- Penanganan input tidak valid ($n \le 0$, $b = x_0$, pembagi nol $y = -2$) (T-09)
- Uji laju konvergensi orde akurasi ($n = 15, 30, 60, 120$)

---

## 7. Contoh Hasil Output Program

Berikut adalah ringkasan hasil keluaran pada kondisi default ($n = 15, h = 2/15$):

### Tabel Ringkasan Hasil Integrasi
```text
============================ TABEL RINGKASAN HASIL y(2.0) ============================
+---------------+--------------------+---------------+---------------+-------------------+
| Metode        | y(2.0) Aproksimasi | Galat Absolut | Galat Relatif | Galat Relatif (%) |
+---------------+--------------------+---------------+---------------+-------------------+
| Eksak         | 4.08276253         | -             | -             | -                 |
| Euler         | 3.87369194         | 0.20907059    | 0.05120812    | 5.1208 %          |
| Heun          | 4.09531155         | 0.01254902    | 0.00307366    | 0.3074 %          |
| Runge-Kutta 4 | 4.08277347         | 1.0944e-05    | 2.6805e-06    | 0.00027 %         |
+---------------+--------------------+---------------+---------------+-------------------+
```

### Analisis Akurasi dan Orde Konvergensi
```text
---------------------------- ANALISIS AKURASI METODE ----------------------------
Urutan metode dari yang paling akurat (galat absolut terkecil ke terbesar):
 1. Runge-Kutta 4  | Galat Absolut = 1.0944e-05   (Orde-4, O(h^4))
 2. Heun           | Galat Absolut = 0.01254902   (Orde-2, O(h^2))
 3. Euler          | Galat Absolut = 0.20907059   (Orde-1, O(h))

Penjelasan Teoretis:
Metode Runge-Kutta Orde-4 (RK4) memiliki akurasi tertinggi karena memiliki galat pemotongan
global berorde O(h^4), disusul oleh Metode Heun dengan orde O(h^2), dan Metode Euler dengan
orde O(h) yang menghasilkan galat terbesar. Hasil perhitungan konsisten sepenuhnya
dengan teori konvergensi metode numerik: Galat RK4 << Galat Heun < Galat Euler.
```

---

## 8. Berkas Keluaran

Semua hasil diekspor secara otomatis ke folder `output/`:
1. `ringkasan.csv`: Berisi tabel ringkasan aproksimasi dan nilai galat seluruh metode.
2. `iterasi_euler.csv`: Riwayat detail iterasi metode Euler ($i = 0 \dots 15$, kolom $x_i, y_i, k_1, y_{\text{eksak}}, \text{galat}$).
3. `iterasi_heun.csv`: Riwayat detail iterasi metode Heun ($i = 0 \dots 15$, kolom $x_i, y_i, k_1, k_2, y_{\text{eksak}}, \text{galat}$).
4. `iterasi_rk4.csv`: Riwayat detail iterasi metode RK4 ($i = 0 \dots 15$, kolom $x_i, y_i, k_1, k_2, k_3, k_4, y_{\text{eksak}}, \text{galat}$).
5. `grafik_perbandingan.png`: Visualisasi kurva solusi eksak vs aproksimasi ketiga metode numerik pada domain $[0, 2]$.
6. `grafik_galat.png`: Visualisasi perbandingan galat absolut tiap langkah dalam skala semi-logaritmik.

