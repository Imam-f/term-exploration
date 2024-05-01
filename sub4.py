import subprocess

# Start a Bash shell in interactive mode
process = subprocess.Popen(["/bin/bash", "-i"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Example of sending a command to the Bash shell
process.stdin.write('echo "Hello from Bash!"\n')
process.stdin.flush()

# Read the output from Bash
output = process.stdout.readline()
print(output)

output = process.stderr.readline()
print(output)

# Close the Bash shell
process.stdin.write('exit\n')
process.stdin.flush()
process.wait()
