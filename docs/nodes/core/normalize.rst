normalize
=========
.. image:: http://kube.pl/wp-content/uploads/2018/03/normalize_01.png

Funkcja
-------

Normalizuje normę lub zakres wartości tablicy.


Atrybuty wejściowe
------------------

- image_in - obraz wejściowy
- alpha_in - wartość normy w celu normalizacji lub dolny zakres granicy w przypadku normalizacji zakresu
- beta_in - górna granica zakresu w przypadku normalizacji zakresu; nie służy do normalizacji norm


Atrybuty wyjściowe
------------------

- image_out – obraz wyjściowy

Atrybuty wewnętrzne
-------------------

- norm_type_in - typ normalizacji (NORMAL_CLONE, NORMCONV_FILTER, NORM_HAMMING_ NORM_HAMMING2, NORM_INF, NORM_L1, NORM_L2, NORM_L2SQR_NORM_MINMAX, NORM_RELATIVE, NORM_TYPE_MASK)
- kanały i głębia koloru

 - CV_8U
 - CV_16U


Przykłady zastosowania
----------------------
.. image:: http://kube.pl/wp-content/uploads/2018/03/normalize_02.png