
#!/usr/bin/env python3
import os
import sys
import stat
import errno

def pipe_is_reading(pipe_path):
    """Check if the FIFO has a reader."""
    try:
        fd = os.open(pipe_path, os.O_WRONLY | os.O_NONBLOCK)
        os.close(fd)
        return True
    except OSError as e:
        if e.errno == errno.ENXIO:
            return False
        raise

def send_actions(actions):
    """
    Write a list of action bytes to the pipe.
    Each action should be a byte string.
    """
    pipe_path = os.environ.get("DOTOOL_PIPE", "/tmp/dotool-pipe")
    
    # Check if pipe exists and has write permission.
    if os.path.exists(pipe_path) and stat.S_ISFIFO(os.stat(pipe_path).st_mode):
        if not os.access(pipe_path, os.W_OK):
            sys.stderr.write(f"dotoolc: the pipe does not grant write permission: {pipe_path}\n")
            sys.exit(1)
    # Verify that a reader is present.
    if not pipe_is_reading(pipe_path):
        sys.stderr.write(f"dotoolc: no dotoold instance is reading the pipe: {pipe_path}\n")
        sys.exit(1)
    
    try:
        with open(pipe_path, 'w') as pipe:
            # Write each action followed by a newline.
            for action in actions:
                pipe.write(action.decode() + "\n")
                pipe.flush()
    except BrokenPipeError:
        sys.exit(0)

def get_move(x, y):
    """Return a move action as a byte string."""
    return f"mouseto {x} {y}".encode()

def get_button_down():
    """Return a left button down action as a byte string."""
    return b"buttondown left"

def get_button_up():
    """Return a left button up action as a byte string."""
    return b"buttonup left"

def pipe_server():
    """
    Acts like the original dotoolc:
    Reads from stdin and writes to the named pipe.
    """
    pipe_path = os.environ.get("DOTOOL_PIPE", "/tmp/dotool-pipe")
    
    if os.path.exists(pipe_path) and stat.S_ISFIFO(os.stat(pipe_path).st_mode):
        if not os.access(pipe_path, os.W_OK):
            sys.stderr.write(f"dotoolc: the pipe does not grant write permission: {pipe_path}\n")
            sys.exit(1)
    if not pipe_is_reading(pipe_path):
        sys.stderr.write(f"dotoolc: no dotoold instance is reading the pipe: {pipe_path}\n")
        sys.exit(1)
    try:
        with open(pipe_path, 'w') as pipe:
            for line in sys.stdin:
                pipe.write(line)
                pipe.flush()
    except BrokenPipeError:
        sys.exit(0)

def main():
    # If arguments are provided, show help.
    if len(sys.argv) != 1:
        sys.stderr.write(
            "dotoolc writes its stdin to the pipe being read by dotoold.  "
            "dotoolc will exit immediately if the pipe is not being read.  "
            "The path of the pipe is $DOTOOL_PIPE else /tmp/dotool-pipe.\n"
        )
        sys.exit(0)
    pipe_server()


if __name__ == "__main__":
    main()
