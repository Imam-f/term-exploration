import subprocess

# Start a bash shell in subprocess
process = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def send_command(command):
    """Send a command to the bash process"""
    print(f"Sending command: {command}")
    process.stdin.write(command + "\n")
    process.stdin.flush()  # Ensure the command is sent

def read_output():
    """Read the output of a command"""
    output = []
    # Read line by line until we get the prompt back
    while True:
        line = process.stdout.readline()
        print(line)
        if line.strip() == "end":  # We expect 'end' at the end of command output
            break
        output.append(line)
    return ''.join(output)

# Example usage:
send_command('echo "Hello, World!"')  # Sending a simple echo command
send_command('echo "end"')  # Mark the end of commands
print("Output:")
print(read_output())  # Reading and printing the output

# Important: close the process
process.stdin.close()
process.terminate()
process.wait()
