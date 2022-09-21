from os import sep as os_sep
from os.path import dirname as os_path_dirname,\
                    isdir as os_path_isdir,\
                    normpath as os_path_normpath,\
                    join as os_path_join
from shutil import copytree as shutil_copytree,\
                   rmtree as shutil_rmtree
from subprocess import check_call as subprocess_check_call
from sys import executable as sys_executable


def install_library(library_name):
    subprocess_check_call([sys_executable, '-m', 'pip', 'install', library_name])


PIL_library_name = "Pillow"
lacel_library_name = "lacel"
libraries_relative_directory = "Lib/site-packages"

library_folder_path = os_path_normpath(os_path_join(os_path_dirname(__file__), lacel_library_name))

sys_executable_list = os_path_normpath(sys_executable).split(os_sep)[:-1]
sys_executable_path = ""
for directory in sys_executable_list:
    sys_executable_path += directory
    sys_executable_path += os_sep
sys_executable_path = os_path_normpath(sys_executable_path)

libraries_absolute_directory = os_path_join(sys_executable_path,
                                            os_path_normpath(libraries_relative_directory),
                                            lacel_library_name)

print("Python executable file directory: "+sys_executable_path)
print("Library source absolute path: "+libraries_absolute_directory)


print("Trying to install "+PIL_library_name+" library.")
install_library("Pillow")

copy_library_directory = True

loop = True
while loop and os_path_isdir(libraries_absolute_directory):
    user_input = input("Directory "+libraries_absolute_directory +
                       " already exists. Do you want to remove it? (Y/n):")

    if user_input == "Y":
        loop = False
        copy_library_directory = True
        shutil_rmtree(libraries_absolute_directory)
    elif user_input == "n":
        loop = False
        copy_library_directory = False

if copy_library_directory:
    print("Trying to copy directory "+library_folder_path+" to "+libraries_absolute_directory+".")
    shutil_copytree(library_folder_path, libraries_absolute_directory)
    print("Directory successfully copied.")
else:
    print("Directory "+library_folder_path+" cannot be copied to "+libraries_absolute_directory+".")

input("Press Enter to exit the setup.")
