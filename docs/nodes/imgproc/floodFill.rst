floodFill
=========

.. image:: http://kube.pl/wp-content/uploads/2018/03/floodFill_01.png

Funkcja
-------

Wypełnia określony obszar danym kolorem.

Atrybuty wejściowe
------------------

- image_in - obraz wejściowy
- seedPoint_in - początkowy punkt wypełniania
- newVal_in - nowa wartość dla malowanych pikseli
- loDiff_in - maksymalna mniejsza jasność / różnica koloru między aktualnie obserwowanym pikselem a jednym z jego sąsiadów należących do komponentu lub dodawany piksel początkowy do komponentu
- upDiff_in - maksymalna górna jasność / różnica koloru między aktualnie obserwowanym pikselem a jednym z jego sąsiadów należących do komponentu lub dodawany piksel początkowy do komponentu
- flagi operacji - opcje dotyczące wypełnienia
    - flag_fixed_range_in - jeśli jest ustawiony, to piksele są porównywane z oryginalnym punktem zalążkowym, a w przeciwnym przypadku z pikselami sąsiednimi
    - flag_mask_only_in - jeśli jest ustawiony, obraz wejściowy nie zostaje zmodyfikowany; opcja ma sens wyłącznie w wariantach funkcji, które posiadają parametr maski

Atrybuty wyjściowe
------------------

- image_out - obraz wyjściowy
- mask_out - maska wyjściowa
- rect_out - opcjonalny parametr wyjściowy ustawiony przez funkcję na minimalny prostokąt ograniczający dla odmalowanej domeny

Atrybuty wewnętrzne
-------------------

- seedPoint_in - umożliwia wybór dowolnego punktu początkowego na powiększonym obrazie wejściowym

Przykłady zastosowania
----------------------

.. image:: http://kube.pl/wp-content/uploads/2018/03/floodFill_11.png
.. image:: http://kube.pl/wp-content/uploads/2018/03/floodFill_12.png

