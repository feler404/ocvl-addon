# OpenCV Laboratory

Application for rapid prototyping and testing algorithms of computer vision.


[![Documentation Status](https://readthedocs.org/projects/opencv-laboratory/badge/?version=latest)](http://opencv-laboratory.readthedocs.io/en/latest/?badge=latest) [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)


## Specification
The main advantages of the application are: 
convenient and elastic node system, 
quick parameter change using sliders and switches, 
immediate visualization of the result, easy and continuous code execution, 
integrated image preview system and integrated code editor, 
the ability to enter your own code, fast writing/reading including images, codes and description, 
easy tutorials and ready-made templates. 

The application was created on the basis of proven engines: Python, OpenCV, Blender.

## Borrows
Many of ideas and solutions was borrowed from:
- https://github.com/nortikin/sverchok
- https://github.com/JacquesLucke/animation_nodes

## Change Log

### [2.9.2] - 2020-03-01

- add support for native Blender UI rendering on numpy images
- add new nodes: fastNlMeansDenoising, fastNlMeansDenoisingColored, and more...
- add default UI layout for Laboratory view
- add support full options color mode in cvtColor
- fix bug loadfile in SampleImage
- fix memory leak in SampleImage/SampleVideo Nodes
- and more small fixes

### [2.9.0] - 2019-07-15

- add to whole nodes quick_link support
- add mask node
- add support custom kernel node
- add new sockets: OCVLMaskSocket, OCVLRectSocket, OCVLContourSocket, OCVLVectorSocket, MatrixSocket and OCVLStethoscopeSocket
- support opencv-python-headless 4.1.0.25
- support opencv-contrib-python-headless 4.1.0.25
- fix no hidden texture during rolling node.

### [1.2.0] - 2018-03-06

- support Python 3.7
- support Blender 2.8
- support opencv-python-headless 3.4.2.17
- support opencv-contrib-python-headless 3.4.2.17
- binary available for Windows, Linux and OSX


## Shortcut

**Addon for**: [Blender](http://blender.org)  (version *2.80* and above).  
**Current version**: 2.9.2 beta
**License**: [GPL3](http://www.gnu.org/licenses/quick-guide-gplv3.html)   
**Prerequisites**: Python 3.7, `opencv`, `numpy`  
**Docs**: [In English](http://opencv-laboratory.readthedocs.io/) - Documentation   
**Problems** [Issue Tracker](https://github.com/feler404/ocvl-addon/issues) - If you have problem   
**Binaries** [Download](https://www.ocvl.teredo.tech/#download-tab) - Current version for various platforms