import pandas as pd

def extract_data_from_excel_doc(filename):
	data_names = []
	data_id = []
	sheetData = pd.read_excel(filename,sheet_name=0)
	data_names = sheetData['Name'].tolist()
	data_id = sheetData['ID'].tolist()
	print(data_names)
	print(data_id)
	
extract_data_from_excel_doc('Data.xlsx')