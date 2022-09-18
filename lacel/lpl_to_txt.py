from .constants import all_extensions_dict

from .manager import check_correct_extension,\
                     read_file_as_bytes,\
                     save_bytes_to_file

# constant values
internal_save_extensions = all_extensions_dict.get("internal_save_extensions")
txt_extensions = all_extensions_dict.get("txt_extensions")


def read_rename_save_lpl_as_txt(lpl_file_name,
                                txt_file_name):
    """Function reads, renames and saves any *.lpl file as a *.txt file."""

    # check if the file has the correct extension
    check_correct_extension(file_name=txt_file_name,
                            acceptable_extensions=txt_extensions)

    # check if the file has the correct extension
    check_correct_extension(file_name=lpl_file_name,
                            acceptable_extensions=internal_save_extensions)

    # read *.lpl file as a string of hexadecimal symbols
    lpl_bytes = read_file_as_bytes(file_name=lpl_file_name)

    # coversion is not needed
    txt_bytes = lpl_bytes

    # save *.txt data to a file
    save_bytes_to_file(name=txt_file_name,
                       data=txt_bytes)
