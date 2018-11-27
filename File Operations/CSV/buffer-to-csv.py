import csv

def data_logger_csv(buffer,fileName):
	with open(fileName,"w+") as my_csv:
		csvWriter = csv.writer(my_csv,delimiter=',')
		csvWriter.writerow(buffer)	
		
buffer = []
for i in range(0,100):
	buffer.append(i)
	
print("Writing buffer to buffer.csv now...")
data_logger_csv(buffer,"buffer.csv")