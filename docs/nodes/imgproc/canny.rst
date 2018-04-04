canny
=================
.. image:: http://kube.pl/wp-content/uploads/2018/03/canny_1.png

Funkcja
-------

Znajduje krawędzie obrazu za pomocą algorytmu [Canny86].


Atrybuty wejściowe
------------------
- image_in – obraz wejściowy
- threshold1 - pierwszy próg dla procedury histerezy.
- threshold2 - drugi próg dla procedury histerezy.


Atrybuty wyjściowe
------------------
- edges_out – krawędzie na wyjściu

Atrybuty wewnętrzne
-------------------
- L2gradient_in - norma kalkulacji gradientu
- apertureSize_in - wielkość apertury dla operatora Sobel ().


Przykłady zastosowania
----------------------
.. image:: http://kube.pl/wp-content/uploads/2018/03/canny_02.png