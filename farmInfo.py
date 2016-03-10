from defusedxml.ElementTree import parse
from PIL import Image 

# This is a test method for returning the position location and the name of objects
# located on the players farm.
# 
# returns a dict with an array of tuples of the form: (name, x, y)

def getFarmInfo(saveFileLocation):
	ns= "{http://www.w3.org/2001/XMLSchema-instance}"

	farm = {}

	root = parse(saveFileLocation).getroot()

	locations = root.find('locations').findall("GameLocation")
	# things = []
	s = []
	for item in locations[1].find('objects').iter("item"):
		name = item.find('value').find('Object').find('Name').text
		x = int(item.find('value').find('Object').find('tileLocation').find('X').text)
		y = int(item.find('value').find('Object').find('tileLocation').find('Y').text)
		# if name not in things:
		# 	things.append(name)
		s.append((name, x, y))

	# print(things)

	farm['objects'] = s

	s = []

	for item in locations[1].find('terrainFeatures').iter('item'):
		name = item.find('value').find('TerrainFeature').get(ns+'type')
		x = int(item.find('key').find('Vector2').find('X').text)
		y = int(item.find('key').find('Vector2').find('Y').text)
		s.append((name, x, y))

	farm['terrainFeatures'] = s

	s = []

	for item in locations[1].find('resourceClumps').iter('ResourceClump'):
		t = int(item.find('parentSheetIndex').text)
		x = int(item.find('tile').find('X').text)
		y = int(item.find('tile').find('Y').text)
		w = int(item.find('width').text)
		h = int(item.find('height').text)
		s.append((t,x, y, w, h))

	farm['resourceClumps'] = s

	s = []
	for item in locations[1].find('buildings').iter('Building'):
		name = item.find('buildingType').text 
		x = int(item.find('tileX').text)
		y = int(item.find('tileY').text)
		w = int(item.find('tilesWide').text)
		h = int(item.find('tilesHigh').text)
		s.append((name, x, y, w, h))

	farm['buildings'] = s

	return farm

def colourBox(x, y, colour, pixels, scale = 8):
	for i in range(scale):
		for j in range(scale):
			pixels[x*scale+ i, y*scale + j] = colour
	return pixels

# Renders a PNG of the players farm where one 8x8 pixel square is equivalent to one in game tile.
# Legend:	Shades of green - Trees, Weeds, Grass
# 		Shades of brown - Twigs, Logs
# 		Shades of grey - Stones, Boulders, Fences
# 		Dark red - Static buildings
# 		Light red - Player placed objects (Scarecrows, etc)
# 		Blue - Water
# 		Off Tan - Tilled Soil

def generateImage(farm):
	image = Image.open(".//data//img//base.png")
	pixels = image.load()

	pixels[1,1] = (255,255,255) 

	for building in farm['buildings']:
		for i in range(building[3]):
			for j in range(building[4]):
				colourBox(building[1] + i, building[2] + j, (255,150,150), pixels)

	for tile in farm['terrainFeatures']:
		name = tile[0]
		if name == "Tree":
			colourBox(tile[1], tile[2], (0,175,0), pixels)
		elif name == "Grass":
			colourBox(tile[1], tile[2], (0,125,0), pixels)
		elif name == "HoeDirt":
			colourBox(tile[1], tile[2], (196,196,38), pixels)
		elif name == "Flooring":
			colourBox(tile[1], tile[2], (50,50,50), pixels)
		else:
			colourBox(tile[1], tile[2], (0,0,0), pixels)

	for tile in farm['objects']:
		name= tile[0]
		if name == "Weeds":
			colourBox(tile[1], tile[2], (0,255,0), pixels)
		elif name == "Stone":
			colourBox(tile[1], tile[2], (125,125,125), pixels)
		elif name == "Twig":
			colourBox(tile[1], tile[2], (153,102,51), pixels)
		elif 'Fence' in name:
			colourBox(tile[1], tile[2], (200,200,200), pixels)
		else:
			colourBox(tile[1], tile[2], (255,0,0), pixels)

	for tile in farm['resourceClumps']:
		if tile[0] == 672:
			for i in range(tile[3]):
				for j in range(tile[3]):
					colourBox(tile[1] + i, tile[2] + j, (102, 51, 0), pixels)
		elif tile[0] == 600:
			for i in range(tile[3]):
				for j in range(tile[3]):
					colourBox(tile[1]+i, tile[2] + j, (75,75,75), pixels)

	return image

def main():
	generateImage(getFarmInfo('./save/Crono_116230451')).save('farm.png')

if __name__ == '__main__':
	main()