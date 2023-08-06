

def time_convert(arr):
    num = int(arr[1])
    units = arr[2]
    if units == 'day':
        units = 'days'

    gran_order = [['start', 0], ['seconds', 59], ['minutes', 3599], ['hours', 86399],
                  ['days', 2591999], ['months', 31103999], ['years', 31104000000]]
    end_div = [['start', 0], ['seconds', 1], ['minutes', 60], ['hours', 3600], ['days', 86400],
               ['months', 2592000], ['years', 31104000]]
    all_units = [k[0] for k in gran_order]
    starting_point = all_units.index(units)
    starting_value = (gran_order[starting_point - 1][1] + 1) * num
    i = 0
    for i in range(starting_point, len(gran_order)):
        if gran_order[i][1] < starting_value:
            continue
        else:
            break
    conv = starting_value // end_div[i][1]
    un = end_div[i][0]

    if conv == 1:
        un = un[:-1]
    return str(conv), ' ' + un


def stretch_image_size(image_width, image_height, max_width, max_height):
    res_width = max_width
    mul = max_width / image_width
    res_height = mul * image_height

    if res_height > max_height:
        mul = max_height / image_height
        res_width = mul * image_width

    return {
        "width": res_width,
        "height": res_height,
        "factor": mul
    }
