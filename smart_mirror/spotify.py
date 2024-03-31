import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser

# Set up Spotify credentials
SPOTIFY_CLIENT_ID = 'a5828eeb0885407b9b98d4d2319ac661'
SPOTIFY_CLIENT_SECRET = 'cfc6e731ebb148da9c44b3df6ea0fcc9'

# Authenticate with Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                      client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Define mood and language mappings
mood_map = {
    'angry': {'telugu': 'Mass Beats', 'hindi': 'Aggressive Bhangra', 'tamil': 'Powerful Kuthu', 'malayalam': 'Intense Folk', 'english': 'Intense Rock'},
    'disgust': {'telugu': 'Peaceful Carnatic', 'hindi': 'Serene Ghazals', 'tamil': 'Melancholic Film Songs', 'malayalam': 'Soulful Sufi', 'english': 'Calming Classical'},
    'fear': {'telugu': 'Uplifting Devotional', 'hindi': 'Motivational Qawwali', 'tamil': 'Inspirational Bhajan', 'malayalam': 'Courageous Classical', 'english': 'Empowering Pop'},
    'happy': {'telugu': 'Joyful Folk', 'hindi': 'Festive Bollywood', 'tamil': 'Celebratory Gaana', 'malayalam': 'Cheerful Mappila', 'english': 'Energetic Dance'},
    'sad': {'telugu': 'Melancholic Melodies', 'hindi': 'Heartfelt Sufi', 'tamil': 'Emotional Classical', 'malayalam': 'Reflective Film Songs', 'english': 'Melancholic Ballads'},
    'surprise': {'telugu': 'Dynamic Fusion', 'hindi': 'Eclectic Filmi', 'tamil': 'Unexpected Carnatic', 'malayalam': 'Vibrant Fusion', 'english': 'Dynamic Jazz'},
    'neutral': {'telugu': 'Tranquil Instrumental', 'hindi': 'Soothing Raag', 'tamil': 'Relaxing Raga', 'malayalam': 'Peaceful Instrumental', 'english': 'Ambient Chill'}
}

# Prompt user for mood and language
selected_language = input(f"Enter language ({', '.join(mood_map['angry'].keys())}): ").lower()
while selected_language not in mood_map['angry']:
    print("Invalid language. Please try again.")
    selected_language = input(f"Enter language ({', '.join(mood_map['angry'].keys())}): ").lower()

selected_mood = input(f"Enter mood ({', '.join(mood_map.keys())}): ").lower()
while selected_mood not in mood_map:
    print("Invalid mood. Please try again.")
    selected_mood = input(f"Enter mood ({', '.join(mood_map.keys())}): ").lower()

# Search for tracks based on mood and language
query = f"mood:{mood_map[selected_mood][selected_language]} language:{selected_language}"
results = sp.search(q=query, type='track', limit=10)

# Display search results
print("Search Results:")
for idx, track in enumerate(results['tracks']['items']):
    print(f"{idx + 1}: {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")

# Let the user choose a track to play
selected_idx = int(input("Enter the number of the track you want to play: ")) - 1
selected_track_id = results['tracks']['items'][selected_idx]['id']

# Open the selected track in the Spotify app
webbrowser.open(f"spotify:track:{selected_track_id}")
