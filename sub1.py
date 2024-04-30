import subprocess
import os


r_pipe, w_pipe = os.pipe()

os.write(w_pipe, b"ls\n")

os.write(w_pipe, b"cd ..\n")
os.write(w_pipe, b"pwd\n")
os.write(w_pipe, b"ls\n")
os.close(w_pipe)

shell = subprocess.run(
    # list("python3 sub2.py".split(" ")),
    list("sh".split(" ")),
    stdin=r_pipe,
    stdout=subprocess.PIPE,
    # shell=True
)

# shell.stdin.write(b"hello")
print(shell.stdout.decode("utf-8"))