# Version 0.2.6
# Changelog
#   - 31.03.2022: Removed documentation about custom usage since the library is now available on PyPI, fixed a bug in the buffer clearing of the serial port
#   - 14.02.2022: Created a workaround for a bug that caused the serial buffer to not clear properly unless updating some specific element in a gui
#   - 26.01.2022: Fixed a bug that caused writing to a port to fail after a reconnect, lowered reconnect speed in favour of stability
#   - 19.01.2022: Added functionality to read data from a serial port via a thread
#   - 14.01.2022: Added functionality to update a canvas with optional refitting of the data, added functionality for reading raw bytes from serial port
#   - 11.01.2022: Added functionality to update a canvas when an included plot has its data changed
#   - 10.01.2022: Added functionality for serial ports including automatically re-establishing connection, if disconnected
#   - 07.01.2022: Initial version

import serial
import time


import matplotlib.figure as fig
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from serial.serialposix import Serial
from serial.threaded import ReaderThread, Protocol
import serial.tools.list_ports

# Custom exception for a closed serial port
class SerialDisconnect(Exception):
    pass

# Prints the argument.
def p(a):
    print(a, end='')

# Prints the argument followed by a newline character.
def pln(*args):
    if len(args) > 0:
        p(args[0])
    print()


# Window to bind events to
window = None

# Updates a canvas with axis in it
def updateCanvas(fig, ax, rescaleX=True, rescaleY=True):
    # store previous axes limits
    xl = ax.get_xlim()
    yl = ax.get_ylim()
    # Refit plot to data
    ax.relim()
    ax.autoscale()
    # Possibly keep previous axis limits
    if not rescaleX:
        ax.set_xlim(xl)
    if not rescaleY:
        ax.set_xlim(yl)
    # Update canvas
    fig.canvas.draw()
    # Flush events (if this was called by a tkinter event)
    fig.canvas.flush_events()

# Protocol for a threaded serial port
# Usage:
#   1. Create object by calling "<port variable> = DSMVLib.sPort(<port name>)"
#   2. Start the thread by calling "<port variable>.start(<maximum buffer size>, <function to call when data is received>)"
# Important notes: 
#   - Currently only supports one serial port open at a time!
#   - Since this port is threaded, it doesn't provide functionality for reading with a timeout!
class sPort(Protocol):
    # Nested class for internal buffer and port
    class Buffer:
        port = None
        content = bytes(0)
        size = 4096
        disconnected = False
        dummyFig = fig.Figure()
    
    buffer = Buffer()

    # Placeholder function to be called when data has been read
    def dummy(self):
        pass

    handleData = dummy

    # Constructor method
    def __init__(self, name="Auto"):
        # Create serial port
        self.buffer.port = self.serPort(name)
    
    # Initializes a serial port
    # name is the name of the port
    def serPort(self, name):
        try:
            if name == "Auto":
                ports=serial.tools.list_ports.comports()
                if len(ports) > 1:
                    name = "/dev/" + ports[1].name
            port = serial.Serial(name)
            return port
        except serial.serialutil.SerialException:
            pln("Could not open the serial port! Try un- and replugging the device or providing the correct port name.")
            raise SerialDisconnect

    # Method start the thread (can't be in the constructor)
    def start(self, maxSize=4096, handleFunc=None):
        # Store function to be called when data is read
        if handleFunc != None:
            sPort.handleData = handleFunc
        # Set the maximum buffer size
        self.buffer.size = maxSize
        # Add a canvas to the dummy figure
        FigureCanvasTkAgg(self.buffer.dummyFig)
        # Initialize reading thread
        self.reader = ReaderThread(self.buffer.port, sPort)
        # Start reading thread
        self.reader.start()
    
    # Callback function to store read data to the internal buffer and possibly do externally configured tasks
    def readStoreBuffer(self, data):
        # Write data to internal buffer if it fits (discard it otherwise)
        if len(self.buffer.content) + len(data) <= self.buffer.size:
            self.buffer.content += data
        self.handleData()

    # Clear the internal buffer
    def clearBuffer(self, clearLine=False):
        # Flush events
        self.buffer.dummyFig.canvas.flush_events()
        # Update the GUI
        window.update_idletasks()
        if clearLine:
            # Empty the buffer up to the last newline character
            numBytes = len(self.buffer.content)
            for newLineIndex in range(numBytes-1, -1, -1):
                p("index: ")
                pln(newLineIndex)
                if chr(self.buffer.content[newLineIndex]) == "\n":
                    self.buffer.content = self.buffer.content[newLineIndex+1:len(self.buffer.content)]
                    break
        else:
            # empty the buffer
            self.buffer.content = bytes(0)

    def connection_made(self, transport):
        """Called when reader thread is started"""
        pass
        #print("Connected, ready to receive data...")

    def data_received(self, data):
        """Called with snippets received from the serial port"""
        window.after(0, self.readStoreBuffer, data)

    def reopen(self):
        newPort = None
        try:
            # Get available ports
            ports=serial.tools.list_ports.comports()
            if len(ports) > 1:
                newPort = Serial("/dev/" + ports[1].name)
        except serial.serialutil.SerialException:
            pass
        if newPort != None:
            self.buffer.port = newPort
            self.buffer.disconnected = False
            newReader = ReaderThread(self.buffer.port, sPort)
            newReader.start()
        else:
            window.after(1, self.reopen)

    def connection_lost(self, exc=None):
        print("Serial port disconnected. Trying to reconnect...")
        self.reopen()
        self.buffer.disconnected = True
    
    # Returns wether the port is disconnected
    def disconnected(self):
        return self.buffer.disconnected

    # Reads a specified number of bytes (1 if no parameter is given) from the wrapped serial port (if there is data available), 
    # removes it from the buffer and returns it
    def readB(self, bytes=1):
        numBytes = len(self.buffer.content)
        if numBytes < bytes:
            return "not enough data"
        retVal = self.buffer.content[0:bytes]
        self.buffer.content = self.buffer.content[bytes:len(self.buffer.content)]
        return retVal

    # Reads a line from the wrapped serial port (if there is one available), 
    # removes it from the buffer and returns it as a string (without the newline character at the end).
    def readL(self, forceWait=True):
        numBytes = len(self.buffer.content)
        newLineIndex = 0
        for newLineIndex in range(numBytes):
            if chr(self.buffer.content[newLineIndex]) == "\n":
                try:
                    retVal = self.buffer.content[0:newLineIndex].decode()
                except UnicodeDecodeError:
                    retVal = "Read data isn't a string"
                self.buffer.content = self.buffer.content[newLineIndex+1:len(self.buffer.content)]
                return retVal
        return "not enough data"
    
    # Writes a line to the wrapped serial port.
    def writeL(self, s):
        try:
            self.buffer.port.write((s + '\n').encode())
        except OSError:
            raise SerialDisconnect
