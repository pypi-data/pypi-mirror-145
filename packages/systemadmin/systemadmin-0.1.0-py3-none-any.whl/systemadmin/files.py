# File : Standard files  | directories
import os


class File:

    def __init__(self, path: str) -> None:
        self.path = path

    def type_of_file(self) -> str:
        if os.path.isfile(self.path):
            return "standard file"
        elif os.path.isdir(self.path):
            return "dir"
        else:
            return "not a file"
