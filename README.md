FILE COMPARISON TOOL

About: This tool compared the reports generated from X-Crash software and gererates an output file listing the differences between the two reports. The reports consist of json and image files.

Standalone exe: Use the standalone file_comparison.exe to run the tool without installing any libraries. Use the config.txt file to specify folder paths and output path. Run the exe file and it will generate
an excel file with listed differnces at the output path. The file can be found here: https://1drv.ms/f/s!AjLRDKsmxWg9tAGn3lxstdtB04yh?e=EgT6F1

file_comparison.py: In order to use the python files we need to setup the python following python libraries which are being use by the tool.
  openpyxl, configparser , numpy, scipy, opencv, pyemf, PIL (pillow).

Once the libraries are install you can run the file_comparison.py file using python file_comparison.py. It also needs config.txt file where the folder paths and output path is stated.

