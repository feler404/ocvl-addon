**********
Instalacja
**********

Instalacja z pakietu binarnego
==============================

Jeśli program instalowany jest z pakietu binarnego, wszystkie zależności są już zawerte w tym pakiecie.
Jeśli więc system spełnia minimalne wymagania, po instalacji pakietu binarnego program będzie gotowy do pracy.


Instalacja pakietu źródłowego bezpośrednio w Blender-rze
========================================================

W przypadku gdy chcemy zainstalować program z kodu źródłowego, potrzebujemy spełnić kilka warunków wstępnych.

- Blender (https://www.blender.org/download/) - sugerowana wersja 2.49
- opencv-python (https://pypi.python.org/pypi/opencv-python) - sugerowana wersja 3.1.0.1
- pynput - (https://pypi.python.org/pypi/pynput/1.3.10) - sugerowna wersja 1.3.10
- tornado - (https://pypi.python.org/pypi/tornado/5.0.2) - sugerowana wersja 4.5.3
- sverchok addon - (https://github.com/nortikin/sverchok) - sugerowana wersja cae276520184c94b877ffc88e196469086e9f7eb


Instalacja Belnder-a
--------------------
Blender-a można pobrać ze strony programu http://blender.org/ . OCVL działa stabilnie na wersji 2.49 i zalecana jest
instalacja wej wersji Blender-a.

Instalacja OpenCV, pynput, tornado
----------------------------------

Do instalacja pakietów `python`-owych najlepiej użyć `pip`-a. Domślnie `Python` znajdujący się w Blender-rze nie zawiera
`Pip`-a i trzeba go zainstalować jako pierwszego.
`Pip`-a można pobrać z: `https://bootstrap.pypa.io/get-pip.py`. Później wystarczy uruchmić skrypt z pozimu Python-a.

W zależności od systemu operacyjnego i wersji Blendera, Python może mieć różną nazwe i miejsce.
Oto przykładowe położenie Python-a w Blender-rze:
`~/Downloads/blender-2.79-macOS-10.6/blender.app/Contents/Resources/2.79/python/bin/python3.5m`
Instalacja Pip-a będzie wyglądać:
`~/Downloads/blender-2.79-macOS-10.6/blender.app/Contents/Resources/2.79/python/bin/python3.5m ./get-pip.py`

Teraz mając Pip-a można instalować pakiety bezpośrednio za jego pośrednictwem. Pip w zależności od systemu może
zainstalować się jako skrypt lub jako modul.

teraz już można instalować pakiety:
    ../python/bin/python3.5m ../python/bin/pip install pynput==1.3.10
    ../python/bin/python3.5m ../python/bin/pip install opencv-python==3.1.0.5
    ../python/bin/python3.5m ../python/bin/pip install tornado==4.5.3


    wget https://github.com/nortikin/sverchok/archive/cae276520184c94b877ffc88e196469086e9f7eb.zip
    cd ~/Downloads/blender-2.79-macOS-10.6/blender.app/Contents/Resources/2.79/scripts/

    unzip ./cae276520184c94b877ffc88e196469086e9f7eb.zip
    mv ./sverchok-cae276520184c94b877ffc88e196469086e9f7eb ./addons/sverchok
    ln -s ~/workspace/tales/ocvl-addon ocvl


Dodanie dodatku OCVL do Blender-a
---------------------------------
Po ściągnięciu OCVL (https://github.com/feler404/ocvl-addon), wystarczy go rozpakować i skompiować do katalogu addons

Uruchomienie Blender-a z dodadkiem
----------------------------------
Aby Blender mógł poprawnie uruchmoć wszsytkie dodatki trzeba go uruchmic przez komende:
`./blender --addons ocvl,sverchok`