import paramiko
import getpass
from tkinter import *

root = Tk()
root.geometry("800x600")
root.title("Python SSH client")
ssh_output_window = Text(root, height=35, width=80)
ssh_output_window.pack()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

host_address = input ("Give host address: ") or "192.168.10.60"
host_port = input ("Give host port, empty for 22:") or 22

username = input ("Give username: ") or "sshtesti"
password = getpass.getpass("Give password: ") or "salasana"
shell_text = (username + "@" + host_address + ": ")

ssh.connect(host_address, port=host_port, username = username, password = password)

keyboard_input = ""

while keyboard_input != "QUIT":
	keyboard_input = input (shell_text)
	stdin, stdout, stderr = ssh.exec_command(keyboard_input)
	ssh_output = stdout.readlines()
	ssh_output_window.insert(END, ssh_output)
	
	if keyboard_input != "QUIT":
		ssh_output = stderr.readlines()
		ssh_output_window.insert(END, ssh_output)
	root.mainloop()

ssh.close()
print ("Connection closed")

	