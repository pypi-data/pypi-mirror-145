#: Created by Kavun Nuggihalli
#: Email: kavunnuggihalli@gmail.com
#: Website: https://kavunnuggihalli.com
class Inode:

	def __init__(self, plastron, id, title):
		#: All items have an idea this is a programmatic way to understand what that item represents
		self.id = id
		#: All items expect an association to the original total instance therefore it expects plastron to pass self
		self.plastron = plastron
		#: All items have a title
		self.title = title
		#: All items have a tape the default is that item
		self.type = "Item"
		#: All items have procedures the default is set to none
		self.procedure = None

	def add_procedure(self, procedure):
		"""
		This is a programmatic way to add a procedure to this objects instance variable called procedure
		"""
		self.procedure = procedure
