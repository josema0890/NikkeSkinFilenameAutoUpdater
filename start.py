import subprocess

def check_selenium():
    try:
        import selenium
        print("Selenium is already installed.")
    except ImportError:
        print("Selenium is not installed, runing pip install selenium...")
        subprocess.call(['pip', 'install', 'selenium'])
        print("Selenium successfully installed.")

def check_webdriver():
    try:
        from selenium import webdriver
        print("Webdriver is already installed")
    except ImportError:
        print("Webdriver is not installed, running pip install webdriver-manager")
        subprocess.call(['pip', 'install', 'webdriver-manager'])
        print("Webdriver-manager successfully installed.")

def check_dotenv():
    try:
        import dotenv
        print("Dotenv is already installed")
    except ImportError:
        print("Dotenv is not installed, runing pip install dotenv...")
        subprocess.call(['pip', 'install', 'python-dotenv'])
        print("Dotenv successfully installed.")

def downloadSpreadsheet():
    subprocess.call(['python', 'downloadSpreadsheet.py'])
        
# Check if we need to install Selenium and webdriver
check_selenium()
check_webdriver()
check_dotenv()
downloadSpreadsheet()
print("Spreadsheets downloaded, extracting the names and renaming the files")