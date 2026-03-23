import sys, tty, termios, select

def read_key():
    char = sys.stdin.read(1)
    if char == '\x1b':
        r, _, _ = select.select([sys.stdin], [], [], 0.1)
        if r:
            char += sys.stdin.read(2)
    return char

fd = sys.stdin.fileno()
old = termios.tcgetattr(fd)
try:
    tty.setcbreak(fd)
    # print("Press a key (q to quit)")
    # while True:
    #     k = read_key()
    #     print(repr(k))
    #     if k == 'q': break
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old)
