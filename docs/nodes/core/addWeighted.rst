AddWeighted
=================
.. image:: http://kube.pl/wp-content/uploads/2018/03/AddWeighted_1.png

Funkcja
-------

Oblicza ważoną sumę dwóch tablic.


Atrybuty wejściowe
------------------
- image_in_1 – obraz wejściowy pierwszy
- image_in_2 - obraz wejściowy drugi
- alpha - waga elementów pierwszej tablicy
- beta - waga elementów drugiej tablicy
- gamma - skalar dodany do każdej sumy

Atrybuty wyjściowe
------------------
- image_out – obraz wyjściowy

Atrybuty wewnętrzne
-------------------
- automatyczne dopasowanie rozmiaru obrazu

 - OFF - brak
 - FIRST - zmienia rozmiar względem pierwszego obrazu
 - SECOND - zmienia rozmiar względem drugiego rozmiaru

- pożądana głębia koloru

 - CV_8U - kolor 8 bitowy
 - CV_16U - kolor 16 bitowy

Przykłady zastosowania
----------------------
.. image:: http://kube.pl/wp-content/uploads/2018/03/AddWeighted_2.png