import os
import subprocess
import tempfile as tf
from . import vars
from .config import get_token
from .cc_debug import cc_print
from time import sleep

def __quit__(tmp, ssh_timeout=False):
    # Remote process has finished
    os.system("kill $(pidof tail) 2>/dev/null")
    # Now we can safely remove the local temp file
    subprocess.run("rm {}".format(tmp), shell=True)
    # Remove the remote temp file, if any
    if ssh_timeout is False:
        os.system("/usr/bin/ssh -p {} {} 'rm {}'".format(vars.ssh_port, vars.ssh_host, tmp))
    # Exit to prevent the calling script to run locally after remote exeuction
    exit(0)

def remote_exec(path, rdir="./", verbose=True, logfile="nohup.out"):
    # If localhost, return
    if 'localhost' in vars.ssh_host or '127.0.0.1' in vars.ssh_host:
        cc_print("Running on local machine...", 2)
        return
    cc_print("Running from file: {}".format(path), 1)

    # Check if this file is already running remotely
    # >>> TO DO

    # Open the calling script (from path) and read the file
    fin = open(path, 'r')
    # Split the script and take everything after separator
    s = fin.read().split("__file__")[-1]
    s = s[s.find("\n")+1:len(s)]   

    # Do we need to import CloudComputing? 
    if "CloudComputing" in s or "cc" in s:
        s = "import CloudComputing as cc\ncc.vars.token = {}\ncc.__token__ = cc.vars.token\ncc.connect()\n".format(get_token()) + s
    
    # Write to file
    tmp = os.path.join(tf.gettempdir(), os.urandom(8).hex() + '.py')
    fout = open(tmp, 'w')
    fout.write(s)
    fout.close()
    
    # Clear nohup.out (if any)
    os.system('echo "---" > {}/nohup.out'.format(os.environ['HOME']))
    
    # Copy the temp file (script) to the remote working dir
    xmd = "/usr/bin/scp -o ConnectTimeout=2 -P {} {} {}:/tmp/ > /dev/null".format(vars.ssh_port, tmp, vars.ssh_host) # Copy to /tmp/
    r = subprocess.Popen(xmd, shell=True)
    r.wait()
    # Check if SSH connection timed-out
    if r.returncode == 1:
        cc_print("SSH connection timed out! Check settings and retry.", 2)
        __quit__(tmp, ssh_timeout=True)
    
    # Command to run over ssh
    cmd = cmd = "nohup /usr/bin/ssh -p {} {} 'cd {} &&".format(vars.ssh_port, vars.ssh_host, rdir)
    cmd = cmd + " python -u {} &' > {}/{}".format(tmp, os.environ['HOME'], logfile) # Run file from /tmp
    # '&' in remote command will not exit if we close the local shell
    if not verbose:
        cmd = cmd + " 1>/dev/null 2>&1"
    if logfile != 'nohup.out':
        cc_print("Logging to file: {}".format(logfile), 1)
        cmd = cmd + " > {}".format(logfile)
    print(cmd)
    r = subprocess.Popen(cmd, shell=True)   # Popen is non blocking, code execution locally will continue
    subprocess.Popen("tail -f {}/{}".format(os.environ['HOME'], logfile), shell=True)    

    while r.poll() is None:
        sleep(0.75)
        # Catch here CTRL-X to stop remote execution > to do
        # Catch here CTRL-C > close local only and continue on remote server
    
    __quit__(tmp)