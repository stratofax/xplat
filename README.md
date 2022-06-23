# Xplat

## Cross-platform Python tools for batch file management and conversion at the command line

Created with Python 3.9, this package uses the [pathlib module, Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html), introduced in Python 3.4

## Getting Started

1. Create a fork of this repo on your computer.
2. Ensure that `poetry` is installed on your computer: `poetry --version`
3. In the root directory of this project, run `poetry install` to ensure you have all the required packages
4. Start the virtual environment: `poetry shell`
5. Run `xplat --help` for a list of subcommands and options.
6. (Optional) Run `xplat --install-completion` with the name of your shell (bash, zsh, fish, etc.) to enable tab completion.

## Bugs and Testing

If the steps described above in the **Getting Started** section worked for you, you'll also be able to run the `pytest` test suite. Simply enter:

```bash
pytest
```

If you find an error, please report it by tweeting @stratofax with the hastag `#xplatbug`. You can also tweet @stratofax if you have any questions or suggestions about this project -- just use the `xplat` hashtag. Please note that I won't reply to DMs.

## Subcommands

The `xplat` utility offers several useful sub-commands (or, more simply, _commands_). Here's the latest list, from `xplat --help`

```bash
Commands:
  info   Display platform information.
  list   List files in the specified directory.
  names  Convert names of multiple files for internet compatibility.
  pdfs   Convert PDF files to image files (formats: JPEG, PNG, TIFF or PPM).
```

### info

Display platform information, from Python's perspective. Useful for troubleshooting and debugging. Sample output from a Mac M1 mini:

```bash
➤ xplat info

-- Platform Information --------------------
macOS-12.4-arm64-arm-64bit

-- System Information ----------------------
System:          Darwin
Node:            My-Mac-mini.local
Release:         21.5.0
Version:         Darwin Kernel Version 21.5.0: Tue Apr 26 21:08:29 PDT 2022; root:xnu-8020.121.3~4/RELEASE_ARM64_T8101
Machine:         arm64

-- Python Information ----------------------
Python Branch:                 (not found)
Python Compiler:               Clang 13.1.6 (clang-1316.0.21.2)
Python Implementation:         CPython
Python Revision:               (not found)
Python Version:                3.9.13

-- macOS Information -----------------------
macOS Version:                 12.4
```

### list

List files in the specified directory. Especially useful to see which files you'll modify with any of the other conversion commands, since it uses the same file listing code as the other commands.

Here are some samples:

```bash
# list all the files (no directories) in your home directory
xplat list ~

# list all pdf files in ~/Downloads -- note the ext is case-sensitive
xplat list ~/Downloads/ --ext pdf
```

## names

Convert names of multiple files for internet compatibility; specifically:

* Replace spaces with underscores ("_").
* Replace all periods with underscores ("_").
* Convert all characters to lower case.

Here are some samples:

```bash
# Use the "dry run" option to preview name conversion for all the files in the ~/Downloads directory
xplat names --source-dir ~/Downloads/ --dry-run

# move and rename all the pdf files in ~/Downloads to ~/temp
xplat names --source-dir ~/Downloads/ --output-dir ~/temp/ --ext pdf
```

### pdfs

Convert PDF files to bitmap image files. Supported output formats:

* JPEG
* PNG
* TIFF
* PPM

Here are some samples:

```bash
# convert all the pdfs in ~/temp to png files in ~/temp/png
# full color images, 512 pixels wide
xplat pdfs --source-dir ~/temp/ --output-dir ~/temp/png/ --image-ext png --full-color --width=512

# convert all the pdfs in ~/temp to png files in ~/temp/png
# black & white (grayscale) images, 512 pixels wide
xplat pdfs --source-dir ~/temp/ --output-dir ~/temp/png/ --image-ext png --no-full-color --width=512
```

## FAQ

Some questions and answers about the `xplat` utility.

### Why doesn't xplat do X?

I've added the different features as I've needed them for my web development work. If you'd like to suggest a new feature, simply tweet @stratofax -- just use the `xplat` hashtag, and you can contact me this way if you have any questions or suggestions about this project. Please note that I won't reply to DMs.

New features that have a wide appeal, or work well when processing more than one file, will be considered before obscure features that you can already perform on a single file using an existing tool.

If you really want to see a new feature, fork this repo, create a branch, and start coding! Even better, send me a tweet (@stratofax) with the hashtag `#xplat` and I'll open an issue for your new code.

### I can already do this thing using another program on my favorite computer. Why would I want to use xplat?

Because:

* You might want to perform the same types of conversions to a larger group of files, not just one, and xplat is designed to process a directory's worth of files.
* You'd like to automate your workflow instead of opening a graphics program and making the same changes over and over again by hand.
* You have to switch from one type of computer to another and the program you used to use for converting files is not available / crazy expensive / no fun to use on the new platform.
* You want to contribute to open source.

### I can't code, but I want to help! What can I do?

* If you find a bug, let us know: please report it by tweeting @stratofax with the hastag `#xplatbug`, and we'll open an issue to track the bug, especially if we can reproduce it.
* You can help improve the documentation, by writing, editing, or creating diagrams.
* You can help translate the program to a different language.

If you want to learn how to code Python, a great place to start is by writing `pytest` tests. These tests are incredibly helpful for the project, as they will ensure the program doesn't break when we add new features. Writing tests is a great way to learn how the code works.

If you're having trouble writing a test, it may be because the code you're trying to test isn't well written. Contact us and let us know how we can make our code better.

If these options, or any others appeal to you, contact us by tweeting @stratofax with the hashtag `#xplat`.

### Why is xplat so slow?

Because xplat is written as a cross-platform tool, not all of the code has been compiled and optimized for your specific platform. Having said that, if you're using `xplat` to process hundreds, or thousands, of files, let us know how you're using the program and perhaps we'll code up some optimizations or add multi-threaded execution to speed things up for you.

In general, though, `xplat` was designed to run through a set of files without intervention, after you've selected your options and answered a few prompts. You can just let it run in the background or overnight while you do something else.

Note that `xplat` also uses some compiled helper programs, which help speed up code execution. In the future, we may compile sections of xplat to improve performance.
