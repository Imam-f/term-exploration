import subprocess
import os

p = subprocess.Popen(
    # list("python3 sub2.py".split(" ")),
    list("bash".split(" ")),
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE
)

p.stdin.write(b"ls\n")
p.stdin.write(b"pwd\n")
out, err = p.communicate()
print(out.decode())