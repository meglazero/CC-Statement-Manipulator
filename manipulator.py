import sys, os, time, shutil

print("Credit card statement .txt to .csv converter. At any input break can enter q, quit, e, or exit to quit out.")
print("Originally created in 2023, updated in 2025")
time.sleep(1)

entireYear = False
singleFile = False
monthCheck = []
#if true just outputs text for debugging purposes
informational = False
TESTING_DELETES_FILES_FOLDER_BE_CAREFUL = False

if TESTING_DELETES_FILES_FOLDER_BE_CAREFUL == True:
    try:
        shutil.rmtree('Files/')
    except:
        print("Was no Files/ folder to remove")

monthList = ['January','February','March','April','May','June',
             'July','August','September','October','November','December']

dir_name = os.path.dirname(os.path.realpath(__file__))
directory = os.listdir(dir_name)
filesDirName = ""
filesDirectory = []

#print("Directory: {directory} | Directory Name: {dir_name}".format(directory = directory, dir_name = dir_name))

def scanFolder():
    dir_name = os.path.dirname(os.path.realpath(__file__))
    directory = os.listdir(dir_name)

    for i, x in enumerate(directory):
        if x == "Files":
            #print("found files directory")
            filesDirName = dir_name + "/" + x
            filesDirectory = os.listdir(dir_name+"/"+directory[i])
            break
        else:
            filesDirName = ""
            filesDirectory = []
    #print("Within scanFolder(): ")        
    #print("Directory: {directory} | Directory Name: {dir_name}".format(directory = directory, dir_name = dir_name))
    return filesDirName, filesDirectory, dir_name, directory

filesDirName, filesDirectory, dir_name, directory = scanFolder()
'''for i, x in enumerate(directory):
    if x == "Files":
        #print("found files directory")
        filesDirName = dir_name + "/" + x
        filesDirectory = os.listdir(dir_name+"/"+directory[i])
'''

def quitApp(uInput):
    if (uInput.lower() == 'e' or 
        uInput.lower() == 'exit' or
        uInput.lower() == 'q' or
        uInput.lower() == 'quit'):
        sys.exit()

def missingFiles():
    print('Directory is likely not set up to run, would you like to load test files or exit?')
    option = input("(T)est or (E)xit: ")

    quitApp(option)
    if (option.lower() == 'test' or option.lower() == 't'):
        #will need to add an option for pdf vs txt when I get around to it
        choice = 't'
        #choice = input("PDF or TXT file?: ")
        #find a way to copy demofile.txt to dir_name/Files/someyear/somemonth.txt
        if (choice.lower() == 't' or choice.lower() == 'txt' or choice.lower() == 'text'):
            import datetime
            try:
                if not os.path.isdir('Files'):
                    os.makedirs('Files')
            except:
                input("Could not make 'Files' folder")
                quitApp('q')
            
            variableYear = str(datetime.datetime.now().year)
            myPath = 'Files/' + variableYear
            try:
                if not os.path.isdir(myPath):
                    os.makedirs(myPath)
            except:
                input("Couldn't make {path} directory for some reason".format(path=myPath))
                quitApp('q')

            try:
                source_file_path = dir_name+'/demofile.txt'
                source_file = open(source_file_path, 'rb')
            except:
                input("Could not open the source file")
                quitApp('q')
            try:
                variableMonth = monthList[datetime.datetime.now().month-1]
                #print(variableYear)
                #print(dir_name + '/Files/' + variableYear + '/' + variableMonth + '.txt')
                destination_file_path = dir_name + '/Files/{variableYear}/{variableMonth} {variableYear} Statement.txt'.format(
                    variableYear = variableYear, variableMonth = variableMonth)
                #print(destination_file_path)
                destination_file = open(destination_file_path, 'wb')
            except:
                input('Could not open destination file')
                quitApp('q')

            shutil.copyfileobj(source_file, destination_file)
        return

if filesDirName == "":
    print('Files folder wasn\'t found')
    missingFiles()
    filesDirName, filesDirectory, dir_name, directory = scanFolder()

if filesDirectory == []:
    print('No files in files folder')
    missingFiles()
    filesDirName, filesDirectory, dir_name, directory = scanFolder()

