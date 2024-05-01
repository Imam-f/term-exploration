import asyncio

async def read_from_user(proc):
    # Loop to continuously read from user and send to Bash
    try:
        while True:
            user_input = await asyncio.get_running_loop().run_in_executor(None, input, ">>> ")
            if user_input.strip().lower() == 'exit':
                print("Exiting interactive mode.")
                proc.stdin.write(b"exit\n")
                await proc.stdin.drain()
                break
            proc.stdin.write((user_input + '\n').encode())
            await proc.stdin.drain()
    except asyncio.CancelledError:
        pass  # Handle the cancellation of the input reader

async def read_from_bash(proc):
    # Loop to continuously read from Bash and print
    try:
        while True:
            line = await proc.stdout.readline()
            if not line:
                break
            print(line.decode(), end='')
    except asyncio.CancelledError:
        pass  # Handle the cancellation of the bash reader

async def interactive_bash():
    # Start Bash in interactive mode
    proc = await asyncio.create_subprocess_shell(
        '/bin/bash',  # Consider adding -i if specifically needed
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Create tasks for reading from user and Bash
    user_input_task = asyncio.create_task(read_from_user(proc))
    bash_output_task = asyncio.create_task(read_from_bash(proc))

    # Wait for both tasks to complete
    await asyncio.wait([user_input_task, bash_output_task], return_when=asyncio.FIRST_COMPLETED)

    # Cleanup: ensure all tasks are cancelled if one completes
    user_input_task.cancel()
    bash_output_task.cancel()
    await proc.wait()  # Wait for the subprocess to exit

# Run the async function to start interactive mode
asyncio.run(interactive_bash())
