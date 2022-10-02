# Łoś assets conversions external library

## Introduction

**Łoś assets conversions external library** (shortly "*Łacel*") is a library written in Python 3 for assets and files conversions from the video game "*Po prostu Łoś*".

**The library supports following versions of the game:**

(Original archive name) | (Executable file compilation date) | (Version number)

* `LosV1_03.zip`  2nd Jul 2002 `1.03`
* `los.zip`  31st Aug 2003 `2.01`
* `Los2.zip`  28th Sep 2003 `2.01`
* `Los_murek.zip`  11th May 2006  `2.01`

**The library supports following conversions:**

* `*.bar` &harr; `*.bmp`
* `*.bar` &harr; `*.png`
* `*.cfg` &harr; `*.json`
* `*.dat` &harr; folder/files
* `*.lpl` &harr; `*.txt`
* `*.pln` &harr; `*.json`
* `*.zpl` &harr; folder/files

## Installation

**Dependencies:**

Following programs and packages must be installed in order to use *Łacel*:

* [python 3](https://www.python.org/) (tested with python 3.10.5)
* python 3 built-in libraries:
  * [datetime](https://docs.python.org/3/library/datetime.html)
  * [json](https://docs.python.org/3/library/json.html)
  * [os](https://docs.python.org/3/library/os.html)
* [setuptools](https://pypi.org/project/setuptools/) (necessary only for `setup.py` script) (tested with setuptools 65.3.0)
* [Pillow](https://pypi.org/project/Pillow/) (tested with Pillow 9.2.0)

In order to install *Łacel* run the following command ([Git](https://git-scm.com/) is required):
```bash
pip3 install git+https://github.com/Mikulus6/lacel.git
```

You can also manually install all dependencies and paste the directory `lacel` into the directory `Lib\site-packages`.

## Documentation

### Functions

lacel.**arch2dir**(*archive_name*, *directory_name*)

> Reads content of a `.*dat` or `.*zpl` archive under given *archive_name* file path, extracts its content and saves all files and subfolders included in that archive under given *directory_name* file path.

lacel.**bar2bmp**(*bar_file_name*, *bmp_file_name*)

> Reads content of a `*.bar` image file under given *bar_file_name* file path, converts its content to a `*.bmp` image file data with colors palette `R5 G6 B5` and saves it as a `*.bmp` file under given *bmp_file_name* file path.

lacel.**bar2img**(*bar_file_name*, *image_file_name*, *set_black_to_alpha*=`False`)

> Reads content of a `*.bar` image file under given *bar_file_name* file path, converts its content to a Pillow Image Object with color pallete `R8 G8 B8` or `R8 G8 B8 A8` and saves it as a `*.bmp` or `*.png` file under given *image_file_name* file path.
> 
> If *set_black_to_alpha* is set to `True`, all black pixels will be replaced with transparent pixels.

lacel.**bmp2bar**(*bmp_file_name*, *bar_file_name*)

> Reads content of a `*.bmp` image file with colors palette `R5 G6 B5` under given *bmp_file_name* file path, converts its content to `*.bar` image data and saves it as a `*.bar` file under given *bar_file_name* file path.

lacel.**cfg2json**(*cfg_file_name*, *json_file_name*)

> Reads content of a `*.cfg` file under given *cfg_file_name* file path, converts its content to a human-readable list and saves it as a `*.json` file under given *json_file_name* file path.

lacel.**dir2arch**(*directory_name*, *archive_name*)

> Reads content of a directory under given *directory_name* file path and archives its content to a `.*dat` or `.*zpl` archive under given *archive_name* file path.
> 
> Headers of archived files do not contain folder name in their names.
> 
> Empty directories will not be archived.

lacel.**img2bar**(*image_file_name*, *bar_file_name*)

> Reads content of a `*.bmp` or `*.png` file image file under given *image_file_name* file path, converts its content to a Pillow Image Object with color pallete `R5 G6 B5` and saves it as a `*.bar` file under given *bar_file_name* file path. 

lacel.**json2cfg**(*json_file_name*, *cfg_file_name*)

> Reads content of a specific `*.json` file under given *json_file_name* file path, converts its content to `*.cfg` file data and saves it as a `*.cfg` file under given *cfg_file_name* file path.

lacel.**json2pln**(*json_file_name*, *pln_file_name*)

> Reads content of a specific `*.json` file under given *json_file_name* file path, converts its content to a `*.pln` file data and saves it as a `*.pln` file under given *pln_file_name* file path.

lacel.**list2arch**(*files_list*, *archive_name*, *remove_base_dirs_from_names*=`False`, *remove_all_dirs_from_names*=`False`)

> Reads content of each file path included in list under given *files_list* object and archives theirs content to a `.*dat` or `.*zpl` archive under given *archive_name* file path.
> 
> If *remove_base_dirs_from_names* is set to `True`, headers of archived files will not contain the highest folder names from given file paths.
> 
> If *remove_all_dirs_from_names* is set to `True`, headers of archived files will contain only the name of given archived files. This option consequently removes any potential directories inside the archive.
> 
> Empty directories will not be archived.

lacel.**lpl2txt**(*lpl_file_name*, *txt_file_name*)

> Reads content of an `*.lpl` file under given *lpl_file_name* file path and copies it to `*.txt` file under given *txt_file_name* file path without any data conversion.

lacel.**pln2json**(*pln_file_name*, *json_file_name*)

> Reads content of a `*.pln` file under given *pln_file_name* file path, converts its content to a human-readable list and saves it as a `*.json` file under given *json_file_name* file path.

lacel.**txt2lpl**(*txt_file_name*, *lpl_file_name*)

> Reads content of a `*.txt` file under given *txt_file_name* file path and copies it to `*.lpl` file under given *lpl_file_name* file path with potential encoding fixes from `ANSI`, `ASCII` or `UTF-8` to `Windows-1250`.
> 
> Encoding correction may not always work.

### Json structure

Each point/subpoint in following section describes one element of list/sublist included in specific `*.json` file.

#### `*.json` converted from `*.cfg`:

* Key value "*W LEWO*" (left) (<u>each key value can be an integer or a specific string in encoding `Windows-1250` displayed in game settings. All string values for keys are in file `lacel/data/keys.json`</u>)
* Key value "*W PRAWO*" (right)
* Key value "*W GÓRĘ*" (up)
* Key value "*W DÓŁ*" (down)
* Key value "*PURCHAWA*" (puffball / bomb)
* Highscores
  * First record data
    * 1st record numeric value
    * names list (current 1st record holder name and all potential corrupted names)
  * Second record data 
    * 2nd record numeric value
    * names list (current 2nd record holder name and all potential corrupted names)
  * **[...]** 
  * Tenth record data 
    * 10th record numeric value
    * names list (current 10th record holder name and all potential corrupted names)
* Last played level numeric value
* Sound volume numeric value
* String with garbage data represented by hexadecimal digits
* `*.cfg` file creation time (formatted as `yyyy.mm.dd HH:MM:SS.SSSSSSS` in [Gregorian Calendar](https://en.wikipedia.org/wiki/Gregorian_calendar) and [Coordinated Universal Time](https://en.wikipedia.org/wiki/Coordinated_Universal_Time))
* Key value "*PAUZA*" (pause)
* Key value "*HARAKIRI*" (suicide)
* (<u>Optional</u>) Last played package data
  * Last played package name
  * Two empty bytes
  * String of garbage data represented by hexadecimal digits
* (<u>Optional</u>) Music volume numeric value
* (<u>Optional</u>) Key value "*ZMIANA MUZYCZKI*" (music change)

##### Corrupted names in `*json` converted from `*.cfg`.

Config files can contain more than one name per record data.  
Whenever a new name with `n` characters is saved to the config file, first `n` bytes are overwritten with certain characters and `n+1`th byte is set to null value. All remaining bytes hold their previous values which may contain older and longer names corrupted by newer and shorter names.  
All corrupted bytes are saved as `\u0000` in `*.json` files.


#### `*.json` converted from `*.pln`:

* Stage width numeric value
* Stage height numeric value
* Stage content
  * First tile data
    * 1st tile numeric value (without including water bit)
    * 1st tile water bit
  * Second tile data
    * 2nd tile numeric value (without including water bit)
    * 2nd tile water bit
  * **[...]** 
  * Last tile data
    * Last tile numeric value (without including water bit)
    * Last tile water bit
* Required cones numeric value
* Camera blockades data
  * First blockade data
    * 1st blockade numeric value (without including horizontal bit)
    * 1st blockade horizontal bit
  * Second blockade data
    * 2nd blockade numeric value (without including horizontal bit)
    * 2nd blockade horizontal bit
  * **[...]** 
  * Last blockade data (<u>Maximum number of camera blockades is 10</u>)
    * Last tile numeric value (without including horizontal bit)
    * Last blockade horizontal bit
* Camera blockades breakpoint (<u>should always be equal to 0</u>)
* String encoded in encoding `Windows-1250` with stage name (<u>Maximal number of characters is 20</u>)

##### 9th byte interpretation

When reading and writing tile data or blockade data in `*.pln` files, water bit and horizontal bit values are based on 9th bit of numeric value.  
If 9th bit is set to `1`, number `2^15` will be subtracted from numeric value and separated bool value will be set to `true` in `*.json` file. Otherwise, number `2^15` will not be subtracted and separated bool value will be set to `false` in `*.json` file.  
Therefore while editing `*.json` file content, numeric value describing tile or blockade cannot have 9th bit set to `1` while separated bool value is set to `false`.

### Color conversion

While using **bar2img()** and **img2bar()** functions, primary colors are converted between `R5 G6 B5` and `R8 G8 B8` in a way described below by given formulas:

`R5 G6 B5` &rarr; `R8 G8 B8`:
* `red :=  round(red * 255/31)`
* `green := round(green * 255/63)`
* `blue := round(blue * 255/31)`

`R8 G8 B8` &rarr; `R5 G6 B5`:
* `red :=  round(red * 31/255)`
* `green := round(green * 63/255)`
* `blue := round(blue * 31/255)`

### Text conversion

In order to avoid incorrect text conversion while using **json2cfg()**, **json2pln()** and **txt2lpl()** all `*.txt` and `*.json` flies should be saved in encoding `Windows-1250`.

It is recommended to use [Notepad++](https://notepad-plus-plus.org/) or similar application while reading or editing `*.json` files.

## Examples

Unpack all textures from an archive `bary/bary.dat` and save them as `*.png` files.

```python
import lacel
import os

lacel.arch2dir("bary/bary.dat", "bary_new")

for filename in os.listdir("bary_new"):

    file_path = os.path.join("bary_new", filename)

    if os.path.isfile(file_path) and filename[-4:] == ".bar":

        new_filename = filename.replace(".bar", ".png")
        new_file_path = os.path.join("images", new_filename)

        lacel.bar2img(file_path, new_file_path)
```

Print in-game timer initial values from stages from an archive `plansze/los1.dat`.

```python
import json
import lacel
import os

lacel.arch2dir("plansze/los1.dat", "plansze/los1_stages")

for filename in os.listdir("plansze/los1_stages"):

    file_path = os.path.join("plansze/los1_stages", filename)

    if os.path.isfile(file_path) and filename[-4:] == ".pln":

        new_filename = filename.replace(".pln", ".json")
        new_file_path = os.path.join("plansze/los1_stages/jsons", new_filename)

        lacel.pln2json(file_path, new_file_path)

        file = open(new_file_path)
        json_data = json.load(file)
        in_game_time = json_data[4]
        file.close()

        print(filename + " time = "+str(in_game_time)+"s")
input()
```

Reset highscores in a file `los.cfg`.

```python
import json
import lacel

lacel.cfg2json("los.cfg", "los.json")

file = open("los.json", 'r')
json_data = json.load(file)
file.close()
highscores_data = json_data[5]

for index_counter in range(len(highscores_data)):
    json_data[5][index_counter] = [0, ["---"]]

file = open("los.json", 'w')
file.write(json.dumps(json_data))
file.close()

lacel.json2cfg("los.json", "los.cfg")
```

## Credits

*Łacel* was created by *Mikołaj Walc* aka. "*Mikulus*" ([GitHub profile](https://github.com/Mikulus6)).

This library is a fan-made tool. It is not affiliated with the official legacy of the video game "*Po prostu Łoś*".

For an archived version of the official "_Po prostu Łoś_" website, visit [*baroslaw.republika.pl* via *web.archive.org*](https://web.archive.org/web/20180320052703/http://www.baroslaw.republika.pl/).
