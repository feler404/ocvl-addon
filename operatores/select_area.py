import bpy
from bgl import *
from bpy.props import *
from mathutils import Vector

from ocvl.core.drawing_2d import drawLine, drawVerticalLine, drawHorizontalLine, drawPolygon
from ocvl.core.blender_ui import redrawAll, iterAreas, splitAreaVertical, splitAreaHorizontal, getDpiFactor
from ocvl.core.register_utils import ocvl_register, ocvl_unregister


class OCVL_OT_SelectArea(bpy.types.Operator):
    bl_idname = "ocvl.select_area"
    bl_label = "Select Area"
    bl_description = ""
    bl_options = {"REGISTER"}

    bl_image_name: bpy.props.StringProperty(default="")
    bl_text_name: bpy.props.StringProperty(default="")

    def invoke(self, context, event):
        self.registerDrawHandlers()
        self.window = context.window
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def registerDrawHandlers(self):
        self.drawHandlers = []
        for area in iterAreas():
            space = area.spaces.active
            regionTypes = set(region.type for region in area.regions if region.type != "")
            for regionType in regionTypes:
                handler = space.draw_handler_add(self.drawCallback, tuple(), regionType, "POST_PIXEL")
                self.drawHandlers.append((space, handler, regionType))

    def unregisterDrawHandlers(self):
        for space, handler, regionType in self.drawHandlers:
            space.draw_handler_remove(handler, regionType)

    def modal(self, context, event):
        redrawAll()
        self.mousePosition = Vector((event.mouse_x, event.mouse_y))

        if event.type == "LEFTMOUSE":
            area, nearestBorder, factor = self.getSelection()
            if area is None:
                return self.finish()
            elif nearestBorder == "CENTER":
                selectedArea = area
            else:
                try:
                    selectedArea = self.createNewArea(area, nearestBorder, factor)
                except:
                    self.finish()
                    self.report({"INFO"}, "Cannot create new area")
                    return {"CANCELLED"}

            self.finish()
            if self.bl_image_name:
                selectedArea.type = "IMAGE_EDITOR"
                for space in selectedArea.spaces:
                    if space.type == "IMAGE_EDITOR":
                        space.image = bpy.data.images[self.bl_image_name]
            elif self.bl_text_name:
                selectedArea.type = "TEXT_EDITOR"
                for space in selectedArea.spaces:
                    if space.type == "TEXT_EDITOR":
                        space.text = bpy.data.texts[self.bl_text_name]
            return {"FINISHED"}

        if event.type in {"RIGHTMOUSE", "ESC"}:
            return self.finish()

        return {"RUNNING_MODAL"}

    def finish(self):
        self.unregisterDrawHandlers( )
        return {"FINISHED"}


    def createNewArea(self, area, border, factor):
        if border == "LEFT":
            newArea, _ = splitAreaVertical(area, factor)
        elif border == "RIGHT":
            _, newArea = splitAreaVertical(area, factor)
        elif border == "BOTTOM":
            newArea, _ = splitAreaHorizontal(area, factor)
        elif border == "TOP":
            _, newArea = splitAreaHorizontal(area, factor)
        return newArea

    def getSelection(self):
        for area in bpy.context.screen.areas:
            border, factor = calcUserSelectionInArea(area, self.mousePosition)
            if border != "NONE":
                return area, border, factor
        return None, None, None

    def drawCallback(self):
        if not hasattr(self, "mousePosition"):
            return
        if bpy.context.window != self.window:
            return

        area = bpy.context.area
        region = bpy.context.region
        offset = Vector((-region.x + area.x, -region.y + area.y))

        selectedBorder, factor = calcUserSelectionInArea(area, self.mousePosition)
        if selectedBorder != "NONE":
            drawSelection(area, offset.x, offset.y, selectedBorder, factor)

lineThickness = 1
centerRadius = 0.1
lineColor = (0, 0, 0, 0.5)
polyColor = (0.4, 0.4, 0.4, 0.3)

