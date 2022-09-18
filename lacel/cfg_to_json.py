from .constants import all_extensions_dict,\
                       cfg_highscores,\
                       encoding_type,\
                       error_values,\
                       name_corruption_replacement,\
                       package_name_max_length

from .manager import check_correct_extension,\
                     filetime_to_date_str, \
                     hexstr_le_to_key_value, \
                     hexstr_to_int_le,\
                     hexstr_to_int_le_any,\
                     hexstr_to_str,\
                     json_dumps,\
                     read_file_as_hexstr,\
                     save_bytes_to_file

# constant values
internal_config_extensions = all_extensions_dict.get("internal_config_extensions")
json_extensions = all_extensions_dict.get("json_extensions")
last_package_hexstr_length = (2*package_name_max_length) + 2


def read_higscores(highscores_hexstr):
    """Function converts highscore data from a string of hexadecimal symbols to a list."""

    # set variable to initial value
    highscores_list = []

    # iterate through 10 highscores
    for iteration_index in range(cfg_highscores):
        single_highscore_hexstr = highscores_hexstr[iteration_index*72:
                                                    (iteration_index+1)*72]

        single_higscore_value = hexstr_to_int_le(single_highscore_hexstr[0:8])

        # set variables to initial value
        current_name = ""
        all_names = []
        add_name = False

        # iterate through 32 characters in single highscore
        for iteration_index_2 in range(32):
            single_name_hexstr = single_highscore_hexstr[(iteration_index_2*2)+8:
                                                         (iteration_index_2*2)+10]

            if single_name_hexstr == "00":
                current_name += name_corruption_replacement
                add_name = True
            else:
                current_name += hexstr_to_str(single_name_hexstr)

            if add_name:

                fixed_name = ((iteration_index_2-len(current_name)+1) * name_corruption_replacement) + current_name[:-1]

                all_names.append(fixed_name)
                add_name = False
                current_name = ""

                # if the rest of single highscore data is empty
                if int(single_highscore_hexstr[(iteration_index_2*2)+8: 72], 16) == 0:
                    break

        highscores_list.append([single_higscore_value, all_names])

    return highscores_list


def read_package_name(last_package_hexstr):
    """Function converts last package data from a string of hexadecimal symbols to a list."""

    package_name = ""

    for iteration_index in range(package_name_max_length + 1):
        single_package_char = last_package_hexstr[(iteration_index*2):
                                                  (iteration_index*2)+2]
        if single_package_char == "00":
            remaining_garbage = "0x"+last_package_hexstr[(iteration_index*2)+2: last_package_hexstr_length]
            break
        else:
            package_name += hexstr_to_str(single_package_char)
    else:
        # hexadecimal string "00" was not found during iteration.
        raise IndexError(error_values.get("breakpoint_not_found"))

    if remaining_garbage == "":
        return [package_name, "0x00"]
    else:
        return [package_name, "0x00", remaining_garbage]


def convert_cfg_to_list(cfg_hexstr):
    """Function converts a string of hexadecimal symbols representing a *.cfg file content to a list."""

    if len(cfg_hexstr) == 852:
        version = 1.03  # LosV1.03.zip

    elif len(cfg_hexstr) == 1054:
        version = 2.0  # los.zip

    elif len(cfg_hexstr) == 1070:
        version = 2.01  # Los2.zip

    else:
        raise IndexError(error_values.get("unknown_game_version"))

    key_left = hexstr_le_to_key_value(cfg_hexstr[0:8])
    key_right = hexstr_le_to_key_value(cfg_hexstr[8:16])
    key_up = hexstr_le_to_key_value(cfg_hexstr[16:24])
    key_down = hexstr_le_to_key_value(cfg_hexstr[24:32])
    key_puffball = hexstr_le_to_key_value(cfg_hexstr[32:40])

    highscores_list = read_higscores(cfg_hexstr[40:760])

    last_level_number = hexstr_to_int_le(cfg_hexstr[760:768])
    is_in_game_time_on = hexstr_to_int_le_any(cfg_hexstr[768:770])
    sound_volume = hexstr_to_int_le(cfg_hexstr[770:778])
    garbage_data_hexstr = cfg_hexstr[778:820]
    filetime = filetime_to_date_str(hexstr_to_int_le_any(cfg_hexstr[820:836]))
    pause_key = hexstr_le_to_key_value(cfg_hexstr[836:844])
    suicide_key = hexstr_le_to_key_value(cfg_hexstr[844:852])

    # set variables to initial values
    cfg_list = []
    last_package_list = []
    music_key = 0
    music_volume = 0

    if version > 1.03:
        last_package_list = read_package_name(cfg_hexstr[852:1054])

        if version > 2:
            music_volume = hexstr_to_int_le(cfg_hexstr[1054:1062])
            music_key = hexstr_le_to_key_value(cfg_hexstr[1062:1070])

    garbage_data_str = "0x"+garbage_data_hexstr

    if version == 1.03:
        cfg_list = [
                    key_left,
                    key_right,
                    key_up,
                    key_down,
                    key_puffball,
                    highscores_list,
                    last_level_number,
                    is_in_game_time_on,
                    sound_volume,
                    garbage_data_str,
                    filetime,
                    pause_key,
                    suicide_key
                    ]

    elif version == 2.0:

        cfg_list = [
                    key_left,
                    key_right,
                    key_up,
                    key_down,
                    key_puffball,
                    highscores_list,
                    last_level_number,
                    is_in_game_time_on,
                    sound_volume,
                    garbage_data_str,
                    filetime,
                    pause_key,
                    suicide_key,
                    last_package_list
                    ]

    elif version == 2.01:

        cfg_list = [
                    key_left,
                    key_right,
                    key_up,
                    key_down,
                    key_puffball,
                    highscores_list,
                    last_level_number,
                    is_in_game_time_on,
                    sound_volume,
                    garbage_data_str,
                    filetime,
                    pause_key,
                    suicide_key,
                    last_package_list,
                    music_volume,
                    music_key
                    ]

    return cfg_list


def read_convert_save_cfg_as_json(cfg_file_name,
                                  json_file_name):
    """Function reads, converts and saves any *.cfg file as a *.json file."""

    # check if the file has the correct extension
    check_correct_extension(file_name=json_file_name,
                            acceptable_extensions=json_extensions)

    # check if the file has the correct extension
    check_correct_extension(file_name=cfg_file_name,
                            acceptable_extensions=internal_config_extensions)

    # read *.cfg file as a string of hexadecimal symbols
    cfg_hexstr = read_file_as_hexstr(file_name=cfg_file_name)

    # convert a *.cfg file to a list
    cfg_list = convert_cfg_to_list(cfg_hexstr=cfg_hexstr)

    # convert a list to a *.json file
    json_bytes = json_dumps(cfg_list, ensure_ascii=False).encode(encoding_type)

    # save *.json data to a file
    save_bytes_to_file(name=json_file_name,
                       data=json_bytes)
