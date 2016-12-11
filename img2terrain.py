#img2terrain by freundTech

import os
import mcplatform
import pygame
import numpy
import math
import time
import datetime

displayName = "Image2Terrain"

inputs = (
	("Image Mode:", ("Height-Map", "Color-Map")),
	("Terrain Mode:", ("Fill", "Surface")),
	("Image path:", ("string","value=None")),
	("Invert Height-Map:", False),
	("Rotation:", ("0", "90", "180", "270"))
	)

colors = (
	([1, 0], [125, 125, 125]), #Stone
	([1, 1], [153, 113, 98]), #Granite
	([1, 2], [159, 114, 98]), #Smooth Granite
	([1, 3], [179, 179, 182]), #Diorite
	([1, 4], [183, 183, 185]), #Smooth Diorite
	([1, 5], [130, 131, 131]), #Andesite
	([1, 6], [133, 133, 134]), #Smooth Andesite
	([3, 1], [119, 85, 59]), #Coarse Dirt
	([3, 2], [90, 63, 28]), #Podzol
	([4, 0], [122, 122, 122]), #Cobblestone
	([5, 0], [156, 127, 78]), #Oak Planks
	([5, 1], [103, 77, 46]), #Spruce Planks
	([5, 2], [195, 179, 123]), #Birch Planks
	([5, 3], [154, 110, 77]), #Jungle Planks
	([5, 4], [169, 91, 51]), #Acacia Planks
	([5, 5], [61, 39, 18]), #Dark Oak Planks
	([12, 0], [219, 211, 160]), #Sand
	([12, 1], [169, 88, 33]), #Red Sand
	([13, 0], [126, 124, 122]), #Gravel
	([19, 0], [194, 195, 84]), #Sponge
	([22, 0], [38, 67, 137]), #Lapis Lazuli Block
	([23, 0], [96, 96, 96]), #Dispencer
	([24, 0], [218, 210, 158]), #Sandstone
	([25, 0], [100, 67, 50]), #Noteblock
	([35, 0], [221, 221, 221]), #White Wool
	([35, 1], [219, 125, 62]), #Orange Wool
	([35, 2], [179, 80, 188]), #Magenta Wool
	([35, 3], [106, 138, 201]), #Lightblue Wool
	([35, 4], [177, 166, 39]), #Yellow Wool
	([35, 5], [65, 174, 56]), #Lime Wool
	([35, 6], [208, 132, 153]), #Pink Wool
	([35, 7], [64, 64, 64]), #Gray Wool
	([35, 8], [154, 161, 161]), #Light Gray Wool
	([35, 9], [46, 110, 137]), #Cyan Wool
	([35, 10], [126, 61, 181]), #Purple Wool
	([35, 11], [46, 56, 141]), #Blue Wool
	([35, 12], [79, 50, 31]), #Brown Wool
	([35, 13], [53, 70, 27]), #Green Wool
	([35, 14], [150, 52, 48]), #Red Wool
	([35, 15], [25, 22, 22]), #Black Wool
	([41, 0], [249, 236, 78]), #Gold Block
	([42, 0], [219, 219, 219]), #Iron Block
	([43, 0], [159, 159, 159]), #Double Stone Slab
	([45, 0], [146, 99, 86]), #Brick
	([48, 0], [103, 121, 103]), #Mossy Cobblestone
	([49, 0], [20, 18, 29]), #Obsidian
	([57, 0], [97, 219, 213]), #Diamond Block
	([80, 0], [239, 251, 251]), #Snow Block
	([82, 0], [158, 164, 176]), #Clay
	([87, 0], [111, 54, 52]), #Netherrack
	([88, 0], [84, 64, 51]), #Soul Sand
	([89, 0], [143, 118, 69]), #Glowstone
	([98, 0], [122, 122, 122]), #Stone Bricks
	([98, 1], [114, 119, 106]), #Mossy Stone Bricks
	([98, 2], [118, 118, 118]), #Cracked Stone Bricks
	([99, 0], [202, 171, 120]), #Inside Mushroom Block
	([99, 15], [207, 204, 194]), #Stem Mushroom Block
	([99, 14], [141, 106, 83]), #Brown Mushroom Block
	([100, 14], [182, 37, 36]), #Red Mushroom Block
	([103, 0], [151, 153, 36]), #Melon
	([110, 0], [111, 99, 105]), #Mycelium
	([112, 0], [44, 22, 26]), #Nether Brick
	([121, 0], [221, 223, 165]), #End Stone
	([133, 0], [81, 217, 117]), #Emerald Block
	([152, 0], [171, 27, 9]), #Redstone Block
	([155, 0], [236, 233, 226]), #Quartz Block
	([155, 1], [231, 228, 219]), #Quartz Block Chiseled
	([159, 0], [209, 178, 161]), #White Stained Clay
	([159, 1], [161, 83, 37]), #Orange Stained Clay
	([159, 2], [149, 88, 108]), #Magenta Stained Clay
	([159, 3], [113, 108, 137]), #Light Blue Stained Clay
	([159, 4], [186, 133, 35]), #Yellow Stained Clay
	([159, 5], [103, 117, 52]), #Lime Stained Clay
	([159, 6], [161, 78, 78]), #Pink Stained Clay
	([159, 7], [57, 42, 35]), #Gray Stained Clay
	([159, 8], [135, 106, 97]), #Light Gray Stained Clay
	([159, 9], [86, 91, 91]), #Cyan Stained Clay
	([159, 10], [118, 70, 86]), #Purple Stained Clay
	([159, 11], [74, 59, 91]), #Blue Stained Clay
	([159, 12], [77, 51, 35]), #Brown Stained Clay
	([159, 13], [76, 83, 42]), #Green Stained Clay
	([159, 14], [143, 61, 46]), #Red Stained Clay
	([159, 15], [37, 22, 16]), #Black Stained Clay
	([168, 0], [99, 152, 141]), #Prismarine
	([168, 1], [99, 160, 143]), #Prismarine Bricks
	([168, 2], [59, 87, 75]), #Dark Prismarine
	([169, 0], [172, 199, 190]), #Sea Lantern
	([172, 0], [150, 92, 66]), #Hardend Clay
	([173, 0], [18, 18, 18]), #Coal Block
	([174, 0], [165, 194, 245]), #Packed Ice
	([179, 0], [166, 85, 29]) #Red Sandstone
)
	
	
def getNearColor(r, g, b):
	nearest = [1, 0]
	nearDist = 256
	for block in colors:
		dist = math.sqrt(math.pow(block[1][0]-r, 2)*0.21 + math.pow(block[1][1]-g, 2)*0.72  + math.pow(block[1][2]-b, 2)*0.07)

		if dist < nearDist:
			nearest = block[0]
			nearDist = dist
	return nearest


