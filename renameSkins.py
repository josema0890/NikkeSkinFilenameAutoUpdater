import csv
import os
from dotenv import load_dotenv
from datetime import datetime

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

stringAim = str(os.getenv('STRING_AIM'))
stringCover = str(os.getenv('STRING_COVER'))
stringStanding = str(os.getenv('STRING_STANDING'))
underscoreSeparator = str(os.getenv('UNDERSCORE_SEPARATOR'))
stringPlatformPC = str(os.getenv('STRING_PLATFORM_PC'))
stringPlatformAndroid = str(os.getenv('STRING_PLATFORM_ANDROID'))

logsFilename = str(os.getenv('LOGS_FILENAME'))

skinsRenamedPC = 0
skinsRenamedAndroid = 0
filesFoundByName = 0
filesFoundByBinary = 0

logNewLines = ""

fechaActual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

#Maintain a log file to keep track of all the files renamed
def updateLogFile():
	global skinsRenamedPC, skinsRenamedAndroid, logNewLines

	#Read content of log file or create one if file doesn't exists
	try:
		with open(logsFilename, "a") as log:
			log.write(logData)
			log.write(logNewLines)
	except FileNotFoundError:
		with open(logsFilename, "w") as log:
			log.write(logData)
			log.write(logNewLines)


#Read the CSV and return all the data Format (FilenameToGetData, RowsToSkip, ColumnsToSkip)
def read_csv_file(filename, rowsToSkip, ColumnsToSkip):
	global logNewLines

	#print("Obtaining data from " + filename)
	#logNewLines += f"Obtaining data from {filename}\n"
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

androidData = read_csv_file(androidFilenameFile, skipRowsAndroid, skipColumnsAndroid)
pcData = read_csv_file(pcFilenameFile, skipRowsPC, skipColumnsPC)
characterCodesData = read_csv_file(characterCodesFile, skipRowsCC, skipColumnsCC)

#Obtain all the files in the folder of the PC or Android Skins
def obtainFilesOfFolder(folder):
	global logNewLines

	#logNewLines += f"Obtaining data from folder {folder}\n"
	filenames = []
	for path, _, files in os.walk(folder):
		for file in files:
			completePath = os.path.join(path, file)
			filenames.append(completePath)
	return filenames

