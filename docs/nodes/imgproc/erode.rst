erode
=================
.. image:: http://kube.pl/wp-content/uploads/2018/03/erode_1.png

Funkcja
-------

Eroduje obraz za pomocą określonego elementu strukturyzacji. 


Atrybuty wejściowe
------------------

- image_in – obraz wejściowy
- ksize_in – obszar erozji w odniesieniu do jądra
- anchor_in – punkt zakotwiczenia, wartość domyślna ustawiona na (-1,-1) oznacza, że punkt zakotwiczenia znajduje się w centrum jądra
- iterations_in – ile razy erozja jest zastosowana


Atrybuty wyjściowe
------------------

- image_out – obraz wyjściowy

Atrybuty wewnętrzne
-------------------

- borderType_in –  metoda ekstrapolacji pikseli (wybrane tryby: BORDER_REFLECT, BORDER_ISOLATED, BORDER_DEFAULT, BORDER_TRANSPARENT, BORDER_REFLECT_101, BORDER_WRAP, BORDER_REPLICATE, BORDER_CONSTANT)


Przykłady zastosowania
----------------------
.. image:: http://kube.pl/wp-content/uploads/2018/03/erode_2.png