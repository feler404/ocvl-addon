cvtColor
========

.. image:: http://kube.pl/wp-content/uploads/2018/03/cvtColor_01.png

Funkcja
-------

Konwertuje obraz z jednej przestrzeni kolorów (liczby kanałów) na inną przy zachowaniu tego samego typu danych.

Atrybuty wejściowe
------------------

- image_in – obraz wejściowy
- code – kod konwersji przestrzeni kolorów 
    - COLOR_BGR2RGB – transformacja z przestrzeni kolorów BGR na RGB 
    - COLOR_BGR2GREY – transformacja z przestrzeni kolorów BGR do skali szarości
- dstCn – liczba kanałów w docelowym obrazie

Atrybuty wyjściowe
------------------

- image_out – obraz wyjściowy

Przykłady zastosowania
----------------------

.. image:: http://kube.pl/wp-content/uploads/2018/03/cvtColor_11.png
.. image:: http://kube.pl/wp-content/uploads/2018/03/cvtColor_12.png
