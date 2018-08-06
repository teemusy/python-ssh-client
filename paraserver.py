import threading
import paramiko
import subprocess
import sys
import socket

host_key = paramiko.RSAKey(filename='test_rsa.key')

class Server(paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        if(username=='sshtesti') and (password == 'salasana'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
		

server = sys.argv[1]
ssh_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((server, ssh_port))
sock.listen(100)
print ('[+] Listening for connection ...')
client, addr = sock.accept()
print ('[+] Got a connection!')

bhSession = paramiko.Transport(client)
bhSession.add_server_key(host_key)

class Server(paramiko.ServerInterface):

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == "sshtesti") and (password == "salasana"):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_gssapi_with_mic(
        self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    ):
        """
        .. note::
            We are just checking in `AuthHandler` that the given user is a
            valid krb5 principal! We don't check if the krb5 principal is
            allowed to log in on the server, because there is no way to do that
            in python. So if you develop your own SSH server with paramiko for
            a certain platform like Linux, you should call ``krb5_kuserok()`` in
            your local kerberos library to make sure that the krb5_principal
            has an account on the server and is allowed to log in as a user.
        .. seealso::
            `krb5_kuserok() man page
            <http://www.unix.com/man-page/all/3/krb5_kuserok/>`_
        """
        if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_gssapi_keyex(
        self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    ):
        if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def enable_auth_gssapi(self):
        return True

    def get_allowed_auths(self, username):
        return "gssapi-keyex,gssapi-with-mic,password,publickey"

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        return True



server = Server()

bhSession.start_server(server=server)

chan = bhSession.accept(20)
print ('[+] Authenticated!')

chan.send("Welcome to bh_ssh\n")


server.event.wait(10)
if not server.event.is_set():
	print("*** Client never asked for a shell.")
	sys.exit(1)

chan.send("\r\n\r\nWelcome to my dorky little BBS!\r\n\r\n")
chan.send("We are on fire all the time!  Hooray!  Candy corn for everyone!\r\n")
chan.send("Happy birthday to Robot Dave!\r\n\r\n")
chan.send("Username: ")
f = chan.makefile("rU")
username = f.readline().strip("\r\n")
chan.send("\r\nI don't like you, " + username + ".\r\n")
chan.close()

