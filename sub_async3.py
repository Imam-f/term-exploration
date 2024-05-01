import asyncio
import signal


# Ignore SIGTSTP
signal.signal(signal.SIGTSTP, signal.SIG_IGN)

ev = asyncio.Event()

async def read_from_subprocess(process):
    """Asynchronously read lines from subprocess stdout and print them."""
    while True:
        line = await process.stdout.readline()
        if line:
            if line.decode().strip()[-3:] == "end":
                # print("end of output")
                ev.set()
            else:
                # print("| ", line.decode().strip())
                print("| ", line)
        else:
            ev.set()
            break  # No more output

async def error_from_subprocess(process):
    """Asynchronously read lines from subprocess stdout and print them."""
    while True:
        line = await process.stderr.readline()
        if line:
            if line.decode().strip() == "end":
            #     # print("end of output")
                ev.set()
            # else:
            # print("x> ", line.decode().strip())
            print("x> ", line)
        else:
            # ev.set()
            break
            # continue  # No more output

async def write_to_subprocess(process):
    """Asynchronously get user input and write to subprocess stdin."""
    process.stdin.write("set +m".encode() + b'\n')
    process.stdin.write(b'echo end < /dev/null\n')
    try:
        while True:
            # Get input using an asynchronous input function
            await ev.wait()
            ev.clear()
            cmd = await aioinput()
            if cmd.strip().lower() == "exit":
                process.stdin.write_eof()
                break
            process.stdin.write(cmd.encode() + b'\n')
            process.stdin.write(b'echo end < /dev/null\n')
            await process.stdin.drain()  # Ensure the command is sent
            # process.stdin.write(b'\n')
    except asyncio.CancelledError:
        process.stdin.write_eof()

async def aioinput(prompt="> "):
    """Asynchronous input to allow getting user input without blocking the event loop."""
    print(prompt, end="", flush=True)
    return await asyncio.get_event_loop().run_in_executor(None, input)

async def main():
    # Create subprocess with pipes for interaction
    process = await asyncio.create_subprocess_shell(
        'bash --rcfile ./custom_bashrc -i',
        # 'bash',
        # 'python3',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        # text=True
    )

    # Create tasks for reading and writing
    read_task = asyncio.create_task(read_from_subprocess(process))
    error_task = asyncio.create_task(error_from_subprocess(process))
    write_task = asyncio.create_task(write_to_subprocess(process))

    # Wait for all tasks to complete
    ev.set()
    await asyncio.wait([read_task, write_task, error_task], return_when=asyncio.ALL_COMPLETED)

    # Cleanup
    await process.wait()

# Run the main function in the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
