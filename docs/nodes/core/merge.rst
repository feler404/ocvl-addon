merge
=================
.. image:: http://kube.pl/wp-content/uploads/2018/03/merge_1.png

Funkcja
-------

Tworzy jedną tablicę wielokanałową z kilku jednokanałowych.


Atrybuty wejściowe
------------------

- layer_0_in – pierwszy kanał Blue
- layer_1_in – drugi kanał Green
- layer_2_in – trzeci kanał Red


Atrybuty wyjściowe
------------------

- image_out – obraz wyjściowy

.. note :: W przykładzie użytwo węzła cvtColor by stworzyć jednokanałową tablicę, obraz w skali szarości. Węzeł merge na wejściu kanału Red tworzy tablicę wielokanałową.


Przykłady zastosowania
----------------------
.. image:: http://kube.pl/wp-content/uploads/2018/03/merge_2.png