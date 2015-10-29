import base,random
import entity.monster.monster_modification as mo
import entity.item.weapon_modification as wm
import entity.item.armor_modification

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
		Mod = {
			"Common":
				[wm.Common,
				wm.Iron,
				wm.Rusty,
				wm.Used,
				wm.Weathered,
				wm.Wooden,
				wm.Notched,
				wm.Scratched],
			 "Uncommon":
				[wm.Good,
				 wm.Shining,
				 wm.Steel,
				 wm.Archaic,
				 wm.Brutal],
			 "Rare":
				[wm.Ceremonial,
				 wm.Silver,
				 wm.Killing,
				 wm.Blessed],
			 "Legendary":
				[wm.Kingly,
				 wm.Enchanted,
				 wm.Master],
			 "Divined":
				[wm.Celestial,
				wm.Divine,
				wm.Heavenly,
				wm.Arch]
			 }
		rander=random.random()*100
		mylist = []
		if(rander<76):
			mylist=Mod["Common"]
		elif(rander<91):
			mylist=Mod["Uncommon"]
		elif(rander<99):
			mylist=Mod["Rare"]
		elif(rander<99.99):
			mylist=Mod["Legendary"]
		else:
			mylist=Mod['Divine']
		namer = random.choice(mylist)
		modification_instance = namer()
		Item.modifiers.append(modification_instance)

		Item.name="%s %s" % (modification_instance.to_str(), Item.name)
		return Item
