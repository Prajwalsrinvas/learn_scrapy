import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer

# Configure the FTP server
authorizer = DummyAuthorizer()
HOMEDIR = "./test_ftp_folder/"
os.makedirs(HOMEDIR, exist_ok=True)
authorizer.add_user(
    os.getenv("FTP_USERNAME"), os.getenv("FTP_PASSWORD"), HOMEDIR, perm="elradfmw"
)

handler = FTPHandler
handler.authorizer = authorizer

# Specify the server address and port
address = ("127.0.0.1", 2121)

# Start the FTP server
server = ThreadedFTPServer(address, handler)
server.serve_forever()
