drawContours
============

.. image:: http://kube.pl/wp-content/uploads/2018/03/drawContours_01.png

Funkcja
-------

Rysuje kontury lub wypełnione kontury.

Atrybuty wejściowe
-------------------

- image_in – obraz wejściowy
- contours - kontury wejściowe
- hierarchy - opcjonalny wektor wejsciowy, zawierający informacje o topologii obrazu
- contourldx - kontur do narysowania. Jeśli parametr jest ujemny, wszystkie kontury są rysowane.
- color - kolor konturów:
    - R - czerwony kanał
    - G - zielony kanał
    - B - niebieski kanał
    - A - alpha kanał
- thickness_in - grubość linii konturów
- maxLevel - maksymalna głębokość hierarchii
- offset - opcjonalne przesunięcie wszystkich punktów

Atrybuty wyjściowe
------------------

- image_out – obraz wyjściowy

Atrybuty wewnętrzne
-------------------

- lineType_in – spójność, typ segmentów linii (LINE_4, LINE_8, LINE_AA)

Przykłady zastosowania
----------------------

.. image:: http://kube.pl/wp-content/uploads/2018/03/drawContours_11.png
