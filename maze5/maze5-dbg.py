from pwn import *
from pwnhelper.gdb import *


local_dir = None
remote_binary = None
cloned_binary = None
libc = None
libc_path = None
ld_path = None
elf = None
def connect(level,pw):
    global remote_binary
    global local_dir
    global cloned_binary
    global port
    global libc
    global elf
    global libc_path
    global ld_path
    local_dir = "/home/kali/PycharmProjects/maze/maze"+level
    remote_binary = "/maze/maze"+level
    cloned_binary = local_dir+remote_binary
    s = ssh("maze"+level, "176.9.9.172", password=pw, cache=True, port=2225)
    s.libs(remote_binary, local_dir)
    log.info(f"cloned_binary: {cloned_binary}")
    elf = ELF(cloned_binary)
    libc_path = local_dir + "/lib32/libc.so.6"
    ld_path = local_dir + "/lib/ld-linux.so.2"
    libc = ELF(libc_path)
    context.clear()
    context.binary = cloned_binary
    context.log_file = "/tmp/docgillog"
    return s

# cd ..;update-pwnhelper;install-pwnhelper; cd maze5/


def pad(s, slen):
    return s+b"B"*(slen-len(s))


s = connect("5", "ishipaeroo")


# binary = "/home/kali/PycharmProjects/maze/maze5/maze/maze5"
binary = cloned_binary

context.binary = binary
context.terminal = ["tmux", "splitw", "-h"]

# env = {"LD_PRELOAD": libc_path + " " + ld_path}
# env = {"LD_PRELOAD": libc_path}

dbg = Debugger(binary)
# dbg.gdb.execute("set stop-on-solib-event 1")
# print(context)


# # should be in main frame
dbg.go_to("main")
# dbg.gdb.continue_and_wait()
# data = dbg.io.recv()
# log.info(f"data: {data}")

# dbg.send("AAAABBBB")

# data = dbg.io.recv()
# log.info(f"data: {data}")

# print("frame: " + str(main.name))

# base_pointer = main.read_register("ebp")
# print("base pointer: ")
# print(base_pointer)


