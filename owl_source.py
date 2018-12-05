
import threading
import time
import os
import subprocess
from subprocess import Popen, PIPE
import tkinter as tk
from tkinter import *
from tkinter import IntVar
from tkinter import messagebox

#get icon data (https://stackoverflow.com/questions/23554142/best-strategy-to-improve-the-compatibility-between-pyinstaller-and-tkinter-icon)
datafile = "owlicon.ico"
if not hasattr(sys, "frozen"):   # not packed
    datafile = os.path.join(os.path.dirname(__file__), datafile)
else:
    datafile = os.path.join(sys.prefix, datafile)


#create window
MainWindow = Tk()
MainWindow.title('Owl Easy Commands')
MainWindow.iconbitmap(default=datafile)

#----- CHECKBOX VALUES --------

#get ip checkbox values
pingValue = IntVar()
ipValue = IntVar()
netValue = IntVar()


#-- END OF CHECKBOX VALUES --

# -- Flag list--
pingList=[" ", "-4", "-6"] #flags for ping
ipconfigList = [" ", "/all","/displaydns"] #flags for ipconfig
netList = [" ", "-a", "-e"]

#---------- THESE ARE THE COMMAND FUNCTIONS !!!  MUST COME FIRST BEFORE WIDGETS!!! -----------

#about application dialogue
def about():
    messagebox.showinfo('About', '© 2018 OWL Easy Commands \n OWL Easy Commands Version 1.0')


#Performs ping function
def ping():
    value = pingValue.get()
    value = int(value)
    pingTrue = ""
    if len(domainInput.get()) == 0:
        messagebox.showerror("Error!", "Domain box must contain text")
    else:
        MainWindow.config(cursor="wait")
        domainText = domainInput.get()
        pingData = os.popen('ping ' + domainText+ " " + pingList[value]).read()
        print(pingData)
        pingFind = pingData.find('(0% loss)')
        print(pingFind)
        MainWindow.config(cursor="")
        #looks for string data
        if pingFind != -1:
            messagebox.showinfo("Ping", "Connection Successful")
        else:
            messagebox.showinfo("Ping", "Connection Error")
#threads ping command
def pingThread():
    global startthread1
    startthread1 = threading.Thread(name="ping", target=ping)
    startthread1.start()


#performs nslookup for domain search
def nslookup():
    if len(domainInput.get()) == 0:
        messagebox.showerror("Error!", "Domain box must contain text")
    else:
        domainText = domainInput.get()
        nslookupData = os.popen('nslookup ' + domainText).read()
        print(nslookupData)
        messagebox.showinfo("DNS Info", nslookupData)

#performs netstat command
def netstat():
    value = netValue.get()
    value =int(value)
    question = messagebox.askyesno("Caution", "Running netstat may take up to 5 minutes. Are you sure you want to peform this action?")
    MainWindow.config(cursor="wait")
    time.sleep(3)
    if question == True:
        netOpen = os.popen('netstat ' + netList[value]).read()
        #print (netOpen)
        if value == 0:
            netstatFile = open("netstat.txt", "w")
            netstatFile.write(netOpen)
            directory = os.getcwd()
            messagebox.showinfo("Netstat", "netstat.txt saved in directory " + directory)
            MainWindow.config(cursor="")
        elif value == 1:
            netstatFile = open("netstat_all.txt", "w")
            netstatFile.write(netOpen)
            directory = os.getcwd()
            messagebox.showinfo("Netstat", "netstat_all.txt saved in directory " + directory)
            MainWindow.config(cursor="")
        else:
            netstatFile = open("netstat_ethernet.txt", "w")
            netstatFile.write(netOpen)
            directory = os.getcwd()
            messagebox.showinfo("Netstat", "netstat_ethernet.txt saved in directory " + directory)
            MainWindow.config(cursor="")
    else:
        MainWindow.config(cursor="")
#threads netstat command
def netstatThread():
    global startthread2
    startthread2 = threading.Thread(name="netstat", target=netstat)
    startthread2.start()

