#!/usr/bin/python
# Description: Monitors and moves file to their Appropriate Folder on the Homw Directory

# Inspired by Kalle Hadden


import os
import json
import time
import shutil
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



with open('config.yml') as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

folder_to_track = data.get('track')
folder_destination = data.get('dst_path')
extenstions = data.get('content_path')


class MyHandler(FileSystemEventHandler):

    def on_modified(self, event):
        for filename in os.listdir(folder_to_track):
            if not os.path.isdir(os.path.join(folder_to_track, filename)):
                i = 1
                new_name = filename
                split_name = os.path.splitext(new_name)
                while os.path.exists(os.path.join(folder_destination, new_name)):
                    print('Renaming ' + new_name)
                    new_name = split_name[0] + '(' +  str(i) + ')' + split_name[1]
                    i += 1
                if split_name[1] in extenstions:
                    ext = extenstions.get(split_name[1])
                    src = os.path.join(folder_to_track, filename)
                    dst = os.path.join(os.path.join(folder_destination, ext), new_name)
                    print('Copying {} to --> {}'.format(src, dst))
                    shutil.move(src, dst)
            else:
                print('Directory found: ' + filename)


event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
print('[+] Created handler')
print('[+] Starting program!')
observer.start()
print('[+] Program Running')

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print('\n[-] Stopping program')
    observer.stop()

observer.join()
