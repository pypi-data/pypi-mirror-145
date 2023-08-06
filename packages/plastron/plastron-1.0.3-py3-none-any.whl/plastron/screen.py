import os
from art import *
import shutil

#: Created by Kavun Nuggihalli
#: Email: kavunnuggihalli@gmail.com
#: Website: https://kavunnuggihalli.com
class Screen:

    def __init__(self, plastron):
        """
        The screen class is used to create objects that are then render to the screen this class will be able to create lines tables and more complex items in the future for now it is utilized by the main plastron class in order to generate all the required screen based outputs initialization of the screen class create multiple colors and text options such as bold and underline
        """
        #: An instance of screen needs a reference to the original plastron instance therefore it expects that the plastron instance passes self
        self.plastron = plastron
        #: All screens have titles the default title is set to screen
        self.title = "screen"
        #: Purple
        self.PURPLE = '\033[95m'
        #: CYAN
        self.CYAN = '\033[96m'
        #: Dark Cyan
        self.DARKCYAN = '\033[36m'
        #: Blue
        self.BLUE = '\033[94m'
        #: Green
        self.GREEN = '\033[92m'
        #: Yellow
        self.YELLOW = '\033[93m'
        #: Red
        self.RED = '\033[91m'
        #: Bold
        self.BOLD = '\033[1m'
        #: Underline
        self.UNDERLINE = '\033[4m'
        #: End
        self.END = '\033[0m'

    def clear(self):
        """
        This method allows you to clear the screen regardless of the operating system you are using this technology with. This method will also print the logo extend some lines to the dimensions of the current terminal upon refresh then show what running procedure exists.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_logo()
        self.line("=")
        self.print_creator(self.plastron.creator)
        self.print_description(self.plastron.description)
        self.line("=")
        self.print_menu_path(self.plastron.current_menu_path)
        self.line("=")

        if self.plastron.current_procedure != None:
            print(self.add_style("Running procedure: ", self.BOLD)+self.plastron.current_procedure.title)
            self.line("=")
            self.plastron.current_procedure = None

    def ascii_logo(self, title):
        """
        This method allows you to generate ASCII based character sets with the provided import string
        """
        self.logo = text2art(title)
        return self.logo

    def print_logo(self):
        """
        This is a method that allows you to print the Asci-based logo
        """
        print(self.logo)

    def print_menu_path(self, menu):
        """
        This method allows you to print a menu based on passing the actual object with a menu class
        """
        str = ""
        if len(menu) == 1:
            for item in menu:
                str = item.title
        else:
            for item in menu:
                str += item.title +" > "
            str = str[:len(str) - 3]
        print(self.add_style("Menu Path: ", self.BOLD)+str)

    def print_creator(self,creator):
        """
        A method to Print the creator of the shell
        """
        print(self.add_style("Designed by: ", self.BOLD)+creator)

    def print_description(self,description):
        """
        A method to print the description of the shell
        """
        print(self.add_style("Description: ", self.BOLD)+description)

    def title(self, title):
        """
        A method to print the title of the shell
        """
        tprint(title, font="cybermedum")

    def text(self, text):
        """
        A simple print method
        """
        print(text)

    def header(self):
        """
        A method to print the header of the shell
        """
        print(self.logo)

    def line(self, type="-"):
        """
        A method to print a line the default is a "–" pass any character. This method will print the line based on the dimensions of the shell upon drawing the screen.

        """
        self.line_string = ""
        self.logo_width = 0
        for i in self.logo:
            self.logo_width += 1
            if '\n' in i:
                break
        for i in range(0,self.plastron.columns):
            self.line_string += type
        self.print_style(self.line_string, self.BOLD)

    def print_style(self,text,style):
        """
        This method allows you to print in a specific style
        """
        print(style + text + self.END)

    def add_style(self,text,style):
        """
        This method adds a style to text
        """
        return style + text + self.END

    # Create a line dark top
    def dark_line_top(self):
        """
        A method to print a line faced upwards
        """
        self.line("¯")

    # Create a line dark bottom
    def dark_line_bottom(self):
        """
        A method to print a lion face downwards
        """
        self.line("_")

    # Create a line dark bottom
    def thin_line(self):
        """
        A method to print a thin line
        """
        self.line("-")

    # Create a line dark bottom
    def wiggle_line(self):
        """
        A method to print a wiggly or squiggly line
        """
        self.line("~")

    # Create a thick light line
    def bubble_line(self):
        """
        A method to print bubbled lines
        """
        self.line("°")

    def create_table(self, cols):
        """
        A starter method in order to create tables
        """
        table = ""
        for col in cols:
            table += col +" | "
        return table

    def add_item_to_table(self, table, item):
        """
        A starter method in order to add items to tables
        """
        pass
