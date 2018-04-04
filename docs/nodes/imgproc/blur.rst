blur
====

.. image:: http://kube.pl/wp-content/uploads/2018/03/blur_01.png

Funkcja
-------

Rozmycie obrazu przy pomocy znormalizowanego filtra skrzynkowego.

Atrybuty wejściowe
------------------

- image_in – obraz wejściowy
- ksize_in – obszar rozmycia w odniesieniu do jądra
- anchor_in – punkt zakotwiczenia, wartość domyślna ustawiona na (-1,-1) oznacza, że punkt zakotwiczenia znajduje się w centrum jądra

Atrybuty wyjściowe
------------------

- image_out – obraz wyjściowy

Atrybuty wewnętrzne
-------------------

- borderType_in – tryb graniczny używany do eksploratacji pikseli poza obrazem (BORDER_REFLECT, BORDER_ISOLATED, BORDER_DEFAULT, BORDER_TRANSPARENT, BORDER_REFLECT_101, BORDER_WRAP, BORDER_REPLICATE, BORDER_CONSTANT)

Przykłady zastosowania
----------------------

.. image:: http://kube.pl/wp-content/uploads/2018/03/blur_11.png
