import spotipy
from spotipy.oauth2 import SpotifyOAuth
import hashlib
import time
from db import Master
clientid = 'bcf5ae487d80494faefae8a16bb3eba3'
clientsecret = 'af12f89cf2da44e6a042943d1c0a0ed5'
redirecturi = 'http://localhost:8888/callback'
scope = "user-library-read, playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=clientid,client_secret=clientsecret,redirect_uri=redirecturi, open_browser=False))


def run(playlists):

    exists = []

    cleanres = {}
    # results = sp.current_user_playlists()
    ploffset = 0
    totalpl = 1
    items = []
    while ploffset < totalpl:
        plresults = sp.user_playlists('12179895190', offset=ploffset)
        totalpl = plresults['total']
        for item in plresults['items']:
            items.append(item)
        ploffset += 50
    for item in items:
        print(item['name'])
        if item['name'] in playlists:
            print('started loading :', item['name'])
            offset = 0
            totaltracks = 1
            while offset < totaltracks:
                tracks = []
                playlist = sp.playlist_items(playlist_id=item['id'], limit=100, offset=offset)
                for track in playlist['items']:
                    tracks.append(track)
                totaltracks = playlist['total']
                print("total tracks:", totaltracks, "Offset:", offset)
                offset += 100
                for track in tracks:
                    artist = track['track']['artists'][0]['name']
                    a = track['track']['name'] + artist
                    h = hashlib.sha256(a.encode(encoding='UTF-8', errors='strict'))
                    if h.hexdigest() in exists:
                        print('Skipped', a)
                        continue
                    saved = None
                    if track['track']['uri'][0:13] != 'spotify:local':
                        if sp.current_user_saved_tracks_contains(tracks=[track['track']['uri']])[0] == True:
                            saved = 'Saved - todo'
                    if h.hexdigest() in cleanres:
                        cleanres[h.hexdigest()]['items'].append('#'+item['name']+';')
                    else:
                        cleanres[h.hexdigest()] = {'range': a, 'items': ['#'+item['name']+';'], 'tags': [saved], 'uri': track['track']['uri']}

            print('finished loading :', item['name'])

    keylist = list(cleanres.keys())
    length = len(keylist)
    currentbatch = 0

    def batchwrite(list,keys,currbatch,len):
        with Master.batch_write(auto_commit=True) as batch:
            items = [Master(hash=keys[x], name=list[keys[x]]['range'], items=list[keys[x]]['items'], tags=list[keys[x]]['tags'], uri=list[keys[x]]['uri']) for x in range(currbatch, min((currbatch + 300), len))]
            for item in items:
                batch.save(item)
                print('Saved: ', item)

    while currentbatch < length:
        try:
            batchwrite(list=cleanres, keys=keylist, currbatch=currentbatch, len=length)
            currentbatch += 300
        except:
            time.sleep(15)
            batchwrite(list=cleanres, keys=keylist, currbatch=currentbatch, len=length)
            currentbatch += 300



def scratch():
    results = sp.current_user_playlists()
    for i in results['items']:
        print(i['name'])



    # results = sp.current_user_playlists()
    # for item in results['items']:
    #     playlist = sp.playlist(playlist_id=item['id'])
    #     for track in playlist['tracks']['items']:
    #         print(sp.current_user_saved_tracks_contains(tracks=[track['track']['uri']]))

if __name__ == '__main__':
    playlists = [
        'House',
        'Progressive House',
        'DnB',
        'Liquid',
        'Heavy Liquid',
        'Indie Dance',
        'Techno',
        'Trance',
        'Rollers',
        'Uplifting DnB',
        'Progressive Breaks',
        'TechHouse',
        'Garage',
        'Nu Disco & French house',
        'Tropical House',
        'Downtempo Deep House',
        'Brazilian Bass',
        'BassHouse',
        'Deep House',
        'Electronica',
        'Electro Funk',
        'Future Bass',
        'Rap & Hip Hop',
        # 'Misc classics',
        # 'Lo-Fi',
        # '70/80s',
        # '2000s',
    ]
    run(playlists=playlists)
