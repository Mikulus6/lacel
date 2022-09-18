from .constants import all_extensions_dict,\
                       bmp_header_part_1,\
                       bmp_header_part_2,\
                       bmp_header_part_3,\
                       bmp_header_part_4

from .manager import check_correct_extension,\
                     hexstr_to_int_le,\
                     int_to_hexstr_le,\
                     read_file_as_hexstr,\
                     save_hexstr_to_file

# constant values
bmp_image_extensions = all_extensions_dict.get("bmp_image_extensions")
internal_image_extensions = all_extensions_dict.get("internal_image_extensions")


def convert_bar_to_bmp(bar_hexstr):
    """Function converts a strings of hexadecimal symbols from a *.bar file content to a R5 G6 B5 *.bmp content."""

    # get bitmap dimensions
    bitmap_size_horizontal = hexstr_to_int_le(bar_hexstr[0:8])
    bitmap_size_vertical = hexstr_to_int_le(bar_hexstr[8:16])

    bitmap_size_horizontal_hexstr = bar_hexstr[0:8]
    # negative height prevents bitmap from flipping upside-down during conversion
    bitmap_size_vertical_rotated_hexstr = int_to_hexstr_le(-abs(bitmap_size_vertical))

    bitmap_hexstr_data = bar_hexstr[16:]

    if bitmap_size_horizontal % 2 == 1:  # if variable bitmap_size_horizontal is odd

        # set variables to initial values
        new_bitmap_hexstr_data = ""
        iteration_index = 0

        # iterate through image horizontal lines
        while iteration_index < bitmap_size_vertical:

            hexstr_line_content = bitmap_hexstr_data[iteration_index * bitmap_size_horizontal * 4:
                                                     (iteration_index+1) * bitmap_size_horizontal * 4]

            # padding for 4 byte alignment (could be a value other than "0000")
            hexstr_line_content += "0000"

            new_bitmap_hexstr_data += hexstr_line_content

            iteration_index += 1

        bitmap_hexstr_data = new_bitmap_hexstr_data

    file_size_hexstr = int_to_hexstr_le(int((len(bmp_header_part_1) + 8 +
                                             len(bmp_header_part_2) + 16 +
                                             len(bmp_header_part_3) + 8 +
                                             len(bmp_header_part_4) +
                                             len(bitmap_hexstr_data))//2))

    bitmap_size_hexstr = int_to_hexstr_le(int(len(bitmap_hexstr_data)//2))

    # combine all headers and data into *.bmp file content
    bmp_hexstr = bmp_header_part_1 + \
                 file_size_hexstr + \
                 bmp_header_part_2 + \
                 bitmap_size_horizontal_hexstr + \
                 bitmap_size_vertical_rotated_hexstr + \
                 bmp_header_part_3 + \
                 bitmap_size_hexstr + \
                 bmp_header_part_4 + \
                 bitmap_hexstr_data

    return bmp_hexstr


def read_convert_save_bar_as_bmp(bar_file_name,
                                 bmp_file_name):
    """Function reads, converts and saves any *.bar file as a R5 G6 B5 *.bmp file."""

    # check if the file has the correct extension
    check_correct_extension(file_name=bar_file_name,
                            acceptable_extensions=internal_image_extensions)

    # check if the file has the correct extension
    check_correct_extension(file_name=bmp_file_name,
                            acceptable_extensions=bmp_image_extensions)

    # read *.bar file as a string of hexadecimal symbols
    bar_hexstr = read_file_as_hexstr(file_name=bar_file_name)

    # convert *.bar file to *.bmp file
    bmp_hexstr = convert_bar_to_bmp(bar_hexstr=bar_hexstr)

    # save *.bmp file
    save_hexstr_to_file(name=bmp_file_name,
                        data=bmp_hexstr)
