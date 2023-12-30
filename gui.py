from tkinter import *
import time
import datetime

# set up main window
root = Tk()
root.geometry("455x233")
root.title("Water Warriors Moisture Harvester Data Management Interface")

# set up changeable status bar for main window
statusvar = StringVar()
statusvar.set("Ready to perform tasks...")
status = Label(root, textvariable=statusvar, relief=SUNKEN, anchor="w")
status.pack(side=BOTTOM, fill=X)

# initiate global variables
global importedOnce
importedOnce = False
global importedMultiple
importedMultiple = False
global importCount
importCount = 0


# create function for the import data interface
def import_data_interface():
    # set up import data window
    newWindowImport = Toplevel(root)
    newWindowImport.title("Import Data Interface")
    newWindowImport.geometry("455x233")

    # informational label
    Label(newWindowImport, text="Welcome to the Import Data interface."
                                "\nHere, you can import previous data to an output file.",
          font=("Bahnschrift", 12)).pack()

    # update status bar
    statusvar.set("Import Data Interface is open...")

    # set up changeable status bar
    statusimportvar = StringVar()
    statusimportvar.set("Ready to import data.")
    statusimport = Label(newWindowImport, textvariable=statusimportvar, relief=SUNKEN, anchor='w')
    statusimport.pack(side=BOTTOM, fill=X)

    # creating the labels and entries for users to input file names
    inputFileLabel = Label(newWindowImport, text="Input the name of the file to be imported:")
    inputFileLabel.pack()

    inputFileEntry = Entry(newWindowImport, width=40)
    inputFileEntry.pack()

    outputFileLabel = Label(newWindowImport, text="Input the name of the file to be outputted to:")
    outputFileLabel.pack()

    outputFileEntry = Entry(newWindowImport, width=40)
    outputFileEntry.pack()

    # sets focus on the input file textbox
    inputFileEntry.focus_set()

    # create function to close window and update main status bar
    def close_window_import():
        statusvar.set("Import Data Interface was closed.")
        newWindowImport.destroy()

    # create import data function
    def import_data():
        # update status bar
        statusimportvar.set("Importing...")

        # get our variables from the text boxes
        outputFile = outputFileEntry.get()
        inputFile = inputFileEntry.get()

        # call global variables
        global importedOnce
        global importedMultiple

        # changes global variables accordingly
        if importedOnce is False:
            importedOnce = True
        else:
            importedMultiple = True

        # opens and reads input file
        file = open(inputFile, "r")
        lines = file.readlines()

        # opens output file and is ready to append to it
        output = open(outputFile, "a")

        # determines whether to add in the first line
        if importedMultiple is False:
            output.write("First Line Goes Here")
            output.write("\n")

        # writes the input files, except for the first line
        output.writelines(lines[1:])
        output.write("\n")

        # create new window
        importFinishPopup = Toplevel(newWindowImport)
        importFinishPopup.title("Importing Finished!")

        # create info label
        finished = Label(importFinishPopup, text="File import finished!")
        finished.pack()

        # call and change global variable
        global importCount
        importCount += 1

        # updates status bar
        statusimportvar.set("Data imported. Any more files?")

    def import_count():
        # create new window
        importCountPopup = Toplevel(newWindowImport)
        importCountPopup.title("Number of Imported Files Popup")

        # create labels in grid form
        count1 = Label(importCountPopup, text="You have imported")
        count1.grid(row=0, column=0)
        count2 = Label(importCountPopup, text=importCount)
        count2.grid(row=0, column=1)
        count3 = Label(importCountPopup, text="file(s).")
        count3.grid(row=0, column=2)

        # updates status bar
        statusimportvar.set("Number of imported files popup was opened.")

    # create toolbar
    toolbarImport = Frame(newWindowImport)

    # create function buttons
    quitButton = Button(toolbarImport, text="Quit and Return to Main Interface", command=close_window_import)
    quitButton.pack(side=BOTTOM, padx=2, pady=2)

    countButton = Button(toolbarImport, text="Check Number of Imported Files", command=import_count)
    countButton.pack(side=BOTTOM, padx=2, pady=2)

    importButton = Button(toolbarImport, text="Import Data", command=import_data)
    importButton.pack(side=BOTTOM, padx=2, pady=2)

    # finish toolbar
    toolbarImport.pack(side=BOTTOM, fill=X)


