from .constants import all_extensions_dict
from .manager import bytes_to_str,\
                     check_correct_extension,\
                     read_file_as_bytes,\
                     save_bytes_to_file,\
                     str_to_bytes
# constant values
internal_save_extensions = all_extensions_dict.get("internal_save_extensions")
txt_extensions = all_extensions_dict.get("txt_extensions")


def read_convert_save_txt_as_lpl(txt_file_name,
                                 lpl_file_name):
    """Function reads, renames and saves any *.txt file as an *.lpl file."""

    # check if the file has the correct extension
    check_correct_extension(file_name=txt_file_name,
                            acceptable_extensions=txt_extensions)

    # check if the file has the correct extension
    check_correct_extension(file_name=lpl_file_name,
                            acceptable_extensions=internal_save_extensions)

    # read *.lpl file as a string of hexadecimal symbols
    txt_bytes = read_file_as_bytes(file_name=txt_file_name)

    # change potential encoding difference
    lpl_bytes = str_to_bytes(bytes_to_str(txt_bytes))

    # save *.txt data to a file
    save_bytes_to_file(name=lpl_file_name,
                       data=lpl_bytes)
