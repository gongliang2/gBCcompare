gBCcompare is a tool to compare two CSV file or binary files. It use the gBCviewer to display the content and the differences, which is also one of my projects.

Quick start:

* to run the python script you need numpy, CSV libraries and PyQt ect. Maybe the best way is that you just use one of the SciPy distributions like Anaconda, PythonXY, or WinPython. Once you have it intalled(WinPython don't need to be intalled.), just run the python script. For more information see https://www.scipy.org/install.html. gBCviewer is implemented and tested with Anaconda 4.3.0 on Windows.

* Once two files are opened to compare, differences between 2 files are marked with red background color. Yellow background color indicate the differences within a file.

* uncheck "diff" checkbox, if you don't want to see the differences marked with yellow background color.

* use "next Diff" or "last Diff" to navigate between differences between two files. We stop looking for further differece after we find one.

* clicking on "get all Diffs" will get all differences between 2 files. The statusbar will show the result.
