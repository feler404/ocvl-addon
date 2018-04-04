ellipse
=======

.. image:: http://kube.pl/wp-content/uploads/2018/03/ellipse_01.png

Funkcja
-------

Węzeł pozwalający tworzyć łuk eliptyczny, elipsę lub wycinek koła.

Atrybuty wejściowe
------------------

- image_in - obraz wejściowy na którym rysowany jest obiekt
- color_in - kolor rysowanej linii
- thickness_in - grubość linii (wartość -1 pozwala otrzymać wypełnienie narysowanego obiektu)
- center_in - środek elipsy
- axes_in - połowa rozmiaru głównych osi elipsy
- angle_in - kąt obrotu elipsy w stopniach
- startAngle_in - kąt początkowy łuku eliptycznego w stopniach
- endAngle_in - kąt końcowy łuku eliptycznego w stopniach
- box_in - rysowana elipsa wpisana jest w granice obróconego prostokąta  

Atrybuty wyjściowe
------------------

- image_out - obraz wyjściowy

Atrybuty wewnętrzne
-------------------

- lineType_in - spójność, typ segmentów linii (LINE_4, LINE_8, LINE_AA)
- tryb pracy węzła
    - FULL - domyślny tryb tworzenia elipsy
    - SIMPLE - tworzenie elipsy wpisanej w granice obróconego prostokąta

Przykłady zastosowania
----------------------

.. image:: http://kube.pl/wp-content/uploads/2018/03/ellipse_11.png
.. image:: http://kube.pl/wp-content/uploads/2018/03/ellipse_12.png
.. image:: http://kube.pl/wp-content/uploads/2018/03/ellipse_13.png
