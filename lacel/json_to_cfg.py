from .constants import all_extensions_dict,\
                       cfg_highscores,\
                       error_values,\
                       json_cfg_list_types,\
                       keyboard_values,\
                       name_corruption_replacement,\
                       name_max_length,\
                       package_name_max_length

from .manager import bytes_to_str,\
                     check_correct_extension,\
                     check_correct_type,\
                     date_str_to_filetime,\
                     int_8_bits_to_hexstr,\
                     int_to_hexstr_le_any,\
                     int_to_hexstr_le,\
                     join_strings_to_string,\
                     json_loads,\
                     read_file_as_bytes, \
                     save_hexstr_to_file,\
                     split_string_to_list,\
                     str_to_hexstr

# constant values
corruption_replacement_hexstr = str_to_hexstr(name_corruption_replacement)
internal_config_extensions = all_extensions_dict.get("internal_config_extensions")
json_extensions = all_extensions_dict.get("json_extensions")
last_package_hexstr_length = (2*package_name_max_length) + 2


def write_highscores(highscores_list):
    """Function converts highscore data from a list to a string of hexadecimal symbols."""

    if len(highscores_list) != cfg_highscores:
        raise IndexError(error_values.get("wrong_number_of_highscores"))

    highscores_hexstr = ""

    for iteration_index in range(cfg_highscores):
        highscore_data = highscores_list[iteration_index]
        highscore_value = highscore_data[0]
        highscore_names = highscore_data[1]

        highscore_name = ""

        for name in highscore_names:
            # add all names (displayed and corrupted)
            highscore_name += name[len(highscore_name):]

        if len(highscore_name) > name_max_length:
            raise NameError(error_values.get("too_long_stage_name"))

        highscore_name += name_corruption_replacement*(name_max_length - len(highscore_name))
        highscore_name_hexstr = str_to_hexstr(highscore_name)

        highscore_name_hexstr_list = split_string_to_list(highscore_name_hexstr, 2)

        # iterate through characters
        for char_index in range(len(highscore_name_hexstr_list)):
            if highscore_name_hexstr_list[char_index] == corruption_replacement_hexstr:
                highscore_name_hexstr_list[char_index] = "00"

        highscore_name_hexstr = join_strings_to_string(highscore_name_hexstr_list)

        highscore_hexstr = int_to_hexstr_le(highscore_value) + highscore_name_hexstr
        highscores_hexstr += highscore_hexstr

    return highscores_hexstr


def key_to_int(object_data):
    """Function converts a key value to an integer."""

    if check_correct_type(object_data=object_data,
                          correct_type=int):
        return object_data

    else:
        for dict_key in list(keyboard_values.keys()):
            if object_data == keyboard_values.get(dict_key):
                return dict_key

    raise ValueError(error_values.get("key_not_found"))