def rotate(img, width, height, nWidth, nHeight, degrees):
	print("rotating")
	degrees += 90
	rotImg = numpy.empty([nWidth, nHeight, 3])
	if degrees == 90:
		for r in range(width):
			for c in range(height):
				rotImg[c][width-r-1] = img[r][c]
	elif degrees == 270:
		for r in range(width):
			for c in range(height):
				rotImg[height-c-1][r] = img[r][c]
	elif degrees == 180:
		for r in range(width):
			for c in range(height):
				rotImg[width-r-1][height-c-1] = img[r][c]
	elif degrees == 0 or degrees == 360:
		rotImg = img
	print("finished rotating")
	return rotImg

def perform(level, box, options):
	startTime = time.time()
	
	mode = options["Image Mode:"]
	tmode = options["Terrain Mode:"]
	imgpath = options["Image path:"]
	invert = options["Invert Height-Map:"]
	rotation = int(options["Rotation:"])

	lDiff = box.maxy - box.miny

	if imgpath != "None":
		if os.path.exists(imgpath):
			image_path = imgpath
		else:
			image_path = mcplatform.askOpenFile(title="Select an Image", schematics=False)
	else:
		image_path = mcplatform.askOpenFile(title="Select an Image", schematics=False)
	if image_path == None:
		raise Exception("No file selected!")
		return
	image = pygame.image.load(image_path)
	(imgHeight, imgWidth) = image.get_size()

	selHeight = box.maxz - box.minz
	selWidth = box.maxx - box.minx

	

	imageData = numpy.fromstring(pygame.image.tostring(image, "RGB"),dtype=numpy.uint8).reshape(imgWidth,imgHeight,3)

	if rotation == 0 or rotation == 180:
		newHeight = imgWidth
		newWidth = imgHeight
	else:
		newHeight = imgHeight
		newWidth = imgWidth
	
	rotationTime = time.time()
	
	imageData = rotate(imageData, imgWidth, imgHeight, newWidth, newHeight, rotation)

	afterRotationTime = time.time()


	
	scaleZ = newHeight / selHeight
	scaleX = newWidth / selWidth

	size = selHeight * selWidth
	print(str(size) + " blocks to process!")
	genTime = time.time()
	
	
	for x in range(box.minx, box.maxx):
		progress = round(float((x-box.minx)*selHeight) / size * 100, 0)
		print(str(progress) + "% done.")
		for z in range(box.minz, box.maxz):
			imgX = round((x-box.minx) * scaleX, 0)
			imgZ = (round((z-box.minz) * scaleZ, 0)-(newHeight/2-0.5))*(-1)+(newHeight/2-0.5)
			
			if mode == "Height-Map":
				block = 1
				blockData = 0
				for y in range(box.miny, box.maxy):
					if level.blockAt(x, y, z) != 0:
						block = level.blockAt(x, y, z)
						blockData = level.blockDataAt(x, y, z)
				color = imageData[imgX, imgZ, 0] * 0.21 + imageData[imgX, imgZ, 1] * 0.72 + imageData[imgX, imgZ, 2] * 0.07
				if invert:
					color = (color - 127.5) * (-1) + 127.5
				theight = int(round((color / 255) * lDiff + box.miny, 0))
				#if theight <= 0:
				#	theight = 1
				if tmode == "Fill":
					for y in range(box.miny, theight):
						level.setBlockAt(x, y, z, block)
						level.setBlockDataAt(x, y, z, blockData)
				elif tmode == "Surface":
					level.setBlockAt(x, theight, z, block)
					level.setBlockDataAt(x, y, z, blockData)
			elif mode == "Color-Map":
				block = getNearColor(imageData[imgX, imgZ, 0], imageData[imgX, imgZ, 1], imageData[imgX, imgZ, 2])
				if tmode == "Fill":
					for y in range(box.miny, box.maxy):
						if level.blockAt(x, y, z) != 0:
							level.setBlockAt(x, y, z, block[0])
							level.setBlockDataAt(x, y, z, block[1])
				elif tmode == "Surface":
					for y in range(box.maxy, box.miny):
						if level.blockAt(x, y, z) != 0:
							level.setBlockAt(x, y, z, block[0])
							level.setBlockDataAt(x, y, z, block[1])
							break
							
	
	afterGenTime = time.time()


	print("Execution started at " + datetime.datetime.fromtimestamp(startTime).strftime('%Y-%m-%d %H:%M:%S') + " (" + str(startTime) + ").")
	print("Rotation started at " + datetime.datetime.fromtimestamp(rotationTime).strftime('%Y-%m-%d %H:%M:%S') + " (" + str(rotationTime) + ").")
	print("Preperation took " + str(datetime.timedelta(seconds=rotationTime-startTime)))

	print("Rotation finished at " + datetime.datetime.fromtimestamp(afterRotationTime).strftime('%Y-%m-%d %H:%M:%S') + " (" + str(afterRotationTime) + ").")
	print("Rotation took " + str(datetime.timedelta(seconds=afterRotationTime-rotationTime)))

	print("Terrain generation started at " + datetime.datetime.fromtimestamp(genTime).strftime('%Y-%m-%d %H:%M:%S') + " (" + str(genTime) + ").")

	print("Terrain generation finished at " + datetime.datetime.fromtimestamp(afterGenTime).strftime('%Y-%m-%d %H:%M:%S') + " (" + str(afterGenTime) + ").")
	print("Terrain generation took " + str(datetime.timedelta(seconds=afterGenTime-genTime)))
	print("Total execution took " + str(datetime.timedelta(seconds=afterGenTime-startTime)))
