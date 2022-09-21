from .constants import all_extensions_dict,\
                       error_values,\
                       json_pln_list_types,\
                       pln_max_camera_blockades,\
                       pln_max_stage_name_length

from .manager import binstr_to_hexstr,\
                     bytes_to_str,\
                     check_correct_extension,\
                     check_correct_type,\
                     int_to_binstr_le,\
                     int_to_hexstr_le,\
                     json_loads,\
                     read_file_as_bytes,\
                     save_hexstr_to_file,\
                     str_to_hexstr

# constant values
json_extensions = all_extensions_dict.get("json_extensions")
internal_stage_extensions = all_extensions_dict.get("internal_stage_extensions")
max_stage_name_hexstr_length = pln_max_stage_name_length * 2


def tuple_to_pln_hexstr(tuple_data):
    """Function converts a tuple with values of a *.pln file variables to a string of hexadecimal symbols."""

    data_int = tuple_data[0]
    bool_var = tuple_data[1]

    data_binstr = int_to_binstr_le(data_int)

    if int(data_binstr[8]) == 1 != int(bool_var):
        raise ValueError(error_values.get("conflicting_9th_bit_flag"))

    bool_var_str = str(int(bool_var))
    pln_binstr = data_binstr[0:8] + bool_var_str + data_binstr[9:32]

    pln_hexstr = binstr_to_hexstr(pln_binstr)
    return pln_hexstr


def convert_list_to_pln(pln_list):
    """Function converts a list to a string of hexadecimal symbols representing *.pln file content."""

    for iteration_index in range(8):
        if not check_correct_type(object_data=pln_list[iteration_index],
                                  correct_type=json_pln_list_types[iteration_index]):
            raise TypeError(error_values.get("wrong_filetype"))

    stage_size_horizontal = pln_list[0]
    stage_size_vertical = pln_list[1]
    stage_data_list = pln_list[2]
    cones_required = pln_list[3]
    in_game_time = pln_list[4]
    camera_data = pln_list[5]
    break_data = pln_list[6]
    stage_name = pln_list[7]

    if len(camera_data) > pln_max_camera_blockades:
        return IndexError(error_values.get("too_many_cam_blockades"))

    stage_size_horizontal_hexstr = int_to_hexstr_le(stage_size_horizontal)
    stage_size_vertical_hexstr = int_to_hexstr_le(stage_size_vertical)

    # set variable to initial value
    stage_data_hexstr = ""

    for tile_data in stage_data_list:
        single_tile_data_hexstr = tuple_to_pln_hexstr(tuple_data=tile_data)

        stage_data_hexstr += single_tile_data_hexstr

    cones_required_hexstr = int_to_hexstr_le(cones_required)
    in_game_time = int_to_hexstr_le(in_game_time)

    # set variable to initial valie
    camera_data_hexstr = ""

    for single_camera_data in camera_data:

        single_camera_data_hexstr = tuple_to_pln_hexstr(tuple_data=single_camera_data)

        if single_camera_data_hexstr == "00000000":
            raise ValueError(error_values.get("empty_cam_blockade"))

        camera_data_hexstr += single_camera_data_hexstr

    break_data_hexstr = int_to_hexstr_le(break_data)
    stage_name_hexstr = str_to_hexstr(stage_name) # this line also changes potential encoding difference

    if len(stage_name_hexstr) < max_stage_name_hexstr_length:
        stage_name_hexstr += "0"*(max_stage_name_hexstr_length - len(stage_name_hexstr))
    elif len(stage_name_hexstr) > max_stage_name_hexstr_length:
        raise IndexError(error_values.get("too_long_stage_name"))

    pln_hexstr = stage_size_horizontal_hexstr + \
                 stage_size_vertical_hexstr + \
                 stage_data_hexstr + \
                 cones_required_hexstr + \
                 in_game_time + \
                 camera_data_hexstr + \
                 break_data_hexstr + \
                 stage_name_hexstr

    return pln_hexstr


def read_convert_save_json_as_pln(json_file_name,
                                  pln_file_name):

    """Function reads, converts and saves specific *.json file as a *.pln file."""

    # check if the file has the correct extension
    check_correct_extension(file_name=json_file_name,
                            acceptable_extensions=json_extensions)

    # check if the file has the correct extension
    check_correct_extension(file_name=pln_file_name,
                            acceptable_extensions=internal_stage_extensions)

    # read *.json file as a data object
    json_bytes = read_file_as_bytes(file_name=json_file_name)
    json_str = bytes_to_str(json_bytes)
    json_list = json_loads(json_str)

    # check if the *.json file content have the correct data type
    if not check_correct_type(object_data=json_list,
                              correct_type=list):
        raise TypeError(error_values.get("wrong_filetype"))

    # convert a list to a *.pln file
    pln_hexstr = convert_list_to_pln(pln_list=json_list)

    # save *.pln file
    save_hexstr_to_file(name=pln_file_name,
                        data=pln_hexstr)
