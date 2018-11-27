import csv

def conv_strlist_to_numlist(strlist):
	numlist = []
	for i in range(0,len(strlist)):
		numlist.append(int(strlist[i]))
	return numlist

def get_data_from_csv(logfile):
	datalist = []
	csvreadout = []
	numdatalist = []
	with open(logfile,'r') as f:
		reader = csv.reader(f)
		datalist = list(reader)
	for i in range(0,len(datalist)):
		templist = conv_strlist_to_numlist(datalist[i])
	return templist
	
mylist = get_data_from_csv('buffer.csv')
print(mylist)