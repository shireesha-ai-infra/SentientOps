import os

def is_ci():
    return os.getenv("CI") =="true"