def inputYear(funcDirectory,funcError = 0):
    if(funcError == 1):
        print("Please select a valid option")
    elif(funcError == 2):
        print("Current year has no files yet, pick a valid option")
    print("Year options: (Default is current year)")
    options = ""
    for i, x in enumerate(funcDirectory):
        if(i!=len(funcDirectory)-1):
            options = options + x + ", "
        else:
            options = options + x
    print(options)
    year = input("Enter year: ")

    matches = False
    quitApp(year)
    if(year == " " or year == ""):
        return year
    else:
        for x in funcDirectory:
            if(year == x):
                return year
    
    if(matches == False):
        return inputYear(funcDirectory, 1)

variableYear = inputYear(filesDirectory)
if(variableYear == "" or variableYear == " "):
    import datetime
    variableYear = str(datetime.datetime.now().year)

yearDirName = ""
yearDirectory = []
for i, x in enumerate(filesDirectory):
    if x == variableYear:
        yearDirName = filesDirName + "/" + x
        yearDirectory = os.listdir(filesDirName+"/"+filesDirectory[i])

monthsSorting = {"Jan":0,"Feb":1,"Mar":2,"Apr":3,"May":4,"Jun":5,"Jul":6,"Aug":7,"Sep":8,"Oct":9,"Nov":10,"Dec":11}
def sortByMonths(input):
    return monthsSorting[input[0:3]]

def inputMonth(funcDirectory, funcError = 0):
    if(funcError == 1):
        print("Please select a valid option")
    print("Month options: (Default is current month)")
    options = ""
    funcDirectory.sort(key=sortByMonths)
    for i, x in enumerate(funcDirectory):
        if(i!=len(funcDirectory)-1):
            options = options + x + ", "
        else:
            options = options + x
    print(options)
    month = input("Enter month: ")

    quitApp(month)
    matches = False
    inputLength = len(month)
    for x in funcDirectory:
        firstSpace = x.find(" ")
        if(month.lower() == x[0:firstSpace].lower() or month == " " or month == ""):
            matches = True
        if(month.lower() == x[0:inputLength].lower()):
            matches = True
            month = x[0:firstSpace]
    
    if(matches == False):
        return inputMonth(funcDirectory, 1)

    month.capitalize()

    return month

def monthInput(funcError = 0):
    if(funcError == 1):
        print("Ending month must be higher than starting month")
    startMonth = input("Starting month to check (1-12): ")
    endMonth = input("Ending month to check (1-12): ")
    if(endMonth <= startMonth):
        return monthInput(1)
    return [int(startMonth), int(endMonth)]

def durationChoice(funcError = 0):
    if(funcError != 0):
        print("Please enter valid option (S, M, Y)")
    option = input("Single, Multiple, Year: ")
    correctOptions = ["single", "s", "multiple", "m", "year", "y"]
    optionMatches = False
    #print(option)
    quitApp(option)
    for x in correctOptions:
        if (x == option.lower()):
            return option
        
    return durationChoice(1)

if(len(yearDirectory) > 1):
    multipleMonths = False
    print("Choose which months: Single month (S), multiple months (M), whole year (Y)")
    lengthChoices = durationChoice()

    multipleMonths = False
    if(lengthChoices == "single" or lengthChoices == "s"):
        variableMonth = inputMonth(yearDirectory)
        if(variableMonth == "" or variableMonth == " "):
            import datetime
            variableMonth = monthList[datetime.datetime.now().month-1]
    elif(lengthChoices == "year" or lengthChoices == "y"):
        multipleMonths = True
        entireYear = True
        print("Would you like this year to be contained in a single file?")
        singleFileChoice = input("Yes/No: ").lower()
        if(singleFileChoice == "yes" or singleFileChoice == "y"):
            singleFile = True
    elif(lengthChoices == "multiple" or lengthChoices == "m"):
        monthCheck = monthInput()
else:
    variableMonth = inputMonth(yearDirectory)
    if(variableMonth == "" or variableMonth == " "):
        import datetime
        variableMonth = monthList[datetime.datetime.now().month-1]

def readInformation(month, year):
    monthCount = 1

    for x in monthList:
        if (month == x):
            monthNum = monthCount
        monthCount+=1
    try:
        #PDF needs to be manually copy/pasted into Year folder with 'Month Year Statement.txt' as the name
        #text document has to have each cell on a new line to work with parser
        with open('Files/' + year + '/' + month + ' ' + year + ' Statement.txt', 'r') as reader:
            fullLines = reader.read()
    except FileNotFoundError:
        print("Requested file was not found: " + month + " " + year + " Statement.txt")
        sys.exit()

    noCommaFullLines = fullLines.replace(",","")
    return monthNum, noCommaFullLines

