import base
import entity.monster.monster_modification as mo
import entity.item.weapon_modification
import entity.item.armor_modification
import random

class Apply(object):
	def __init__(self):
		self.monster_modifiers = [mo.Acidic,mo.Camphoric,mo.Caustic,mo.Dank,mo.Decaying,mo.Destructive,mo.Dieing,mo.Dusty,mo.Fetid,mo.Flowery,mo.Forgotten,mo.Foul,mo.Funky,mo.Lightning,mo.Lowly,mo.Musky,mo.Nasty,mo.Normal,mo.Putrid,mo.Rancid,mo.Scorched,mo.Tiny,mo.Weak]

# the size of this method was reduced by 1,460%, lol
	def modify_monster(self,Monster):
		mod = random.choice(self.monster_modifiers)()
		Monster.modifiers.append(mod)
		Monster.name = "%s %s" % (mod.to_str(),Monster.name)
		return Monster

	def modify_item(self,Item):
		Mod={"Common": {"Common ":1,
						"Iron ":1.1,
						"Rusty ":.5,
						"Used ":.8,
						"Weathered ":.7,
						"Wooden ":.5,
						"Notched ":.9,
						"Scratched ":.9},
			 "Uncommon":{"Good ":1.3,
			 			 "Shining ":1.4,
			 			 "Steel ":1.6,
			 			 "Archaic ":1.3,
			 			 "Brutal ":2},
			 "Rare":{"Ceremonial ":2.5,
			 		 "Silver ":2.4,
			 		 "Killing ":3,
			 		 "Blessed ":3.2},
			 "Legendary":{"Kingly ":4,
			 			  "Enchanted ":3.8,
			 			  "Master ":4.6},
			 "Divine": {"Celestial ":6,
			 			"Divine ":6.8,
			 			"Heavenly ":6.4,
			 			"Arch":8}
			 }
		rander=random.random()*100
		mymap={}
		if(rander<76):
			mymap=Mod["Common"]
		elif(rander<91):
			mymap=Mod["Uncommon"]
		elif(rander<99):
			mymap=Mod["Rare"]
		elif(rander<99.99):
			mymap=Mod["Legendary"]
		else:
			mymap=Mod['Divine']
		namer = random.choice(mymap.keys())
		run = mymap[namer]
		try:
			Item.damage=Item.damage*run
		except:
			try:
				Item.armor=Item.armor*run
			except:
				print "HELP ME BOBBY"
		Item.name=namer+Item.name
		return Item
