import xml.etree.ElementTree as ET

def find_leaf(deptree,leaf):
	tree = ET.parse(deptree)
	root = tree.getroot()
	retList = []
	for level in root.iter('Level'):
		if(level.find('First').text == leaf):
			print("Found %s and Last Name is %s" %(leaf,level.find('Last').text))
			
find_leaf('simple.xml','Jon')
find_leaf('simple.xml','Joffrey')
find_leaf('simple.xml','Robb')
