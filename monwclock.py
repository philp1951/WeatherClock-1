# Monitor weatherclock.py
# Read PID file and if not running restart

import os, errno, time

while True:
    def pid_exists(pid):
        # Check whether pid exists in the current process table.
        # UNIX only.

        if pid < 0:
            return False
        try:
            os.kill(pid, 0)
        except OSError as err:
            if err.errno == errno.ESRCH:
                # ESRCH == No such process
                return False
            elif err.errno == errno.EPERM:
                # EPERM clearly means there's a process to deny access to
                return True
            else:
                # According to "man 2 kill" possible error values are
                # (EINVAL, EPERM, ESRCH)
                raise
        else:
            return True

    homedir = "/home/phil/weatherpi/"               # EDIT THIS TO BE THE RUNNING DIRECTORY

    firsttime = 1                                   # Set first time flag - no valid PID file at reboot
    if firsttime == 0:                              # Read the PID file
        pidf = open(homedir + "pid.log","r")
        pid = pidf.read()                           # Read PID of running process
        pidf.close()

        pidn = int(pid)                             # Need it to be integer number
        if pid_exists(pidn) == False: os.system("/usr/bin/python3 "+ homedir +"weatherclock.py 2>&1")
    else:  # start it going
        os.system("/usr/bin/python3 "+ homedir +"weatherclock.py 2>&1")
        firsttime = 0                               # Clear firsttime flag
    # now sleep for a minute and go again
    time.sleep(1)               # sleep for a minute
