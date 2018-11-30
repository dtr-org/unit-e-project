# Developing using CLion

CLion is an IDE by JetBrains for C/C++ development. Unfortunately, CLion lacks support for the GNU Autotools suite, which is very popular among OpenSource projects and also used by unit-e core. CLion used CMake as a build system. It is possible, with a bit of switching between terminal/command line and your IDE, to enjoy the usability of CLion while still using the autotools based build for building.

## Importing the Project

The project is built using GNU autotools, and CLion does not have support for that.
In order to import the project nicely into CLion, one needs have a CMakeLists.txt.
A small script can auto-generate a basic CMakeLists.txt for you:

    contrib/cmake/gen-cmakelists.sh

The paths are adjusted for macOS; in Linux you might need to adapt that script.

## Configuring `clang-format`

`clang-format` can be configured as an external tool in CLion. The unit-e project is already setup with code style definitions in `.clang-format` files.

clang-format can be obtained via `npm install -g clang-format` (`brew install npm` on macOS if you do not have npm).

To use `clang-format` from within CLion:

1. Go to `CLion → Preferences` (macOS) / `File → Settings` (linux/win)
2. Look for `External Tools` (search for it or navigate to `Tools → External Tools`)
3. Add a tool by pressing the `+` button in the lower left corner of the settings window
4. In the `Create Tool` dialog
   1. Choose a `Name` (for example "clang-format", this is what will appear in your `External Tools` menu)
   2. Program: `clang-format`
   3. Arguments: `-i $FileName$ -style=file`
   4. Working Directory: `$FileDir`
5. `OK` your way out

You can now use `clang-format` from the `Tools → External Tools` menu or via the `External Tools` menu in the context menu.
