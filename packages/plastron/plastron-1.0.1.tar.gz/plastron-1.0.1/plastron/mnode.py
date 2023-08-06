#: Created by Kavun Nuggihalli
#: Email: kavunnuggihalli@gmail.com
#: Website: https://kavunnuggihalli.com
class Mnode:

	def __init__(self, plastron, id, title):
		#: How many years have an idea this it's a programmatic way for developers to understand what a menu is
		self.id = id
		#: All menus reference the plastron instance itself therefore it is expected that plastron will pass self
		self.plastron = plastron
		#: All menus are expected to have titles
		self.title = title
		#: This object type is a menu
		self.type = "Menu"
		#: Menus contain lists
		self.list = []

		try:
			self.back = self.plastron.main_menu
		except:
			pass

	def add_item(self,item):
		"""
		This method allows you to add an item to a menu an item in this sense can be either a menu or another item. Objects are stored in the menus list when accessed plastron will automatically parts whether the object is a menu or an item.
		"""
		self.list.append(item)

	def add_items(self,items):
		"""
		For convenience you can generate a list of items which can be either menus or item instances and append them all at once to the plastron menu list. This method is a programmatic way to add many items to a menu.
		"""
		for item in items:
			self.list.append(item)

	def get_list(self):
		"""
		This method allows you to get the list of the menu
		"""
		return self.list
