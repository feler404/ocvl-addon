polylines
=========

.. image:: http://kube.pl/wp-content/uploads/2018/03/polylines_01.png

Funkcja
-------

Rysuje dowolną liczbę krzywych wieloboków.

Atrybuty wejściowe
-------------------

- image_in – obraz wejściowy
- pts_in - tablica krzywych wielobocznych
- thickness_in - grubość linii
- shift_in - liczba bitów promienia, które mają być traktowane jako ułamkowe
- color_in - kolor rysowanej linii
    - R - czerwony kanał
    - G - zielony kanał
    - B - niebieski kanał
    - A - alpha kanał

.. note:: Przykładowy efekt działania prezentowanego węzła można uzyskać, wprowadzając do wejścia pts_in, za pomocą dodatkowego węzła Custominput, następujące dane określające punkty wielokąta: pts = np.array ([[[15,50], [30,20], [60,20], [75,50], [45,75]]]). 

Atrybuty wyjściowe
------------------

- image_out – obraz wyjściowy

Atrybuty wewnętrzne
-------------------

- lineType_in – spójność, typ segmentów linii (LINE_4, LINE_8, LINE_AA)
- isClosed_in - flaga określająca zamknięcie lub otwarcie łamanej. Jeśli argument jest zaznaczony, funkcja narysuje odcinek łączący ostatni element z pierwszym, w przeciwnym przypadku kontur będzie otwarty.

Przykłady zastosowania
----------------------
.. image:: http://kube.pl/wp-content/uploads/2018/03/polylines_11.png
