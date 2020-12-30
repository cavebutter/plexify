from plexapi.myplex import MyPlexAccount
import plexconfig as p
from telegram.ext import Updater, CommandHandler
import logging

#######################
#    Set up logging   #
#######################

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO, filename='plexigram.log')

#############################
#    Plex Authentication    #
#############################
try:
    account = MyPlexAccount(p.username, p.password)
    plex = account.resource(p.servername).connect()
    print('Plex connected')
except:
    print('Could not reach plex')

########################
#    Telegram Setup    #
########################

updater = Updater(token=p.t_token)
dispatcher = updater.dispatcher

##############################################################
#    Telegram Commands that will perform queries on Plex     #
#    server and return the results as a message to the       #
#    sender                                                  #
##############################################################

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="""Hi!  
    I'm Franklin the Robot.  I'm the brains behind the secret Plex server.
    Enter a command or type '/help' to see what's available.""")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="""You can give me 
    the following commands:
    /new_tv - This will send you a list of the 5 most recent TV seasons added to the 
    library.
    
    /new_masterclass - This will send you a list of the 5 most recent Masterclass 
    seasons added to the library.
    
    /new_movie - This will send you a list of the most recent movies added to the 
    library and their year of release.  It's kind of a long list, maybe 20 or so.
    
    You can click any of the command links above instead of typing them, too.
    """)


#  List all shows of specified genre
def list_shows(genre):
    shows = plex.library.section('TV Shows')
    for show in shows.search(genre=genre):
        print(show.title, show.addedAt)


#  Print 'Recently Added' movies to terminal
def new_movie(update, context):
    results = plex.library.section('Movies').recentlyAdded()
    movies = [movie.title + ' (' + str(movie.year) + ')' for movie in results]
    message = ''
    for movie in movies:
        message += '\n' + movie + '\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


#  List of Recently Added TV Seasons
def new_tv(update, context):
    shows_list = []
    new_tv = plex.library.section('TV Shows').recentlyAdded()
    shows = [show for show in new_tv]
    for show in shows:
        summary_item = show.grandparentTitle + ' - ' + show.parentTitle
        shows_list.append(summary_item)
    new_seasons = []
    for i in shows_list:
        if i not in new_seasons:
            new_seasons.append(i)
            if len(new_seasons) == 5:
                break
    message = ''
    for season in new_seasons:
        message += '\n' + season + '\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

#  List of Recently Added Masterclasses
def new_masterclass(update, context):
    shows_list = []
    new_tv = plex.library.section('Masterclass').recentlyAdded()
    shows = [show for show in new_tv]
    for show in shows:
        summary_item = show.grandparentTitle + ' - ' + show.parentTitle
        shows_list.append(summary_item)
    new_seasons = []
    for i in shows_list:
        if i not in new_seasons:
            new_seasons.append(i)
            if len(new_seasons) == 5:
                break
    message = ''
    for season in new_seasons:
        message += '\n' + season + '\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

#  This one is not working as intended.  Returns a list of Artist objects and I can't
#  get album info from that.
def new_music():
    #music_list = []
    new_music = plex.library.section('Music').recentlyAdded()
    music_list = [music for music in new_music]
    return music_list

###############################
#  Telegram Command Handlers  #
###############################

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

new_tv_handler = CommandHandler('new_tv', new_tv)
dispatcher.add_handler(new_tv_handler)

new_masterclass_handler = CommandHandler('new_masterclass', new_masterclass)
dispatcher.add_handler(new_masterclass_handler)

new_movie_handler = CommandHandler('new_movie', new_movie)
dispatcher.add_handler(new_movie_handler)

#################
#  Run the bot  #
#################

updater.start_polling()

print('Sign of life')

#updater.stop()

#print('Done')