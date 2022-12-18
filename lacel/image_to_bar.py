from .constants import all_extensions_dict,\
                       bytes_per_color,\
                       error_values

from .manager import binstr_to_hexstr,\
                     check_correct_extension,\
                     check_correct_type,\
                     int_8_bits_to_binstr,\
                     int_to_hexstr_le,\
                     save_hexstr_to_file,\
                     scale_color

try:
    # If error occurs here please install following library: https://pypi.org/project/Pillow/
    from PIL import Image as PIL_Image
except ImportError:
    raise ImportError(error_values.get("pil_not_found"))

# constant values
internal_image_extensions = all_extensions_dict.get("internal_image_extensions")
acceptable_image_file_extensions = all_extensions_dict.get("acceptable_image_file_extensions")


def load_file_as_image_object(file_name):
    """Function loads any image file as a PIL image object."""

    image_object = PIL_Image.open(file_name)

    return image_object


def convert_image_object_to_bitmap(image_object):
    """Function returns bitmap data from a given PIL image object."""

    bitmap_size_horizontal, bitmap_size_vertical = image_object.size
    bitmap_size = (bitmap_size_horizontal, bitmap_size_vertical)

    bitmap_data_list = list(image_object.getdata())

    return bitmap_size, bitmap_data_list


def convert_bitmap_to_bar(bitmap_size, bitmap_data_list):
    """Function returns a strings of hexadecimal symbols representing content of *.bar file from bitmap data."""

    # get bitmap size
    bitmap_size_horizontal = bitmap_size[0]
    bitmap_size_vertical = bitmap_size[1]

    bitmap_length = bitmap_size_horizontal * bitmap_size_vertical

    bitmap_size_hexstr = int_to_hexstr_le(bitmap_size_horizontal) + \
                         int_to_hexstr_le(bitmap_size_vertical)

    # set variable to initial value
    bitmap_hexstr_data = ""
    iteration_index = 0

    # iterate through bitmap pixels
    while iteration_index < bitmap_length:
        color_value = bitmap_data_list[iteration_index]

        if not check_correct_type(object_data=color_value,
                                  correct_type=tuple):
            raise TypeError(error_values.get("wrong_filetype"))

        # convert a given color mode value to R5 G6 B5 color value

        red_value = int_8_bits_to_binstr(scale_color(var=color_value[0],
                                                     init_bytes_size=bytes_per_color,
                                                     final_bytes_size=5))

        green_value = int_8_bits_to_binstr(scale_color(var=color_value[1],
                                                       init_bytes_size=bytes_per_color,
                                                       final_bytes_size=6))

        blue_value = int_8_bits_to_binstr(scale_color(var=color_value[2],
                                                      init_bytes_size=bytes_per_color,
                                                      final_bytes_size=5))

        # combine binary data to a hexadecimal color value
        pixel_binstr = green_value[-3:] + blue_value[-5:] + red_value[-5:] + green_value[-6:-3]
        pixel_hexstr = binstr_to_hexstr(pixel_binstr)

        bitmap_hexstr_data += pixel_hexstr

        iteration_index += 1

    # combine bitmap size and bitmap data to a *.bar file data
    bar_hexstr = bitmap_size_hexstr + bitmap_hexstr_data

    return bar_hexstr


def read_convert_save_image_file_as_bar(image_file_name,
                                        bar_file_name):
    """Function reads, converts and saves any image under a given name as a *.bar file."""

    # check if the file has the correct extension
    check_correct_extension(file_name=bar_file_name,
                            acceptable_extensions=internal_image_extensions)

    # check if the file has the correct extension
    check_correct_extension(file_name=image_file_name,
                            acceptable_extensions=acceptable_image_file_extensions)

    # load a given file as a PIL image object
    image_object = load_file_as_image_object(file_name=image_file_name)

    # convert PIL image object to bitmap data
    bitmap_size, bitmap_data_list = convert_image_object_to_bitmap(image_object=image_object)

    # convert bitmap data to a string of hexadecimal symbols representing content of *.bar file
    bar_hexstr = convert_bitmap_to_bar(bitmap_size=bitmap_size,
                                       bitmap_data_list=bitmap_data_list)

    # save a string of hexadecimal symbols as a file
    save_hexstr_to_file(name=bar_file_name,
                        data=bar_hexstr)
