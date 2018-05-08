import textwrap

import cv2
import os
import uuid
import bpy
from logging import getLogger
from bpy.props import BoolProperty, StringProperty

from ...nodes.laboratory.ta_docs import draw_docs_buttons
from ...tutorial_engine.settings import TUTORIAL_PATH
from ...tutorial_engine.engine_app import NodeCommandHandler
from ...utils import cv_register_class, cv_unregister_class, OCVLPreviewNode, updateNode

logger = getLogger(__name__)

full_tutorial_path = os.path.abspath(os.path.join(TUTORIAL_PATH, "arithmetic_operations_on_images/arithmetic_operations_on_images.html"))


TEXT_STEP_1 = "Step 1 - add image sample node"
TEXT_STEP_2 = "Step 2 - add image viewer node"
TEXT_STEP_3 = "Step 3 - link sample with viewer"
TEXT_STEP_4 = "Step 4 - add blur node"
TEXT_STEP_5 = "Step 5 - put blur node between sample and viewer"
TEXT_STEP_6 = "Step 6 - ste blur ksize value to 10, 10"
TEXT_STEP_7 = "Step 7 - add another image sample node"
TEXT_STEP_8 = "Step 8 - change sample image node mode"
TEXT_STEP_9 = "Step 9 - select file for image sample"
TEXT_STEP_10 = "Step 10 - add addWeighted node"
TEXT_STEP_11 = "Step 11 - connect first input addWeighted"
TEXT_STEP_12 = "Step 12 - connect second input addWeighted"
TEXT_STEP_13 = "Step 13 - connect output addWeighted to viewer"
TEXT_STEP_14 = "Step 14 - show image in image mode"





TIP_STEP_1 = "If you press SPACE BAR, search menu shows"
TIP_STEP_2 = "If you press SPACE BAR, search menu shows"
TIP_STEP_3 = "Grab green spot by side image_out and drag to green spot image_in"
TIP_STEP_4 = "If you press SPACE BAR, search menu shows"
TIP_STEP_5 = "Put blur node on link, link should be lighten"
TIP_STEP_6 = "Click in blur node to number box by side ksize_in ant type 10, after click TAB and type 10 again"
TIP_STEP_7 = "TIP_STEP_7"
TIP_STEP_8 = "TIP_STEP_8"
TIP_STEP_9 = "TIP_STEP_9"
TIP_STEP_10 = "TIP_STEP_10"
TIP_STEP_11 = "TIP_STEP_11"
TIP_STEP_12 = "TIP_STEP_12"
TIP_STEP_13 = "TIP_STEP_13"
TIP_STEP_14 = "Finish!"


def show_long_tip(tip, col):
    for i, chank in enumerate(textwrap.wrap(tip, 50)):
        if i == 0:
            icon = "INFO"
        else:
            icon = "SMALL_TRI_RIGHT_VEC"
        col.label(text=chank, icon=icon)


