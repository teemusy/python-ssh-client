import paramiko
import getpass

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

host_address = input ("Give host address: ")
host_port = input ("Give host port, empty for 22:") or 22

username = input ("Give username: ")
password = getpass.getpass("Give password: ")
shell_text = (username + "@" + host_address + ": ")

ssh.connect(host_address, port=host_port, username = username, password = password)

keyboard_input = ""

while keyboard_input != "QUIT":
	keyboard_input = input (shell_text)
	stdin, stdout, stderr = ssh.exec_command(keyboard_input)
	ssh_output = stdout.readlines()
	print ("\n".join(ssh_output))	
	if keyboard_input != "QUIT":
		ssh_output = stderr.readlines()
		print ("\n".join(ssh_output))
	
ssh.close()
print ("Connection closed")
	
	