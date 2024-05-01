import os
import pty
import select

import termios
import tty

def main():
    # Create a pseudo-terminal pair
    master, slave = pty.openpty()
    master2, slave2 = pty.openpty()

    # Fork the current process
    pid = os.fork()

    # Set terminal to raw mode
    fd = slave
    oldterm = termios.tcgetattr(fd)
    tty.setraw(fd)
    # termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    if pid == 0:
        # Child process
        # Make the slave side of the PTY the standard input, output, and error
        os.setsid()
        os.dup2(slave, 0)
        os.dup2(slave, 1)
        # os.dup2(slave, 2)
        os.dup2(slave2, 2)

        # Close the slave descriptor as it's no longer needed in the child
        os.close(slave)
        os.close(slave2)
        os.close(master)
        os.close(master2)

        # Execute Bash in interactive mode
        os.execlp('bash', 'bash', '-i')
    else:
        # Parent process
        os.close(slave)  # Close the slave end as it's not needed in the parent
        os.close(slave2)  # Close the slave end as it's not needed in the parent

        try:
            while True:
                # Wait for data to become available on the master end or standard input
                # r, w, e = select.select([master, 0], [], [])
                r, w, e = select.select([master, master2, 0], [], [])

                if master in r:
                    # Read from the PTY and write to standard output
                    data = os.read(master, 1024)
                    if not data:  # EOF
                        break
                    # print("[tty", data.decode(), end='tty]\n\n')
                    print(data.decode(), end='')
                    # os.write(1, data)

                if master2 in r:
                    # Read from the PTY and write to standard output
                    try:
                        # data = 0
                        data = os.read(master2, 1024)
                        pass
                    except Exception as e:
                        data = b'0'
                        # print(e, e.__traceback__)
                        # os.write(1, data)
                    if not data:  # EOF
                        break
                    else:
                        if data != b'0':
                            # print("[err ", data.decode(), end='err]\n\n')
                            print(data.decode(), end='')
                            # os.write(1, data)

                if 0 in r:
                    # Read from standard input and write to the PTY
                    data = os.read(0, 1024)
                    os.write(master, data)
        except OSError:
            pass
        finally:
            # Clean up the PTY and wait for the child process to finish
            os.close(master)
            os.close(master2)
            os.waitpid(pid, 0)

if __name__ == "__main__":
    main()
