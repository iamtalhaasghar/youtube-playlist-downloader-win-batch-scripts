#!/home/programmer/.local/share/virtualenvs/scripts-jY1tn_AR/bin/python
import os, sys
import yt_dlp
import sqlite3

# Set up the SQL database connection
conn = sqlite3.connect('youtube.db')
cursor = conn.cursor()

# Create a table to store the channel and playlist information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS playlists (
        playlist_id TEXT PRIMARY KEY,
        channel_name TEXT,
        video_count INTEGER,
        playlist_name TEXT,
        downloaded TEXT,
        priority INTEGER
    )
''')

# Set up the yt-dlp options
ytdl_options = {
    'dump_single_json': True,
    'extract_flat': 'in_playlist',
    'simulate': True,
    'ignoreerrors': True,
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'merge_output_format': 'mp4',
}

def fetch_metadata(link):
    with yt_dlp.YoutubeDL(ytdl_options) as ydl:
        # Retrieve channel and playlist information
        info = ydl.extract_info(link, download=False)

        if info.get('channel') and info.get('entries'):
            playlist_id = link.split('?list=')[1]
            channel_name = info['channel']
            video_count = len(info['entries'])
            playlist_name = info['title']

            return [playlist_id, channel_name, video_count, playlist_name]

def explore_files():
    # Folder path containing the text files
    folder_path = os.getcwd()
    links = []
    # Iterate over the text files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            print('reading file', file_path)
            # Read YouTube links from the text file
            with open(file_path, 'r', encoding='utf-8') as file:
                links.extend(file.read().splitlines())

    return links

if __name__=="__main__":
    # Iterate over the YouTube links
    for link in sys.argv[1:]:
        try:
            priority = 0
            if '#' in link:
                link, priority = link.split('#')
            print('fetching', link)
            meta = fetch_metadata(link)
            meta.append(priority)
            # Store the channel and playlist information in the database
            cursor.execute('''
                INSERT INTO playlists (playlist_id, channel_name, video_count, playlist_name, priority)
                VALUES (?, ?, ?, ?, ?)
            ''', meta)
            print('inserted', meta)

        except Exception as e:
            print(e)
        finally:
            # Commit the changes to the database
            conn.commit()


