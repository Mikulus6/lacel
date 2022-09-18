from .constants import all_extensions_dict,\
                       encoding_type,\
                       error_values,\
                       pln_max_camera_blockades

from .manager import check_correct_extension,\
                     hexstr_to_binstr,\
                     hexstr_to_int_le,\
                     hexstr_to_int_le_any,\
                     hexstr_to_str,\
                     json_dumps,\
                     read_file_as_hexstr,\
                     save_bytes_to_file

# constant values
json_extensions = all_extensions_dict.get("json_extensions")
internal_stage_extensions = all_extensions_dict.get("internal_stage_extensions")


def pln_hexstr_to_tuple(pln_hexstr):
    """Function converts a string of hexadecimal symbols to a tuple with values of a *.pln file variables."""

    if len(pln_hexstr) != 8:
        raise ValueError(error_values.get("hexstr_wrong_length"))

    data_binstr = hexstr_to_binstr(pln_hexstr)
    data_int = hexstr_to_int_le_any(pln_hexstr)

    bool_var = (int(data_binstr[8], 2) == 1)
    if bool_var:
        data_int -= (2 ** 15)

    output_tuple = (data_int, bool_var)

    return output_tuple


def convert_pln_to_list(pln_hexstr):
    """Function converts a string of hexadecimal symbols representing a *.pln file content to a list."""

    # get bitmap size
    stage_size_horizontal = hexstr_to_int_le(pln_hexstr[0:8])
    stage_size_vertical = hexstr_to_int_le(pln_hexstr[8:16])

    if stage_size_horizontal > 0 and stage_size_vertical > 0:
        stage_size = stage_size_horizontal * stage_size_vertical
    else:
        stage_size = 0

    # set variables to initial values
    stage_data_list = []
    iteration_index = 0

    while iteration_index < stage_size:
        single_tile_data_hexstr = pln_hexstr[(iteration_index + 2) * 8:
                                               (iteration_index + 3) * 8]

        single_tile_tuple = pln_hexstr_to_tuple(pln_hexstr=single_tile_data_hexstr)

        stage_data_list.append(single_tile_tuple)

        iteration_index += 1

    stage_additional_data_hexstr = pln_hexstr[16 + (stage_size*8):]

    cones_required = hexstr_to_int_le(stage_additional_data_hexstr[0:8])
    in_game_time = hexstr_to_int_le(stage_additional_data_hexstr[8:16])

    # set variables to initial values
    camera_data = []
    iteration_index = 0

    while iteration_index < pln_max_camera_blockades:
        single_camera_data_hexstr = stage_additional_data_hexstr[(iteration_index+2)*8:
                                                                 (iteration_index+3)*8]

        if single_camera_data_hexstr == "00000000":
            break

        single_camera_data_tuple = pln_hexstr_to_tuple(pln_hexstr=single_camera_data_hexstr)

        camera_data.append(single_camera_data_tuple)

        iteration_index += 1
    else:
        raise IndexError(error_values.get("too_many_cam_blockades"))

    stage_name_hexstr = stage_additional_data_hexstr[(iteration_index+3)*8:
                                                     (iteration_index+13)*8]

    while stage_name_hexstr[-2:] == "00":
        stage_name_hexstr = stage_name_hexstr[:-2]
    stage_name = hexstr_to_str(stage_name_hexstr)

    pln_list = [stage_size_horizontal,
                stage_size_vertical,
                stage_data_list,
                cones_required,
                in_game_time,
                camera_data,
                0,
                stage_name]

    return pln_list


def read_convert_save_pln_as_json(pln_file_name,
                                  json_file_name):

    """Function reads, converts and saves any *.pln file as a *.json file."""

    # check if the file has the correct extension
    check_correct_extension(file_name=json_file_name,
                            acceptable_extensions=json_extensions)

    # check if the file has the correct extension
    check_correct_extension(file_name=pln_file_name,
                            acceptable_extensions=internal_stage_extensions)

    # read *.pln file as a string of hexadecimal symbols
    pln_hexstr = read_file_as_hexstr(file_name=pln_file_name)

    # convert a *.pln file to a list
    pln_list = convert_pln_to_list(pln_hexstr=pln_hexstr)

    # convert a list to a *.json file
    json_bytes = json_dumps(pln_list, ensure_ascii=False).encode(encoding_type)

    # save *.json data to a file
    save_bytes_to_file(name=json_file_name,
                       data=json_bytes)
