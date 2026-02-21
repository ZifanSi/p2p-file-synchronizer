# p2p-file-synchronizer

run_all.bat

Before
Peer 1: file A
Peer 2: file B
Peer 3: file C
Tracker.py terminal 
Waiting for connections on port 9000
Client connected with 127.0.0.1:51543
Client connected with 127.0.0.1:51545
Client connected with 127.0.0.1:51546
client server127.0.0.1:8000
client server127.0.0.1:8001
client server127.0.0.1:8002


Peer 1  terminal 
Waiting for connections on port 8000
Waiting for connections on port 8000
('connect to:127.0.0.1', 9000)
received from tracker: {"fileA.txt": {"ip": "127.0.0.1", "port": 8000, "mtime": 1771289241}}
received from tracker: {"fileA.txt": {"ip": "127.0.0.1", "port": 8000, "mtime": 1771289241},
 "fileB.txt": {"ip": "127.0.0.1", "port": 8001, "mtime": 1771289244},
 "fileC.txt": {"ip": "127.0.0.1", "port": 8002, "mtime": 1771289247}}

Peer2  terminal 
Waiting for connections on port 8001
('connect to:127.0.0.1', 9000)
received from tracker: {"fileA.txt": {"ip": "127.0.0.1", "port": 8000, "mtime": 1771289241},
 "fileB.txt": {"ip": "127.0.0.1", "port": 8001, "mtime": 1771289244}}
received from tracker: {"fileA.txt": {"ip": "127.0.0.1", "port": 8000, "mtime": 1771289241},
 "fileB.txt": {"ip": "127.0.0.1", "port": 8001, "mtime": 1771289244},
 "fileC.txt": {"ip": "127.0.0.1", "port": 8002, "mtime": 1771289247}}


peer 3  terminal 
Waiting for connections on port 8002
('connect to:127.0.0.1', 9000)
received from tracker: {"fileA.txt": {"ip": "127.0.0.1", "port": 8000, "mtime": 1771289241},
 "fileB.txt": {"ip": "127.0.0.1", "port": 8001, "mtime": 1771289244},
 "fileC.txt": {"ip": "127.0.0.1", "port": 8002, "mtime": 1771289247}}


 after: Before
Peer 1: file A,B,C
Peer 2: file A,B,C
Peer 3: file A,B,C