import os
import tempfile
from contextlib import contextmanager
import subprocess


def safe_subprocess(command_array):
    """Executes shell command. Do not raise

        Args:
            command_array (list): ideally an array of string elements, but
                may be a string. Will be converted to an array of strings

        Returns:
            True/False, command output
    """

    try:
        # Ensure all args are strings
        if isinstance(command_array, list):
            command_array_str = [str(x) for x in command_array]
        else:
            command_array_str = [str(command_array)]
        return True, subprocess.check_output(command_array_str,
                                             stderr=subprocess.STDOUT)
    except OSError as e:
        return False, e.__str__()
    except subprocess.CalledProcessError as e:
        return False, e.output


@contextmanager
def atomic_write(filepath):
    """
        Writeable file object that atomically
        updates a file (using a temporary file).

        :param filepath: the file path to be opened
    """

    # Put tmp file to same directory as target file, to allow atomic move
    realpath = os.path.realpath(filepath)
    tmppath = os.path.dirname(realpath)
    with tempfile.NamedTemporaryFile(dir=tmppath, delete=False) as tf:
        with open(tf.name, mode='w+') as tmp:
            yield tmp
            tmp.flush()
            os.fsync(tmp.fileno())
        os.rename(tf.name, realpath)
