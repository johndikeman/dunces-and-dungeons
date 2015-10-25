def monster(arg):
	if isinstance(arg,entity.monster.monsters.Monster):
		return True
	return False

def monster_modifier(arg):
	if isinstance(arg,entity.monster.monster_modification.ModifyMons):
		return True
	return False

def weapon(arg):
	if isinstance(arg,entity.item.weapon.Weapon):
		return True
	return False

