clc;
clear;
close all;

fprintf('============================================================\n');
fprintf('            TUGAS PRAKTIKUM KE-2 MATLAB/OCTAVE\n');
fprintf('             PENGENALAN MATLAB/OCTAVE 1\n');
fprintf('============================================================\n\n');


%% ============================================================
%  1. VARIABEL
% =============================================================

fprintf('============================================================\n');
fprintf('1. VARIABEL\n');
fprintf('============================================================\n');

a = 15;
b = 6;
c = a + b;

fprintf('Nilai a = %d\n', a);
fprintf('Nilai b = %d\n', b);
fprintf('Hasil c = a + b = %d\n\n', c);


%% ============================================================
%  2. OPERASI ARITMETIKA
%     Penjumlahan, Pengurangan, Perkalian, Pembagian
% =============================================================

fprintf('============================================================\n');
fprintf('2. OPERASI ARITMETIKA\n');
fprintf('============================================================\n');

x = 25;
y = 4;

penjumlahan = x + y;
pengurangan = x - y;
perkalian   = x * y;
pembagian   = x / y;

fprintf('x + y = %d\n', penjumlahan);
fprintf('x - y = %d\n', pengurangan);
fprintf('x * y = %d\n', perkalian);
fprintf('x / y = %.2f\n\n', pembagian);


%% ============================================================
%  3. MODULO
%     mod(a,b)
% =============================================================

fprintf('============================================================\n');
fprintf('3. OPERASI MODULO\n');
fprintf('============================================================\n');

angka1 = 47;
angka2 = 6;

sisa = mod(angka1, angka2);

fprintf('Angka pertama = %d\n', angka1);
fprintf('Angka kedua   = %d\n', angka2);
fprintf('Sisa pembagian = mod(%d,%d) = %d\n\n', ...
        angka1, angka2, sisa);


% Variasi modulo lainnya
fprintf('Variasi modulo:\n');
fprintf('mod(100,7) = %d\n', mod(100,7));
fprintf('mod(85,9)  = %d\n', mod(85,9));
fprintf('mod(144,12) = %d\n\n', mod(144,12));


%% ============================================================
%  4. SHORTHAND OPERATOR
%     += dan *=
% =============================================================

fprintf('============================================================\n');
fprintf('4. SHORTHAND OPERATOR\n');
fprintf('============================================================\n');

shorthand = 10;

fprintf('Nilai awal shorthand = %d\n', shorthand);

shorthand += 7;
fprintf('Setelah shorthand += 7  -> %d\n', shorthand);

shorthand *= 3;
fprintf('Setelah shorthand *= 3  -> %d\n\n', shorthand);


% Variasi -= dan /=
shorthand2 = 100;

fprintf('Nilai awal shorthand2 = %d\n', shorthand2);

shorthand2 -= 25;
fprintf('Setelah shorthand2 -= 25 -> %d\n', shorthand2);

shorthand2 /= 5;
fprintf('Setelah shorthand2 /= 5  -> %d\n\n', shorthand2);


%% ============================================================
%  5. INCREMENT
%     ++x
% =============================================================

fprintf('============================================================\n');
fprintf('5. INCREMENT\n');
fprintf('============================================================\n');

increment = 8;

fprintf('Nilai awal = %d\n', increment);

++increment;
fprintf('Setelah ++increment = %d\n', increment);

++increment;
fprintf('Setelah ++increment = %d\n\n', increment);


%% ============================================================
%  6. DECREMENT
%     x--
% =============================================================

fprintf('============================================================\n');
fprintf('6. DECREMENT\n');
fprintf('============================================================\n');

decrement = 20;

fprintf('Nilai awal = %d\n', decrement);

decrement--;
fprintf('Setelah decrement-- = %d\n', decrement);

decrement--;
fprintf('Setelah decrement-- = %d\n\n', decrement);


%% ============================================================
%  7. ARRAY SATU DIMENSI
% =============================================================

fprintf('============================================================\n');
fprintf('7. ARRAY SATU DIMENSI\n');
fprintf('============================================================\n');

array1 = [5 10 15 20 25];
array2 = [3 6 9 12 15 18 21 24];

disp('Array 1:');
disp(array1);

disp('Array 2:');
disp(array2);


% Array vertikal
array3 = [11;
          22;
          33;
          44;
          55];

disp('Array vertikal:');
disp(array3);


%% ============================================================
%  8. MATRIKS
% =============================================================

fprintf('============================================================\n');
fprintf('8. MATRIKS\n');
fprintf('============================================================\n');

