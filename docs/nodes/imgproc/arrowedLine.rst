arrowedLine
===========

.. image:: http://kube.pl/wp-content/uploads/2018/03/arrowedLine_01.png

Funkcja
-------

Rysuje segment strzałki wskazujący punkt od pierwszego do drugiego.

Atrybuty wejściowe
------------------

- image_in - obraz wejściowy na którym rysowana jest strzałka
- pt1_in - Punkt z którego strzałka się zaczyna
- pt2_in - punkt w którym strzałka wskazuje
- thickness_in - grubość linii 
- shift_in - liczba bitów ułamkowych we współrzędnych środka i wartości promienia
- color_in - kolor rysowanej strzałki


Atrybuty wyjściowe
------------------

- image_out - obraz wyjściowy

Atrybuty wewnętrzne
-------------------

- lineType_in - spójność, typ segmentów linii (LINE_4, LINE_8, LINE_AA)
- pt1_in, pt2_in - narzędzie wskazywania kursorem punktów pt1, pt2


Przykłady zastosowania
----------------------

.. image:: http://kube.pl/wp-content/uploads/2018/03/arrowedLine_02.png
