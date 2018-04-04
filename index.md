> ### This file is parsed by menu.py
>
> The following strict rules apply to editing this file:
>
> - do not use tabs, anywhere
> - indent the Node's line using 4 spaces
> - use `>` to add a comment, place it at the start of the line.
> - if you aren't sure, follow the existing convention
>
> Failing to follow these points will break the node category parser.
## core
># Data Struct
    ---
    OCVLPointNode
    OCVLPoint3Node
    OCVLRectNode
    OCVLRotatedRectNode
    OCVLKeyPointNode
    OCVLRangeNode
># Operations on arrays
    ---
    OCVLaddWeightedNode
    OCVLconvertScaleAbsNode
    OCVLdctNode
    OCVLdftNode
    OCVLdivideNode
    OCVLexpNode
    OCVLflipNode
    OCVLidctNode
    OCVLgemmNode
    OCVLidftNode
    OCVLinRangeNode
    OCVLinvertNode
    OCVLlogNode
    OCVLLUTNode
    OCVLmagnitudeNode
    OCVLMahalanobisNode
    OCVLmaxNode
    OCVLmeanNode
    OCVLmeanStdDevNode
    OCVLmergeNode
    OCVLminNode
    OCVLminMaxLocNode
    OCVLmixChannelsNode
    OCVLnormalizeNode
    OCVLsplitNode
    OCVLcopyMakeBorderNode
    OCVLeigenNode
    OCVLmulSpectrumsNode
## imgproc
># Filtering
    ---
    OCVLbilateralFilterNode
    OCVLblurNode
    OCVLboxFilterNode
    OCVLdilateNode
    OCVLerodeNode
    OCVLfilter2dNode
    OCVLGaussianBlurNode
    OCVLGetDerivKernelsNode
    OCVLgetGaussianKernelNode
    OCVLmorphologyExNode
    OCVLLaplacianNode
    OCVLpyrDownNode
    OCVLpyrUpNode
    OCVLsepFilter2dNode
    OCVLSobelNode
    OCVLScharrNode
># Geometric Transformations
    ---
    OCVLconvertMapsNode
    OCVLgetAffineTransformNode
    OCVLgetPerspectiveTransformNode
    OCVLgetRectSubPixNode
    OCVLgetRotationMatrix2DNode
    OCVLinvertAffineTransformNode
    OCVLremapNode
    OCVLresizeNode
    OCVLwarpAffineNode
    OCVLwarpPerspectiveNode
    OCVLinitUndistortRectifyMapNode
    OCVLgetDefaultNewCameraMatrixNode
    OCVLundistortNode
    OCVLundistortPointsNode
># Miscellaneous Transformations
    ---
    OCVLadaptiveThresholdNode
    OCVLcvtColorNode
    OCVLdistanceTransformNode
    OCVLfloodFillNode
    OCVLintegralNode
    OCVLintegral2Node
    OCVLintegral3Node
    OCVLthresholdNode
># Drawing
    ---
    OCVLcircleNode
    OCVLclipLineNode
    OCVLellipseNode
    OCVLellipse2PolyNode
    OCVLgetTextSizeNode
    OCVLlineNode
    OCVLarrowedLineNode
    OCVLrectangleNode
    OCVLpolylinesNode
    OCVLdrawContoursNode
    OCVLputTextNode
    OCVLboxPointsNode
># ColorMaps in OpenCV
># Description
># Histograms
    ---
    OCVLequalizeHistNode
># Structural Analysis and Shape Descriptors
    ---
    OCVLmomentsNode
    OCVLfindContoursNode
    OCVLapproxPolyDPNode
    OCVLarcLengthNode
    OCVLboundingRectNode
    OCVLcontourAreaNode
    OCVLconvexHullNode
    OCVLfitEllipseNode
    OCVLfitLineNode
    OCVLisContourConvexNode
    OCVLminAreaRectNode
    OCVLminEnclosingCircleNode
># Motion Analysis and Object Tracking
># Feature Detection
    ---
    OCVLCannyNode
    OCVLcornerHarrisNode
    OCVLHoughLinesNode
    OCVLHoughLinesPNode
    OCVLmatchTemplateNode
## photo
    OCVLinpaintNode
## objdetect
    OCVLCascadeClassifierNode
## video
    OCVLcreateBackgroundSubtractorMOG2Node
## laboratory
    OCVLImageViewerNode
    OCVLImageSampleNode
    OCVLCustomInputNode
    OCVLStethoscopeNode
    OCVLBitwiseNode
    OCVLTestNode
    OCVLROINode
    OCVLTypeConvertNode

>## Number
>    SvNumberNode
>    FloatNode
>    IntegerNode
>    Float2IntNode
>    ScalarMathNode
>    SvScalarMathNodeMK2
>    Formula2Node
>    SvExecNodeMod
>    ---
>    GenListRangeIntNode
>    SvGenFloatRange
>    SvMapRangeNode
>    SvListInputNode
>    SvGenFibonacci
>    SvGenExponential
>    ---
>    SvRndNumGen
>    RandomNode
>    SvEasingNode
>    SvMixNumbersNode
## Alpha Nodes
## Beta Nodes
## List Masks
## List Main
## List Mutators
## Objects
## BPY Data
## Generators Extended
## Generator