A = [9 8 7 6;
     1 2 3 4;
     5 6 0 1;
     10 11 12 13];

disp('Matriks A:');
disp(A);


% Matriks 2 x 3
B = [2 4 6;
     8 10 12];

disp('Matriks B:');
disp(B);


% Matriks kolom
C = [7;
     14;
     21;
     28];

disp('Matriks C:');
disp(C);


%% ============================================================
%  9. OPERASI / INDEXING MATRIKS
%     A(x,3)
%     A(3,x)
%     A(x,:)
%     A(:,x)
% =============================================================

fprintf('============================================================\n');
fprintf('9. INDEXING DAN OPERASI MATRIKS\n');
fprintf('============================================================\n');

x = [2 3];

disp('Matriks A:');
disp(A);

disp('Index x:');
disp(x);


% A(x,3)
hasil_b = A(x,3);

disp('A(x,3):');
disp(hasil_b);


% A(3,x)
hasil_c = A(3,x);

disp('A(3,x):');
disp(hasil_c);


% A(x,:)
hasil_d = A(x,:);

disp('A(x,:):');
disp(hasil_d);


% A(:,x)
hasil_e = A(:,x);

disp('A(:,x):');
disp(hasil_e);


% Mengambil satu elemen
elemen = A(3,2);

fprintf('Elemen A(3,2) = %d\n\n', elemen);


%% ============================================================
%  10. ZEROS
% =============================================================

fprintf('============================================================\n');
fprintf('10. FUNGSI ZEROS\n');
fprintf('============================================================\n');

F = zeros(4);

disp('zeros(4):');
disp(F);


% zeros dengan ukuran berbeda
F2 = zeros(2,5);

disp('zeros(2,5):');
disp(F2);


% Mengisi sebagian matriks zeros
F(2:3,:) = A(1:2,:);

disp('F setelah F(2:3,:) = A(1:2,:):');
disp(F);


%% ============================================================
%  11. ONES
% =============================================================

fprintf('============================================================\n');
fprintf('11. FUNGSI ONES\n');
fprintf('============================================================\n');

G = ones(3);

disp('ones(3):');
disp(G);


% ones dengan ukuran lain
G2 = ones(2,4);

disp('ones(2,4):');
disp(G2);


% Mengisi sebagian matriks ones
G(2:3,1:2) = A(1:2,3:4);

disp('G setelah G(2:3,1:2) = A(1:2,3:4):');
disp(G);


%% ============================================================
%  12. RAND
% =============================================================

fprintf('============================================================\n');
fprintf('12. FUNGSI RAND\n');
fprintf('============================================================\n');

H = rand(3,4);

disp('Matriks random H:');
disp(H);


% Mengganti sebagian isi matriks random
H(2,:) = A(1,:);

disp('H setelah H(2,:) = A(1,:):');
disp(H);


%% ============================================================
%  13. OPERASI PENJUMLAHAN MATRIKS
% =============================================================

fprintf('============================================================\n');
fprintf('13. PENJUMLAHAN MATRIKS\n');
fprintf('============================================================\n');

M = [1 2 3;
     4 5 6;
     7 8 9];

N = [9 8 7;
     6 5 4;
     3 2 1];

O = M + N;

disp('M =');
disp(M);

disp('N =');
disp(N);

disp('M + N =');
disp(O);


%% ============================================================
%  14. PENGURANGAN MATRIKS
% =============================================================

fprintf('============================================================\n');
fprintf('14. PENGURANGAN MATRIKS\n');
fprintf('============================================================\n');

P = M - N;

disp('M - N =');
disp(P);


%% ============================================================
%  15. PERKALIAN MATRIKS
%     *
% =============================================================

fprintf('============================================================\n');
fprintf('15. PERKALIAN MATRIKS (*)\n');
fprintf('============================================================\n');

X = [1 2 3;
     3 2 1;
     2 1 3];

Y = [4 1 2;
     2 5 3;
     1 3 6];

perkalian_matriks = X * Y;

disp('Matriks X:');
disp(X);

disp('Matriks Y:');
disp(Y);

disp('X * Y:');
disp(perkalian_matriks);


%% ============================================================
%  16. PERKALIAN ELEMEN PER ELEMEN
%     .*
% =============================================================

fprintf('============================================================\n');
fprintf('16. PERKALIAN ELEMEN PER ELEMEN (.*)\n');
fprintf('============================================================\n');

perkalian_elemen = X .* Y;

disp('X .* Y:');
disp(perkalian_elemen);


