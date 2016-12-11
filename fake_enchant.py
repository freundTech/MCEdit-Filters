# This is a modified version of the Enchant Filter by SethBling

from pymclevel import MCSchematic
from pymclevel import TileEntity
from pymclevel import TAG_Compound
from pymclevel import TAG_String
from pymclevel import TAG_List

displayName = "Fake Enchant"	

inputs = (
	("Effect", ("string","value=")),
	("Level", (1, -127, 127)),
)

def perform(level, box, options):
	effect = options["Effect"]
	lvl = options["Level"]
	
	displvl = ""
	if lvl == 1:
		displvl = "I"
	elif lvl == 2:
		displvl = "II"
	elif lvl == 3:
		displvl = "III"
	elif lvl == 4:
		displvl = "IV"
	elif lvl == 5:
		displvl = "V"
	elif lvl == 6:
		displvl = "VI"
	elif lvl == 7:
		displvl = "VII"
	elif lvl == 8:
		displvl = "VIII"
	elif lvl == 9:
		displvl = "IX"
	elif lvl == 10:
		displvl = "X"
	else:
		displvl = "enchantment.level." + str(lvl)
	

	lore = u"\u00A77" + effect + " " + displvl

	for (chunk, slices, point) in level.getChunkSlices(box):
		for te in chunk.TileEntities:
			x = te["x"].value
			y = te["y"].value
			z = te["z"].value

			if x < box.minx or x >= box.maxx:
				continue
			if y < box.miny or y >= box.maxy:
				continue
			if z < box.minz or z >= box.maxz:
				continue

				
			if "Items" in te:
				for item in te["Items"]:
					if "tag" not in item:
						item["tag"] = TAG_Compound()
					if "ench" not in item["tag"]:
						item["tag"]["ench"] = TAG_List()
					if "display" not in item["tag"]:
						item["tag"]["display"] = TAG_Compound()
					if "Lore" not in item["tag"]["display"]:
						item["tag"]["display"]["Lore"] = TAG_List()
					
					item["tag"]["display"]["Lore"].append(TAG_String(lore))
						
					

						
					chunk.dirty = True
				
