GaussianBlur
=================
.. image:: http://kube.pl/wp-content/uploads/2018/03/gaussianblur_1.png

Funkcja
-------

Zamazuje obraz za pomocą filtru Gaussa.


Atrybuty wejściowe
------------------
- image_in – obraz wejściowy
- ksize_in - obszar rozmycia w odniesieniu do jądra
- sigmaX_in - Odchylenie standardowe Gaussa w kierunku X.
- sigmaY_in - Odchylenie standardowe Gaussa w kierunku Y.


Atrybuty wyjściowe
------------------
- image_out – obraz wyjściowy

Atrybuty wewnętrzne
-------------------

- borderType_in - tryb graniczny używany do eksploratacji pikseli poza obrazem (BORDER_REFLECT, BORDER_ISOLATED, BORDER_DEFAULT, BORDER_TRANSPARENT, BORDER_REFLECT_101, BORDER_WRAP, BORDER_REPLICATE, BORDER_CONSTANT)


Przykłady zastosowania
----------------------
.. image:: http://kube.pl/wp-content/uploads/2018/03/gaussianblur_2.png