class TutorialFirstStep:


    def __init__(self, layout, col, node):
        self.layout = layout
        self.col = col
        self.node = node

    def start(self):
        return self.step_1()

    def step_1(self):
        nt = NodeCommandHandler.get_or_create_node_tree()

        if nt.nodes.get('ImageSample'):
            self.col.label(text=TEXT_STEP_1, icon="FILE_TICK")
            return self.step_2()
        else:
            self.col.operator('node.tutorial_mode_command', text=TEXT_STEP_1, icon='NODETREE').loc_command = ' imagesample!'
            show_long_tip(TIP_STEP_1, self.col)

    def step_2(self):
        nt = NodeCommandHandler.get_or_create_node_tree()
        if nt.nodes.get('ImageViewer'):
            self.col.label(text=TEXT_STEP_2, icon="FILE_TICK")
            return self.step_3()
        else:
            self.col.operator('node.tutorial_mode_command', text=TEXT_STEP_2, icon='NODETREE').loc_command = ' imageviewer!'
            show_long_tip(TIP_STEP_2, self.col)

    def step_3(self):
        nt = NodeCommandHandler.get_or_create_node_tree()
        img_sample = nt.nodes.get('ImageSample')
        img_viewer = nt.nodes.get('ImageViewer')
        if img_sample.outputs['image_out'].is_linked and img_viewer.inputs['image_in'].is_linked:
            self.col.label(text=TEXT_STEP_3, icon="FILE_TICK")
            return self.step_4()
        else:
            self.col.operator('node.tutorial_mode_command', text=TEXT_STEP_3,icon='NODETREE').loc_command = 'connect_sample_and_view'
            show_long_tip(TIP_STEP_3, self.col)

    def step_4(self):
        nt = NodeCommandHandler.get_or_create_node_tree()
        if nt.nodes.get('blur'):
            self.col.label(text=TEXT_STEP_4, icon="FILE_TICK")
            return self.step_5()
        else:
            self.col.operator('node.tutorial_mode_command', text=TEXT_STEP_4, icon='NODETREE').loc_command = ' blur!'
            show_long_tip(TIP_STEP_4, self.col)

    def step_5(self):
        nt = NodeCommandHandler.get_or_create_node_tree()
        img_sample = nt.nodes.get('ImageSample')
        img_viewer = nt.nodes.get('ImageViewer')
        blur = nt.nodes.get('blur')
        if blur and (img_sample.outputs['image_out'].is_linked and img_viewer.inputs['image_in'].is_linked and
                blur.inputs['image_in'].is_linked and blur.outputs['image_out'].is_linked):
            self.col.label(text=TEXT_STEP_5, icon="FILE_TICK")
            return self.step_6()
        else:
            self.col.operator('node.tutorial_mode_command', text=TEXT_STEP_5,icon='NODETREE').loc_command = 'connect_sample_and_view_and_blur'
            show_long_tip(TIP_STEP_5, self.col)

    def step_6(self):
        nt = NodeCommandHandler.get_or_create_node_tree()
        blur = nt.nodes.get('blur')

        if blur.ksize_in[0] == 10 and blur.ksize_in[1] == 10:
            self.col.label(text=TEXT_STEP_6, icon="FILE_TICK")
            return self.step_7()
        else:
            self.col.operator('node.tutorial_mode_command', text=TEXT_STEP_6, icon='NODETREE').loc_command = 'set_ksize_on_blur'
            show_long_tip(TIP_STEP_6, self.col)

    def step_7(self):
        nt = NodeCommandHandler.get_or_create_node_tree()

        if nt.nodes.get('ImageSample.001'):
            self.col.label(text=TEXT_STEP_7, icon="FILE_TICK")
            return self.step_8()
        else:
            self.col.operator('node.tutorial_mode_command', text=TEXT_STEP_7, icon='NODETREE').loc_command = ' imagesample!'
            show_long_tip(TIP_STEP_7, self.col)

    def step_8(self):
        nt = NodeCommandHandler.get_or_create_node_tree()
        image_sample = nt.nodes.get('ImageSample.001')
        if image_sample and image_sample.loc_image_mode == "FILE":
            self.col.label(text=TEXT_STEP_8, icon="FILE_TICK")
            return self.step_9()
        else:
            self.col.operator('node.tutorial_mode_command', text=TEXT_STEP_8, icon='NODETREE').loc_command = 'file_mode_for_image_sample'
            show_long_tip(TIP_STEP_8, self.col)

    def step_9(self):
        nt = NodeCommandHandler.get_or_create_node_tree()
        image_sample = nt.nodes.get('ImageSample.001')
        if image_sample and image_sample.loc_image_mode == "FILE" and image_sample.loc_filepath != "" :
            self.col.label(text=TEXT_STEP_9, icon="FILE_TICK")
            return self.step_10()
        else:
            self.col.operator('node.tutorial_mode_command', text=TEXT_STEP_9, icon='NODETREE').loc_command = 'select_file_for_sample'
            show_long_tip(TIP_STEP_9, self.col)

    def step_10(self):
        nt = NodeCommandHandler.get_or_create_node_tree()
        add_weighted = nt.nodes.get('addWeighted')
        if add_weighted:
            self.col.label(text=TEXT_STEP_10, icon="FILE_TICK")
            return self.step_11()
        else:
            self.col.operator('node.tutorial_mode_command', text=TEXT_STEP_10, icon='NODETREE').loc_command = ' addweighted!'
            show_long_tip(TIP_STEP_10, self.col)

    def step_11(self):
        nt = NodeCommandHandler.get_or_create_node_tree()
        add_weighted = nt.nodes.get('addWeighted')
        if add_weighted and add_weighted.inputs["image_1_in"].is_linked:
            self.col.label(text=TEXT_STEP_11, icon="FILE_TICK")
            return self.step_12()
        else:
            self.col.operator('node.tutorial_mode_command', text=TEXT_STEP_11, icon='NODETREE').loc_command = 'connect_addweighted_first_input'
            show_long_tip(TIP_STEP_11, self.col)

    def step_12(self):
        nt = NodeCommandHandler.get_or_create_node_tree()
        add_weighted = nt.nodes.get('addWeighted')
        if add_weighted and add_weighted.inputs["image_1_in"].is_linked and add_weighted.inputs["image_2_in"].is_linked:
            self.col.label(text=TEXT_STEP_12, icon="FILE_TICK")
            return self.step_13()
        else:
            self.col.operator('node.tutorial_mode_command', text=TEXT_STEP_12, icon='NODETREE').loc_command = 'connect_addweighted_second_input'
            show_long_tip(TIP_STEP_12, self.col)

    def step_13(self):
        nt = NodeCommandHandler.get_or_create_node_tree()
        add_weighted = nt.nodes.get('addWeighted')
        if add_weighted and add_weighted.inputs["image_1_in"].is_linked and add_weighted.inputs["image_2_in"].is_linked and add_weighted.outputs["image_out"].is_linked:
            self.col.label(text=TEXT_STEP_13, icon="FILE_TICK")
            return self.step_14()
        else:
            self.col.operator('node.tutorial_mode_command', text=TEXT_STEP_13, icon='NODETREE').loc_command = 'connect_addweighted_output'
            show_long_tip(TIP_STEP_13, self.col)

    def step_14(self):
        self.col.label(text=TEXT_STEP_14, icon="FILE_TICK")
        self.col.operator('image.image_full_screen', text="Show image on full screen", icon="FULLSCREEN").origin = "TutorialNodeTree|><|ImageViewer"
        self.col.operator('node.clean_desk', text="Start with blank desk - Community version", icon='RESTRICT_VIEW_OFF')
        show_long_tip(TIP_STEP_14, self.col)
        return True


class OCVLFirstStepsNode(OCVLPreviewNode):
    origin = StringProperty("")
    docs = BoolProperty(default=False)

    def sv_init(self, context):
        self.width = 340
        # self.outputs.new("StringsSocket", "docs")

    def wrapped_process(self):
        pass

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)

        tutorial = TutorialFirstStep(layout=layout, col=col, node=self)
        finish = tutorial.start()
        if finish is True:
            col = layout.column(align=True)
            row = col.row(align=True)
            row.prop(self, "docs", expand=True,  text="More tutorials")
        if self.docs:
            draw_docs_buttons(col, layout, self)


def register():
    cv_register_class(OCVLFirstStepsNode)


def unregister():
    cv_unregister_class(OCVLFirstStepsNode)
