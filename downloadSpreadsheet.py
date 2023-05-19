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
AndroidFilenameFile = os.path.join(current_dir, str(os.getenv('ANDROID_CSV_FILENAMES')))
PCFilenameFile = os.path.join(current_dir, str(os.getenv('PC_CSV_FILENAMES')))

#Create Chrome options object, set the language to en-US and change the download folder
chrome_options = Options()
chrome_options.add_argument('--headless --lang=en-US')
chrome_options.add_experimental_option('prefs', {'download.default_directory': current_dir})

def downloadSpreadsheet(url):

	try:
		#Delete old files to avoid ending up with a XXXX(1).csv
		print("Deleting old files to avoid duplicates")
		if(os.path.exists(AndroidFilenameFile)):
			os.remove(AndroidFilenameFile)
		
		if(os.path.exists(PCFilenameFile)):
			os.remove(PCFilenameFile)

		#Open a selenium browser and download the files
		driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
		driver.get(url)

		#Obtain the Android/iOS.csv file
		print("Download Android/iOS Filenames")
		driver.find_element("id", "docs-file-menu").click()
		driver.find_element(By.CLASS_NAME, "docs-icon-editors-ia-download").click()
		driver.find_element(By.XPATH, "//*[@aria-label[contains(., '(.csv)')]]").click()

		# Wait until the file is completely downloaded
		WebDriverWait(driver, 10).until(
            lambda driver: any("Android" in filename for filename in os.listdir(current_dir))
        )

		#Rename the downloaded file to AndroidFilenames.csv
		androidPath = glob.glob(current_dir + "/*Android*.csv")

		for file_path in androidPath:
			directory, filename = os.path.split(file_path)

			new_filename = str(os.getenv('ANDROID_CSV_FILENAMES'))
			new_file_path = os.path.join(directory, new_filename)
			os.rename(file_path, new_file_path)

		#Obtain the PC .csv
		print("Download PC Filenames")
		driver.find_element(By.XPATH, "//*[text()='PC Models']").click()
		driver.find_element("id", "docs-file-menu").click()
		driver.find_element(By.CLASS_NAME, "docs-icon-editors-ia-download").click()
		driver.find_element(By.XPATH, "//*[@aria-label[contains(., '(.csv)')]]").click()

		# Wait until the file is completely downloaded
		WebDriverWait(driver, 10).until(
            lambda driver: any("PC" in filename for filename in os.listdir(current_dir))
        )

		#Rename the downloaded file to PCFilenames.csv
		androidPath = glob.glob(current_dir + "/*PC*.csv")

		for file_path in androidPath:
			directory, filename = os.path.split(file_path)

			new_filename = str(os.getenv("PC_CSV_FILENAMES"))
			new_file_path = os.path.join(directory, new_filename)
			os.rename(file_path, new_file_path)

		#Close the selenium browser
		driver.close()
		print("Files downloaded correctly")
	except Exception as e:
		print("Error trying to open google chromedriver")
		print(e)

downloadSpreadsheet(urlSpreadsheet)