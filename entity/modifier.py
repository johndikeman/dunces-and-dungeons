import base,random
import entity.monster.monster_modification as mo
import entity.item.weapon_modification as wm
import entity.item.armor_modification as ar


class Apply(object):
	def __init__(self):
		self.monster_modifiers = [mo.Acidic,mo.Camphoric,mo.Caustic,mo.Dank,mo.Decaying,mo.Destructive,mo.Dieing,mo.Dusty,mo.Fetid,mo.Flowery,mo.Forgotten,mo.Foul,mo.Funky,mo.Lightning,mo.Lowly,mo.Musky,mo.Nasty,mo.Normal,mo.Putrid,mo.Rancid,mo.Scorched,mo.Tiny,mo.Weak]

# the size of this method was reduced by 1,460%, lol
	def modify_monster(self,Monster):
		mod = random.choice(self.monster_modifiers)()
		Monster.modifiers.append(mod)
		mod.apply()
		Monster.name = "%s %s" % (mod.to_str(),Monster.name)
		return Monster

	# lol this method will work for armor too cause theyre the exact same modifiers
	def modify_armor(self,Item):
		Mod = {}
		# i sincerely apologize about this 
		Mod = {
			"Common":
				[ar.Iron,
				ar.Rusty,
				ar.Used,
				ar.Weathered,
				ar.Wooden,
				ar.Notched,
				ar.Scratched],
			 "Uncommon":
				[ar.Good,
				 ar.Shining,
				 ar.Steel,
				 ar.Archaic,
				 ar.Brutal],
			 "Rare":
				[ar.Ceremonial,
				 ar.Silver,
				 ar.Killing,
				 ar.Blessed],
			 "Legendary":
				[ar.Kingly,
				 ar.Enchanted,
				 ar.Master],
			 "Divined":
				[ar.Celestial,
				ar.Divine,
				ar.Heavenly,
				ar.Arch]
			 }
			
		return self.decide(Mod,Item)

	def modify_weapon(self,Item):
		Mod = {
			"Common":
				[wm.Iron,
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
		return self.decide(Mod,Item)

	def decide(self,Mod,Item):
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
		modification_instance.apply()
		Item.name="%s %s" % (modification_instance.to_str(), Item.name)
		return Item
