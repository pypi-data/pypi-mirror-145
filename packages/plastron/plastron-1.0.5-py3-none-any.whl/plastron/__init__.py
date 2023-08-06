# Version of plastron
__version__ = "1.0.5"

import os, shutil
from . import mnode, inode, screen
from art import *

#: Created by Kavun Nuggihalli
#: Email: kavunnuggihalli@gmail.com
#: Website: https://kavunnuggihalli.com
class Plastron:
    """
    <br><p style="text-align: left;"><strong style="color: #000;"><img src="https://kavunnuggihalli.com/wp-content/uploads/2022/03/plastron.png" alt="" width="120" height="100" style="float: left; padding-right: 20px;" /> </strong></p> <h4 style="text-align: left;">A python shell development library</h4> <p style="text-align: left;"><span style="color: #000000;">Use plastron to create interactive shell applications automated using python.</span></p> <p style="text-align: left;"><span style="color: #000000;">Find tutorials and sample code here <a href="https://kavunnuggihalli.com/plastron"><span style="background-color: #4485b8; color: #fff; display: inline-block; padding: 2px 8px; font-weight: bold; border-radius: 5px;">Learn Plastron</span>&nbsp;</a></span></p>
    """

    #: Functionality to instantiate plastron
    def __init__(self, creator="Authors name", name="Shell name", description="A short description of this shell"):
        #: Access creator instance variable from your Plastron instance in order to change the name of the author of the shell application
        self.creator = creator
        #: Access the description instance variable in order to change the description of this shell application
        self.description = description
        #: Upon instantiating plastron a main menu/home menu will be created and attached to the instance
        self.main_menu = mnode.Mnode(self, "main", "Home")
        #: An instance of the screen class instantiated in the plastron class
        self.screen = screen.Screen(self)
        #: Debug mode is always False by default
        self.debug = False
        #: The name of the precheck being conducted
        self.precheck = ""
        #: A flag to determine if there were errors in prechecks
        self.prechecks_error = False
        #: OS command to get the dimensions on the terminal
        self.columns, self.lines = os.get_terminal_size()
        #: Instantiating a plastron object will automatically set a name
        self.set_name(name)
        #: An instance variable containing the current procedure to be executed
        self.current_procedure = None
        # Upon instantiating plastron you will also create a current menu the default is main menu
        self.current_menu = self.main_menu
        #: An instance variable that contains the current menu part as an array
        self.current_menu_path = []
        #: Upon instantiating plastron the main menu or the current menu will be appended to the current menu path
        self.current_menu_path.append(self.current_menu)
        #: A dictionary of all menus created upon instantiation
        self.menus = {}
        #: Adding the main menu to the dictionary of menus
        self.menus['main'] = self.main_menu

    def set_debug(self,value):
        """
        Set the debug variable for the shell's event loop. Set to False for production. Default is already false.
        """
        self.debug = value

    def item(self, id, title):
        """
        Plastron is fundamentally based off of two concepts and menu and items. Use the item method in order to instantiate class item. This allows you to create an object on the screen that when interfaced against will run a procedure that it is linked to. You have the ability to define what these procedures are and map them to the eye nose procedure local instance variable. For more information on items take a look at the items submodule class in plastron.
        """
        item = inode.Inode(self, id, title)
        return item

    def menu(self, id, title):
        """
        Plastron is fundamentally based off of two concepts a menu and items. The menu method helps plastron instantiate the class menu in order to create a menu object that is then appended to the plastron shell. Utilize this method to create your own menus.Provide an ID for the menu, a short unified way to understand what that menu does programmatically. Then provide a title in order to define the name of the menu itself. Let plastron manage the menu's tracking. For more information on menus take a look at the Menu submodule class and plastron.
        """
        menu = mnode.Mnode(self, id, title)
        self.menus[id] = menu
        return menu

    def set_name(self, title):
        """
        Allows you to set the name of your shell. An ASCII logo will automatically be generated.
        """
        self.name = title
        self.logo = self.screen.ascii_logo(title)

    def get_menus(self):
        """
        Returns all the menus as a dictionary
        """
        return self.menus

    def shell(self):
        """
        Shell is the launch command for plastron. Shell is an event loop using standard blocking IO. Shell is not an asynchronous event loop nor is intended to be one. The shell method will figure out what menu or item is currently being presented to the user then graphically represent that through the terminal/shell interface.
        """
        #: variables for the shell
        self.selected_number = 0
        #: variable for error messages
        self.error_message = None
        #: variable for debug messages
        self.debug_message = None

        if self.prechecks_error == False:
            while True:
                self.columns, self.lines = os.get_terminal_size()
                self.screen.clear()

                if self.debug == True:
                    if self.debug_message != None:
                        print(self.debug_message)
                        self.screen.line("=")
                        self.debug_message = None

                if self.current_menu.title != "Home":
                    print("0)[<] Go Back")
                    self.screen.line("-")

                #Reset varabiles each loop
                menu_item = 1
                items_start = 0
                items_end = 0

                # Print Remaing items
                menus = []
                items = []
                for item in self.current_menu.get_list():
                    if item.type == "Menu":
                        menus.append(str(menu_item)+") "+item.title)
                        menu_item += 1
                for item in self.current_menu.get_list():
                    if item.type == "Item":
                        items.append(str(menu_item)+") "+item.title)
                        menu_item += 1


                # Print Remaing items
                if len(menus) != 0:
                    print("Choose a menu:")
                    self.screen.line("-")
                for menu in menus:
                    print(menu)
                if len(items) != 0:
                    if len(menus) != 0:
                        self.screen.line("-")
                    print("Execute procedures:")
                    self.screen.line("-")
                for item in items:
                    print(item)

                # Get user input
                self.screen.line("=")
                if self.error_message != None:
                    print(self.error_message)
                    self.screen.line("=")
                    self.error_message = None

                # verify input is number in range
                try:
                    self.selected_number = int(input("Select a number: "))
                    # Check selection within range
                    if self.selected_number < 0 or self.selected_number >= menu_item:
                        self.error_message = "Try again..."

                    if self.selected_number == 0 and self.current_menu.title == "Home":
                        final = int(input("Press 0 again to exit..."))
                        if final == 0:
                            break

                except ValueError:
                    self.error_message = "Input was not acceptiable. Try again..."

                # Assume no errors above
                if self.error_message == None:

                    if self.selected_number == 0 and self.current_menu.title != "Home":
                        self.current_menu_path.pop()
                        self.current_menu = self.current_menu_path.pop()
                        self.current_menu_path.append(self.current_menu)

                    if self.selected_number != 0:
                        # If a menu is selected
                        item = self.current_menu.list[(self.selected_number-1)]
                        if item.type == "Menu":
                            self.current_menu = item
                            self.current_menu_path.append(item)

                        if item.type == "Item":
                            self.current_procedure = item
                            self.screen.clear()
                            item.procedure()
                            self.screen.line("_")
                            input("Done? Hit enter...")
        else:
            print(self.precheck)
