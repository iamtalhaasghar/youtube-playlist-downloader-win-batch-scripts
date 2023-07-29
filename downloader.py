#!/home/programmer/.local/share/virtualenvs/scripts-jY1tn_AR/bin/python
import os
import yt_dlp
import sqlite3
import time

# Set up the SQL database connection
conn = sqlite3.connect('youtube.db')
cursor = conn.cursor()

# Set up the yt-dlp options
ytdl_options = {
    'ignoreerrors': False,
    'format_sort': ['res:1080', 'ext:mp4:m4a'],
#    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    #bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'merge_output_format': 'mp4',
    'download_archive': '.archive.txt',
}

# Folder path containing the text files
folder_path = os.getcwd()
wait = 0

while True:
    # Iterate over the playlists from the database and download videos
    cursor.execute('SELECT playlist_id,channel_name, playlist_name FROM playlists where downloaded="F" or downloaded IS NULL order by priority desc')
    playlists = cursor.fetchall()
    if not playlists:
        break
    for playlist_id, channel_name, playlist_name in playlists:
        try:
            playlist_name = playlist_name.strip().replace(' ', '_').strip()
            channel_name = channel_name.strip().replace(' ', '_').strip()
            # Create the directory for the channel and playlist
            directory = os.path.join('F:\\youtube\\channels', channel_name, playlist_name)
            os.makedirs(directory, exist_ok=True)

            # Download the videos using yt-dlp
            with yt_dlp.YoutubeDL(ytdl_options) as ydl:
                # todo: ude 03d in playlist index
                ydl.params['outtmpl'] = {'default':os.path.join(directory, '%(playlist_index)s-%(title)s.%(ext)s')}
                ydl.download([f'https://www.youtube.com/playlist?list={playlist_id}'])

            cursor.execute('''
                        UPDATE playlists
                        SET downloaded = ?
                        WHERE playlist_name = ?
                    ''', ('T', playlist_name))
            conn.commit()
            wait = 0 # reset wait
        except Exception as e:
            print(e)
            if not ('Private video' in str(e) or 'Video unavailable' in str(e)):
                wait += 5
            print(f'waiting for {wait}s...')
            time.sleep(wait)

# Close the database connection
conn.close()