%% ============================================================
%  17. PANGKAT ELEMEN PER ELEMEN
%     .^
% =============================================================

fprintf('============================================================\n');
fprintf('17. PANGKAT ELEMEN PER ELEMEN (.^)\n');
fprintf('============================================================\n');

Z = [2 3 4;
     5 6 7;
     8 9 10];

pangkat_matriks = Z .^ 2;

disp('Matriks Z:');
disp(Z);

disp('Z .^ 2:');
disp(pangkat_matriks);


%% ============================================================
%  18. DETERMINAN MATRIKS
%     det()
% =============================================================

fprintf('============================================================\n');
fprintf('18. DETERMINAN MATRIKS\n');
fprintf('============================================================\n');

det_X = det(X);

disp('Matriks X:');
disp(X);

fprintf('det(X) = %.2f\n\n', det_X);


%% ============================================================
%  19. INVERS MATRIKS
%     inv()
% =============================================================

fprintf('============================================================\n');
fprintf('19. INVERS MATRIKS\n');
fprintf('============================================================\n');

inv_Y = inv(Y);

disp('Matriks Y:');
disp(Y);

disp('inv(Y):');
disp(inv_Y);


%% ============================================================
%  20. TRANSPOSE MATRIKS
%     A'
% =============================================================

fprintf('============================================================\n');
fprintf('20. TRANSPOSE MATRIKS\n');
fprintf('============================================================\n');

T = [10 20 30;
     40 50 60];

disp('Matriks T:');
disp(T);

transpose_T = T';

disp('Transpose T:');
disp(transpose_T);


% Variasi transpose
transpose_A = A';

disp('Transpose A:');
disp(transpose_A);


%% ============================================================
%  21. COLON OPERATOR
%     1:10
%     1:2:10
%     1:.2:2
% =============================================================

fprintf('============================================================\n');
fprintf('21. COLON OPERATOR (:)\n');
fprintf('============================================================\n');

deret1 = 1:10;

disp('1:10');
disp(deret1);


deret2 = 1:2:10;

disp('1:2:10');
disp(deret2);


deret3 = 1:.2:2;

disp('1:.2:2');
disp(deret3);


% Variasi colon
deret4 = 5:15;

disp('5:15');
disp(deret4);


deret5 = 2:3:20;

disp('2:3:20');
disp(deret5);


deret6 = 0:0.5:5;

disp('0:0.5:5');
disp(deret6);


%% ============================================================
%  22. INPUT
%     input()
% =============================================================

fprintf('============================================================\n');
fprintf('22. INPUT DATA\n');
fprintf('============================================================\n');

nama = input('Masukkan nama mahasiswa: ', 's');
umur = input('Masukkan umur: ');
nilai = input('Masukkan nilai: ');

fprintf('\n');


%% ============================================================
%  23. OUTPUT DENGAN DISP
%     disp()
% =============================================================

fprintf('============================================================\n');
fprintf('23. OUTPUT DENGAN DISP()\n');
fprintf('============================================================\n');

disp('DATA MAHASISWA');

disp('Nama mahasiswa:');
disp(nama);

disp('Umur mahasiswa:');
disp(umur);

disp('Nilai mahasiswa:');
disp(nilai);


%% ============================================================
%  24. OUTPUT DENGAN FPRINTF
%     fprintf()
% =============================================================

fprintf('============================================================\n');
fprintf('24. OUTPUT DENGAN FPRINTF()\n');
fprintf('============================================================\n');

fprintf('Nama  = %s\n', nama);
fprintf('Umur  = %d tahun\n', umur);
fprintf('Nilai = %.2f\n\n', nilai);


%% ============================================================
%  25. IF - ELSE
% =============================================================

fprintf('============================================================\n');
fprintf('25. DECISION IF-ELSE\n');
fprintf('============================================================\n');

if nilai >= 60
    fprintf('Status: LULUS\n');
else
    fprintf('Status: TIDAK LULUS\n');
end

fprintf('\n');


%% ============================================================
%  26. IF - ELSEIF - ELSE
% =============================================================

fprintf('============================================================\n');
fprintf('26. IF - ELSEIF - ELSE\n');
fprintf('============================================================\n');

if nilai >= 85
    grade = 'A';
elseif nilai >= 75
    grade = 'B';
elseif nilai >= 65
    grade = 'C';
elseif nilai >= 50
    grade = 'D';
else
    grade = 'E';
end

fprintf('Grade mahasiswa = %s\n\n', grade);


%% ============================================================
%  27. SWITCH - CASE
% =============================================================

