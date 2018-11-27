def read_lines_of_file(filename):
	with open(filename) as f:
		content = f.readlines()
		return content,len(content)
		
alltext,alltextlen = read_lines_of_file('read.txt')
for line in alltext:
	print(line.rstrip())
print("Number of lines read from file --> %d" %(alltextlen))