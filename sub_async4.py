import asyncio

async def read_from_subprocess(process):
    """Asynchronously read lines from subprocess stdout and print them."""
    while True:
        line = await process.stdout.readline()
        if line:
            print(line.decode().strip(), end="", flush=True)  # Print output without additional newline
        else:
            break  # No more output

async def write_to_subprocess(process):
    """Asynchronously get user input and write to subprocess stdin."""
    try:
        while True:
            # Get input using an asynchronous input function
            cmd = await aioinput()
            if cmd.strip().lower() == "exit":
                process.stdin.write_eof()
                break
            process.stdin.write(cmd.encode() + b'\n')
            await process.stdin.drain()  # Ensure the command is sent
    except asyncio.CancelledError:
        process.stdin.write_eof()

async def aioinput(prompt=""):
    """Asynchronous input to allow getting user input without blocking the event loop."""
    return await asyncio.get_event_loop().run_in_executor(None, input, prompt)

async def main():
    # Create subprocess with pipes for interaction and set a custom PS1
    custom_prompt = "\\w \$ "  # e.g., "/path/to/dir $ "
    bash_command = f'export PS1="{custom_prompt}"; exec bash -i'

    process = await asyncio.create_subprocess_shell(
        bash_command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Create tasks for reading and writing
    read_task = asyncio.create_task(read_from_subprocess(process))
    write_task = asyncio.create_task(write_to_subprocess(process))

    # Wait for all tasks to complete
    await asyncio.wait([read_task, write_task], return_when=asyncio.ALL_COMPLETED)

    # Cleanup
    await process.wait()

# Run the main function in the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
