Sobel
============

.. image:: http://kube.pl/wp-content/uploads/2018/03/Sobel_01.png

Funkcja
-------

Oblicza pochodne dowolnie wysokiego rzędu, jak również dla mieszanych pochodnych cząstkowych.

Atrybuty wejściowe
-------------------

- image_in – obraz wejściowy
- dx_in - rząd odpowiedniej pochodnej dla X
- dy_in - rząd odpowiedniej pochodnej dla Y
- ksize_in - rozmiar przedłużonego jądra Sobela ; musi to być 1, 3, 5 lub 7
- scale_in - opcjonalny współczynnik skali dla wyliczonych wartości pochodnych; domyślnie nie stosuje się skalowania
- delta_in - opcjonalna wartość przesunięcia dodawana do wyników przed przypisaniem

Atrybuty wyjściowe
------------------

- image_out – obraz wyjściowy

Atrybuty wewnętrzne
-------------------
- borderType_in – tryb graniczny używany do eksploratacji pikseli poza obrazem (BORDER_REFLECT, BORDER_ISOLATED, BORDER_DEFAULT, BORDER_TRANSPARENT, BORDER_REFLECT_101, BORDER_WRAP, BORDER_REPLICATE, BORDER_CONSTANT)
- ddepth_in - głębia pikseli wyniku (CV_8U, CV_16U)

Przykłady zastosowania
----------------------
.. image:: http://kube.pl/wp-content/uploads/2018/03/Sobel_11.png
.. image:: http://kube.pl/wp-content/uploads/2018/03/Sobel_12.png
.. image:: http://kube.pl/wp-content/uploads/2018/03/Sobel_13.png
.. image:: http://kube.pl/wp-content/uploads/2018/03/Sobel_14.png
