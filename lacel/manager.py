from datetime import datetime as datetime_datetime,\
                     timezone as datetime_timezone

from json import dumps as json_dumps,\
                 loads as json_loads

from os import listdir as os_listdir,\
               mkdir as os_mkdir,\
               sep as os_sep

from os.path import isabs as os_path_isabs,\
                    isdir as os_path_isdir,\
                    isfile as os_path_isfile,\
                    join as os_path_join,\
                    normpath as os_path_normpath

# If error occurs here please install following library: https://pypi.org/project/Pillow/
from PIL import Image as PIL_Image

# Libraries imported above may be used by other modules. Please ignore warnings saying that they are unused.

from .constants import acceptable_decoding_types,\
                       date_format,\
                       encoding_type,\
                       error_values,\
                       key_type_name,\
                       keyboard_values,\
                       unix_epoch_as_filetime


def split_string_to_list(var, length):
    """Function splits a string to lists"""

    splitted_list = []
    splitted_list_length = len(splitted_list)/length

    if splitted_list_length != round(splitted_list_length):
        raise IndexError(error_values.get("indivisibility"))

    for iteration_index in range(len(var)):
        if iteration_index % length == 0:
            splitted_list.append("")
        splitted_list[-1] += var[iteration_index]

    return splitted_list


def join_strings_to_string(lists):
    """Function merges multiple strings into a single string"""

    return "".join(lists)


def hexstr_to_int_le(var):
    """Function converts a string of hexadecimal symbols to a 32-bits signed integer (little-endian)."""

    hex1 = str(var[0]) + str(var[1])
    hex2 = str(var[2]) + str(var[3])
    hex3 = str(var[4]) + str(var[5])
    hex4 = str(var[6]) + str(var[7])

    negative = False

    if int(var[6], 16) >= 8:
        hex4 = hex(int(var[6], 16)-8)[2:] + str(var[7])
        negative = True

    hex_var = int(hex1, 16) + \
              int(hex2, 16) * (2 ** 8) + \
              int(hex3, 16) * (2 ** 16) + \
              int(hex4, 16) * (2 ** 24)

    if negative:
        hex_var -= 2**31

    return hex_var


