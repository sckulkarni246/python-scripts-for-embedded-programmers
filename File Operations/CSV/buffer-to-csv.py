import csv

def data_logger_csv(buffer,fileName):
	with open(fileName,"w+") as my_csv:
		csvWriter = csv.writer(my_csv,delimiter=',')
		csvWriter.writerow(buffer)	
		
buff = []
for i in range(0,100):
	buff.append(i)

buffer = buff
	
print("Writing buffer to buffer.csv now...")
data_logger_csv(buffer,"buffer.csv")