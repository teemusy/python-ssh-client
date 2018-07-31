import paramiko
import getpass
from tkinter import *

root = Tk()
root.geometry("800x600")
root.title("Python SSH client")
#ssh_output_window = Text(root, height=35, width=80)
#ssh_input_window = Text(root, height=10, width=80)




#Label(root, text="Input").pack(side=LEFT)

ssh_output_window = Text(root)
ssh_input_window = Entry(root)
#ssh_input_window.grid(row=0, column=1)
#Label(parent, text=caption).pack(side=LEFT)

ssh_output_window.grid(row = 0)
ssh_input_window.grid(row = 40)


#ssh_output_window.grid(row = 0, column = 0)
#ssh_input_window.grid(row = 1, column = 1)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def print_to_console_window():
	pass
	
def read_input_window():
	keyboard_input = ssh_input_window.get()

host_address = input ("Give host address: ") or "192.168.10.60"
host_port = input ("Give host port, empty for 22:") or 22

username = input ("Give username: ") or "sshtesti"
password = getpass.getpass("Give password: ") or "salasana"
shell_text = (username + "@" + host_address + ": ")

ssh.connect(host_address, port=host_port, username = username, password = password)

keyboard_input = ""

while keyboard_input != "QUIT":
	
	Button(root, text='Show', command=read_input_window).grid(row = 40, column = 50)
		
	stdin, stdout, stderr = ssh.exec_command(keyboard_input)
	ssh_output = stdout.readlines()
	ssh_output_window.insert(END, ssh_output)
	
	if keyboard_input != "QUIT":
		ssh_output = stderr.readlines()
		ssh_output_window.insert(END, ssh_output)
	root.mainloop()

ssh.close()
print ("Connection closed")

	