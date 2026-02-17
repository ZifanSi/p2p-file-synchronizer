#!/usr/bin/python3
#==============================================================================
#description     :This is a skeleton code for programming assignment 
#usage           :python Skeleton.py trackerIP trackerPort
#python_version  :>= 3.5
#Authors         :Yongyong Wei, Rong Zheng
#==============================================================================

import socket, sys, threading, json,time,os,ssl
import os.path
import glob
import json
import optparse

def validate_ip(s):
    """
    Validate the IP address of the correct format
    Arguments: 
    s -- dot decimal IP address in string
    Returns:
    True if valid; False otherwise
    """
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

def validate_port(x):
    """Validate the port number is in range [0,2^16 -1 ]
    Arguments:
    x -- port number
    Returns:
    True if valid; False, otherwise
    """
    if not x.isdigit():
        return False
    i = int(x)
    if i < 0 or i > 65535:
            return False
    return True

def get_file_info():
    """Get file info in the local directory (subdirectories are ignored).
    Return: a JSON array of {'name':file,'mtime':mtime}
    i.e, [{'name':file,'mtime':mtime},{'name':file,'mtime':mtime},...]
    Hint: a. you can ignore subfolders, *.so, *.py, *.dll, and this script
          b. use os.path.getmtime to get mtime, and round down to integer
    """
    file_arr = []
    #YOUR CODE
    for name in os.listdir("."):
        if not os.path.isfile(name):
            continue
        n = name.lower()
        if n.endswith(".so") or n.endswith(".py") or n.endswith(".dll"):
            continue
        if os.path.abspath(name) == os.path.abspath(__file__):
            continue
        file_arr.append({"name": name, "mtime": int(os.path.getmtime(name))})

    return file_arr

def get_files_dic():
    """Get file info as a dictionary {name: mtime} in local directory.
    Hint: same filtering rules as get_file_info().
    """
    file_dic = {}
    #YOUR CODE
    for name in os.listdir("."):
        if not os.path.isfile(name):
            continue
        n = name.lower()
        if n.endswith(".so") or n.endswith(".py") or n.endswith(".dll"):
            continue
        if os.path.abspath(name) == os.path.abspath(__file__):
            continue
        file_dic[name] = int(os.path.getmtime(name))
    return file_dic

def check_port_avaliable(check_port):
    """Check if a port is available
    Arguments:
    check_port -- port number
    Returns:
    True if valid; False otherwise
    """
    if str(check_port) in os.popen("netstat -na").read():
        return False
    return True
	
def get_next_avaliable_port(initial_port):
    """Get the next available port by searching from initial_port to 2^16 - 1
       Hint: You can call the check_port_avaliable() function
             Return the port if found an available port
             Otherwise consider next port number
    Arguments:
    initial_port -- the first port to check

    Return:
    port found to be available; False if no port is available.
    """

    #YOUR CODE
    n = 2**16 - 1
    for p in range(int(initial_port), n + 1):
        if check_port_avaliable(p):
            return p
    return False


