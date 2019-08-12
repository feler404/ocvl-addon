import bpy
import uuid
import numpy as np

from ocvl.core.node_base import OCVLNodeBase


NP_VALUE_TYPE_ITEMS = (
    ("intc", "intc", "intc", "", 0),
    ("intp", "intp", "intp", "", 1),
    ("int8", "int8", "int8", "", 2),
    ("int16", "int16", "int16", "", 3),
    ("int32", "int32", "int32", "", 4),
    ("int64", "int64", "int64", "", 5),
    ("uint8", "uint8", "uint8", "", 6),
    ("uint16", "uint16", "uint16", "", 7),
    ("uint32", "uint32", "uint32", "", 8),
    ("uint64", "uint64", "uint64", "", 9),
    ("float16", "float16", "float16", "", 10),
    ("float32", "float32", "float32", "", 11),
    ("float64", "float64", "float64", "", 12),
)


class OCVLTypeConvertNode(OCVLNodeBase):
    ''' Change values of array.
    intc	Identical to C int (normally int32 or int64)
    intp	Integer used for indexing (same as C ssize_t; normally either int32 or int64)
    int8	Byte (-128 to 127)
    int16	Integer (-32768 to 32767)
    int32	Integer (-2147483648 to 2147483647)
    int64	Integer (-9223372036854775808 to 9223372036854775807)
    uint8	Unsigned integer (0 to 255)
    uint16	Unsigned integer (0 to 65535)
    uint32	Unsigned integer (0 to 4294967295)
    uint64	Unsigned integer (0 to 18446744073709551615)
    float16	Half precision float: sign bit, 5 bits exponent, 10 bits mantissa
    float32	Single precision float: sign bit, 8 bits exponent, 23 bits mantissa
    float64	Double precision float: sign bit, 11 bits exponent, 52 bits mantissa
    '''

    n_doc = "Custom Python code input."
    n_requirements = {}

    def update_layout(self, context):
        self.process()

    array_in: bpy.props.StringProperty(name="array_in", default=str(uuid.uuid4()))
    array_out: bpy.props.StringProperty(name="array_out", default=str(uuid.uuid4()))

    value_type_in: bpy.props.EnumProperty(items=NP_VALUE_TYPE_ITEMS, default='float32', update=update_layout, description="Data type.")

    def init(self, context):
        self.inputs.new("OCVLObjectSocket", "array_in")

        self.outputs.new("OCVLObjectSocket", "array_out")

    def wrapped_process(self):
        self.check_input_requirements(["array_in"])

        array_in = self.get_from_props("array_in")
        value_type_in = self.get_from_props("value_type_in")
        if not isinstance(array_in, np.ndarray):
            array_in = np.int0(array_in)

        array_out = array_in.astype(getattr(np, value_type_in))
        self.refresh_output_socket("array_out", array_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "value_type_in")
