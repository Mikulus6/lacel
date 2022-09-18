from .constants import all_extensions_dict,\
                       bytes_per_color,\
                       color_mode,\
                       color_mode_alpha

from .manager import check_correct_extension,\
                     create_missing_subdirectories,\
                     hexstr_to_binstr,\
                     hexstr_to_int_le,\
                     os_path_normpath,\
                     PIL_Image,\
                     read_file_as_hexstr,\
                     scale_color

# constant values
internal_image_extensions = all_extensions_dict.get("internal_image_extensions")
acceptable_image_file_extensions = all_extensions_dict.get("acceptable_image_file_extensions")


def convert_bar_to_bitmap(bar_hexstr, set_black_to_alpha=False):
    """Function returns bitmap data from a strings of hexadecimal symbols representing content of *.bar file"""

    # get bitmap size
    bitmap_size_horizontal = hexstr_to_int_le(bar_hexstr[0:8])
    bitmap_size_vertical = hexstr_to_int_le(bar_hexstr[8:16])

    bitmap_length = bitmap_size_horizontal * bitmap_size_vertical
    bitmap_size = (bitmap_size_horizontal, bitmap_size_vertical)

    bitmap_hexstr_data = bar_hexstr[16:]
    bitmap_binstr_data = hexstr_to_binstr(bitmap_hexstr_data)

    # set variables to initial values
    bitmap_data_list = []
    iteration_index = 0

    # iterate through bitmap pixels
    while iteration_index < bitmap_length:

        # convert R5 G6 B5 color value to a given color mode value

        red_value = int(
                        bitmap_binstr_data[iteration_index*16 + 8:
                                           iteration_index*16 + 13],
                        2)

        green_value = int(
                          bitmap_binstr_data[iteration_index*16 + 13:
                                             iteration_index*16 + 16] +
                          bitmap_binstr_data[iteration_index * 16:
                                             iteration_index * 16 + 3],
                          2)

        blue_value = int(
                        bitmap_binstr_data[iteration_index*16 + 3:
                                           iteration_index*16 + 8],
                        2)

        if set_black_to_alpha:
            # if color is black
            if (red_value, green_value, blue_value) == (0, 0, 0):
                # transparent color
                alpha_value = 0
            else:
                # non-transparent color
                alpha_value = (2 ** bytes_per_color) - 1

            # RGBA
            color_value = (
                           # red value
                           scale_color(var=red_value,
                                       init_bytes_size=5,
                                       final_bytes_size=bytes_per_color),

                           # green value
                           scale_color(var=green_value,
                                       init_bytes_size=6,
                                       final_bytes_size=bytes_per_color),

                           # blue value
                           scale_color(var=blue_value,
                                       init_bytes_size=5,
                                       final_bytes_size=bytes_per_color),

                           # alpha value
                           alpha_value)

        else:
            # RGB
            color_value = (
                # red value
                scale_color(var=red_value,
                            init_bytes_size=5,
                            final_bytes_size=bytes_per_color),

                # green value
                scale_color(var=green_value,
                            init_bytes_size=6,
                            final_bytes_size=bytes_per_color),

                # blue value
                scale_color(var=blue_value,
                            init_bytes_size=5,
                            final_bytes_size=bytes_per_color),
                           )

        # add converted pixel to the new bitmap
        bitmap_data_list.append(color_value)

        iteration_index += 1

    return bitmap_size, bitmap_data_list


def convert_bitmap_to_image_object(bitmap_size,
                                   bitmap_data_list,
                                   include_alpha=False):
    """Function returns PIL image object from a given bitmap data."""

    if include_alpha:
        image_object = PIL_Image.new(mode=color_mode_alpha,
                                     size=bitmap_size)
    else:
        image_object = PIL_Image.new(mode=color_mode,
                                     size=bitmap_size)
    image_object.putdata(bitmap_data_list)

    return image_object


def save_image_object_as_file(file_name,
                              image_object):
    """Function saves any PIL image object as a file under a given name."""

    file_name = os_path_normpath(file_name)

    create_missing_subdirectories(file_name)

    image_object.save(file_name)


def read_convert_save_bar_as_image_file(bar_file_name,
                                        image_file_name,
                                        set_black_to_alpha=False):
    """Function reads, converts and saves any *.bar file as an image under a given name."""

    # check if the file has the correct extension
    check_correct_extension(file_name=bar_file_name,
                            acceptable_extensions=internal_image_extensions)

    # check if the file has the correct extension
    check_correct_extension(file_name=image_file_name,
                            acceptable_extensions=acceptable_image_file_extensions)

    # read *.bar file as a string of hexadecimal symbols
    bar_hexstr = read_file_as_hexstr(file_name=bar_file_name)

    # convert *.bar file to bitmap data
    bitmap_size, bitmap_data_list = convert_bar_to_bitmap(bar_hexstr=bar_hexstr,
                                                          set_black_to_alpha=set_black_to_alpha)

    # convert bitmap data to PIL image object
    image_object = convert_bitmap_to_image_object(bitmap_size=bitmap_size,
                                                  bitmap_data_list=bitmap_data_list,
                                                  include_alpha=set_black_to_alpha)

    # save PIL image object as an image file
    save_image_object_as_file(file_name=image_file_name,
                              image_object=image_object)