def drawSelection(area, xOffset, yOffset, border, factor):

    # Precalculate Coordinates
    #############################################

    centerWidth = area.width * centerRadius * 2
    centerHeight = area.height * centerRadius * 2

    areaLeft = xOffset
    areaRight = xOffset + area.width
    areaBottom = yOffset
    areaTop = yOffset + area.height

    centerLeft = xOffset + area.width * 0.5 - centerWidth / 2
    centerBottom = yOffset + area.height * 0.5 - centerHeight / 2
    centerRight = xOffset + area.width * 0.5 + centerWidth / 2
    centerTop = yOffset + area.height * 0.5 + centerHeight / 2

    polyLeft = [
        (areaLeft, areaBottom),
        (areaLeft, areaTop),
        (centerLeft, centerTop),
        (centerLeft, centerBottom) ]
    polyRight = [
        (areaRight, areaBottom),
        (centerRight, centerBottom),
        (centerRight, centerTop),
        (areaRight, areaTop) ]
    polyTop = [
        (areaLeft, areaTop),
        (areaRight, areaTop),
        (centerRight, centerTop),
        (centerLeft, centerTop) ]
    polyBottom = [
        (areaLeft, areaBottom),
        (centerLeft, centerBottom),
        (centerRight, centerBottom),
        (areaRight, areaBottom) ]
    polyCenter = [
        (centerLeft, centerBottom),
        (centerLeft, centerTop),
        (centerRight, centerTop),
        (centerRight, centerBottom) ]

    # Draw
    #############################################

    glEnable(GL_LINE_SMOOTH)
    glLineWidth(lineThickness * getDpiFactor())

    # Draw Polygon
    if border == "LEFT":   drawPolygon(polyLeft, polyColor)
    if border == "RIGHT":  drawPolygon(polyRight, polyColor)
    if border == "BOTTOM": drawPolygon(polyBottom, polyColor)
    if border == "TOP":    drawPolygon(polyTop, polyColor)
    if border == "CENTER": drawPolygon(polyCenter, polyColor)

    factorIndicatorX = areaLeft + area.width * factor
    factorIndicatorY = areaBottom + area.height * factor
    if border in ("LEFT", "RIGHT"):
        height = area.height * (0.5 - factor) * 2
        drawVerticalLine(factorIndicatorX, factorIndicatorY, height, color = lineColor)
    if border in ("BOTTOM", "TOP"):
        width = area.width * (0.5 - factor) * 2
        drawHorizontalLine(factorIndicatorX, factorIndicatorY, width, color = lineColor)

    # Draw Center Rectangle
    drawHorizontalLine(centerLeft, centerBottom, centerWidth, color = lineColor)
    drawHorizontalLine(centerLeft, centerTop, centerWidth, color = lineColor)
    drawVerticalLine(centerLeft, centerBottom, centerHeight, color = lineColor)
    drawVerticalLine(centerRight, centerBottom, centerHeight, color = lineColor)

    # Draw Diagonals
    drawLine(areaLeft, areaBottom, centerLeft, centerBottom, color = lineColor)
    drawLine(centerRight, centerTop, areaRight, areaTop, color = lineColor)
    drawLine(areaLeft, areaTop, centerLeft, centerTop, color = lineColor)
    drawLine(centerRight, centerBottom, areaRight, areaBottom, color = lineColor)

    glDisable(GL_LINE_SMOOTH)
    glLineWidth(1)

def calcUserSelectionInArea(area, point):
    if not isPointInArea(area, point):
        return "NONE", 0.0

    xFactor = (point.x - area.x) / area.width
    yFactor = (point.y - area.y) / area.height

    if abs(0.5 - xFactor) < centerRadius  and abs(0.5 - yFactor) < centerRadius:
        return "CENTER", 0.0

    if yFactor > xFactor:
        if 1 - yFactor > xFactor:
            return "LEFT", xFactor
        else:
            return "TOP", yFactor
    else:
        if 1 - yFactor > xFactor:
            return "BOTTOM", yFactor
        else:
            return "RIGHT", xFactor

def isPointInArea(area, point):
    return area.x < point.x < area.x + area.width and area.y < point.y < area.y + area.height


def register():
    ocvl_register(OCVL_OT_SelectArea)


def unregister():
    ocvl_unregister(OCVL_OT_SelectArea)