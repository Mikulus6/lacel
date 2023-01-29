# === Łoś assets converter ===

from json import loads as json_loads
from json.decoder import JSONDecodeError
from sys import argv as sys_argv
from os.path import basename

import lacel  # https://github.com/Mikulus6/lacel

commands = \
    {
        "dir2arch": lacel.dir2arch,
        "list2arch": lacel.list2arch,
        "arch2dir": lacel.arch2dir,
        "bar2bmp": lacel.bar2bmp,
        "bmp2bar": lacel.bmp2bar,
        "pln2json": lacel.pln2json,
        "json2pln": lacel.json2pln,
        "cfg2json": lacel.cfg2json,
        "json2cfg": lacel.json2cfg,
        "lpl2txt": lacel.lpl2txt,
        "bar2img": lacel.bar2img,
        "img2bar": lacel.img2bar
    }

commands_str = str(sorted(tuple(commands.keys())))

for char in "[]()":
    commands_str = commands_str.replace(char, "")


help_text = \
    f"""Łoś assets converter
----------------------------------------------------------------------
Łac (Łoś assets converter) is based on Łacel.
Łacel is a library (package) written in Python 3 for assets and files conversions from the video game "Po prostu Łoś".
----------------------------------------------------------------------
Usage (as a batch command):
    {basename(sys_argv[0])} <command name> <input file> <output file> <*optional arguments>
----------------------------------------------------------------------
Command names: {commands_str}
----------------------------------------------------------------------
For further information read file "README.md". from Łacel documentation."""


def display_help():
    print(help_text+"\n")


if len(sys_argv) > 1:

    if not sys_argv[1] in commands.keys():
        if sys_argv[1] == "help":
            display_help()
            exit()
        raise NameError

    command = commands[sys_argv[1]]
    arguments = []

    if len(sys_argv) > 1:

        for argument in sys_argv[2:]:
            try:
                argument_new = json_loads(argument)
            except (TypeError, JSONDecodeError) as errtext:
                argument_new = argument
            arguments.append(argument_new)

        command(*arguments)
        print("Command has been executed successfully.")

else:
    display_help()


input("Press any key to continue ...")
