import os
import glob
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

#Obtain the variables saved on .env file
load_dotenv()

#Define the variables for the program execution
current_dir = os.path.dirname(os.path.abspath(__file__))
urlSpreadsheet = str(os.getenv('SPREADSHEET_URL'))
androidFilenameFile = os.path.join(current_dir, str(os.getenv('ANDROID_FILENAMES_CSV')))
pcFilenameFile = os.path.join(current_dir, str(os.getenv('PC_FILENAMES_CSV')))
characterCodesFile = os.path.join(current_dir, str(os.getenv('CHARACTER_CODES_CSV')))

#Create Chrome options object, set the language to en-US and change the download folder
chrome_options = Options()
chrome_options.add_argument('--headless --lang=en-US')
chrome_options.add_experimental_option('prefs', {'download.default_directory': current_dir})

def downloadSpreadsheet(url):

	try:
		#Delete old files to avoid ending up with a XXXX(1).csv
		print("Deleting old files to avoid duplicates")
		if(os.path.exists(androidFilenameFile)):
			os.remove(androidFilenameFile)
		
		if(os.path.exists(pcFilenameFile)):
			os.remove(pcFilenameFile)

		if(os.path.exists(characterCodesFile)):
			os.remove(characterCodesFile)

		#Open a selenium browser and download the files
		driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
		driver.get(url)

		#Obtain the Android/iOS.csv file
		print("Download Android/iOS Filenames")
		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "docs-file-menu")))
		driver.find_element("id", "docs-file-menu").click()
		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "docs-icon-editors-ia-download")))
		driver.find_element(By.CLASS_NAME, "docs-icon-editors-ia-download").click()
		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label[contains(., '(.csv)')]]")))
		driver.find_element(By.XPATH, "//*[@aria-label[contains(., '(.csv)')]]").click()

		#Wait until the file is completely downloaded
		WebDriverWait(driver, 10).until(
            lambda driver: any("Android" in filename and filename.endswith(".csv") for filename in os.listdir(current_dir))
        )

		#Rename the downloaded file to AndroidFilenames.csv
		androidPath = glob.glob(current_dir + "/*Android*.csv")

		for file_path in androidPath:
			directory, filename = os.path.split(file_path)

			os.rename(file_path, os.path.join(directory, str(os.getenv('ANDROID_FILENAMES_CSV'))))

		#Obtain the PC .csv
		print("Download PC Filenames")
		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[text()='PC Models']")))
		driver.find_element(By.XPATH, "//*[text()='PC Models']").click()
		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "docs-file-menu")))
		driver.find_element("id", "docs-file-menu").click()
		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "docs-icon-editors-ia-download")))
		driver.find_element(By.CLASS_NAME, "docs-icon-editors-ia-download").click()
		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label[contains(., '(.csv)')]]")))
		driver.find_element(By.XPATH, "//*[@aria-label[contains(., '(.csv)')]]").click()

		# Wait until the file is completely downloaded
		WebDriverWait(driver, 10).until(
            lambda driver: any("PC" in filename and filename.endswith(".csv") for filename in os.listdir(current_dir))
        )

		#Rename the downloaded file to PCFilenames.csv
		androidPath = glob.glob(current_dir + "/*PC*.csv")

		for file_path in androidPath:
			directory, filename = os.path.split(file_path)

			os.rename(file_path, os.path.join(directory, str(os.getenv("PC_FILENAMES_CSV"))))

		#Obtain the CharacterCodes.csv
		print("Download Character Codes")
		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Character Codes']")))
		driver.find_element(By.XPATH, "//*[text()='Character Codes']").click()
		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "docs-file-menu")))
		driver.find_element("id", "docs-file-menu").click()
		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "docs-icon-editors-ia-download")))
		driver.find_element(By.CLASS_NAME, "docs-icon-editors-ia-download").click()
		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label[contains(., '(.csv)')]]")))
		driver.find_element(By.XPATH, "//*[@aria-label[contains(., '(.csv)')]]").click()

		# Wait until the file is completely downloaded
		WebDriverWait(driver, 10).until(
            lambda driver: any("Character Codes" in filename and filename.endswith(".csv") for filename in os.listdir(current_dir))
        )

		#Rename the downloaded file to PCFilenames.csv
		androidPath = glob.glob(current_dir + "/*Character Codes*.csv")
		
		for file_path in androidPath:
			directory, filename = os.path.split(file_path)

			os.rename(file_path, os.path.join(directory, str(os.getenv("CHARACTER_CODES_CSV"))))

		#Close the selenium browser
		driver.close()
		print("Files downloaded correctly")
		programExitCode = 0
		return programExitCode

	except Exception as e:
		print("Error trying to open google chromedriver")
		print(e)
		return programExitCode

programExitCode = -1
downloadSpreadsheet(urlSpreadsheet)