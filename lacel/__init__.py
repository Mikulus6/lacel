"""
Łoś assets conversions external library

Łacel is a library written in Python 3 for assets and files conversions from the video game "Po prostu Łoś".
For further information read file "README.md".
"""

from .archiver import pack_directory_to_archive as dir2arch,\
                      pack_files_to_archive as list2arch

from .extractor import extract_archive_to_directory as arch2dir

from .bar_to_bmp import read_convert_save_bar_as_bmp as bar2bmp
from .bmp_to_bar import read_convert_save_bmp_as_bar as bmp2bar

from .pln_to_json import read_convert_save_pln_as_json as pln2json
from .json_to_pln import read_convert_save_json_as_pln as json2pln

from .cfg_to_json import read_convert_save_cfg_as_json as cfg2json
from .json_to_cfg import read_convert_save_json_as_cfg as json2cfg

from .lpl_to_txt import read_rename_save_lpl_as_txt as lpl2txt
from .txt_to_lpl import read_convert_save_txt_as_lpl as txt2lpl

try:
    from .bar_to_image import read_convert_save_bar_as_image_file as bar2img
    from .image_to_bar import read_convert_save_image_file_as_bar as img2bar

except ImportError as exception:
    print(exception)
