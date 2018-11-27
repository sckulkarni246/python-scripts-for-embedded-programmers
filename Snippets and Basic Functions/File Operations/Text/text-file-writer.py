def write_lines_to_file(filename,content):
	with open(filename,"a") as f:
		f.write("%s\n"%(content))
		
write_lines_to_file('write.txt','This is a line...')
write_lines_to_file('write.txt','This is a line as well...')