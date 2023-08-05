##########################################################################
# This module aim is to stream Android shadow files to a running device  #
##########################################################################
import time
from os_file_handler import file_handler as fh
from os_android_adb_handler import adb_handler as adb


# Set here the directory in which you download all of the shadow files. It will auto stream
# the newest shadow file to your device.
# NOTICE: Make sure you connect your device using adb before running this function
def stream_shadows_directory(shadows_dir_path):
    # while loop on a directory
    files = fh.get_dir_content(shadows_dir_path, recursive=False, collect_dirs=False, collect_files=True)
    old_file_count = len(files)
    while True:
        files = fh.get_dir_content(shadows_dir_path, recursive=False, collect_dirs=False, collect_files=True)
        if len(files) != old_file_count:
            old_file_count = len(files)
            file = fh.get_latest_added_file(shadows_dir_path)
            if fh.get_extension_from_file(file) != 'crdownload':
                adb.send_file(file, './storage/emulated/0/Download/shadow.9.png')
        time.sleep(1)
        print("Waiting for a shadow update...")