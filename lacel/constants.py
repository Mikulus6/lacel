from datetime import datetime as datetime_datetime, \
                     timezone as datetime_timezone

from json import dumps as json_dumps, \
                 loads as json_loads

from os import listdir as os_listdir, \
               mkdir as os_mkdir, \
               sep as os_sep

from os.path import dirname as os_path_dirname, \
                    isabs as os_path_isabs, \
                    isdir as os_path_isdir, \
                    isfile as os_path_isfile, \
                    join as os_path_join, \
                    normpath as os_path_normpath

# Libraries imported above may be used by other modules. Please ignore warnings saying that they are unused.


# ===== Constant dictionaries =====
from .data.extensions import all_extensions_dict
from .data.errors import error_values
from .data.keys import keyboard_values


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
int32_max_value = 2147483647
int32_min_value = -2147483648
internal_os_sep = "\\"  # "\"
key_type_name = "keyboard_id"
name_corruption_replacement = "\u0000"  # null char
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
