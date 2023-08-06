#  Plastron
An interactive shell application  [Learn More](https://kavunnuggihalli.com/plastron/)
Build interactive, menu driven, shell programs using Python 3+

##  Getting started
The easiest way to get started with Plastron is to install the library from pip.

 1. `Create a file: shell.py`
 2. `pip install plastron`
 3. `from plastron import Plastron`

Here is sample code for a shell program with one menu to check disk space on the machine.

```
# An import we need
import os

# Import plastron module
from plastron import Plastron

# A useful function
def useful_disk_free_check():
    os.system("df -h")

# Inatalize the shell
my_shell = Plastron("Kavun", "PLASTRON", "A personal shell")

# Create a menu for this shell
metrics_menu = my_shell.menu("metrics","Metrics")

# Create an item for this menu to run the function
disk_item = my_shell.item("disk", "Disk check")

# Add the useful function to the item's procedure
disk_item.add_procedure(useful_disk_free_check)

# Add the item to the menu
metrics_menu.add_item(disk_item)

# Add the new menu to the main menu
my_shell.menus['main'].add_item(metrics_menu)

# Launch the shell
my_shell.shell()
```
Now run `python shell.py`  you should see something like this:

<img src="https://kavunnuggihalli.com/wp-content/uploads/2022/04/plastron-use-item.png" alt="" width="100%" height="100%" style="float: left; padding-right: 20px;" />
