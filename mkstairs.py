#Copyright (C) 2015  Adrian Freund (freundTech)

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import copy

displayName = "Make Stairs"

inputs = ( 
    ("Direction (Top to bottom):", ("N->S", "E->W", "S->N", "W->E")),
    ("Stair Block:", "blocktype"),
    ("Ceiling Block:", "blocktype"),
    ("Wall Block:", "blocktype"),
    ("Room Height:", 3),
    ("Don't adjust Data Values:", False),
    
    ("Make Stairs MCEdit Filter by freundTech. Licenced under GPLv3+", "label"),
)

#Axis for better readability
x = 0 
y = 1
z = 2

#Stair BlockIDs
stairs = [
    53,     #Oak
    67,     #Cobblestone
    108,    #Brick
    109,    #Stone Brick
    114,    #Nether Brick
    128,    #Sandstone
    134,    #Spruce
    135,    #Birch
    136,    #Jungle
    156,    #Quartz
    163,    #Acacia
    164,    #Dark Oak
    180,    #Red Sandstone
]

#Slab BlockIDs
slabs = [
    44,     #All Stone
    182,    #Red Sandstone
    126,    #All Wood
]

#Datavalue bit for turing upside down
stairupsidedown = 0x4
slabupsidedown = 0x8

def perform(level, box, options):
    #Read inputs
    rotateblocks = not options["Don't adjust Data Values:"]
    roomheight = options["Room Height:"]
    stairblock = copy.copy(options["Stair Block:"])
    wallblock = copy.copy(options["Wall Block:"])
    ceilingblock = copy.copy(options["Ceiling Block:"])

    #Initiale direction dependend values
    if options["Direction (Top to bottom):"] == "N->S":
        start = [box.minx, box.maxy - roomheight - 2, box.minz]
        end = [box.maxx, box.miny, box.maxz]
        sidedir = x
        forwarddir = z

        if rotateblocks:
            if stairblock.ID in stairs:
                stairblock.blockData = 3
            if ceilingblock.ID in stairs:
                ceilingblock.blockData = 2 | stairupsidedown

    elif options["Direction (Top to bottom):"] == "E->W":
        start = [box.maxx-1, box.maxy - roomheight - 2, box.minz]
        end = [box.minx-1, box.miny, box.maxz]
        sidedir = z
        forwarddir = x

        if rotateblocks:
            if stairblock.ID in stairs:
                stairblock.blockData = 0
            if ceilingblock.ID in stairs:
                ceilingblock.blockData = 1 | stairupsidedown

    elif options["Direction (Top to bottom):"] == "S->N":
        start = [box.minx, box.maxy - roomheight - 2, box.maxz-1]
        end = [box.maxx, box.miny, box.minz-1]
        sidedir = x
        forwarddir = z

        if rotateblocks:
            if stairblock.ID in stairs:
                stairblock.blockData = 2
            if ceilingblock.ID in stairs:
                ceilingblock.blockData = 3 | stairupsidedown

    elif options["Direction (Top to bottom):"] == "W->E":
        start = [box.minx, box.maxy - roomheight - 2, box.minz]
        end = [box.maxx, box.miny, box.maxz]
        sidedir = z
        forwarddir = x

        if rotateblocks:
            if stairblock.ID in stairs:
                stairblock.blockData = 1
            if ceilingblock.ID in stairs:
                ceilingblock.blockData = 0 | stairupsidedown

    else:
        raise ValueError("This should never happen.\n please reinstall the filter.")

    #Check for slabs and adjust blockData
    flatstairs = False
    if rotateblocks:
        if stairblock.ID in slabs:
            stairblock.blockData = stairblock.blockData & ~slabupsidedown
            flatstairs = True
            isfulllayer = False
        if ceilingblock.ID in slabs:
            ceilingblock.blockData = ceilingblock.blockData | slabupsidedown
    
    #Check if walls should be build
    if wallblock.ID != 0:
        haswalls = True
        start[sidedir] += 1
        end[sidedir] -= 1
    else:
        haswalls = False

    height = start[y]
    blockpos = [None, None, None]
    for f in range(start[forwarddir], end[forwarddir], 1 if start[forwarddir] < end[forwarddir] else -1):
        #Check if finished
        if height < end[y]:
            break

        #Build walls
        if haswalls:
            for h in range(height, height+roomheight+2):
                blockpos[forwarddir] = f
                blockpos[y] = h
                blockpos[sidedir] = start[sidedir]-1
                level.setBlockAt(*(blockpos + [wallblock.ID]))
                level.setBlockDataAt(*(blockpos + [wallblock.blockData]))

                blockpos[sidedir] = end[sidedir]
                level.setBlockAt(*(blockpos + [wallblock.ID]))
                level.setBlockDataAt(*(blockpos + [wallblock.blockData]))
        
        for s in range(start[sidedir], end[sidedir], 1 if start[sidedir] < end[sidedir] else -1):
            #Build Stairs
            blockpos[forwarddir] = f
            blockpos[y] = height
            blockpos[sidedir] = s
            if flatstairs and stairblock.ID in slabs and isfulllayer:
                #Doubleslab ID is 1 less than slab ID
                level.setBlockAt(*(blockpos + [stairblock.ID-1]))
                level.setBlockDataAt(*(blockpos + [stairblock.blockData & ~slabupsidedown]))
            else:
                level.setBlockAt(*(blockpos + [stairblock.ID]))
                level.setBlockDataAt(*(blockpos + [stairblock.blockData]))

            #Clear room above stair
            for  h in range(height+1, height+roomheight+1):
                blockpos[forwarddir] = f
                blockpos[y] = h
                blockpos[sidedir] = s
                level.setBlockAt(*(blockpos + [0]))

            #Build Ceiling
            if ceilingblock.ID != 0:
                blockpos[forwarddir] = f
                blockpos[y] = height + roomheight + 1
                blockpos[sidedir] = s
                if flatstairs and stairblock.ID in slabs and not isfulllayer:
                    #Doubleslab ID is 1 less than slab ID
                    level.setBlockAt(*(blockpos + [ceilingblock.ID-1]))
                    level.setBlockDataAt(*(blockpos + [ceilingblock.blockData & ~slabupsidedown]))
                else:
                    level.setBlockAt(*(blockpos + [ceilingblock.ID]))
                    level.setBlockDataAt(*(blockpos + [ceilingblock.blockData]))

        #Move 1 block down
        if not flatstairs:
            height -= 1
        else:
            if not isfulllayer:
                height -= 1
            isfulllayer = not isfulllayer
