import subprocess

def checkLibraries():
    subprocess.call(['python', 'checkLibraries.py'])

def downloadSpreadsheets():
    return subprocess.call(['python', 'downloadSpreadsheet.py'])

def renameSkins():
    subprocess.call(['python', 'renameSkings.py'])
        
# Check if we need to install Selenium, Webdriver Manager and Python DotEnv
checkLibraries()

#Download all the spreadsheets needed by the programm and check if we downloaded correctly or the download failed and stop the programm
statusCode = downloadSpreadsheets()

if statusCode == -1:
    print("Error downloading the files in downloadspreadsheet")
else:
    print("Files downloaded correctly, statusCode is " + str(statusCode))
    print("TODO: Stop the program if the download fails")
    
print("Spreadsheets downloaded, extracting the names and renaming the files (Here we will execute renameSkins())")