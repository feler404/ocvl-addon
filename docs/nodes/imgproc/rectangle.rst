rectangle
=========

.. image:: http://kube.pl/wp-content/uploads/2018/03/rectangle_01.png

Funkcja
-------

Funkcja rysująca. Rysuje prosty, gruby lub wypełniony prawostronny prostokąt.

Atrybuty wejściowe
------------------

- Dla trybu X, Y, W, H

 - image_in - obraz wejściowy na którym rysowany jest obiekt
 - color_in - kolor rysowanej linii prostokąta
 - thickness_in - grubość linii (wartość -1 pozwala otrzymać wypełnienie narysowanego obiektu)
 - shift_in - liczba bitów ułamkowych we współrzędnych środka i wartości promienia
 - x_in - X dla punktu górnego lewego rogu
 - y_in - Y dla punktu górnego lewego rogu
 - w_in - waga prostokąta
 - h_in - wysokość prostokąta

- Dla trybu PT1, PT2

 - image_in - obraz wejściowy na którym rysowany jest obiekt
 - color_in - kolor rysowanej linii prostokąta
 - thickness_in - grubość linii (wartość -1 pozwala otrzymać wypełnienie narysowanego obiektu)
 - shift_in - liczba bitów ułamkowych we współrzędnych środka i wartości promienia
 - pt1_in - wierzchołek prostokąta
 - pt2_in - wierzchołek prstokąta przeciwnego do punktu pt1

- Dla trybu Rect

 - image_in - obraz wejściowy na którym rysowany jest obiekt
 - color_in - kolor rysowanej linii prostokąta
 - thickness_in - grubość linii (wartość -1 pozwala otrzymać wypełnienie narysowanego obiektu)
 - shift_in - liczba bitów ułamkowych we współrzędnych środka i wartości promienia
 - rect_in - X, Y, waga i wysokość w jednym wektorze


Atrybuty wyjściowe
------------------

- image_out - obraz wyjściowy

Atrybuty wewnętrzne
-------------------

- lineType_in - spójność, typ segmentów linii (LINE_4, LINE_8, LINE_AA)
- tryb pracy węzła
    
 - X, Y, W, H
 - PT1, PT2
 - Rect

Przykłady zastosowania
----------------------

.. image:: http://kube.pl/wp-content/uploads/2018/03/rectangle_02.png