def parseArray(unparsedArray):
    i=0
    dollarSignAppearance=0
    #lastSplitPoint=0
    testList = []
    lastTempSplitPoint=0
    endOfEntry = 0
    tempList = []
    entryCount = 1

    for x in unparsedArray:
        if(x == "\n" and i == endOfEntry):
            tempList.append(unparsedArray[lastTempSplitPoint:i])
            entry = ",".join(tempList)
            testList.append(entry)
            tempList = []
            lastTempSplitPoint = i+1
            entryCount = 1
        elif(x == "\n" or (x == " " and entryCount != 4)):
            tempList.append(unparsedArray[lastTempSplitPoint:i])
            lastTempSplitPoint = i+1
            entryCount += 1
        elif(x == " " and entryCount == 4):
            if(unparsedArray[i+1] == "$"):
                tempList.append(unparsedArray[lastTempSplitPoint:i])
                lastTempSplitPoint = i+1
                entryCount += 1
        elif(i+1 == len(unparsedArray)):
            tempList.append(unparsedArray[lastTempSplitPoint:i+1])
            entry = ",".join(tempList)
            testList.append(entry)
        if (x == "$"):
            endOfEntry = unparsedArray.find("\n", i)
        i+=1

    return testList

def writeInformation(parsedArray, monthNum, month, year):
    twoDigitYear = year[2:4]

    if(month == ""):
        concatenated = ""
        for x in parsedArray:
            joinedArray = "\n".join(x)
            if(len(concatenated) > 0):
                #print("yep")
                concatenated = concatenated + "\n" + joinedArray
            else:
                concatenated = joinedArray
    else:
        concatenated = "\n".join(parsedArray)

    #print(concatenated)
    #print(twoDigitYear + '.' + str(monthNum))

    if(month == ""):
        modifiedFileString = '_' + year + ' Modified Statement.csv'
    else:
        modifiedFileString = twoDigitYear + '.' + str(monthNum) + ' - ' + month + ' ' + year + ' Modified Statement.csv'
    #print(modifiedFileString)

    try:
        if not os.path.isdir('modified/'):
            os.makedirs('modified/')
    except:
        input("Could not make modified directory. Press enter to exit.")
        quitApp('q')

    myPath = 'modified/' + twoDigitYear
    try:
        if not os.path.isdir(myPath):
            os.makedirs(myPath)
    except:
        input("Couldn't make {path} directory for some reason. Press enter to exit.".format(path=myPath))
        quitApp('q')

    try:
        with open(myPath + '/' + modifiedFileString, 'w') as writer:
            writer.write(concatenated)
            
        print("Output " + modifiedFileString + ' to ' + myPath + ' folder')
    except FileNotFoundError:
        input("Could not create {file} in {path} folder. Press enter to exit.".format(file=modifiedFileString, path=myPath))
        quitApp('q')
        
#print(os.listdir())
if(informational):
    print(variableMonth + " | " + variableYear)
elif(entireYear == False and len(monthCheck) > 0):
    monthStart = monthCheck[0]-1
    monthEnd = monthCheck[1]
    i=0

    for x in monthList:
        if(i >= monthEnd):
            break
        if(i >= monthStart):
            monthNumber, unparsedArray = readInformation(x, variableYear)
            writeInformation(parseArray(unparsedArray), monthNumber, x, variableYear)
        i+=1
elif(entireYear == False):
    monthNumber, unparsedArray = readInformation(variableMonth, variableYear)
    writeInformation(parseArray(unparsedArray), monthNumber, variableMonth, variableYear)
elif(entireYear == True):
    if(singleFile == True):
        tempArray = []
        for x in monthList:
            monthNumber, unparsedArray = readInformation(x, variableYear)
            parsedArray = parseArray(unparsedArray)
            parsedArray.append(' ')
            tempArray.append(parsedArray)

        writeInformation(tempArray, 0, "", variableYear)
    else:
        for x in monthList:
            monthNumber, unparsedArray = readInformation(x, variableYear)
            writeInformation(parseArray(unparsedArray), monthNumber, x, variableYear)