def convert_list_to_cfg(cfg_list):
    """Function converts a list to a string of hexadecimal symbols representing *.cfg file content."""

    cfg_list_length = len(cfg_list)

    if cfg_list_length == 13:
        version = 1.03  # LosV1.03.zip

    elif cfg_list_length == 14:
        version = 2.0  # los.zip

    elif cfg_list_length == 16:
        version = 2.01  # Los2.zip

    else:
        raise IndexError(error_values.get("unknown_game_version"))

    for iteration_index in range(cfg_list_length):
        if not check_correct_type(object_data=cfg_list[iteration_index],
                                  correct_type=json_cfg_list_types[iteration_index]):
            raise TypeError(error_values.get("wrong_filetype"))

    key_left = key_to_int(cfg_list[0])
    key_right = key_to_int(cfg_list[1])
    key_up = key_to_int(cfg_list[2])
    key_down = key_to_int(cfg_list[3])
    key_puffball = key_to_int(cfg_list[4])

    key_left_hexstr = int_to_hexstr_le(key_left)
    key_right_hexstr = int_to_hexstr_le(key_right)
    key_up_hexstr = int_to_hexstr_le(key_up)
    key_down_hexstr = int_to_hexstr_le(key_down)
    key_puffball_hexstr = int_to_hexstr_le(key_puffball)

    highscores_list = cfg_list[5]
    highscores_hexstr = write_highscores(highscores_list)

    last_level_number = cfg_list[6]
    is_in_game_time_on = cfg_list[7]
    sound_volume = cfg_list[8]
    garbage_data_str = cfg_list[9]

    last_level_number_hexstr = int_to_hexstr_le(last_level_number)
    is_in_game_time_on_hexstr = int_8_bits_to_hexstr(is_in_game_time_on)
    sound_volume_hexstr = int_to_hexstr_le(sound_volume)

    if garbage_data_str[0:2] != "0x" or len(garbage_data_str) != 44:
        return ValueError(error_values.get("hex_start_0x_not_found"))
    garbage_data_hexstr = garbage_data_str[2:]

    filetime = cfg_list[10]
    filetime_hexstr = int_to_hexstr_le_any(date_str_to_filetime(filetime))

    pause_key = key_to_int(cfg_list[11])
    suicide_key = key_to_int(cfg_list[12])

    pause_key_hexstr = int_to_hexstr_le(pause_key)
    suicide_key_hexstr = int_to_hexstr_le(suicide_key)

    # set variables to initial values
    cfg_hexstr = ""
    last_package_hexstr = ""
    music_volume_hexstr = "00000000"
    music_key_hexstr = "00000000"

    if version > 1.03:
        last_package_list = cfg_list[13]

        last_package_name = last_package_list[0]
        last_package_hexstr += str_to_hexstr(last_package_name)

        for iteration_index in range(len(last_package_list)):
            if iteration_index != 0:
                garbage = last_package_list[iteration_index]
                if garbage[0:2] != "0x":
                    raise ValueError(error_values.get("hex_start_0x_not_found"))
                else:
                    garbage = garbage[2:]
                    last_package_hexstr += garbage

        if len(last_package_hexstr) != last_package_hexstr_length:
            raise IndexError(error_values.get("wrong_length_last_package_data"))

        if version > 2:
            music_volume = cfg_list[14]
            music_key = key_to_int(cfg_list[15])

            music_volume_hexstr = int_to_hexstr_le(music_volume)
            music_key_hexstr = int_to_hexstr_le(music_key)

    if version == 1.03:
        cfg_hexstr = key_left_hexstr + \
                     key_right_hexstr + \
                     key_up_hexstr + \
                     key_down_hexstr + \
                     key_puffball_hexstr + \
                     highscores_hexstr + \
                     last_level_number_hexstr + \
                     is_in_game_time_on_hexstr + \
                     sound_volume_hexstr + \
                     garbage_data_hexstr + \
                     filetime_hexstr + \
                     pause_key_hexstr + \
                     suicide_key_hexstr

    elif version == 2:
        cfg_hexstr = key_left_hexstr + \
                     key_right_hexstr + \
                     key_up_hexstr + \
                     key_down_hexstr + \
                     key_puffball_hexstr + \
                     highscores_hexstr + \
                     last_level_number_hexstr + \
                     is_in_game_time_on_hexstr + \
                     sound_volume_hexstr + \
                     garbage_data_hexstr + \
                     filetime_hexstr + \
                     pause_key_hexstr + \
                     suicide_key_hexstr + \
                     last_package_hexstr

    elif version == 2.01:
        cfg_hexstr = key_left_hexstr + \
                     key_right_hexstr + \
                     key_up_hexstr + \
                     key_down_hexstr + \
                     key_puffball_hexstr + \
                     highscores_hexstr + \
                     last_level_number_hexstr + \
                     is_in_game_time_on_hexstr + \
                     sound_volume_hexstr + \
                     garbage_data_hexstr + \
                     filetime_hexstr + \
                     pause_key_hexstr + \
                     suicide_key_hexstr + \
                     last_package_hexstr + \
                     music_volume_hexstr + \
                     music_key_hexstr

    return cfg_hexstr


def read_convert_save_json_as_cfg(json_file_name,
                                  cfg_file_name):
    """Function reads, converts and saves specific *.json file as a *.cfg file."""

    # check if the file has the correct extension
    check_correct_extension(file_name=json_file_name,
                            acceptable_extensions=json_extensions)

    # check if the file has the correct extension
    check_correct_extension(file_name=cfg_file_name,
                            acceptable_extensions=internal_config_extensions)

    # read *.json file as data object
    json_bytes = read_file_as_bytes(file_name=json_file_name)
    json_str = bytes_to_str(json_bytes)
    json_list = json_loads(json_str)

    # check if the *.json file content have the correct data type
    if not check_correct_type(object_data=json_list,
                              correct_type=list):
        raise TypeError(error_values.get("wrong_filetype"))

    # convert a list to a *.cfg file
    cfg_hexstr = convert_list_to_cfg(cfg_list=json_list)

    # save *.cfg file
    save_hexstr_to_file(name=cfg_file_name,
                        data=cfg_hexstr)
