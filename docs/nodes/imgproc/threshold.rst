threshold
=========
.. image:: http://kube.pl/wp-content/uploads/2018/04/threshold_1.png

Functionality
-------------
Applies a fixed-level threshold to each array element.


Inputs
------
- image_in – Input array (single-channel, 8-bit or 32-bit floating point).
- maxval_in – Maximum value to use with the THRESH_BINARY and THRESH_BINARY_INV thresholding types
- thresh_in – Threshold value.
- type_in – Thresholding type (see the cv::ThresholdTypes).


Outputs
-------
- mask_out – Output mask.
- thresh_out – Threshold value output.


Locals
------
- loc_invert – Invert output mask.


Examples
--------
.. image:: http://kube.pl/wp-content/uploads/2018/04/threshold_2.png

