# Plexify
#### Port your Plex music playlists to Spotify

## Overview
This application will port a single Plex music playlist to your Spotify account.  There
's a fair amount of setup to do, but ultimately this will take you much, much, *much* less
 time than manually entering your Plex playlists into Spotify.

Run from the terminal or command prompt with:
 ```python plexify.py {playlist_name}```
 
 ### Walkthrough
 Assuming that you are starting at ground zero with not much technical knowledge about
  Python, Plex, or Spotify.  You will need to have Python installed on your computer.
  
  #### Download the code
  First thing, clone this github repository or download a zip of it. (More info on that
   [here](https://www.howtogeek.com/451360/how-to-clone-a-github-repository/)).  Also
   , consider using a virtual environment for this. ([Why and How](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/))
   
   #### Install the required modules
   All of the required libraries are listed in the `requirements.txt` file.
   
   *  In the terminal `cd` into the plexify directory.
 *  `pip install -r requirements.txt`
 
 #### Fill in your credentials
 You will need credentials for both your Plex server and your Spotify account.  When
  you get them, enter them in the appropriate place in `credentials.py` (You can edit
   that file with any text editor.)
   
 ##### credentials.py
 `servername =` This is the name of the server your playlists live on.  
 
 `username = `  This is your Plex username
 
 `password = ` This is the password for your Plex account. *Please, please, please* use
  common sense here.  Don't put this file on a public computer.  I could have set
   prompts for all of these credentials but I felt that that would be too burdensome
   .  All the same, be careful with your credentials.  Thank you.
   
   `baseurl = ` Usually this is the local URL of your Plex server.  The default is
    `'http://127.0.0.1:32400'` and most people never change it.  If in doubt, use this.
    
 ##### Spotify Credentials
 You will need to get yourself a developer account at Spotify and register this
  application.  Super easy:
  1.  [Go here](https://developer.spotify.com/dashboard/) and sign up.  They will issue
   you a client_id and a client_secret.  Copy those and paste them in the appropriate
    place in `credentials.py`
    
  2.  [Register Your App](https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app)
  3.  In the settings for your app, pick any valid URL (example.com or google.com or
   anything at all) and add it to the RedirectURL field and enter the exact same value
    in `credentials.py`
    
    
 #### Run the app!
 `python plexify.py {playlist}` in the terminal where {playlist} is the name of your
  playlist **exactly** as it appears in Plex.  If it is more than one word or has
   special characters, wrap it in single quotes `'`.
   
 ####What happens next?
 *  The app will find your playlist in Plex.
 *  If your playlist has more than 100 items, the app will trim it to the first 100
  items because Spotify will only allow 100.
 *  For every track in your Plex playlist, the app will search Spotify for an exact match.
 *  As it loops through, you will be notified of every track that did not match.
 *  Once the loop is done, you will see a message:
    * `Matched x of y` `There were z un-matched`
 * You will then be given a choice to either (1) Not bother with trying to match or (2
 ) Trying to match in a different way.
 *  Choosing (1) will create a playlist on your Spotify account with the exact name as
  on Plex and fill it with the matched tracks of the first 100 on your Plex list.
  *  Choosing (2) will loop through all of the un-matched tracks
     *  You can choose from every album that your track's artist has on Spotify.  If
      you don't see the one you want or you're just fed up with the process, type `skip
      `, otherwise enter the number of your album.
      *  If you chose `skip`, you'll repeat the process with the next un-matched track
      *  If you choose an album number, you will be shown a list of every track on that
       album.  Enter the number of that track to add it to your playlist, or `skip` to
        move on to the next one.
      *  Once you've added or skipped all of the un-matched tracks, the app will create
       the playlist on your Spotify account
       
  ### Notes and Caveats
  *  The error handling in this app is pretty fragile.  Don't try to get too fancy.
  *  The more bootlegs, imports, and weird stuff you have in your playlists, the more
   un-matched tracks you'll get.
   *  If the code looks like it was written by a bumbling amateur...whatever, it works.
   *  `credentials.py` really should have been an .ini file.  I got lazy and it doesn't really make a big difference, just looks sloppy.
   *  Did the app ask you to enter the URL that it just opened in your browser?  Copy and paste the entire link at the prompt.  This should only happen to you once, if ever.
   
   ### Thank you
   I hope you find this application useful.
   
   Please consider a donation to fund more development work:
   
   Venmo: Jayco613
