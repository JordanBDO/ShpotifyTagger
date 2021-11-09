import os
import eyed3
import hashlib
import time
from db import Master, getitem

directory = 'C:/Users/jordan.oh/Music/music'
files = os.listdir(directory)
total = len(files)
fl = 1
for filename in files:
    path = os.path.join(directory, filename)
    print(path)
    file = eyed3.load(path=path)
    print('file loaded into eyed3')
    try:
        artists = file.tag.artist
        if ',' in artists:
            artist = artists[0:artists.find(',')]
        else:
            artist = artists
        info = file.tag.title + artist
        hinfo = info.encode(encoding='UTF-8',errors='strict')
        hash = hashlib.sha256(hinfo)
        print('hash created')
    except:
        print(filename, 'could not get info', fl, '/', total)
        fl += 1
        continue

    at = 0
    while at < 10:

        try:
            res = getitem(table='Master', hash=hash.hexdigest(), range=info, fields=['name', 'items', 'tags'])
            if res == 'not found in db':
                print(hash.hexdigest(), info, res, fl, '/', total)
                fl += 1
                break
            file.tag.genre = ' '.join(res['items'])
            if res['tags'][0] == 'Saved - todo':
                file.tag.comments.set(file.tag.comments[0].text + '  #Saved;')
            file.tag.save()
            print('tagged :', filename, file.tag.genre, fl, '/', total)
            fl += 1
            at = 10

        except:
            time.sleep(1)
            print('slept attempt: ',at)
            res = getitem(table='Master', hash=hash.hexdigest(), range=info, fields=['name', 'items'])
            if res == 'not found in db':
                print(hash.hexdigest(), info, res)
                fl += 1
                break
            print(res)
            file.tag.genre = ' '.join(res['items'])
            # file.tag.comments = file.tag.comments + res['tags'][0]
            file.tag.save()
            print('tagged :', filename, file.tag.genre, fl, '/', total)
            fl += 1
            at = 10
        finally:
            at += 1
