import platform
import sys

def validate_environment():

    if sys.version_info < (3, 10):
        raise RuntimeError("Python 3.10+ required.")

    print("Environment validated:")
    print("Platform:", platform.platform())
