# Arkive

Manage your music/audio collections.

## 1. Installation

A package with the same name is available in [pypi](https://pypi.org/project/arkive)

```
  $ pip install --user arkive
```

This package has been tested mainly on Windows 10 and Linux (Fedora 35), but it should work on all platforms since it
only makes use of cross-platform libraries. You may need to use "pip3", "python3 -m pip" or "python -m" when running on
other platforms, or different Python setups.

You can also use pipx to only make use of the cli app.

```
  $ pipx install arkive
```

## 2. General usage

```
$ arkive -h
usage: arkive [-h] [-V] <command> ...

optional arguments:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit

commands:
  <command>
    show         display actions collection inside a given folder.
    flat         flatten actions files inside a given folder.
    nest         nesting actions files inside a given folder.
```

As explained above, you can use one of 3 commands: show, flat and nest, and finally a positional argument indicating a
folder path.

### show

It will traverse the folders inside the given path and display a table of all the existing (with compatible audio
formats) files, showing artist, album and title.

```
$ arkive show ~/Music
```

### flat

The application will traverse all the subfolders and move the music files up to the given folder while changing their
name. The new name given to each file will be a concatenation of its artist, album and title.

*e.g.* .../folder/subfolder/myfile.mp3 -> .../folder/artist - album - title.mp3

**Note:** the new name will be sanitized to make sure the result is a valid filename.

```
$ arkive flat ~/Music
```

### nest

The application will traverse all the subfolders and move the music files up to the given folder while renaming name
organizing them in new subfolders. The names given to each file and folder structures will result from taking the artist
and album names for the folders, and track title for its name.

*e.g.* .../folder/subfolder/myfile.mp3 -> .../folder/artist/album/title.mp3

**Note:** the new names for each file and folder will be sanitized to make sure the result is a valid file/directory.

```
$ arkive nest ~/Music
```

#### Destination folder

An optional argument "-o/-output" may be used to change the destination directory for the audio files.

## 3. Web storage support (Experimental)

Additionally, arkive includes support for web storage with the same commands shown above. As of now, only pcloud service
is supported but other may be included in the future. To use a command with your pcloud account, pass the "--cloud" flag
followed by the name if the services (e.g. pcloud), and then your user credentials.

```
$ arkive show "/My Music" --cloud pcloud --username <USERNAME> --password <PASSWORD>
```

## 4. Side-effects

This implementation includes a "cleanup" procedure which removes empty sub-folders from the origin directory. This is a
personal decision due to its convenience, but it may be changed in the near future to remove them only under explicit
indication.