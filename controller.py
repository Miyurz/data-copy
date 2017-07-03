import time
import random
import threading
import sys
import subprocess
import Queue


class AsynchronousFileReader(threading.Thread):
    '''
    Read asynchronously from a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''

    def __init__(self, fd, queue):
        assert isinstance(queue, Queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue

    def run(self):
        '''Read lines and put them on the queue.'''
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()


#def copyPeerToPeerInfinite(node):
#    while True:
#        time.sleep(5)
#        print("Copy file to node %s"%node) 

def copyPeerToPeer(node):
    print("Copy file to node %s"%node)
    process = subprocess.Popen(
                               [
                                '/bin/bash','-c',
                                '. functions.sh; copyPeerToPeer '+(str(node))
                               ],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE
                              )
    statusProgress(process.stdout, process.stderr)


def downloadFromSlowSource():
    print("About to download the big file \n")
    process = subprocess.Popen(
                               [
                                '/bin/bash','-c',
                                '. functions.sh; downloadFromSlowSource'
                               ],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE
                              )
    statusProgress(process.stdout, process.stderr)

def statusProgress(out, err):
    # Launch the asynchronous readers - stdout and stderr.
    stdout_queue = Queue.Queue()
    stdout_reader = AsynchronousFileReader(out, stdout_queue)
    stdout_reader.start()

    stderr_queue = Queue.Queue()
    stderr_reader = AsynchronousFileReader(err, stderr_queue)
    stderr_reader.start()

    # Check the queues for output toll you see an EOF
    while not stdout_reader.eof() or not stderr_reader.eof():
        while not stdout_queue.empty():
            line = stdout_queue.get()
            print 'Received line on standard output: ' + repr(line)

        while not stderr_queue.empty():
            line = stderr_queue.get()
            print 'Received line on standard error: ' + repr(line)

        time.sleep(.1)

    # Join the threads 
    stdout_reader.join()
    stderr_reader.join()

    # Close subprocess's file descriptors.
    out.close()
    err.close()


def main():

    #Download from the source
    dl = threading.Thread( target=downloadFromSlowSource)
    dl.daemon = True
    dl.start()

    #Read the node inventory
    try:
        f = open('inventory','r')
        for node in f:
            ''' Call bash function copyPeerToPeer to rsync the file being downloaded to Node
                Spawn n threads where n = number of node '''
            t = threading.Thread( name=node, target=copyPeerToPeer, args = (node,) )
            t.daemon = True
            t.start()
    except IOError:
        print("Wrong file or file path")

    t.join()
    dl.join()

main()
print("Out of main")
