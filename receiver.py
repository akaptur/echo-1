EOL = '\n'      # end of line character
MAX = 1024      # maximum number of bytes to receive at a time

# The Receiver class manages receiving messages over a socket
class Receiver:
    def __init__(self, sock):
        # The socket instance variable stores the socket associated with 
        # the receiver which is passed in when the object is created and is
        # presumed to be connected
        self.sock = sock

        # The open instance variable is used to track when the other side of 
        # the connection closes  
        self.open = True

        # The buffer instance variable is used to collect chunks of data
        # received over the socket and to save received data in between
        # calls to recv_message()
        self.buffer = []

    def recv_message(self):
        """recv_message() returns all bytes received until an end of line character
        is encountered.  Any further bytes that have been received are held in
        a buffer to be used in the next call to recv_message"""
        # Initialize the msg_chunk variable to any excess bytes that were received
        # on the last call to recv_message()
        if len(self.buffer) == 1:
            msg_chunk = self.buffer[0]
        else:
            msg_chunk = ""
            
        # Initialize the end of line position based on the contents of msg_chunk
        eol_pos = msg_chunk.find(EOL)
        
        # Keep reading the socket until an end of line is encountered or the
        # socket is closed
        while self.open and eol_pos == -1:
            # Read up to MAX characters from the socket
            msg_chunk = self.sock.recv(MAX)

            if not msg_chunk:
                # When recv() on the socket returns the empty string, it 
                # indicates that the other end has closed the socket so add 
                # an end of line to the buffer so that the echoed message can 
                # be delimited 
                self.buffer.append(EOL)
                self.open = False
            else:
                # Append the newest chunk of data to the buffer and look
                # for an end of line in the data
                self.buffer.append(msg_chunk)
                eol_pos = msg_chunk.find(EOL)

        # The last chunk of data in the buffer contains an end of line
        # character but there may be additional bytes after the end of line
        # If so, remove those characters from the buffer and save them in
        # leftover temporarily
        leftover = ""
        if self.open:
            if len(self.buffer[-1])-1 != eol_pos:
                leftover = self.buffer[-1][eol_pos+1:]
                last = self.buffer.pop()
                self.buffer.append(last[0:eol_pos+1])

        # Join all the chunks of data into a string and reset the buffer to 
        # either be empty or contain the leftover chunk of data
        message =  "".join(self.buffer)
        if leftover == "":
            self.buffer = []
        else:
            self.buffer = [leftover]
        return message 