def int_to_hexstr_le(var):
    """Function converts a 32-bits unsigned integer to a string of hexadecimal symbols (little-endian)."""

    if not((2**32) >= var >= 0):
        var = var % (2 ** 32)

    var_1 = int(var
                // (2 ** 24))

    var_2 = int(
               (var - (var_1 * (2 ** 24)))
               // (2 ** 16))

    var_3 = int(
               (var - (var_1 * (2 ** 24)) - (var_2 * (2 ** 16)))
               // (2 ** 8))

    var_4 = int(var - (var_1 * (2 ** 24)) - (var_2 * (2 ** 16)) - (var_3 * (2 ** 8)))

    var_list = [str(hex(var_4))[2:],
                str(hex(var_3))[2:],
                str(hex(var_2))[2:],
                str(hex(var_1))[2:]]

    for counter in range(len(var_list)):
        value = var_list[counter]
        if len(value) == 1:
            var_list[counter] = "0"+value

    var_str = join_strings_to_string(var_list).upper()

    return var_str


def int_to_hexstr_le_any(var):
    """Function converts any integer to a string of hexadecimal symbols (little-endian)."""

    var_hexstr = str(hex(var))[2:].upper()

    if len(var_hexstr) % 2 == 1:
        var_hexstr = "0" + var_hexstr

    var_hexstr_le = ""

    for iteration_index in range(len(var_hexstr)//2):
        var_hexstr_le += str(var_hexstr[-(iteration_index*2)-2] + var_hexstr[-(iteration_index*2)-1])

    return var_hexstr_le


def hexstr_to_int_le_any(var):
    """Function converts any string of hexadecimal symbols to an integer (little-endian)."""

    var_len = len(var)

    if var_len % 2 != 0:
        raise ValueError(error_values.get("hexstr_wrong_length"))

    iteration_index = var_len
    hex_list = []

    while iteration_index > 0:
        hex_list.append(var[iteration_index-2:
                            iteration_index])

        iteration_index -= 2
    hexvar_be = join_strings_to_string(hex_list)

    return int(hexvar_be, 16)


def hexstr_to_bytes(var):
    """Function converts a string of hexadecimal symbols to bytes."""

    return bytes.fromhex(var)


def bytes_to_hexstr(var):
    """Function converts bytes to a string of hexadecimal symbols."""

    return str(var.hex()).upper()


def hexstr_to_binstr(var):
    """Function converts a string of hexadecimal symbols to a string of binary symbols."""

    binstr = ""
    for hexchar in var:
        binhexchar = str(bin(int(hexchar, 16)))[2:]
        binstr += "0"*(4-len(binhexchar)) + binhexchar
    return binstr


def binstr_to_hexstr(var):
    """Function converts a string of binary symbols to a string of hexadecimal symbols."""

    hexstr = ""
    var_len = int(len(var)//4)
    for counter in range(0, var_len):
        hexbinchar = str(hex(int(var[counter * 4:
                                 counter * 4 + 4],
                             2)))[2:]
        hexstr += hexbinchar
    return hexstr


def binstr_to_int(var):
    """Function converts a string of binary symbols to an integer."""

    return int(var, 2)


def int_8_bits_to_binstr(var):
    """Function converts an 8-bits integer to a string of binary symbols."""

    if not((2 ** 8)-1 >= var >= 0):
        raise OverflowError(error_values.get("outside_of_values_range"))

    var_str = str(bin(var))[2:]

    return "0"*(8-len(var_str)) + var_str


def int_8_bits_to_hexstr(var):
    """Function converts an 8-bits integer to a string of hexadecimal symbols."""

    if not((2 ** 8)-1 >= var >= 0):
        raise OverflowError(error_values.get("outside_of_values_range"))

    var_str = str(hex(var))[2:]

    return "0"*(2-len(var_str)) + var_str


def int_to_binstr_le(var):
    """Function converts a 32-bits unsigned integer to a string of binary symbols (little-endian)."""
    return hexstr_to_binstr(int_to_hexstr_le(var))


def str_to_bytes(var):
    """Function converts a string to bytes."""

    return var.encode(encoding_type)


def bytes_to_str(var, decoding=None):
    """Function converts bytes to a string in a fixed decoding type."""

    if decoding is None:
        decoding = encoding_type

    try:
        var_str = var.decode(decoding)
        var_str.encode(encoding_type)
        return var_str
    except UnicodeError:
        for decoding in acceptable_decoding_types:
            try:
                var_str = var.decode(decoding)
                var_str.encode(encoding_type)
                return var_str
            except UnicodeError:
                pass

    raise UnicodeError(error_values.get("encoding_error"))


def hexstr_to_str(var):
    """Function converts a string of hexadecimal symbols to a regular string."""

    return bytes_to_str(hexstr_to_bytes(var), encoding_type)


def str_to_hexstr(var):
    """Function converts a regular string to a string of hexadecimal symbols."""

    return bytes_to_hexstr(str_to_bytes(var))


def hexstr_le_to_key_value(var):
    """Function converts a string of hexadecimal symbols (little-endian) to an integer with keyboard value."""

    var_int = hexstr_to_int_le(var)

    if var_int in keyboard_values.keys():
        return keyboard_values.get(var_int)
    else:
        return hexstr_to_int_le(var)


def key_value_to_hexstr_le(var):
    """Function converts an integer with keyboard value to a string of hexadecimal symbols (little-endian)"""

    if var in keyboard_values.values():
        for key_value in keyboard_values.keys():
            if keyboard_values.get(key_value) == var:
                return key_value
    else:
        if 0 <= var <= 255:
            return int_to_hexstr_le(var)
        else:
            raise ValueError(error_values.get("outside_of_values_range"))


def scale_color(var,
                init_bytes_size,
                final_bytes_size):
    """Function converts a color value for different bytes per pixel coding."""

    init_max_color = (2 ** init_bytes_size)-1
    final_max_color = (2 ** final_bytes_size)-1

    var_final = int(round(var * (final_max_color/init_max_color)))

    return var_final


def read_file_as_bytes(file_name):
    """Function returns content of a given file as bytes."""

    try:
        f = open(file_name, "rb")
        data = f.read()
        f.close()

    except:
        raise FileNotFoundError(error_values.get("file_not_found"))

    return data


def read_file_as_hexstr(file_name):
    """Function returns content of a given file as a string of hexadecimal symbols."""

    try:
        f = open(file_name, "rb")
        data = bytes_to_hexstr(f.read())
        f.close()

    except:
        raise FileNotFoundError(error_values.get("file_not_found"))

    return data


def get_filename_extension(file_name):
    """Function returns a file extension from a file name or a file path."""

    return file_name.split(".")[-1].upper()


def save_bytes_to_directory(name,
                            directory_name,
                            data):
    """Function saves any bytes-type variable as a file under a given name in a given directory."""

    full_save_path = os_path_join(directory_name, name)

    # this code fixes saving files in subdirectories
    subdirectory_names = full_save_path.split(os_sep)[:-1]
    subdirectory_name = ""
    for iteration_index in range(len(subdirectory_names)):
        subdirectory_name = os_path_join(subdirectory_name, subdirectory_names[iteration_index])
        create_directory_if_absent(subdirectory_name)

    with open(full_save_path, 'wb') as f:
        f.write(data)
    f.close()


def create_missing_subdirectories(name):
    """Function creates missing subdirectories in given file path."""
    if os_sep in name:
        directory_name = os_path_normpath(name)
        directories_list = directory_name.split(os_sep)[:-1]

        temp_directory_list = ""
        for directory in directories_list:
            temp_directory_list = os_path_join(temp_directory_list, directory)
            if not os_path_isdir(temp_directory_list):
                os_mkdir(temp_directory_list)


def save_bytes_to_file(name,
                       data):
    """Function saves any bytes-type variable as a file under a given name."""

    create_missing_subdirectories(name)

    with open(name, 'wb') as f:
        f.write(data)
    f.close()


def save_hexstr_to_file(name,
                        data):
    """Function saves a string of hexadecimal symbols as a file under a given name."""

    create_missing_subdirectories(name)

    data_bytes = hexstr_to_bytes(data)
    save_bytes_to_file(name,
                       data_bytes)


def create_directory_if_absent(directory_name):
    """Function creates a new directory if it does not exist already."""
    directory_name = os_path_normpath(directory_name)
    directories_list = directory_name.split(os_sep)

    temp_directory_list = ""
    for directory in directories_list:
        temp_directory_list = os_path_join(temp_directory_list, directory)
        if not os_path_isdir(temp_directory_list):
            os_mkdir(temp_directory_list)


def check_correct_extension(file_name,
                            acceptable_extensions):
    """Function raises NameError if a file has an unacceptable extension."""

    if not(get_filename_extension(file_name) in acceptable_extensions):
        raise NameError(error_values.get("wrong_filetype"))


def check_key_type(object_data):
    """Function checks if an object is a valid key value."""

    if check_correct_type(object_data=object_data,
                          correct_type=int):
        return True
    else:
        if object_data in keyboard_values.values():
            return True
        else:
            return False


def check_correct_type(object_data,
                       correct_type):
    """Function checks if an object has a correct type."""

    if type(object_data) == correct_type:
        return True
    elif correct_type == key_type_name:
        return check_key_type(object_data)
    else:
        return False


def filetime_to_date_str(filetime):
    """Function converts a filetime value to a string with date."""

    unix_time = (filetime - unix_epoch_as_filetime) // (10 ** 7)
    second_fraction = (filetime - unix_epoch_as_filetime) % (10 ** 7)
    temp_string_date_format = date_format.replace("%f", str(second_fraction))
    date_value = datetime_datetime.utcfromtimestamp(unix_time)
    date_value.strftime(temp_string_date_format)
    date_str = str(date_value.strftime(temp_string_date_format))

    return date_str


def date_str_to_filetime(date_str):
    """Function converts a string with date to a filetime value."""

    temp_string_date_format = date_format
    if "%f" in date_format:
        second_fraction_index = temp_string_date_format.replace("%Y", "%Y..").index("%f")
        second_fraction = int(date_str[second_fraction_index:
                                       second_fraction_index+7])
        temp_string_date_format = temp_string_date_format.replace("%f", "")
        date_str = date_str[:second_fraction_index] + date_str[second_fraction_index+7:]
    else:
        second_fraction = 0
    date_value = datetime_datetime.strptime(date_str, temp_string_date_format)
    unix_time = int(date_value.replace(tzinfo=datetime_timezone.utc).timestamp())

    filetime = int((unix_time * (10**7)) + unix_epoch_as_filetime + second_fraction)

    return filetime
