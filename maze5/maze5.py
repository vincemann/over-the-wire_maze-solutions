from pwn import *

# reverse engineered code (with ghidra)

'''
int main(void)

{
  size_t user_len;
  long debugging;
  int foo_result;
  char pass [9];
  char user [9];
  
  puts("X----------------");
  printf(" Username: ");
  __isoc99_scanf(&DAT_0804877e,user);
  printf("      Key: ");
  __isoc99_scanf(&DAT_0804877e,pass);
  user_len = strlen(user);
  if ((user_len == 8) && (user_len = strlen(pass), user_len == 8)) {
    // debugging protection, this will return -1 when debugging program
    debugging = ptrace(PTRACE_TRACEME,0,0,0);
    if (debugging == 0) {
      foo_result = foo(user,pass);
      if (foo_result == 0) {
        puts("\nNah, wrong.");
      }
      else {
        puts("\nYeh, here\'s your shell");
        system("/bin/sh");
      }
    }
    else {
      puts("\nnahnah...");
    }
    return 0;
  }
  puts("Wrong length you!");
                    /* WARNING: Subroutine does not return */
  exit(-1);
}




int foo(char *username,char *pass)

{
  size_t username_len;
  char cStack22;
  char printlol_s [9];
  int x;
  int i;
  int count1;
  int count2;
  
  printlol_s._0_4_ = 0x6e697270;
  printlol_s._4_4_ = 0x6c6f6c74;
  printlol_s[8] = '\0';
  i = 0;
  // modify printlol_s according to username
  while (username_len = strlen(username), (uint)i < username_len) {
    printlol_s[i] = printlol_s[i] - (username[i] + -0x41 + (char)i * '\x02');
    i = i + 1;
  }
  // check if modified printlol_s is supplied key
  do {
    count1 = i + -1;
    if (i == 0) {
      return 1;
    }
    count2 = i + -1;
    i = count1;
  } while (printlol_s[count2] == pass[count1]);
  return 0;
}

'''

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


s = connect("5", "ishipaeroo")

username = b"A"*8
printlol_s = b"printlol"
wanted_key = b""
for i in range(8):
    # printlol_s[i] = printlol_s[i] - (username[i] + -0x41 + i * b'\x02')
    char = printlol_s[i] - (username[i] - 0x41 + i * 2)
    log.info("char: " + hex(char))
    log.info(f"char: {char}")
    wanted_key += pack(char, 8)
    log.info(f"wanted_key: {wanted_key}")

io = s.process([remote_binary])
io.sendline(username)
io.sendline(wanted_key)
# "heres your shell"
log.info(io.recv())
io.interactive()

# epheghuoli