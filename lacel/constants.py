# ===== Constant values =====

acceptable_decoding_types = ["ANSI", "ASCII", "UTF-8"]
archive_id_field = "SP"
bmp_id_field = "BM"
bytes_per_color = 8
color_mode = "RGB"
color_mode_alpha = "RGBA"
cfg_highscores = 10
date_format = "%Y.%m.%d %H:%M:%S.%f"
encoding_type = "CP1250"
key_type_name = "keyboard_id"
name_corruption_replacement = ""
name_max_length = 32
package_name_max_length = 100
pln_max_camera_blockades = 10
pln_max_stage_name_length = 20
unix_epoch_as_filetime = 116444736000000000

# ===== Constant json elements types =====

json_cfg_list_types = [key_type_name, key_type_name, key_type_name, key_type_name,
                       key_type_name, list, int, int,
                       int, str, str, key_type_name,
                       key_type_name, list, int, key_type_name]

json_pln_list_types = [int, int, list, int,
                       int, list, int, str]

# ===== Constant extensions =====

# all extensions must be in uppercase
all_extensions_dict = {
                       "acceptable_image_file_extensions": ["BMP", "PNG"],
                       "bmp_image_extensions": ["BMP"],
                       "internal_archive_extensions": ["DAT", "ZPL"],
                       "internal_config_extensions": ["CFG"],
                       "internal_image_extensions": ["BAR"],
                       "internal_save_extensions": ["LPL"],
                       "internal_stage_extensions": ["PLN"],
                       "json_extensions": ["JSON"],
                       "txt_extensions": ["TXT"]
                      }

# ===== Constant parts of R5 G6 B5 *.bmp files =====

bmp_header_part_1 = "424D"
# between header parts: 4 bytes with hexadecimal value describing total file size in bytes (little-endian)
bmp_header_part_2 = "000000008A0000007C000000"
# between header parts: 8 bytes with hexadecimal values describing image dimensions (little-endian)
bmp_header_part_3 = "0100100003000000"
# between header parts: 4 bytes with hexadecimal value describing bitmap size in bytes (little-endian)
bmp_header_part_4 = "130B0000130B00000000000000000000" \
                    "00F80000E00700001F00000000000000" \
                    "42475273000000000000000000000000" \
                    "00000000000000000000000000000000" \
                    "00000000000000000000000000000000" \
                    "00000000020000000000000000000000" \
                    "00000000"
# after header parts: R5 G6 B5 bitmap.
# (If bitmap width is odd, after every image line hexadecimal symbols "0000" must be present.)


# ===== Constant error messages =====
error_values = {
                "absolute_path": "All given paths must be relative.",
                "breakpoint_not_found": "Breakpoint not found.",
                "conflicting_9th_bit_flag": "Flag cannot be set to false if 9th bit is set to 1.",
                "constants_extensions_not_uppercase": "All constant extensions must be in uppercase.",
                "empty_cam_blockade": "Camera blockade must have at least one bit set to 1.",
                "encoding_error": "Given bytes cannot be encoded correctly.",
                "file_duplicated_to_archive": "Two files with same names in headers cannot be archived together.",
                "file_not_found": "File not found.",
                "hex_start_0x_not_found": "\"0x\" is missing at the beginning of string with hexadecimal number.",
                "hexstr_wrong_length": "String with hexadecimal number has incorrect length",
                "indivisibility": "Division does not return whole number.",
                "key_not_found": "Key not found.",
                "key_value_duplicated": "Key value is duplicated.",
                "outside_of_values_range": "Numeric value is outside of acceptable range.",
                "pointer_not_found": "Pointer not found.",
                "too_long_stage_name": "Stage name is too long.",
                "too_many_cam_blockades": "Too many camera blockades.",
                "unknown_game_version": "Unknown game version.",
                "wrong_archive_header": "Archive header is incorrect.",
                "wrong_bmp_header": "*.BMP file header is incorrect. (Color mode must be set to R5 G6 B5.)",
                "wrong_filetype": "Given file has an incorrect extension.",
                "wrong_length_last_package_data": "Last package data has incorrect length.",
                "wrong_number_of_highscores": "Wrong number of highscores."
                }


# ===== Constant names of keys inside game =====

keyboard_values = {
                   8: "BACKSPACE",
                   9: "TAB",
                   12: "NUM CENTER",
                   13: "ENTER",
                   16: "SHIFT",
                   17: "CTRL",
                   20: "CAPS",
                   32: "SPACJA",
                   33: "PAGE UP",
                   34: "PAGE DOWN",
                   35: "END",
                   36: "HOME",
                   37: "LEWO",
                   38: "GÓRA",
                   39: "PRAWO",
                   40: "DÓŁ",
                   45: "INSERT",
                   46: "DELETE",
                   48: "0",
                   49: "1",
                   50: "2",
                   51: "3",
                   52: "4",
                   53: "5",
                   54: "6",
                   55: "7",
                   56: "8",
                   57: "9",
                   65: "A",
                   66: "B",
                   67: "C",
                   68: "D",
                   69: "E",
                   70: "F",
                   71: "G",
                   72: "H",
                   73: "I",
                   74: "J",
                   75: "K",
                   76: "L",
                   77: "M",
                   78: "N",
                   79: "O",
                   80: "P",
                   81: "Q",
                   82: "R",
                   83: "S",
                   84: "T",
                   85: "U",
                   86: "V",
                   87: "W",
                   88: "X",
                   89: "Y",
                   90: "Z",
                   91: "LWINDOW",
                   92: "RWINDOW",
                   93: "POPMENU",
                   96: "NUM 0",
                   97: "NUM 1",
                   98: "NUM 2",
                   99: "NUM 3",
                   100: "NUM 4",
                   101: "NUM 5",
                   102: "NUM 6",
                   103: "NUM 7",
                   104: "NUM 8",
                   105: "NUM 9",
                   106: "NUM *",
                   107: "NUM +",
                   109: "NUM -",
                   110: "NUM .",
                   111: "NUM /",
                   112: "F1",
                   113: "F2",
                   114: "F3",
                   115: "F4",
                   116: "F5",
                   117: "F6",
                   118: "F7",
                   119: "F8",
                   120: "F9",
                   121: "F10",
                   122: "F11",
                   123: "F12",
                   144: "NUM LOCK",
                   186: ";",
                   187: "+",
                   188: ",",
                   189: "-",
                   190: ".",
                   191: "/",
                   192: "~",
                   219: "[",
                   220: "BACKSLASH",
                   221: "]",
                   222: "'",
                   }

# ===== Checks =====

# check do all extensions are in uppercase
for extensions in list(all_extensions_dict.values()):
    for extension in extensions:
        if extension != extension.upper():
            raise ValueError(error_values.get("constants_extensions_not_uppercase"))

# check do keyboard values are not duplicated
values_used = []
for value in keyboard_values.values():
    if value in values_used:
        raise ValueError(error_values.get("key_value_duplicated"))
    else:
        values_used.append(value)
