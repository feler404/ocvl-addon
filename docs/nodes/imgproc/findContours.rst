findContours
============

.. image:: http://kube.pl/wp-content/uploads/2018/03/findContours_01.png

Funkcja
-------

Znajduje kontury na obrazie binarnym.

Atrybuty wejściowe
-------------------

- image_in – obraz wejściowy
- offset - opcjonalne przesunięcie każdego punktu konturu. Opcja szczególnie przydatna, gdy kontury są wyodrębniane z wybranego regionu obrazu, a następnie powinny być analizowane w całym kontekście obrazu.

Atrybuty wyjściowe
------------------

- image_out – obraz wyjściowy
- contours - wykryte kontury
- hierarchy - opcjonalny wektor wyjściowy, zawierający informacje o topologii obrazu

Atrybuty wewnętrzne
-------------------

- mode - tryb wykrywania konturów:
    - RETR_TREE - pobiera wszystkie kontury i rekonstruuje pełną hierarchię zagnieżdżonych konturów
    - RETR_LIST - wyszukuje wszystkie kontury bez nawiązywania żadnych hierarchicznych relacji
    - RETR_CCOMP - pobiera wszystkie kontury i porządkuje je w zorganizowanej dwupoziomowej hierarchii
    - RETR_EXTERNAL - pobiera tylko skrajne, zewnętrzne kontury
    - RETR_FLOODFILL - pobiera kontury według wypełnienia

- method - metoda aproksymacji:
    - CHAIN_APPROX_SIMPLE - kompresuje poziome, pionowe i skośne segmenty, pozostawiając tylko ich punkty końcowe
    - CHAIN_APPROX_NONE - przekształca wszystkie punkty z kodu konturu na punkty
    - CHAIN_APPROX_TC89_L1 lub CHAIN_APPROX_TC89_KCOS - dotyczy jednej z odmian algorytmu aproksymacji łańcuchowej Teha-China

Przykłady zastosowania
----------------------
.. image:: http://kube.pl/wp-content/uploads/2018/03/findContours_11.png
.. image:: http://kube.pl/wp-content/uploads/2018/03/findContours_12.png
.. image:: http://kube.pl/wp-content/uploads/2018/03/findContours_13.png
.. image:: http://kube.pl/wp-content/uploads/2018/03/findContours_14.png