class FileSynchronizer(threading.Thread):
    def __init__(self, trackerhost,trackerport,port, host='0.0.0.0'):

        threading.Thread.__init__(self)

        #Own port and IP address for serving file requests to other peers
        self.port = int(port) #YOUR CODE
        self.host = host #YOUR CODE

        #Tracker IP/hostname and port
        self.trackerhost = trackerhost #YOUR CODE
        self.trackerport = int(trackerport) #YOUR CODE

        self.BUFFER_SIZE = 8192

        #Create a TCP socket to communicate with the tracker
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #YOUR CODE
        self.client.settimeout(180) #YOUR CODE
        self._tracker_buf = b'' #YOUR CODE

    
        #Store the message to be sent to the tracker. 
        #Initialize to the Init message that contains port number and file info.
        #Refer to Table 1 in Instructions.pdf for the format of the Init message
        #You can use json.dumps to conver a python dictionary to a json string
	#Encode using UTF-8
        self.msg = (json.dumps({"port": self.port, "files": get_file_info()}) + "\n").encode("utf-8")

        #Create a TCP socket to serve file requests from peers.
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.server.bind((self.host, self.port))
        except socket.error:
            print(('Bind failed %s' % (socket.error)))
            sys.exit()
        self.server.listen(10)

    def fatal_tracker(self, message, exc=None):
        """Abort the process on tracker failure"""
        if exc is not None:
            print((message, exc))
        else:
            print(message)
        try:
            self.server.close()
        except Exception:
            pass
        os._exit(1)


    # Not currently used. Ensure sockets are closed on disconnect
    def exit(self):
        self.server.close()

    #Handle file request from a peer(i.e., send the file content to peers)
    def process_message(self, conn, addr):
        '''
        Arguments:
        self -- self object
        conn -- socket object for an accepted connection from a peer
        addr -- IP address of the peer (only used for testing purpose)
        '''
        #YOUR CODE
        #Step 1. read the file name terminated by '\n'
        buf = b""
        while b"\n" not in buf:
            part = conn.recv(self.BUFFER_SIZE)
            if not part:
                conn.close()
                return
            buf += part

        filename = buf.split(b"\n", 1)[0].decode("utf-8").strip()
        filename = os.path.basename(filename)       
        #Step 2. read content of that file in binary mode
        if not os.path.isfile(filename):
            conn.sendall(b"Content-Length: 0\n")
            conn.close()
            return

        with open(filename, "rb") as f:
            content = f.read()        
        #Step 3. send header "Content-Length: <size>\n" then file bytes
        header = ("Content-Length: %d\n" % len(content)).encode("utf-8")
        conn.sendall(header)
        if content:
            conn.sendall(content)
    
        #Step 4. close conn when you are done.
        conn.close()

    def run(self):
        #Step 1. connect to tracker; on failure, may terminate
        try:
            self.client.connect((self.trackerhost, self.trackerport))
        except Exception as exc:
            self.fatal_tracker("Failed to connect to tracker", exc)

        t = threading.Timer(2, self.sync)
        t.start()
        print(('Waiting for connections on port %s' % (self.port)))
        while True:
            #Hint: guard accept() with try/except and exit cleanly on failure
            conn, addr = self.server.accept()
            threading.Thread(target=self.process_message, args=(conn,addr)).start()

    #Send Init or KeepAlive message to tracker, handle directory response message
    #and  request files from peers
    def sync(self):
        print(('connect to:'+self.trackerhost,self.trackerport))
        #Step 1. send Init msg to tracker (Note init msg only sent once)
        #Since self.msg is already initialized in __init__, you can send directly
        #Hint: on send failure, may terminate
        #YOUR CODE
        try:
            self.client.sendall(self.msg)
        except Exception as exc:
            self.fatal_tracker("Failed to send to tracker", exc)
            return

        #Step 2. now receive a directory response message from tracker
        directory_response_message = ''
        #Hint: read from socket until you receive a full JSON message ending with '\n'
        #YOUR CODE
        while b"\n" not in self._tracker_buf:
            try:
                part = self.client.recv(self.BUFFER_SIZE)
            except Exception as exc:
                self.fatal_tracker("Failed to receive from tracker", exc)
                return
            if not part:
                self.fatal_tracker("Tracker closed connection")
                return
            self._tracker_buf += part

        line, self._tracker_buf = self._tracker_buf.split(b"\n", 1)
        directory_response_message = line.decode("utf-8")    
        print('received from tracker:',directory_response_message)

        #Step 3. parse the directory response message. If it contains new or
        #more up-to-date files, request the files from the respective peers.
        #NOTE: compare the modified time of the files in the message and
        #that of local files of the same name.
        #Hint: a. use json.loads to parse the message from the tracker
        #      b. read all local files, use os.path.getmtime to get the mtime 
        #         (also note round down to int)
        #      c. for new or more up-to-date file, you can call syncfile()
        #      d. use Content-Length header to know file size
        #      e. if transfer fails, discard partial file
        #      f. finally, write the file content to disk with the file name, use os.utime
        #         to set the mtime
        #YOUR CODE
        try:
            directory = json.loads(directory_response_message) if directory_response_message else {}
        except Exception:
            directory = {}

        local_files = get_files_dic()

        for fname, info in directory.items():
            try:
                remote_mtime = int(info.get("mtime", 0))
            except Exception:
                continue

            need = False
            if fname not in local_files:
                need = True
            elif remote_mtime > int(local_files[fname]):
                need = True

            if need:
                self.syncfile(fname, info)
        #Step 4. construct a KeepAlive message
        #Note KeepAlive msg is sent multiple times, the format can be found in Table 1
        #use json.dumps to convert python dict to json string.
        self.msg = (json.dumps({"port": self.port}) + "\n").encode("utf-8") #YOUR CODE

        #Step 5. start timer
        t = threading.Timer(5, self.sync)
        t.start()

    def syncfile(self, filename, file_dic):
        """Fetch a file from a peer and store it locally.

        Arguments:
        filename -- file name to request
        file_dic -- dict with 'ip', 'port', and 'mtime'
        """
        #YOUR CODE  

        filename = os.path.basename(filename)
        ip = file_dic.get("ip")
        port = int(file_dic.get("port"))
        mtime = int(file_dic.get("mtime"))

        tmp = filename + ".part"

        peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer.settimeout(8)

        try:
            #Step 1. connect to peer and send filename + '\n'
            peer.connect((ip, port))
            peer.sendall((filename + "\n").encode("utf-8"))

            #Step 2. read header "Content-Length: <size>\n"
            buf = b""
            while b"\n" not in buf:
                part = peer.recv(self.BUFFER_SIZE)
                if not part:
                    return
                buf += part

            header_line, rest = buf.split(b"\n", 1)
            header_line = header_line.decode("utf-8").strip()
            if not header_line.lower().startswith("content-length:"):
                return

            size = int(header_line.split(":", 1)[1].strip())

            #Step 3. read exactly <size> bytes; if short, discard partial file
            data = bytearray()
            if rest:
                take = min(len(rest), size)
                data.extend(rest[:take])

            while len(data) < size:
                chunk = peer.recv(min(self.BUFFER_SIZE, size - len(data)))
                if not chunk:
                    break
                data.extend(chunk)

            if len(data) != size:
                if os.path.exists(tmp):
                    os.remove(tmp)
                return

            #Step 4. write file to disk (binary), rename from .part when done
            with open(tmp, "wb") as f:
                f.write(data)
            os.replace(tmp, filename)

            #Step 5. set mtime using os.utime
            os.utime(filename, (mtime, mtime))

        finally:
            try:
                peer.close()
            except Exception:
                pass


if __name__ == '__main__':
    parser = optparse.OptionParser(usage="%prog ServerIP ServerPort")
    try:
        options, args = parser.parse_args()
    except SystemExit:
        sys.exit(1)

    if len(args) < 1:
        parser.error("No ServerIP and ServerPort")
    elif len(args) < 2:
        parser.error("No  ServerIP or ServerPort")
    else:
        if validate_ip(args[0]) and validate_port(args[1]):
            tracker_ip = args[0]
            tracker_port = int(args[1])

            # get a free port
            synchronizer_port = get_next_avaliable_port(8000)
            synchronizer_thread = FileSynchronizer(tracker_ip,tracker_port,synchronizer_port)

            # start the thread
            synchronizer_thread.start()
            synchronizer_thread.join()
        else:
            parser.error("Invalid ServerIP or ServerPort")
