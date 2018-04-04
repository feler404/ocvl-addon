cornerHarris
============

.. image:: http://kube.pl/wp-content/uploads/2018/03/cornerHarris_01.png

Funkcja
-------

Znajduje kluczowe punkty obrazu - rogi Harrisa.

Atrybuty wejściowe
------------------

- image_in – obraz wejściowy
- blockSize_in - obszar wokół danego piksela, który jest uwzględniany w obliczeniach macierzy autokorelacji pochodnych
- ksize_in – rozmiar operatora Sobela
- k_in – czułość (im mniejsza wartość liczby, tym większa czułość algorytmu)

Atrybuty wyjściowe
------------------

- image_out – obraz wyjściowy

Atrybuty wewnętrzne
-------------------

- borderType_in – tryb graniczny używany do eksploratacji pikseli poza obrazem (BORDER_REFLECT, BORDER_ISOLATED, BORDER_DEFAULT, BORDER_TRANSPARENT, BORDER_REFLECT_101, BORDER_WRAP, BORDER_REPLICATE, BORDER_CONSTANT)

Przykłady zastosowania
----------------------

.. image:: http://kube.pl/wp-content/uploads/2018/03/cornerHarris_11.png
