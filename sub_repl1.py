import asyncio
import code
import sys
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

async def aioinput(prompt=""):
    """Asynchronous input to allow getting user input without blocking the event loop."""
    return await asyncio.get_event_loop().run_in_executor(None, input, prompt)

class AsyncInteractiveConsole(code.InteractiveConsole):
    """An asynchronous version of Python's InteractiveConsole."""
    async def interact(self, banner=None):
        """Handle the interactive session."""
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        sys.ps2 = "... "
        
        if banner:
            print(banner)
        buffer = ""
        while True:
            try:
                # Get command input
                line = await aioinput(sys.ps1 if not buffer else sys.ps2)
                if line is None:
                    break
                buffer += line + "\n"
                # More command or execute
                if code.compile_command(buffer, "<stdin>", "single"):
                    stdout = StringIO()
                    stderr = StringIO()
                    with redirect_stdout(stdout), redirect_stderr(stderr):
                        # Try to execute the accumulated command
                        more = self.push(buffer)
                    # Reset buffer if command was executed
                    if not more:
                        buffer = ""
                    output = stdout.getvalue()
                    error = stderr.getvalue()
                    if output:
                        print(output, end="")
                    if error:
                        print(error, end="", file=sys.stderr)
                else:
                    continue
            except EOFError:
                break

async def main():
    console = AsyncInteractiveConsole()
    await console.interact("Python Async REPL (type 'exit()' or use Ctrl-D to exit)")

if __name__ == "__main__":
    asyncio.run(main())
