from .constants import all_extensions_dict,\
                       archive_id_field,\
                       error_values

from .manager import check_correct_extension,\
                     int_to_hexstr_le,\
                     os_listdir,\
                     os_path_isabs,\
                     os_path_isdir,\
                     os_path_isfile,\
                     os_path_join,\
                     os_path_normpath,\
                     os_sep,\
                     save_hexstr_to_file,\
                     str_to_hexstr,\
                     read_file_as_hexstr

# constant value
internal_archive_extensions = all_extensions_dict.get("internal_archive_extensions")


def read_files_content(files_list,
                       remove_base_dirs_from_names=True,
                       remove_all_dirs_from_names=False):
    """Function returns a dictionary with strings of hexadecimal symbols from a given list of files."""

    files_hexstr = {}

    for file_name in files_list:
        if remove_all_dirs_from_names:
            file_name_no_path = file_name.split(os_sep)[-1]
        elif remove_base_dirs_from_names:
            folder_name_length = len(file_name.split(os_sep)[0]) + len(os_sep)
            file_name_no_path = file_name[folder_name_length:]
        else:
            file_name_no_path = file_name

        if os_path_isfile(file_name):

            file_content = read_file_as_hexstr(file_name)

            if file_name_no_path in list(files_hexstr.keys()):
                raise FileExistsError(error_values.get("file_duplicated_to_archive"))

            files_hexstr[file_name_no_path] = file_content

        else:  # if a given file does not exist
            raise FileNotFoundError(error_values.get("file_not_found"))

    return files_hexstr


def get_directory_files(directory_name):
    """Function returns a dictionary with strings of hexadecimal symbols from a given directory."""

    files_list = []

    for file_name in os_listdir(directory_name):
        file_path = os_path_join(directory_name, file_name)

        if os_path_isfile(file_path):
            files_list.append(file_path)

        elif os_path_isdir(file_path):
            subfiles_list = get_directory_files(file_path)
            files_list += subfiles_list

    return files_list


def generate_archive_hexstr(files_dict_hexstr):
    """Function returns a new archive with files from a given dictionary."""

    # set variables to initial values
    headers_hexstr = ""
    content_hexstr = ""

    # iterate through files
    for file_name in list(files_dict_hexstr.keys()):
        file_content = files_dict_hexstr.get(file_name)
        file_content_length = int(len(file_content) // 2)

        # length is divided by two, because one byte (eight bits) is made of two hexadecimal digits
        header_pointer = int(len(content_hexstr) // 2)

        # add files data to archive
        content_hexstr += int_to_hexstr_le(file_content_length)
        content_hexstr += file_content

        # add files headers to archive
        headers_hexstr += int_to_hexstr_le(header_pointer) + str_to_hexstr(file_name) + "00"

    # length is divided by two, because one byte (eight bits) is made of two hexadecimal digits
    main_header_pointer = int(len(headers_hexstr)//2)

    main_header_hexstr = str_to_hexstr(archive_id_field) + int_to_hexstr_le(main_header_pointer)

    # combine headers and data into an archive
    archive_hexstr = main_header_hexstr + headers_hexstr + content_hexstr

    return archive_hexstr


def pack_files_to_archive(files_list,
                          archive_name,
                          remove_base_dirs_from_names=False,
                          remove_all_dirs_from_names=False):
    """Function creates a new archive from a given files list."""

    # check does the list includes absolute paths and normalize file paths
    for iteration_index in range(len(files_list)):
        files_list[iteration_index] = os_path_normpath(files_list[iteration_index])
        if os_path_isabs(files_list[iteration_index]) and (not remove_all_dirs_from_names):
            raise NameError(error_values.get("absolute_path"))

    # check if the file has the correct extension
    check_correct_extension(file_name=archive_name,
                            acceptable_extensions=internal_archive_extensions)

    # read data of every file from a given list
    files_dict_hexstr = read_files_content(files_list=files_list,
                                           remove_base_dirs_from_names=remove_base_dirs_from_names,
                                           remove_all_dirs_from_names=remove_all_dirs_from_names)
    # generate string of hexadecimal symbols representing the archive content
    archive_hexstr = generate_archive_hexstr(files_dict_hexstr=files_dict_hexstr)

    # save archive
    save_hexstr_to_file(name=archive_name,
                        data=archive_hexstr)


def pack_directory_to_archive(directory_name,
                              archive_name):
    """Function creates a new archive from a given directory."""

    files_list = get_directory_files(directory_name=directory_name)

    pack_files_to_archive(files_list=files_list,
                          archive_name=archive_name,
                          remove_base_dirs_from_names=True,
                          remove_all_dirs_from_names=True)