fprintf('============================================================\n');
fprintf('27. DECISION SWITCH-CASE\n');
fprintf('============================================================\n');

fprintf('Pilihan Menu:\n');
fprintf('1. Penjumlahan\n');
fprintf('2. Pengurangan\n');
fprintf('3. Perkalian\n');
fprintf('4. Pembagian\n');

pilihan = input('Masukkan pilihan (1-4): ');

angkaA = input('Masukkan angka pertama: ');
angkaB = input('Masukkan angka kedua: ');

fprintf('\n');

switch pilihan

    case 1
        hasil = angkaA + angkaB;
        fprintf('Anda memilih PENJUMLAHAN\n');
        fprintf('%g + %g = %g\n', angkaA, angkaB, hasil);

    case 2
        hasil = angkaA - angkaB;
        fprintf('Anda memilih PENGURANGAN\n');
        fprintf('%g - %g = %g\n', angkaA, angkaB, hasil);

    case 3
        hasil = angkaA * angkaB;
        fprintf('Anda memilih PERKALIAN\n');
        fprintf('%g * %g = %g\n', angkaA, angkaB, hasil);

    case 4
        if angkaB ~= 0
            hasil = angkaA / angkaB;
            fprintf('Anda memilih PEMBAGIAN\n');
            fprintf('%g / %g = %.2f\n', ...
                    angkaA, angkaB, hasil);
        else
            fprintf('Error: pembagian dengan nol tidak diperbolehkan.\n');
        end

    otherwise
        fprintf('Pilihan tidak tersedia.\n');

end


%% ============================================================
%  28. PROGRAM GABUNGAN OPERASI MATRIKS
% =============================================================

fprintf('\n');
fprintf('============================================================\n');
fprintf('28. RINGKASAN OPERASI MATRIKS\n');
fprintf('============================================================\n');

disp('Matriks X:');
disp(X);

disp('Matriks Y:');
disp(Y);

disp('X + Y:');
disp(X + Y);

disp('X - Y:');
disp(X - Y);

disp('X * Y:');
disp(X * Y);

disp('X .* Y:');
disp(X .* Y);

disp('X .^ 2:');
disp(X .^ 2);

disp('Transpose X:');
disp(X');

fprintf('det(X) = %.2f\n', det(X));

fprintf('inv(Y):\n');
disp(inv(Y));


%% ============================================================
%  29. PROGRAM PERHITUNGAN LUAS DAN KELILING
% =============================================================

fprintf('============================================================\n');
fprintf('29. PERHITUNGAN LUAS DAN KELILING\n');
fprintf('============================================================\n');

panjang = input('Masukkan panjang persegi panjang: ');
lebar = input('Masukkan lebar persegi panjang: ');

luas = panjang * lebar;
keliling = 2 * (panjang + lebar);

fprintf('\n');
fprintf('Panjang  = %.2f\n', panjang);
fprintf('Lebar    = %.2f\n', lebar);
fprintf('Luas     = %.2f\n', luas);
fprintf('Keliling = %.2f\n\n', keliling);


%% ============================================================
%  30. PROGRAM KONVERSI SUHU DENGAN SWITCH
% =============================================================

fprintf('============================================================\n');
fprintf('30. KONVERSI SUHU\n');
fprintf('============================================================\n');

fprintf('1. Celsius -> Fahrenheit\n');
fprintf('2. Fahrenheit -> Celsius\n');
fprintf('3. Celsius -> Kelvin\n');

menu_suhu = input('Pilih menu suhu (1-3): ');
suhu = input('Masukkan suhu: ');

switch menu_suhu

    case 1
        hasil_suhu = (9/5) * suhu + 32;
        fprintf('Hasil = %.2f Fahrenheit\n', hasil_suhu);

    case 2
        hasil_suhu = (5/9) * (suhu - 32);
        fprintf('Hasil = %.2f Celsius\n', hasil_suhu);

    case 3
        hasil_suhu = suhu + 273.15;
        fprintf('Hasil = %.2f Kelvin\n', hasil_suhu);

    otherwise
        fprintf('Pilihan tidak tersedia.\n');

end


%% ============================================================
%  31. PENUTUP
% =============================================================

fprintf('\n');
fprintf('============================================================\n');
fprintf('             SEMUA PERCOBAAN SELESAI\n');
fprintf('============================================================\n');
fprintf('Program telah mempraktikkan materi dasar\n');
fprintf('MATLAB/OCTAVE berdasarkan materi praktikum.\n');
fprintf('============================================================\n');
