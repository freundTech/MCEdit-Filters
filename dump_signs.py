#Dump Signs by freundTech
#Feel free to use this filter and/or it's code for whatever you want, as long as you credit me.
#http://freundTech.ga

#Please not that this is a modified version of TexelElf's Dump Command Blocks Filter:
#http://elemanser.com/filters.html

from pymclevel import TAG_Byte, TAG_Int, TAG_Compound, TAG_String
import mcplatform

sorts = {"Y, X, Z":(1,0,2), "Y, Z, X":(1,2,0),"X, Y, Z":(0,1,2), "Z, Y, X":(2,1,0), "X, Z, Y":(0,2,1), "Z, X, Y":(2,0,1)}

inputs = (
	("Operation:",("Dump signs","Import signs dump")),
	("Sort signs by:",tuple(sorted(sorts.keys()))),
	("Dump only signs containing: (\"None\" to dump all)",("string","value=None")),
	("File path:",("string","value=None")),
	)

displayName = "Dump Signs"

signtypes = [None]*63+["standing"]+[None]*4+["wall"]

standingrot = [
	"south",
	"south-southwest",
	"southwest",
	"west-southwest",
	"west",
	"west-northwest",
	"northwest",
	"north-northwest",
	"north",
	"north-northeast",
	"northeast",
	"east-northeast",
	"east",
	"east-southeast",
	"southeast",
	"south-southeast"
	]

wallrot = [
	None,
	None,
	"north",
	"south",
	"west", 
	"east"
	]


def strcollapse(lines):
	signs = []
	sign = []
	blockInfo = ""
	for l in lines:
		if not l:
			continue
		if l[0] == ";":
			continue
		if l[0] == "#":
			if blockInfo:
				signs.append((blockInfo, sign))
			blockInfo = l[1:].rstrip().decode("unicode-escape")
			sign = []
		else:
			if len(sign) < 4:
				sign.append(l.lstrip().rstrip().decode("unicode-escape"))
	else:
		signs.append((blockInfo, sign))
	
		
	return signs

def getText(e):
	return (e["Text1"].value.decode("unicode-escape"), e["Text2"].value.decode("unicode-escape"), e["Text3"].value.decode("unicode-escape"), e["Text4"].value.decode("unicode-escape"))

def perform(level, box, options):
	op = options["Operation:"]
	filterstr = options["Dump only signs containing: (\"None\" to dump all)"]
	filepath = options["File path:"]
	order = sorts[options["Sort signs by:"]]
	if op == "Dump signs":
		if filterstr == "None":
			filtersigns = False
		else:
			filtersigns = True
		signs = []
		for (chunk, _, _) in level.getChunkSlices(box):
			for e in chunk.TileEntities:
				x = e["x"].value
				y = e["y"].value
				z = e["z"].value
				if (x,y,z) in box:
					if e["id"].value == "Sign":
						bid = level.blockAt(x, y, z)
						bdata = level.blockDataAt(x, y, z)
						block = signtypes[bid]
						if bid == 63:
							rot = standingrot[bdata]
						elif bid == 68:
							rot = wallrot[bdata]
						else:
							continue
						if filtersigns:
							if e["Text1"].value.find(filterstr) != -1 or e["Text1"].value.find(filterstr) != -1 or e["Text2"].value.find(filterstr) != -1 or e["Text3"].value.find(filterstr) != -1 or e["Text4"].value.find(filterstr) != -1:
									signs.append(((x,y,z), getText(e), block, rot))
						else:
							signs.append(((x,y,z), getText(e), block, rot))

		signs.sort(key=lambda s: (s[0][order[0]], s[0][order[1]], s[0][order[2]]))
		outputlines = []
		for (coords, texts, block, rot) in signs:
			outputlines.append("#" + str(coords[0]) + "," + str(coords[1]) + "," + str(coords[2]) + ":" + block + ":" + rot + "\n")
			for text in texts:
				outputlines.append(str(text) + "\n")
			outputlines.append("\n")

		if filepath == "None":
			text_file = mcplatform.askSaveFile(mcplatform.lastSchematicsDir or mcplatform.schematicsDir, "Save Dumped Text File...", "", "Text File\0*.txt\0\0", "txt")
			if text_file == None:
				raise Exception("ERROR: No filename provided!")
		else:
			text_file = filepath
		file = open(text_file, "w")
		file.writelines(outputlines)
		file.close()

	else:
		if filepath == "None":
			text_file = mcplatform.askOpenFile(title="Select a Dumped Text File...", schematics=False)
			if text_file == None:
				raise Exception("ERROR: No filename provided!")
		else:
			text_file = filepath
		file = open(text_file, 'rb')
		filearray = file.readlines()
		file.close()
		signs = strcollapse(filearray)
		for idstr, texts in signs:
			coordstr, block, rot = idstr.split(":")
			cx, cy, cz = coordstr.split(",")
			cx = int(cx)
			cy = int(cy)
			cz = int(cz)
			bid = signtypes.index(block)
			if bid == 63:
				bdata = standingrot.index(rot)
			elif bid == 68:
				bdata = wallrot.index(rot)
			else:
				raise Exception("Rotation \"" + rot + "\" not found for " + block + " sign!")
			level.setBlockAt(cx, cy, cz, bid)
			level.setBlockDataAt(cx, cy, cz, bdata)
			chunk = level.getChunk(cx>>4, cz>>4)
			ent = level.tileEntityAt(cx,cy,cz)
			if ent != None:
				for num, text in enumerate(texts):
					ent["Text" + str(num+1)] = TAG_String(text)
				chunk.dirty = True
			else:
				sign = TAG_Compound()
				sign["id"] = TAG_String("Sign")
				sign["x"] = TAG_Int(cx)
				sign["y"] = TAG_Int(cy)
				sign["z"] = TAG_Int(cz)
				for num, text in enumerate(texts):
					sign["Text" + str(num+1)] = TAG_String(text)
				chunk.TileEntities.append(sign)
				chunk.dirty = True