#performs ipconfig
def ipconfig():
    value = ipValue.get()
    value = int(value)
    if value != 2:
        ipdata = os.popen('ipconfig' + "" +ipconfigList[value]).read()
        print(ipdata)
        messagebox.showinfo('Device Information', ipdata)
    else:
        ipdata = os.popen('ipconfig /displaydns').read()
        print (ipdata)
        dnsCachefile = open("dnscache.txt", "w")
        dnsCachefile.write(ipdata)
        directory = os.getcwd()
        messagebox.showinfo("DNS Cache", "dnscache.txt saved in directory " + directory)
        MainWindow.config(cursor="")

def arp():
    arpData = os.popen('arp -a').read()
    print(arpData)
    messagebox.showinfo('ARP Table', arpData)

def system():
    MainWindow.config(cursor="wait")
    sysData = os.popen('systeminfo').read()
    print(sysData)
    MainWindow.config(cursor="")
    #create child window
    window  = tk.Toplevel()
    window.title('System Information')
    window.resizable(0,0)
    window.geometry("700x425+30+30")
    #crate text frame
    textFrame = Frame(window)
    textFrame.pack(side=TOP)
    #create text widget
    text = tk.Text(textFrame,relief="sunken")
    text.insert(INSERT, sysData)
    scroll = Scrollbar(textFrame, command=text.yview)
    text.configure(yscrollcommand=scroll.set)
    text.pack(side=LEFT)
    scroll.pack(side=LEFT,fill=Y)

    #create button to close
    exitButton = Button(window, text="Close", command=window.destroy)
    exitButton.pack()


def sysThread():
    global startthread3
    startthread3 = threading.Thread(name="system", target=system)
    startthread3.start()

def tasklist():
    def kill():
        kill = killInput.get()
        kill = str(kill)
        killData = os.popen("taskkill /pid " + kill + " /f").read()
        print(killData)
        killFind = killData.find('SUCCESS: The process with PID')
        if killFind == -1:
            messagebox.showerror("Process Error", "The process could not be found")
        else:
            messagebox.showinfo("Process Killed", "Sucessfully killed Process ID " + killData)
            text.delete(1.0, END)
            taskData2 = os.popen('tasklist').read()
            text.insert(INSERT, taskData2)


    taskData = os.popen('tasklist').read()
    print(taskData)

    #create child window
    window2  = tk.Toplevel()
    window2.title('System Tasks')
    window2.resizable(0,0)
    window2.geometry("700x500+30+30")

    #crate text frame
    textFrame = Frame(window2)
    textFrame.pack(side=TOP)

    #create text widget
    text = tk.Text(textFrame,relief="sunken")
    text.insert(INSERT, taskData)
    scroll = Scrollbar(textFrame, command=text.yview)
    text.configure(yscrollcommand=scroll.set)
    text.pack(side=LEFT)
    scroll.pack(side=LEFT,fill=Y)


    #create widgets for task window
    killLabel = Label(window2, text="Enter PID (Process ID) of the task to be killed").pack(side=TOP)
    killInput = Entry(window2)
    print(killInput)



    enterButton = Button(window2, text="  Kill  ", command=kill)

    exitButton = Button(window2, text="Close", command=window2.destroy)


    killInput.pack()
    enterButton.pack()
    exitButton.pack()

def taskThread():
    global startthread4
    startthread4 = threading.Thread(name="tasklist", target=tasklist)
    startthread4.start()

# --- END OF COMMAND FUNCTIONS --------

#------- START OF WIDGETS --------------



#-------- MENU AND BUTTONS ----------

#create menu and display - Menu help from http://effbot.org/tkinterbook/menu.htm
mainMenu = Menu(MainWindow)
fileMenu = Menu(mainMenu,tearoff=0)
fileMenu.add_command(label="About", command=about)
mainMenu.add_cascade(label="File", menu=fileMenu)
MainWindow.config(menu=mainMenu)



#create button frame
buttonFrame = Frame(MainWindow)
buttonFrame.pack(side=TOP)

#create domainInput Frame
domainFrame = Frame(MainWindow)
domainFrame.pack(side=TOP)

