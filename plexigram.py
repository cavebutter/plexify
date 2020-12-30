from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
import plexconfig as p
from datetime import datetime, date, time, timedelta
import telegram

#############################
#    Plex Authentication    #
#############################

account = MyPlexAccount(p.username, p.password)
plex = account.resource(p.servername).connect()

###################################
#    Plex functions that return   #
#    lists of media.              #
###################################

#  List all shows of specified genre
def list_shows(genre):
    shows = plex.library.section('TV Shows')
    for show in shows.search(genre=genre):
        print(show.title, show.addedAt)

#  List all movies added in the last 14 days
def new_movies():
    today = datetime.now()
    recent = timedelta(days=14)
    movies = plex.library.section('Movies')
    new_movies = [movie.title for movie in movies.search(unwatched = True) if today -
                                                                      movie.addedAt
                  < recent]
    return new_movies

#  Print 'Recently Added' movies to terminal
def new_movie2():
    new_movies = plex.library.section('Movies').recentlyAdded()
    print('Recently Added Movies:\n----------------------')
    for movie in new_movies:
        print(f"\n{movie.title}")
        print(f'Added: {movie.addedAt}\n')
        print('-'* 20)

#  List of Recently Added TV Seasons
def new_tv():
    shows_list = []
    new_tv = plex.library.section('TV Shows').recentlyAdded()
    shows = [show for show in new_tv]
    for show in shows:
        summary_item = show.grandparentTitle + ' - ' + show.parentTitle
        shows_list.append(summary_item)
    new_seasons = set(shows_list)
    return new_seasons

#  List of Recently Added Masterclasses
def new_masterclass():
    shows_list = []
    new_tv = plex.library.section('Masterclass').recentlyAdded()
    shows = [show for show in new_tv]
    for show in shows:
        summary_item = show.grandparentTitle + ' - ' + show.parentTitle
        shows_list.append(summary_item)
    new_seasons = set(shows_list)
    return new_seasons

#  This one is not working as intended.  Returns a list of Artist objects and I can't
#  get album info from that.
def new_music():
    #music_list = []
    new_music = plex.library.section('Music').recentlyAdded()
    music_list = [music for music in new_music]
    return music_list
