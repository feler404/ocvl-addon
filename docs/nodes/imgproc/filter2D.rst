filter2D
========

.. image:: http://kube.pl/wp-content/uploads/2018/03/filter2D_01.png

Funkcja
-------

Konwergacja obrazu z jądrem.

Atrybuty wejściowe
------------------

- image_in – obraz wejściowy
- kernel_size – jądro korelacji
- anchor – punkt zakotwiczenia, wartość domyślna ustawiona na (-1,-1) oznacza, że punkt zakotwiczenia znajduje się w centrum jądra
- delta – opcjonalna wartość dodana do filtrowanych pikseli przed przypisaniem

Atrybuty wyjściowe
------------------

- image_out – obraz wyjściowy

Atrybuty wewnętrzne
-------------------

- ddepth – głębia wyniku (CV_8, CV_16)
- borderType_in – tryb graniczny używany do eksploratacji pikseli poza obrazem (BORDER_REFLECT, BORDER_ISOLATED, BORDER_DEFAULT, BORDER_TRANSPARENT, BORDER_REFLECT_101, BORDER_WRAP, BORDER_REPLICATE, BORDER_CONSTANT)

Przykłady zastosowania
----------------------

.. image:: http://kube.pl/wp-content/uploads/2018/03/filter2D_11.png
