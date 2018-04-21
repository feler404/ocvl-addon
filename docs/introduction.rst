*****
Wstęp
*****

Wstęp do OpenCV
===============

OpenCV (Open Source Computer Vision Library http://opencv.org) jest otwartą biblioteką zawierającą kilkaste algorytmów
komputerowego widzenia na licencji BSD. Biblioteka OpenCV jest podzielna na moduły i ten podział jest też
odzwierciedlony OpenCV Laboratory.

- `core` - zwarty moduł definijący podstawowe struktury danych i zawierające podstawowe funkcje używane w reszcie modułów
- `imgproc` - moduł przetważania obrazu, zawiera funkcje: liniowego i nieliniowego filtrowania, transformacji, zmiany
    rozmiaru, zmiany przestrzeniu barw, operacji na histogramach itp.
- `video` - moduł do analizy wideo, zawiera między innymi funkcje: szacowanie ruchu, usówanie tła i śledzenia obiektów
- `calib3d` - podstawowe algorytmy do obliczania geometri wielu obrazów, kalibracji pojendynczej i podwójenj kamery,
    szacowania pozycji obrazu, algorytm korespondecji stero i funkcje rekonstrukcji 3D
- `features2d` - istotne detektory cech, deskryptory i dopasowujące deskryptory
- `objdetect` - detekcja obiektów i instancji predefiniowanych klas (np.: twarzy, oczu, kubków, ludzi, samochodów, itd.)
- ...

Wstęp do Blender-a
==================
Blender to darmowy i open source pakiet do tworzenia 3D. Obsługuje on całe modelowanie rurociągów 3D, takielunek,
animację, symulację, rendering, komponowanie i śledzenie ruchu, a nawet edycję wideo i tworzenie gier. Zaawansowani
użytkownicy wykorzystują interfejs API Blendera do obsługi skryptów w języku Python w celu dostosowania aplikacji i
pisania specjalistycznych narzędzi; często są one zawarte w przyszłych wydaniach Blendera. Blender jest dobrze
dopasowany do osób i małych studiów, które korzystają z jednolitego systemu i elastycznego procesu rozwoju. Przykłady
z wielu projektów opartych na Blenderze są dostępne w formie prezentacji.

Na potrzeby OpenCV Laboratory wykorzystywany jest przedewszystkim system węzłów Blender-a co jest bazą aplikacji.

Wstep do OpenCV Laboratory
==========================
Laboratorium jest szeregiem preinstalowanych bibliotek Python-a i zastawem rozszerzeń Blender-a. Na tej bazie
zaimplementowany został zestaw funkcji OpneCV w formie wygodnych do łączenia węzłów, w których mamy szybki i wygodny
dostęp do wszystkich parametrów funkcji a ponad to natychmiastowy podgląd wyniku działania tych funkcji. Laboratorium
oprócz podstawowych węzłów odpowiedników biblioteki pasiada również bardzo ważne węzły wejścia/wyjścia. Do tej puli
węzłów należą: Image Sampler, Image Viewer, ROI, Custom Input, Custom I/O, Stetoskop, TypeConvert.

Image Sampler
-------------
Węzeł, którego zadaniem jest wygenerowanie/wczytanie obrazu do dalszej obróbki

Image Viewer
------------
Ten węzeł służy do poglądu obrazu. Posiada on wbudowane dwa tryby. Domyślne tryb miniatury, gdzie obraz jest wyświetlany
w samym węźle, i tryb podglądu, gdzie na pełnym ekranie mamy dostęp do wszsytkich szczegułów obrazu, wraz z możliwością
przybliżania czy podglądania piksel po pikselu.

ROI
---
Za pomocą tego węzła możemy wygodnie przyciąć obraz i wybrać interesujący mas fragment.

Custom Input
------------
Ten węzeł ma możliwość wygenerowania/pobrania danych z dowolnych źródeł na bazie kodu Python-a.

Custom I/O
----------
Ten wezeł może przyjąc dowolne dane z innych wezłów i obrabiać je z poziomu kodu Python-a.

Sthetoskop
----------
Jest to wezeł zaczerpnięty z biblioteki Sverchok. Słożący do podglądu danych w formie liczbowej.

TypeConvert
-----------
Za pomocą tego węzła możemy szybko zmieniać typ danych(uint8, float32, float64, itp.) z jakich skłąda się obraz.