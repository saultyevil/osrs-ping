# OldSchool Runescape Ping 

A Python script used to ping OldSchool RuneScape worlds. Currently works on macOS 
and Linux (?) operating systems, but doesn't currently work on Windows. Windows 
support will be added at a later date!

## Usage

python osrs-ping.py [-h] world_list [n_tests]

Currently, the allowed choice for world_list is:

* uk
* allworlds
* custom_list
* an integer for a single world

If the n_tests is not provided, it will default to n_tests = 5.
