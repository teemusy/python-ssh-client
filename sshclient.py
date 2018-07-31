import paramiko
import getpass
from tkinter import *

#TKINTER INIT

root = Tk()
root.geometry("800x600")
root.title("Python SSH client")

ssh_output_window = Text(root)
ssh_input_window = Entry(root)

ssh_output_window.grid(row = 0)
ssh_input_window.grid(row = 40)


#PARAMIKO INIT

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#FUNCTIONS

def read_input_window():
	keyboard_input = ""
	keyboard_input = ssh_input_window.get()
	stdin, stdout, stderr = ssh.exec_command(keyboard_input)
	ssh_output = stdout.readlines()
	ssh_output_window.insert(END, ssh_output)
	ssh_output = stderr.readlines()
	ssh_output_window.insert(END, ssh_output)


#MAIN LOOP

#default address, username and password for testing
host_address = input ("Give host address: ") or "192.168.10.60"
host_port = input ("Give host port, empty for 22:") or 22
username = input ("Give username: ") or "sshtesti"
password = getpass.getpass("Give password: ") or "salasana"

#text for console window
shell_text = (username + "@" + host_address + ": ")

ssh.connect(host_address, port=host_port, username = username, password = password)

#print welcome message, doesn't work, returns nonetype variable
welcome_message = ssh._transport.get_banner()
#print (welcome_message)
#ssh_output_window.insert(END, welcome_message)
#print (type(welcome_message))

Button(root, text='Send', command=read_input_window).grid(row = 40, column = 50)

root.mainloop()

ssh.close()
print ("Connection closed")