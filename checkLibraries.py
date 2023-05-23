import subprocess

def check_selenium():
    try:
        import selenium
        print("Selenium is already installed.")
    except ImportError:
        print("Selenium is not installed, runing pip install selenium...")
        result = subprocess.call(['pip', 'install', 'selenium'], capture_output=True)
        if result.code == 0:
            print("Selenium successfully installed.")
        else:
            print("Failed to install Selenium. Error: ", result.stderr.decode())

def check_webdriver():
    try:
        from selenium import webdriver
        print("Webdriver-manager is already installed")
    except ImportError:
        print("Webdriver-manager is not installed, running pip install webdriver-manager")
        result = subprocess.call(['pip', 'install', 'webdriver-manager'], capture_output=True)
        if result.code == 0:
            print("Selenium successfully installed.")
        else:
            print("Failed to install Selenium. Error: ", result.stderr.decode())

def check_dotenv():
    try:
        import dotenv
        print("Dotenv is already installed")
    except ImportError:
        print("Dotenv is not installed, runing pip install dotenv...")
        result = subprocess.call(['pip', 'install', 'python-dotenv'], capture_output=True)
        if result.code == 0:
            print("Selenium successfully installed.")
        else:
            print("Failed to install Selenium. Error: ", result.stderr.decode())