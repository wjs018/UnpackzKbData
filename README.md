# Unpack zKillboard Data

This is a bit of code that will unpack and condense a dump of kill information from zKillboard into an sqlite database. The most recent dump of over 28 million CREST verified kills can be found [here](http://eve-files.com/dl/275522) (torrent option recommended).

## Dependencies

* Python 2.7.x (Python 3 untested)

## Usage

Downloading the dump of kill information from zKillboard will give you a single 25.3 GB .tar file. The Unpack.py file will, unsurprisingly, unpack this .tar file into a specified location, but leaves the .tar intact. When unpacked, the .tar file contains 50 directories, each containing 1000 .gz files. Unpack.py then proceeds to unzip these .gz files into the final .json files with the kill information. The .gz files are then deleted for the sake of storage space. This unzipping process is done in parallel, utilizing multiple cores for the procedure. The locations of source files and destinations can be changed inside the '__main__' part of the program between the two block comments. Be warned, fully unpacked into .json files, this is 283 GB of drive space.

Once the kill information has been unpacked into .json files by Unpack.py, we can then parse through these and build our sqlite database. Fittingly, the BuildSQLite.py file will do this for us. The location of the source .json files as well as the desired location of the .sqlite database can be specified within the '__main__' part of the program between the block comments. Also in this part of the program, you can enable (default, recommended) or disable parallel processing. This would utilize multiple cores to speed up the parsing process. Parallelization can have dramatic effects in this process, especially when paired with having things stored on an SSD. Even with these optimizations, expect the full operation of parsing the kills to last over an hour. I don't have progress monitoring built into this program yet, but you can check the filesize of the .sqlite database that is being built for progress. The final size after all the files have been parsed is 3.63 GB.

Not all the data contained within the .json files is copied into the database. Notably, all the information relating to the killers is lost. The only things pertaining to the killers that is kept is the number of attackers, the damage taken, the killer's ship typeID, and the killer's ship name where by "killer" I mean the character that dealt the final blow. Detailed information such as name and affiliatioin is lost for the killer, and all information about the other attackers is lost. At a later time I might add this information into antother table if I have some use for it.

## Acknowledgements

Thanks to [zKillboard](https://github.com/zKillboard/zKillboard) and [Squizz Caphinator](https://twitter.com/squizzc) for publishing this data.

## Contact

* Walter Schwenger, wjs018@gmail.com
