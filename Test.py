import os
import eyed3
import hashlib
import time
from db import Master, getitem

directory = 'C:/Users/jordan.oh/Music/test'
files = os.listdir(directory)
total = len(files)
fl = 1
for filename in files:
        path = os.path.join(directory, filename)
        file = eyed3.load(path=path)
        print('file loaded into eyed3')
        print(dir(file.tag))