# create function to create the data collection interface
def data_collection_interface():
    # set up data collection interface
    newWindowData = Toplevel(root)
    newWindowData.title("Data Collection Interface")
    newWindowData.geometry("455x255")

    # create informational label
    Label(newWindowData, text="Welcome to the Data Collection Interface"
                              "\nHere, you can start data collection.",
          font=("Bahnschrift", 12)).pack()
    statusvar.set("Data Collection Interface is open...")

    # create changeable status bar
    statusdatavar = StringVar()
    statusdatavar.set("Waiting to start...")
    statusdata = Label(newWindowData, textvariable=statusdatavar, relief=SUNKEN, anchor='w')
    statusdata.pack(side=BOTTOM, fill=X)

    # create labels and entries
    outputFileLabel = Label(newWindowData, text="Input the name of the file to be outputted to:")
    outputFileLabel.pack()

    outputFileEntry = Entry(newWindowData, width=40)
    outputFileEntry.pack()

    totalTimeLabel = Label(newWindowData, text="Enter the total amount of time for data collection in seconds:")
    totalTimeLabel.pack()

    totalTimeEntry = Entry(newWindowData, width=40)
    totalTimeEntry.pack()

    waitTimeLabel = Label(newWindowData, text="Enter the amount of time between checks in seconds:")
    waitTimeLabel.pack()

    waitTimeEntry = Entry(newWindowData, width=40)
    waitTimeEntry.pack()

    # create function to close window and update main status bar
    def close_window_data():
        statusvar.set("Data Collection Interface was closed.")
        newWindowData.destroy()

    # create function for data collection
    def start_collection():
        # open output file
        outputFile = outputFileEntry.get()
        output = open(outputFile, "a")

        # take inputs from entries
        totalTime = int(totalTimeEntry.get())
        waitTime = float(waitTimeEntry.get())

        # check if it should write the first line
        if importedOnce is False:
            output.write("First Line Goes Here")
            output.write("\n")

        # set up variables
        lastMoisture = 0
        lastTemp = 0
        # [time, moisture, temperature]
        newData = [0, 0, 0]

        # for loop that only writes new data if something changes
        for count in range(0, int(totalTime / waitTime)):

            # take in new inputs
            # newData = information from the collectors

            # initialize the comparison variables
            newMoisture = newData[1]
            newTemp = newData[2]

            # check is the new data has had a change, other than the time
            if newTemp != lastTemp or newMoisture != lastMoisture:
                lastTemp = newTemp
                lastMoisture = newMoisture

                # opening and writing to the file
                output.write(str(newData))
                output.write("\n")

            # delay function executes no matter what
            time.sleep(waitTime)

        # create new window
        dataFinishPopup = Toplevel(newWindowData)
        dataFinishPopup.title("Data Collection Finished!")

        # create info label
        finished = Label(dataFinishPopup, text="Data collection finished!")
        finished.pack()

        # notifies user that the process is done
        statusdatavar.set("Data collection finished. ")

    # create toolbar
    toolbarData = Frame(newWindowData)

    # create function buttons
    quitButton = Button(toolbarData, text="Quit and Return to Main Interface", command=close_window_data)
    quitButton.pack(side=BOTTOM, padx=2, pady=2)

    startButton = Button(toolbarData, text="Start Data Collection", command=start_collection)
    startButton.pack(side=BOTTOM, padx=2, pady=2)

    # finish toolbar
    toolbarData.pack(side=BOTTOM, fill=X)


# informational label
Label(root, text="Welcome to the Water Warriors Data Management Panel.", font=("Bahnschrift", 12)).pack()

# create toolbar
toolbar = Frame(root, bg="blue")

# create buttons for toolbar
insertBtn = Button(toolbar, text="Import Previous Data", command=import_data_interface)
insertBtn.pack(padx=2, pady=2)

printBtn = Button(toolbar, text="Start Data Collection", command=data_collection_interface)
printBtn.pack(padx=2, pady=2)

quitBtn = Button(toolbar, text="Quit Interface", command=root.destroy)
quitBtn.pack(padx=2, pady=2)

# finish toolbar
toolbar.pack(side=TOP, fill=X)

creditLabel = Label(root, text="Created by Eric Wang")
creditLabel.pack(anchor=SE, side=BOTTOM)

# mainloop
root.mainloop()
