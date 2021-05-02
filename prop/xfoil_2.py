"""
This file contains all code necessary for interfacing with XFOIL.
The Xfoil class circumvents blocking problems (caused by the interactive
nature of XFOIL) by using the NonBlockingStreamReader class, that runs the
blocking some_xfoil_subprocess.stdout.readline() call in a separate thread,
exchanging information with it using a queue.
This enables the Xfoil class to interact with XFOIL, and to read polars from
stdout instead of having to write a file to disk, eliminating latency there.
(Airfoil data still needs to be read from a file by XFOIL.)
Multiple XFOIL subprocesses can be run simultaneously, simply by constructing
the Xfoil class multiple times.
As such, this is probably the fastest and most versatile XFOIL automization
script out there. (I've seen a good MATLAB implementation, but it still relied
on files for output, and was not interactive.)
"""


import subprocess as subp
import numpy as np
import os.path
import re
import time

from threading import Thread
from queue import Queue, Empty


'''
   INSTALL from https://github.com/RobotLocomotion/xfoil.git
'''


def get_polar(airfoil, alpha, Re, Mach=None,
             normalize=True, show_seconds=None, iterlim=None, gen_naca=False):
    """
    Convenience function that returns polar for specified airfoil and
    Reynolds number for (range of) alpha or cl.
    Waits on XFOIL to finish so is blocking.
    
    args:
       airfoil        -> Airfoil file or NACA xxxx(x) if gen_naca flag set.
       alpha          -> Single value or list of [start, stop, interval].
       Re             -> Reynolds number
    kwargs:
       Mach           -> Mach number
       normalize=True -> Normalize airfoil through NORM command
       plot=False     -> Display XFOIL plotting window
       iterlim=None   -> Set a new iteration limit (XFOIL standard is 10)
       gen_naca=False -> Generate airfoil='NACA xxxx(x)' within XFOIL
    """
    # Circumvent different current working directory problems
    print(alpha, end=' ') 
    path = os.path.dirname(os.path.realpath(__file__))
    xf = Xfoil(path)

    if normalize:
        xf.cmd("NORM")
    # Generate NACA or load from file
    if gen_naca:
        xf.cmd(airfoil)
    else:
        xf.cmd('LOAD {}\n\n'.format(airfoil),
               autonewline=False)
    if not show_seconds:
        xf.cmd("PLOP\nG\n\n", autonewline=False)
    #xf.cmd("GDES")
    #xf.cmd("CADD\n\n1\n\n\n", autonewline=False)
    xf.cmd("PCOP")
    # Disable G(raphics) flag in Plotting options
    xf.cmd("PLOP\nG\n\n", autonewline=False)
    # Enter OPER menu
    xf.cmd("OPER")
    xf.cmd("VPAR\nVACC 0.0\nN 6\n\n", autonewline=False)
    if iterlim:
        xf.cmd("ITER {:.0f}".format(iterlim))
    xf.cmd("VISC {}".format(Re))
    #xf.cmd("ALFA 3.0")
    #xf.cmd("INIT")
    if Mach:
        xf.cmd("MACH {:.3f}".format(Mach))

    output = ['']
    # Turn polar accumulation on, double enter for no savefile or dumpfile
    xf.cmd("PACC\n\n\n", autonewline=False)
    # Calculate polar
    try:
        a = alpha
        xf.cmd("{:s} {:.3f}".format("ALFA", a))
        test = True
        start_time = time.time()

        while test:
            line = xf.readline()
            if line:
                output.append(line)
                #print line
                if re.search("Point added to stored polar", line):
                    test = False
                if re.search("VISCAL:  Convergence failed", line):
                    xf.cmd("INIT")
                    #print "Convergence failed at alpha=%f. Initializing boundary layer" % a
                    test = False
                #if re.search("TRCHEK2: N2 convergence failed", line):
                    #xf.cmd("INIT")
                    #print "Convergence failed at alpha=%f. Initializing boundary layer" % a
                    #test = False
            else:
                seconds = time.time() - start_time
                if seconds > 30.0:
                    print("Termination under way. Taking too long")

                    xf.close()
                    raise Exception('Runtime took too long')
                
        
                #if (re.search("CPCALC: Local speed too large.", line)):
                    #print "CPCALC: Local speed too large" % a
                    #test = False
        print(("Simulation took {} seconds".format(time.time() - start_time)))
        # List polar and send recognizable end marker
        xf.cmd("PLIS\nENDD\n\n", autonewline=False)
        
        #print "Xfoil module starting read"
        # Keep reading until end marker is encountered
        while not re.search("ENDD", output[-1]):
            seconds = time.time() - start_time
            if seconds > 30.0:
                print("Termination under way. Taking too long")

                xf.close()
                raise Exception('Runtime took too long')

            line = xf.readline()
            if line:
                #print "End Search %s" % line
                output.append(line)
                #if (re.search("CPCALC: Local speed too large.", line)):
                    #break
        return parse_stdout_polar(output)
    except Exception:
        return None

