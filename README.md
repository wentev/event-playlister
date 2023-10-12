# event-playlister
**friend:** you wanna go to this event with me this weekend?  
**me, not knowing anyone on the setlist:** sure!  
**also me:** [furiously tries catching up on music]  

***

### event-playlister is a simple artist to playlist generator using the Spotify API. 
How To Use: 
1. Download all files in repository.
2. Download Python's "dotenv" and "requests" packages.
3. Ensure that **your own personal CLIENT_ID and CLIENT_SECRET** are used. Instructions on how to retrieve a CLIENT_ID and CLIENT_SECRET can be found on Spotify's Developer pages.
4. Create a list of artists in the *artist.txt* file, **using one line per artist**. Note that if the artist contains an ampersand (&), it is recommend to write "and" - otherwise the ampersand in the .txt file gets converted in the read file procress.
5. Run the program. It should return two (2) lists: 1) track_id_list: a list of tracks from each artist, converted into Spotify's specific ID assignment. 2) track_name_list: The name of each track.
