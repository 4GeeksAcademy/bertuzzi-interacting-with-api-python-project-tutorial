import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# load the .env file variables
load_dotenv()

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

client_credential_manager = SpotifyClientCredentials(client_id, client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credential_manager)

res = sp.artist_top_tracks('5hKGLu4Ik88FzWcTPhWNTN')
data = [{'Name':track['name'], 'Duration': track['duration_ms'], 'Popularity' : track['popularity']} for track in res['tracks'] if res]

popular_songs = pd.DataFrame.from_dict(data)
popular_songs.sort_values(by='Popularity', ascending=True, inplace=True)
popular_songs = popular_songs.iloc[:3]

song_duration = popular_songs['Duration'].to_list()
song_popularity = popular_songs['Popularity'].to_list()
print(song_duration, song_popularity)

corr_coeff = scipy.stats.pearsonr(song_duration, song_popularity)
print(corr_coeff.statistic)

plt.figure()
sns.scatterplot(data=popular_songs, x='Duration', y='Popularity')
plt.title('Scatter Plot of Duration vs Popularity')
plt.xlabel('Duration (ms)')
plt.ylabel('Popularity')
plt.show()

"""
Correlation result = There is a moderate relationship between duration of a song and its popularity.
A correlation coefficient of roughly 0.58 indicates a light, moderate relationship between the variables only
"""