def get_polars(airfoil, alpha, Re, Mach=None,
             normalize=True, show_seconds=None, iterlim=None, gen_naca=False):

    polar = None
        
    for a in alpha:
        results = get_polar(airfoil, a, Re, Mach, normalize, show_seconds, iterlim, gen_naca)
        if results is not None:
            labels = results[1]
            values = results[0]
            
            if (polar is None):
                polar = {}
                for label in labels:
                    polar[label] = []
            
            for v in values:
                for label, value in zip(labels, v):
                    polar[label].append(value)
    return polar

def parse_stdout_polar(lines):
    """Converts polar 'PLIS' data to array"""    
    def clean_split(s): return re.split('\s+', s.replace('\n',''))[1:]

    # Find location of data from ---- divider
    for i, line in enumerate(lines):
        if re.match('\s*---', line):
            dividerIndex = i
    
    # What columns mean
    data_header = clean_split(lines[dividerIndex-1])

    # Clean info lines
    info = ''.join(lines[dividerIndex-4:dividerIndex-2])
    info = re.sub("[\r\n\s]","", info)
    # Parse info with regular expressions
    def p(s): return float(re.search(s, info).group(1))
    infodict = {
     'xtrf_top': p("xtrf=(\d+\.\d+)"),
     'xtrf_bottom': p("\(top\)(\d+\.\d+)\(bottom\)"),
     'Mach': p("Mach=(\d+\.\d+)"),
     'Ncrit': p("Ncrit=(\d+\.\d+)"),
     'Re': p("Re=(\d+\.\d+e\d+)")
    }

    # Extract, clean, convert to array
    datalines = lines[dividerIndex+1:-2]
    data_array = np.array(
    [clean_split(dataline) for dataline in datalines], dtype='float')

    return data_array, data_header, infodict


class Xfoil():
    """
    This class basically represents an XFOIL child process, and should
    therefore not implement any convenience functions, only direct actions
    on the XFOIL process.
    """
    
    def __init__(self, path="/usr/bin"):
        """Spawn xfoil child process"""
        xf = "/home/tim/github/xfoil/build/bin/xfoil"
        #xf = "/usr/bin/xfoil"
        self.xfinst = subp.Popen(xf,
                  stdin=subp.PIPE, stdout=subp.PIPE, stderr=subp.PIPE)
        self._stdoutnonblock = NonBlockingStreamReader(self.xfinst.stdout)
        self._stdin = self.xfinst.stdin
        self._stderr = self.xfinst.stderr

    def cmd(self, cmd, autonewline=True):
        """Give a command. Set newline=False for manual control with '\n'"""
        n = '\n' if autonewline else ''
        #print (cmd + n),
        self.xfinst.stdin.write(cmd + n)

    def readline(self):
        """Read one line, returns None if empty"""
        return self._stdoutnonblock.readline()

    def close(self):
        #print "Xfoil: instance closed through .close()"
        self.xfinst.kill()
    def __enter__(self):
        """Gets called when entering 'with ... as ...' block"""
        return self
    def __exit__(self):
        """Gets called when exiting 'with ... as ...' block"""
        #print "Xfoil: instance closed through __exit__"
        self.xfinst.kill()
    def __del__(self):
        """Gets called when deleted with 'del ...' or garbage collected"""
        #print "Xfoil: instance closed through __del__ (e.g. garbage collection)"
        self.xfinst.kill()


class UnexpectedEndOfStream(Exception): pass

class NonBlockingStreamReader:
    """XFOIL is interactive, thus readline() blocks. The solution is to
       let another thread handle the XFOIL communication, and communicate
       with that thread using a queue.
       From http://eyalarubas.com/python-subproc-nonblock.html"""
 
    def __init__(self, stream):
        '''
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        '''
        self._s = stream
        self._q = Queue()
        def _populateQueue(stream, queue):
            '''
            Collect lines from 'stream' and put them in 'quque'.
            '''
            while True:
                line = stream.readline()
                #sleep(0.1)
                if line:
                    queue.put(line)
                    #print line
                else:
                    #print "NonBlockingStreamReader: End of stream"
                    # Make sure to terminate
                    return
        self._t = Thread(target = _populateQueue,
                args = (self._s, self._q))
        self._t.daemon = True
        # Start collecting lines from the stream
        self._t.start()

    def readline(self, timeout = None):
        try:
            if timeout is not None:
                return self._q.get(block = True, timeout = timeout)
            else:
                return self._q.get(block = False)

        except Empty:
            return None


import foil

if __name__ == "__main__":
    polar = get_polar("NACA 2215", 5, 5E4, Mach=.06, gen_naca=True, show_seconds=20)
    print(polar)
    polars = get_polars("NACA 2215", np.arange(-30,30,3), 5E4, Mach=.06, gen_naca=True, show_seconds=20)
    print(polars['CL'])
