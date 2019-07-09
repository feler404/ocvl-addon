

def filter_areas(context, area_type="NODE_EDITOR"):
    selected_areas = []
    for area in context.screen.areas:
        if area.type == area_type:
            selected_areas.append(area)
    return selected_areas
