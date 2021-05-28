from pwn import *

arg = pack(0x1337c0de, 32)
write("gilarg", arg)

# scp -P 2225 gilarg  maze3@maze.labs.overthewire.org:/tmp/gilarg
# ./maze3 `cat /tmp/gilarg`

# deekaihiek

