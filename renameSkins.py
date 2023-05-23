import csv
import os
from dotenv import load_dotenv

#Obtain the variables saved on .env file
load_dotenv()

skipColumnsAndroid = int(os.getenv('SKIP_COLUMNS_ANDROID'))
skipColumnsPC = int(os.getenv('SKIP_COLUMNS_PC'))
skipColumnsCC = int(os.getenv('SKIP_COLUMNS_CC'))

skipRowsAndroid = int(os.getenv('SKIP_ROWS_ANDROID'))
skipRowsPC = int(os.getenv('SKIP_ROWS_PC'))
skipRowsCC = int(os.getenv('SKIP_ROWS_CC'))

androidFilenameFile = str(os.getenv('ANDROID_FILENAMES_CSV'))
pcFilenameFile = str(os.getenv('PC_FILENAMES_CSV'))
characterCodesFile = str(os.getenv('CHARACTER_CODES_CSV'))

androidSkinsFolder = str(os.getenv('ANDROID_SKINS_FOLDER'))
pcSkinsFolder = str(os.getenv('PC_SKINS_FOLDER'))

numberOfSkins = 0

#Format (FilenameToGetData, RowsToSkip, ColumnsToSkip)
def read_csv_file(filename, rowsToSkip, ColumnsToSkip):
	print("Obtaining data from " + filename)
	data = []
    
	with open(filename, 'r') as file:
		reader = csv.reader(file)
        
		#Skip empty data
		for _ in range (rowsToSkip):
			next(reader)

		#Read the data from CharacterCodes.csv	
		for column in reader:

			#Get rid of empty columns
			column = column[ColumnsToSkip:]
			data.append(column)
	return data

#Para buscar el número máximo de skins que tiene el personaje, obtener el nombre usando el CharacterCode en characterCodesData y en androidData
#o pcData buscar los datos que coincidan ese nombre y obtener el número máximo que haya en skin version

androidData = read_csv_file(androidFilenameFile, skipRowsAndroid, skipColumnsAndroid)
pcData = read_csv_file(pcFilenameFile, skipRowsPC, skipColumnsPC)
characterCodesData = read_csv_file(characterCodesFile, skipRowsCC, skipColumnsCC)

#print(pcData)

#Filtrar por la nikke Emma para este ejemplo, tenendo en cuenta el comentario de buscar el número máximo de skins 3 (0,1 y 2)
filteredData = [entry for entry in androidData if entry[0] == "Emma"]

for entry in filteredData:
	number = int(entry[1])
	numberOfSkins = max(numberOfSkins, number)


print(filteredData)
print("Number of skins for Emma " + str(numberOfSkins))