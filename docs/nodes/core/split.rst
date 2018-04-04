split
=================
.. image:: http://kube.pl/wp-content/uploads/2018/03/split_1.png

Funkcja
-------

Dzieli tablicę wielokanałową na kilka tablic jednokanałowych. 


Atrybuty wejściowe
------------------

- image_in – obraz wejściowy


Atrybuty wyjściowe
------------------

- layer_0_out – kanał 0
- layer_1_out – kanał 1
- layer_2_out – kanał 2
- layer_3_out – kanał 3 


.. note :: Węzeł działa dynamicznie. Jeśli na wejściu pojawi się obraz BGR to kanały na wyjściu to odpowiednio niebieski, zielony i czerwony. Jeśli na wejściu mamy RGB to kanały na wyjściu są czerwony, zielony, niebieski. 


Przykłady zastosowania
----------------------
.. image:: http://kube.pl/wp-content/uploads/2018/03/split_2.png