=================EE4210 Socket Programming Assignment=======================
This folder consist of:
- HTTP server that supports Persistent & Non-Persistent HTTP GET request for 
the following files:
	-a.jpg
	-b.mp3
	-c.txt
- HTTP Persistent Client
- HTTP Non-Persistent Client  
============================================================================
Note:
- The server, client codes can be run on different computers separately or on
same local host
- Please ensure python is added to path list through environment variables 
before executing instructions below
============================================================================
Instructions:
- Open command prompt
- Change directory to current folder (cd <path>)

For running Server: (make sure server is online before client)
- Key: ipconfig; to determine IP address of server host (to be used in client exe)
- cd to Server folder
- Key in: python Server.py

For running Client (Persistent/ Non-Persistent):
- cd to Client folder
- Key in: 
python Client_Persistent.py <IP ADDRESS>         	
or python Client_Non_Persistent.py <IP ADDRESS>  	