#creates ping button widget
pingButton = Button(buttonFrame, text="Ping", command=pingThread)
pingButton.pack(side=LEFT)

#creates nslookup button widget
dnsButton = Button(buttonFrame, text="View DNS Record", command=nslookup)
dnsButton.pack(side=LEFT)

#creates netStat button widget
netStatButton = Button(buttonFrame, text = "Run NetStat", command=netstatThread)
netStatButton.pack(side=LEFT)

#creates ipconfig button
ipButton = Button(buttonFrame, text="Network Devices/ipconfig", command=ipconfig)
ipButton.pack(side =LEFT)

#create arp button
arpButton = Button(buttonFrame, text="View ARP Table", command=arp)
arpButton.pack(side=LEFT)

#create syzteminfo button
sysButton = Button(buttonFrame, text="System Information", command=sysThread)
sysButton.pack(side=LEFT)

#create tasklist button
sysButton = Button(buttonFrame, text="View running tasks", command=taskThread)
sysButton.pack(side=LEFT)


#-----------------------------------------------------------

#create input widget
domainLabel = Label(domainFrame, text="Enter domain/IP Address").pack(side=TOP)
domainInput = Entry(domainFrame)

#create checkbox frame
boxFrame = Frame(MainWindow)
boxFrame.pack(side = TOP)

#create ping frame
pingFrame = Frame(boxFrame)
pingFrame.pack(side = LEFT)


#create ipconfig frame
ipFrame = Frame(boxFrame)
ipFrame.pack(side = LEFT)

#create netstat frame
netFrame = Frame(boxFrame)
netFrame.pack(side = LEFT )
#create checkbox widget for pingc
checkLabel = Label(pingFrame, text="Ping Options").pack(side=TOP)
default = Radiobutton(pingFrame,text = "Default", variable= pingValue, value = 0).pack()
ipv4 =Radiobutton(pingFrame,text = "Force IPv4", variable= pingValue, value = 1).pack()
ipv6 =Radiobutton(pingFrame, text = "Force IPv6", variable= pingValue, value = 2).pack()

#create checkbox widget for ipconfig
checkLabel2 = Label(ipFrame, text="IPConfig Options").pack(side=TOP)
default = Radiobutton(ipFrame,text = "Default", variable= ipValue, value = 0).pack()
ipv4 =Radiobutton(ipFrame,text = "All", variable= ipValue, value = 1).pack()
ipv6 =Radiobutton(ipFrame, text = "DNS Cache", variable= ipValue, value = 2).pack()

#create checkbox widget for netstat
checkLabel3 = Label(netFrame, text="Netstat Options").pack(side=TOP)
default =Radiobutton(netFrame, text ="Default", variable = netValue, value = 0).pack()
aFlag = Radiobutton(netFrame, text = "All connections/ports", variable = netValue, value = 1).pack()
eFlag = Radiobutton(netFrame, text = "View Ethernet Statistics", variable = netValue, value = 2).pack()






#Set window size
domainInput.pack()
MainWindow.geometry("800x350+30+30")
MainWindow.mainloop()





#Code Citations:
#http://zetcode.com/gui/tkinter/introduction/
#https://www.python-course.eu/tkinter_entry_widgets.php
#https://stackoverflow.com/questions/15455113/tkinter-check-if-entry-box-is-empty
#https://pythonspot.com/tk-message-box/
#https://stackoverflow.com/questions/47676319/how-to-create-a-tkinter-error-message-box
#https://stackoverflow.com/questions/30685308/how-do-i-change-the-text-size-in-a-label-widget-python-tkinter
#http://www.java2s.com/Code/Python/GUI-Tk/LayoutsideTOPLEFT.htm
#https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
#https://stackoverflow.com/questions/40756417/tkinter-button-click-to-start-thread-to-prevent-gui-from-freezing
#https://python-forum.io/Thread-Tkinter-Print-if-all-checkboxes-marked
#http://effbot.org/tkinterbook/radiobutton.htm
#https://stackoverflow.com/questions/41946222/how-do-i-create-a-popup-window-in-tkinter