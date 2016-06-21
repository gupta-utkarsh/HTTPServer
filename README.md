# HTTP Server

This server is made in python using TCP [socket](https://docs.python.org/2/library/socket.html) module. Meant as a learning exercise.
- Supports HEAD and GET requests.
- Uses multithreading to serve more than one client at a time using the [thread](https://docs.python.org/2/library/thread.html) module.
- Looks up for index.html by default if file not specified.
- Gives 200,400 and 404 responses.
- Set to listen to requests on port 8888 on localhost.

### Set Up : 
- Clone the repository.
- Add files you wish to serve to this repository as this is the base directory.
- Change the port to something else if any other service is using the port 8888.
- Run `./server.py`.
- Go to the address `localhost:8888/relative/path/of/file` using any browser.