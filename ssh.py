import paramiko
from textwrap import dedent

# Set up the SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the remote server
ssh.connect('0.0.0.0', username='', password='')

# Execute the command
stdin, stdout, stderr = ssh.exec_command('ls -l\n')
print(stdout.read().decode())

script = dedent(f"""
    bash -c \"$(cat << EOF
    echo \"Running on remote host\"
    ls -l
    date
    pfetch
    EOF
    )\"
    """)

stdin, stdout, stderr = ssh.exec_command(script)

# Print the output
print(stdout.read().decode())

# Close the connection
ssh.close()

