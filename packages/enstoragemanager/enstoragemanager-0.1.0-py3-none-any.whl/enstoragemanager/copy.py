import os
import shutil


class Storage:
    def __init__(self, mount_point, destination, copy_function) -> None:
        self.copy_function = copy_function
        self.mount_point = mount_point
        self.destination = destination
        os.makedirs(self.destination, exist_ok=True)

    def copy_files(self):
        for dirpath, dirname, filename in os.walk(self.mount_point):
            for filenames in filename:
                if filenames.endswith(".JPG"):
                    print(f"copying {filenames}")
                    shutil.copy((os.path.join(dirpath, filenames)), self.destination)
        return "copy"

    def move_files(self):
        for dirpath, dirname, filename in os.walk(self.mount_point):
            for filenames in filename:
                if filenames.endswith(".JPG"):
                    print(f"moving {filenames}")
                    shutil.move((os.path.join(dirpath, filenames)), self.destination)
        return "move"
