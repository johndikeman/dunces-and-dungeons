import base

class InventoryHandler(base.Entity):
	def __init__(self):
		super(InventoryHandler,self).__init__()
		self.options = ['inventory']

	def do_turn(self,option):
		if option == self.options[0]:
			go=True
			while(go):
				mod_list = self.owner.inventory.get_list([self])
				item_index=base.make_choice([a.to_str() for a in mod_list])
				item_object=mod_list[item_index]
				option_index=base.make_choice(item_object.item_options)
				item_opt=item_object.item_options[option_index]
				if item_opt=='examine':
					# each item needs to define self.descr, which is what will be printed here.
					print item_object.examine()
				if item_opt=='equip':
					item_object.equip()


				# this isn't quiote implemented
				if item_opt == 'give':
					choice = base.make_choice(self.owner.party.inventory.get_list([self.owner]))
					other_player = self.owner.party.inventory.get_list([self.owner])[choice]


				print 'continue? (y/n)'
				ans = raw_input()
				if ans=='y':
					go=True
				else:
					go=False
