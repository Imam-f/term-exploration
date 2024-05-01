import os
import pty
import select

import fcntl
import struct
import termios

def main():
    # Create a pseudo-terminal pair
    master, slave = pty.openpty()

    # Fork the current process
    pid = os.fork()

    # Specify the desired terminal size (e.g., 80x24)
    set_terminal_size(slave, 24, 20)

    if pid == 0:
        # Child process
        # Make the slave side of the PTY the standard input, output, and error
        os.setsid()
        os.dup2(slave, 0)
        os.dup2(slave, 1)
        os.dup2(slave, 2)

        # Close the slave descriptor as it's no longer needed in the child
        os.close(slave)
        os.close(master)

        # Execute Bash in interactive mode
        os.execlp('bash', 'bash', '-i')
    else:
        # Parent process
        os.close(slave)  # Close the slave end as it's not needed in the parent

        try:
            while True:
                # Wait for data to become available on the master end or standard input
                # r, w, e = select.select([master, 0], [], [])
                r, w, e = select.select([master, 0], [], [])

                if master in r:
                    # Read from the PTY and write to standard output
                    data = os.read(master, 1024)
                    if not data:  # EOF
                        break
                    print("[tty", data.decode(), end='tty]\n\n')
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
            os.waitpid(pid, 0)

def set_terminal_size(fd, rows, cols):
    # Create the packed struct for the terminal size
    winsize = struct.pack("HHHH", rows, cols, 0, 0)
    # Set the terminal size
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)

if __name__ == "__main__":
    main()
