adaptiveThreshold
=================

.. image:: http://kube.pl/wp-content/uploads/2018/03/adaptiveThreshold_01.png

Funkcja
-------

Progowanie adaptacyjne - próg obliczany jest dla małych regionów obrazu. Dzięki temu otrzymujemy różne progi dla poszczególnych regionów tego samego obrazu, co daje lepsze wyniki dla obrazów o nierównomiernym oświetleniu. 

Atrybuty wejściowe
------------------

- image_in – obraz wejściowy
- maxValue_in – maksymalna wartość dla operacji górnych
- C_in – stała odejmowana od średniej lub średniej ważonej

Atrybuty wyjściowe
------------------

- image_out – obraz wyjściowy

Atrybuty wewnętrzne
-------------------

- adaptiveMethod_in - metoda progowania adaptacyjnego
    - ADAPTIVE_THRESH_GAUSSIAN_C – piksele w obszarze wokół punktu ważone są według okna gaussowskiego
    - ADAPTIVE_THRESH_MEAN_C – wszystkie piksele w obszarze ważone są jednakowo
- thresholdType_in – typ progowania: THRESH_BINARY, THRESH_BINARY_INV, THRESH_TRUNC, THRESH_TOZERO, THRESH_TOZERO_INV, THRESH_MASK, THRESH_OTSU, THRESH_TRIANGLE
- 3, 5, 7 – rozmiar obszaru pikseli stosowany do obliczenia wartości progowych dla pikseli

Przykłady zastosowania
----------------------

.. image:: http://kube.pl/wp-content/uploads/2018/03/adaptiveThreshold_11.png
.. image:: http://kube.pl/wp-content/uploads/2018/03/adaptiveThreshold_12.png
