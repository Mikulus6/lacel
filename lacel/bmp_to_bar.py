from .constants import all_extensions_dict,\
                       bmp_header_part_1,\
                       bmp_header_part_2,\
                       bmp_header_part_3,\
                       bmp_id_field,\
                       error_values

from .manager import check_correct_extension,\
                     hexstr_to_int_le,\
                     hexstr_to_str,\
                     int_to_hexstr_le,\
                     read_file_as_hexstr,\
                     save_hexstr_to_file

# constant values
bmp_image_extensions = all_extensions_dict.get("bmp_image_extensions")
internal_image_extensions = all_extensions_dict.get("internal_image_extensions")


def convert_bmp_to_bar(bmp_hexstr):
    """Function converts a strings of hexadecimal symbols from a *.bmp file content to a *.bar content"""

    bmp_header_name = hexstr_to_str(bmp_hexstr[:4])

    if bmp_header_name != bmp_id_field:
        raise ValueError(error_values.get("wrong_bmp_header"))

    bmp_file_size_hexstr = bmp_hexstr[4:12]
    bmp_bitmap_size_horizontal_hexstr = bmp_hexstr[36:44]
    bmp_bitmap_size_vertical_hexstr = bmp_hexstr[44:52]
    bitmap_size_hexstr = bmp_hexstr[68:76]

    bmp_header_size = hexstr_to_int_le(bmp_hexstr[20:28])

    bmp_header_hexstr_to_check = bmp_header_part_1 + \
                                 bmp_file_size_hexstr + \
                                 bmp_header_part_2 + \
                                 bmp_bitmap_size_horizontal_hexstr + \
                                 bmp_bitmap_size_vertical_hexstr + \
                                 bmp_header_part_3 + \
                                 bitmap_size_hexstr
    # bmp_header_part_4 is ignored while checking bytes due to unpredictable print resolution data.

    # check does bmp_header represents correctly R5 G6 B5 *.bmp header
    if bmp_header_hexstr_to_check != bmp_hexstr[:len(bmp_header_hexstr_to_check)]:
        raise ValueError(error_values.get("wrong_bmp_header"))

    # get bitmap header data
    bmp_bitmap_size_horizontal = hexstr_to_int_le(bmp_bitmap_size_horizontal_hexstr)
    bmp_bitmap_size_vertical = hexstr_to_int_le(bmp_bitmap_size_vertical_hexstr)
    bmp_bitmap_length = hexstr_to_int_le(bitmap_size_hexstr)

    reverse_bitmap = True
    if bmp_bitmap_size_vertical > (2**31)-1:
        bmp_bitmap_size_vertical = (-bmp_bitmap_size_vertical) % (2**32)
        reverse_bitmap = False

    bmp_bitmap_size_vertical_hexstr = int_to_hexstr_le(bmp_bitmap_size_vertical)

    odd_horizontal_size = (bmp_bitmap_size_horizontal % 2 == 1)

    bmp_bitmap_hexstr = bmp_hexstr[bmp_header_size*2:
                                   (bmp_header_size + bmp_bitmap_length) * 2]

    # additional operations for reversed bitmap or bitmap with 4 empty bytes alignment
    if odd_horizontal_size or reverse_bitmap:

        # set variables to initial values
        new_bmp_bitmap_hexstr = ""
        iteration_index = 0

        while iteration_index < bmp_bitmap_size_vertical:

            if reverse_bitmap:  # if bitmap is reversed, iterate back forwards
                real_iteration_index = bmp_bitmap_size_vertical - iteration_index - 1
            else:  # if bitmap is not reversed, iterate forwards
                real_iteration_index = iteration_index

            if odd_horizontal_size:  # if bitmap has 4 byte alignment empty bytes, do not include them
                line_hexstr = bmp_bitmap_hexstr[real_iteration_index * (bmp_bitmap_size_horizontal+1) * 4:
                                                ((real_iteration_index+1) * (bmp_bitmap_size_horizontal+1) * 4) - 4]
            else:
                line_hexstr = bmp_bitmap_hexstr[real_iteration_index * bmp_bitmap_size_horizontal * 4:
                                                (real_iteration_index+1) * bmp_bitmap_size_horizontal * 4]

            new_bmp_bitmap_hexstr += line_hexstr

            iteration_index += 1

        bmp_bitmap_hexstr = new_bmp_bitmap_hexstr

    bar_hexstr = bmp_bitmap_size_horizontal_hexstr + \
                 bmp_bitmap_size_vertical_hexstr + \
                 bmp_bitmap_hexstr

    return bar_hexstr


def read_convert_save_bmp_as_bar(bmp_file_name,
                                 bar_file_name):
    """Function reads, converts and saves any R5 G6 B5 *.bmp file as a *.bar file"""

    # check if the file has the correct extension
    check_correct_extension(file_name=bar_file_name,
                            acceptable_extensions=internal_image_extensions)

    # check if the file has the correct extension
    check_correct_extension(file_name=bmp_file_name,
                            acceptable_extensions=bmp_image_extensions)

    # read *.bmp file as a string of hexadecimal symbols
    bmp_hexstr = read_file_as_hexstr(file_name=bmp_file_name)

    # convert *.bmp file to *.bar file
    bar_hexstr = convert_bmp_to_bar(bmp_hexstr=bmp_hexstr)

    # save *.bar file
    save_hexstr_to_file(name=bar_file_name,
                        data=bar_hexstr)
