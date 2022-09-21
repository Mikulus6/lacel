from .constants import all_extensions_dict,\
                       archive_id_field,\
                       error_values,\
                       internal_os_sep

from .manager import check_correct_extension,\
                     create_directory_if_absent,\
                     hexstr_to_bytes,\
                     hexstr_to_int_le,\
                     hexstr_to_str, \
                     os_path_normpath,\
                     os_sep,\
                     read_file_as_hexstr,\
                     save_bytes_to_directory

# constant values
constant_main_header_length = len(archive_id_field) + 4
internal_archive_extensions = all_extensions_dict.get("internal_archive_extensions")


def read_file_data(archive_hexstr,
                   main_header_pointer,
                   header_pointer):
    """Function returns an archived file content with a given name."""

    header_absolute_pointer = header_pointer + constant_main_header_length + main_header_pointer

    file_length = hexstr_to_int_le(archive_hexstr[header_absolute_pointer * 2:
                                                  header_absolute_pointer * 2 + 8])

    file_data_hex = archive_hexstr[header_absolute_pointer * 2 + 8:
                                   header_absolute_pointer * 2 + 8 + (file_length * 2)]

    return file_data_hex


def read_all_headers(archive_hexstr):
    """Function returns a dictionary of headers names and headers pointers."""

    # set variables to their initial values
    current_subfile_name = ""
    headers = {}
    header_pointer = 0
    iteration_index = 0
    new_header = True

    # get data from the main header (files names length)
    main_header = archive_hexstr[0:constant_main_header_length * 2]
    main_header_name = hexstr_to_str(main_header[:4])
    main_header_pointer = hexstr_to_int_le(main_header[4:])

    if main_header_name != archive_id_field:
        raise ValueError(error_values.get("wrong_archive_header"))

    iteration_index += constant_main_header_length

    # iterate through headers bytes
    while iteration_index - constant_main_header_length < main_header_pointer:

        # if it starts reading the new header
        if new_header:
            header_pointer = hexstr_to_int_le(archive_hexstr[iteration_index * 2:
                                                             iteration_index * 2 + 8])
            iteration_index += 4
            new_header = False

        # if it continues to read the current header
        else:
            byte_value = archive_hexstr[iteration_index * 2:
                                        iteration_index * 2 + 2]

            # if the header name ended (The current byte is a hexadecimal "00" gap.)
            if int(byte_value, 16) == 0:

                # fix os separator from "Pakowanie.exe" GUI to regular os separator.
                current_subfile_name = os_path_normpath(current_subfile_name).replace(internal_os_sep, os_sep)

                # save file name and file pointer to dictionary
                headers[current_subfile_name] = header_pointer

                # reset variables to their initial values
                current_subfile_name = ""
                new_header = True

            # if the header name continues
            else:
                current_subfile_name += hexstr_to_str(byte_value)

            iteration_index += 1

    return main_header_pointer, headers


# unused function
def read_header_pointer(archive_hexstr,
                        header_name):
    """Function returns the pointer of a header with a given name."""

    # set variables to their initial values
    current_subfile_name = ""
    header_pointer = 0
    iteration_index = 0
    new_header = True

    # get data from the main header (files names length)
    main_header = archive_hexstr[0:constant_main_header_length * 2]
    main_header_name = hexstr_to_str(main_header[:4])
    main_header_pointer = hexstr_to_int_le(main_header[4:])

    if main_header_name != archive_id_field:
        raise ValueError(error_values.get("wrong_archive_header"))

    iteration_index += constant_main_header_length

    # iterate through headers bytes
    while iteration_index - constant_main_header_length < main_header_pointer:

        # if it starts reading the new header
        if new_header:
            header_pointer = hexstr_to_int_le(archive_hexstr[iteration_index * 2:
                                                             iteration_index * 2 + 8])
            iteration_index += 4
            new_header = False

        # if it continues to read the current header
        else:
            byte_value = archive_hexstr[iteration_index * 2:
                                        iteration_index * 2 + 2]

            # if the header name ended (the current byte is 0x00 gap)
            if int(byte_value, 16) == 0:

                # save file name and pointer to dictionary
                if current_subfile_name == header_name:
                    return header_pointer

                # reset variables to their initial values
                current_subfile_name = ""
                new_header = True

            # if the header name continues
            else:
                current_subfile_name += hexstr_to_str(byte_value)

            iteration_index += 1

    raise IndexError(error_values.get("pointer_not_found"))


def read_all_files_data(archive_hexstr):
    """Function returns a dictionary with the content of all files from a given archive."""

    content = {}

    # get headers data
    main_header_pointer, headers = read_all_headers(archive_hexstr=archive_hexstr)

    # iterate through headers names
    for header in list(headers.keys()):
        header_name = header
        header_pointer = headers.get(header_name)

        # read data of file described by current header
        file_data_hex = read_file_data(archive_hexstr=archive_hexstr,
                                       main_header_pointer=main_header_pointer,
                                       header_pointer=header_pointer)

        content[header_name] = file_data_hex

    return content


def extract_archive_to_directory(archive_name,
                                 directory_name):
    """Fuction extracts a given archive in a given directory."""

    # check if the file has the correct extension
    check_correct_extension(file_name=archive_name,
                            acceptable_extensions=internal_archive_extensions)

    # open the archive
    archive_hexstr = read_file_as_hexstr(file_name=archive_name)

    # read the archive content
    content = read_all_files_data(archive_hexstr=archive_hexstr)

    # create destination directory
    create_directory_if_absent(directory_name=directory_name)

    # iterate through all found files
    for file_name in list(content.keys()):
        data = hexstr_to_bytes(content.get(file_name))

        # save each file in a given directory
        save_bytes_to_directory(name=file_name,
                                directory_name=directory_name,
                                data=data)
