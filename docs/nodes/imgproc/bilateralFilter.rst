bilateralFilter
=================

.. image:: http://kube.pl/wp-content/uploads/2018/03/bilateralFilter_01.png

Funkcja
-------

Filtr dwustronny. Redukuje niepożądane szumy zachowując ostre krawędzie. 

Atrybuty wejściowe
------------------

- image_in – obraz wejściowy
- d_in – rozmiar okna wokół piksela
- sigmaColor_in – parametr szerokości dla funkcji wagi koloru
- sigmaSpace_in – parametr szerokości dla funkcji wagi przestrzennej

Atrybuty wyjściowe
------------------

- image_out – obraz wyjściowy

Atrybuty wewnętrzne
-------------------

- borderType_in – tryb graniczny używany do eksploratacji pikseli poza obrazem (BORDER_REFLECT, BORDER_ISOLATED, BORDER_DEFAULT, BORDER_TRANSPARENT, BORDER_REFLECT_101, BORDER_WRAP, BORDER_REPLICATE, BORDER_CONSTANT)

Przykłady zastosowania
----------------------

.. image:: http://kube.pl/wp-content/uploads/2018/03/bilateralFilter_11.png
