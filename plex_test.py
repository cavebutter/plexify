from plexapi.myplex import MyPlexAccount
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import sys
import plexconfig as p  # Change this to 'import credentials as p'


# A simple class for Plex Audio Tracks, combining attributes from various plex classes
class PlexTrack:
    def __init__(self, title, album, artist):
        self.title = title
        self.album = album
        self.artist = artist

    def __str__(self):
        return f'Track: {self.title}; Album: {self.album}; Artist: {self.artist}'



class SpotifyAlbum:
    def __init__(self, album_name, artist_name):
        self.artist_name = artist_name
        self.artist_uri = ''
        self.album_name = album_name
        self.album_uri = ''
        self.position = ''

    def __str__(self):
        print(f"Album: {self.album_name} by {self.artist_name}")

class SpotifyTrack:
    def __init__(self, position, uri, title):
        self.position = position
        self.uri = uri
        self.title = title

    def __str__(self):
        print(f"Track: {self.title} - Track Num: {self.position} - URI: {self.uri}")


#  Open connection to plex server
account = MyPlexAccount(p.username, p.password)
plex = account.resource(p.servername).connect()

# Take playlist name from command line
if len(sys.argv) > 1:
    playlist = sys.argv[1]
else:
    #print("Error:  You need to enter a playlist name.")
    #sys.exit()
    playlist = "Run!"

plex_tracks = []
for item in plex.playlist(playlist).items():
    p_track = str(item.title + 'pt')
    p_track = PlexTrack(item.title, item.parentTitle,
                        item.grandparentTitle)
    plex_tracks.append(p_track)

if len(plex_tracks) > 99:
    print(f"The maximum number of tracks that we can add to Spotify at one time is 100.  You are trying to add {str(len(plex_tracks))}.  We will cut off the list at 100.")
    plex_tracks = plex_tracks[0:99]


scope = 'playlist-modify-public'
sp = spotipy.Spotify(auth=p.token, auth_manager=SpotifyOAuth(
    client_id=p.spotify_client_id,
                                                   client_secret=p.spotify_client_secret,
                                                   scope=scope,
                                                   redirect_uri='https://app.plex.tv/'))
user_id = sp.me()['id']


unmatched_tracks = []
spotify_tracks = {}  # track titles and spotify id's
for track in plex_tracks:
    track_id = sp.search(q='artist:' + track.artist + ' track:' + track.title, limit=1,
                         type='track')
    if len(track_id['tracks']['items']) == 0:
        print(f'No match for {track.title}')
        unmatched_tracks.append(track)
    else:
        spotify_tracks[track.title] = track_id['tracks']['items'][0]['id'] # used to be
        # URI

print(f"Matched {str(len(spotify_tracks))} of {str(len(plex_tracks))}:")

if len(unmatched_tracks) == 0:
    pass
else:
    print(f"There are {str(len(plex_tracks) - len(spotify_tracks))} un-matched.")
    proceed = input("What would you like to do?\n1) Create a playlist without those "
                    "tracks \n2) Try to match them a different way:   ")
    if proceed == "2":

        for track in unmatched_tracks:
            artist_albums = []
            j = 1
            print(f"We are going to try to match {track}")
            result = sp.search(track.artist)
            try:
                artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
            except IndexError:
                print(f"We couldn't fine an artist match for {track.artist}.  "
                      f"Skipping...")
                continue
            sp_artist_albums = sp.artist_albums(artist_uri, album_type='album',limit=50)
            for i in range(len(sp_artist_albums['items'])):
                album_name = sp_artist_albums['items'][i]['name']
                Album = album_name + '_'
                Album = SpotifyAlbum(album_name,track.artist)
                Album.album_uri = sp_artist_albums['items'][i]['uri']
                Album.artist_name = track.artist
                Album.artist_uri = artist_uri
                Album.position = j
                j += 1
                artist_albums.append(Album)
            print(f"For {track}, which album looks like the best match?")
            for album in artist_albums:
                print(f"{album.position}.   {album.album_name}")
            album_selection = input("Select the album that looks right or 'skip' to "
                                    "skip this track and try the next one:  ")
            if album_selection == 'skip':
                pass
            else:
                k = 1
                album_tracks = []
                for album in artist_albums:
                    if album_selection == str(album.position):
                        print("Match! " + album.album_name)
                        sp_tracks = sp.album_tracks(Album.album_uri)
                        for n in range(len(sp_tracks['items'])):
                            track_num = sp_tracks['items'][n]['track_number']
                            track_uri = sp_tracks['items'][n]['id']  # used to be URI
                            track_name = sp_tracks['items'][n]['name']
                            Track = str(k)
                            Track = SpotifyTrack(track_num,track_uri,track_name)
                            print(f"{Track.position} - {Track.title} ")
                            album_tracks.append(Track)
                            k += 1
                        track_selection = input("Select the track number for the track "
                                                "you'd like to add to the playlist or "
                                                "'skip' to skip this one:  ")
                        for album_track in album_tracks:
                            if track_selection == str(album_track.position):
                                spotify_tracks[album_track.title] = album_track.uri
                                print(f"Added {album_track.title} to the list!")


    spotify_track_ids = list(spotify_tracks.values())


sp.user_playlist_create(user_id,playlist)
user_playlists = sp.user_playlists(user_id)
for item in user_playlists['items']:
    if item['name'] == playlist:
        playlist_id = item['id']
sp.playlist_add_items(playlist_id=playlist_id,items=spotify_track_ids)