#Rename all the files obtained before with the data obtained on the csv
def renameFilesOfFolder(filesDesiredFolder, dataToUse, platform):
	global skinsRenamedPC, skinsRenamedAndroid, filesFoundByName, filesFoundByBinary, logNewLines

	#Loop for renaming all the files inside the desired folder (Android or PC) 
	for file in filesDesiredFolder:
		fileToSearch = os.path.basename(file)
		fileFound = ""
		fileAlreadyRenamed = False

		for data in dataToUse:
			nameOfCharacter = data[0]
			oldFileName = data[4]
			newFileName = data[3]

			if fileToSearch == newFileName:
				fileAlreadyRenamed = True
				break

			if fileToSearch == oldFileName:
				fileFound = data
				break

		if fileAlreadyRenamed:
			continue

		if fileFound != "":
			try:
				pathOfSkin, oldFileName = os.path.split(file)
				oldFilePath = os.path.join(pathOfSkin, oldFileName)
				newFilePath = os.path.join(pathOfSkin, fileFound[3])
				#print(f'Renombrando {oldFileName} a {fileFound[3]} en {pathOfSkin}')
				#logNewLines += f'Renaming {oldFileName} to {fileFound[3]} at {pathOfSkin}\n'
				os.rename(oldFilePath, newFilePath)
				filesFoundByName += 1

				if platform == stringPlatformPC:
					skinsRenamedPC += 1
				elif platform == stringPlatformAndroid:
					skinsRenamedAndroid += 1

			except Exception as e:
				#print(f"Error al renombrar {oldFileName} a {fileFound[3]} en {pathOfSkin}")
				#print(f"ERROR: {e}")
				logNewLines += f"Error renaming {oldFileName} to {fileFound[3]} at {pathOfSkin}\n"
				logNewLines += f"ERROR: {e}\n"
				continue

		else:
			archivo = open(file, "rb")
			primerosBytes = archivo.read(4)
			hexadecimal = primerosBytes.hex().upper()

			characterCode = ""

			if hexadecimal == "4E4B4142":
				#print(f"{fileToSearch} es un fichero de nikke, voy a buscar su characterCode en los ficheros para ver si podemos actualizar nombre desfasado")
				#logNewLines += f"{fileToSearch} is a valid nikke file, searching characterCode and pose to try to force updating an old nikke file\n"

				archivo.seek(0)
				datosBinarios = archivo.read()
				archivo.close()

				for character in characterCodesData:
					#Almaceno el valor de characterCode del personaje en cuestión
					characterCode = character[0]

					# Obtengo el valor del numero de skins del personaje en cuestión
					#print(f"Obtengo todos los datos para el personaje {character[1]}")
					filteredData = [entry for entry in dataToUse if entry[0] == character[1]]
					numberOfSkins = 0

					for entry in filteredData:
						if character[1] == entry[0]:
							#print(f"{character[1]} {entry[0]}")
							number = int(entry[1])
							numberOfSkins = max(numberOfSkins, number)
						#print(f"{characterCode} - {character[1]} Nº Skins {numberOfSkins}")

					#print(f"{characterCode} - {character[1]} Nº Skins {numberOfSkins}")

					foundMatch = False  # Reiniciar la variable foundMatch en cada iteración del bucle externo

					for i in range(numberOfSkins + 1):
						iValue = str(i).zfill(2)
						#print(f"{characterCode} Number of Skin {valorI}")
						aimHEX = bytes(f"{characterCode}{underscoreSeparator}{stringAim}{underscoreSeparator}{iValue}", 'utf-8') #c170_aim_00
						coverHEX = bytes(f"{characterCode}{underscoreSeparator}{stringCover}{underscoreSeparator}{iValue}", 'utf-8') #c170_cover_00
						standingHEX = bytes(f"{characterCode}{underscoreSeparator}{iValue}{underscoreSeparator}", 'utf-8') #Valdria c170_00

						if datosBinarios.find(aimHEX) != -1:
							foundMatch = True  # Coincidencia encontrada, establecer la variable de control en True
							#print(f"He encontrado {character[1]} {str(aimHEX, 'utf-8')} en el fichero: {fileToSearch}")
							#logNewLines += f"Found {character[1]} {str(aimHEX, 'utf-8')} on file {fileToSearch}\n"

							filteredNewFileName = [entry for entry in dataToUse if entry[0] == character[1] and entry[2] == stringAim and entry[1] == str(i)]

							try:
								pathOfSkinBin, oldFileNameBin = os.path.split(file)
								oldFilePathBin = os.path.join(pathOfSkinBin, oldFileNameBin)
								newFilePathBin = os.path.join(pathOfSkinBin, filteredNewFileName[0][3])
								#print(f'Renombrando {oldFileName} a {fileFound[3]} en {pathOfSkin}')
								#logNewLines += f'Renaming {oldFileName} to {fileFound[3]} at {pathOfSkin}\n'
								os.rename(oldFilePathBin, newFilePathBin)

								filesFoundByBinary += 1

								if platform == stringPlatformPC:
									skinsRenamedPC += 1
								elif platform == stringPlatformAndroid:
									skinsRenamedAndroid += 1
							except Exception as e:
								#print(f"Error al renombrar {oldFileName} a {fileFound[3]} en {pathOfSkin}")
								#print(f"ERROR: {e}")
								logNewLines += f"Error renaming {file} to {filteredNewFileName[0][3]}\n"
								logNewLines += f"ERROR: {e}\n"
								continue

							break

						if datosBinarios.find(coverHEX) != -1:
							foundMatch = True  # Coincidencia encontrada, establecer la variable de control en True
							#print(f"He encontrado {character[1]} {str(coverHEX, 'utf-8')} en el fichero: {fileToSearch}")
							#logNewLines += f"Found {character[1]} {str(coverHEX, 'utf-8')} on file {fileToSearch}\n"

							filteredNewFileName = [entry for entry in dataToUse if entry[0] == character[1] and entry[2] == stringCover and entry[1] == str(i)]

							try:
								pathOfSkinBin, oldFileNameBin = os.path.split(file)
								oldFilePathBin = os.path.join(pathOfSkinBin, oldFileNameBin)
								newFilePathBin = os.path.join(pathOfSkinBin, filteredNewFileName[0][3])
								#print(f'Renombrando {oldFileName} a {fileFound[3]} en {pathOfSkin}')
								#logNewLines += f'Renaming {oldFileName} to {fileFound[3]} at {pathOfSkin}\n'
								os.rename(oldFilePathBin, newFilePathBin)

								filesFoundByBinary += 1

								if platform == stringPlatformPC:
									skinsRenamedPC += 1
								elif platform == stringPlatformAndroid:
									skinsRenamedAndroid += 1
							except Exception as e:
								#print(f"Error al renombrar {oldFileName} a {fileFound[3]} en {pathOfSkin}")
								#print(f"ERROR: {e}")
								logNewLines += f"Error renaming {file} to {filteredNewFileName[0][3]}\n"
								logNewLines += f"ERROR: {e}\n"
								continue

							break

						if datosBinarios.find(standingHEX) != -1:
							foundMatch = True  # Coincidencia encontrada, establecer la variable de control en True
							#print(f"He encontrado {character[1]} {str(standingHEX, 'utf-8')} en el fichero: {fileToSearch}")
							#logNewLines += f"Found {character[1]} {str(standingHEX, 'utf-8')} on file {fileToSearch}\n"
							
							filteredNewFileName = [entry for entry in dataToUse if entry[0] == character[1] and entry[2] == stringStanding and entry[1] == str(i)]

							try:
								pathOfSkinBin, oldFileNameBin = os.path.split(file)
								oldFilePathBin = os.path.join(pathOfSkinBin, oldFileNameBin)
								newFilePathBin = os.path.join(pathOfSkinBin, filteredNewFileName[0][3])
								#print(f'Renombrando {oldFileName} a {fileFound[3]} en {pathOfSkin}')
								#logNewLines += f'Renaming {oldFileName} to {fileFound[3]} at {pathOfSkin}\n'
								os.rename(oldFilePathBin, newFilePathBin)

								filesFoundByBinary += 1

								if platform == stringPlatformPC:
									skinsRenamedPC += 1
								elif platform == stringPlatformAndroid:
									skinsRenamedAndroid += 1
							except Exception as e:
								#print(f"Error al renombrar {oldFileName} a {fileFound[3]} en {pathOfSkin}")
								#print(f"ERROR: {e}")
								logNewLines += f"Error renaming {file} to {filteredNewFileName[0][3]}\n"
								logNewLines += f"ERROR: {e}\n"
								continue
							
							break

					if foundMatch:
						break  # Romper el bucle interno si se encontró una coincidencia

filesPCFolder = obtainFilesOfFolder(pcSkinsFolder)
filesAndroidFolder = obtainFilesOfFolder(androidSkinsFolder)

renameFilesOfFolder(filesPCFolder, pcData, stringPlatformPC)
renameFilesOfFolder(filesAndroidFolder, androidData, stringPlatformAndroid)

logData = "Execution at " + fechaActual + "\n\nSkins renamed by name: " + str(filesFoundByName) + ", by binary: " + str(filesFoundByBinary) + "\nSkins renamed for Android: " + str(skinsRenamedAndroid) + "\nSkins renamed for PC: " + str(skinsRenamedPC) + "\n"
updateLogFile()