import base

class InventoryHandler(base.Entity):
	def __init__(self):
		super(InventoryHandler,self).__init__()
		self.options = ['inventory']

	def do_turn(self,option):
		if option == self.options[0]:
			go=True
			while(go):
				item_index=base.make_choice([a.to_str() for a in self.owner.inventory.list])
				item_object=self.owner.inventory[item_index]
				option_index=base.make_choice(item_object.item_options)
				item_opt=item_object.item_options[option_index]
				if item_opt=='examine':
					print 'Hey item_object.info need to finish this'
				if item_opt=='equip':						
					if item_object.info=='weapon':
						item_object.equip()
					elif item_object.info=='helmet':
						item_object.equip()
					elif item_object.info=='chest':
						item_object.equip()
					elif item_object.info=='legs':
						item_object.equip()
					elif item_object.info=='boots':
						item_object.equip()
					elif item_object.info=='amulet':
						item_object.equip()
					elif item_object.info=='gauntlet':
						item_object.equip()
					elif item_object.info == 'spell':
						item_object.equip()
					else:
						print "UNKNOWN ITEM CLASSIFICATION!!"
				print 'continue? (y/n)'
				ans = raw_input()
				if ans=='no':
					go=True
				else:
					go=False


