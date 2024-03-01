import requests
from bs4 import BeautifulSoup

# constants:
LIMIT_OF_MAXIMUM_SONGS_TO_DATA_SCRAPE = 100  # set to a high number to fetch all songs

def is_valid_title(title):
    """Check if the title text is valid."""
    unwanted_keywords = ['Songwriter', 'Producer']  # add any more keywords as needed
    return not any(keyword in title for keyword in unwanted_keywords) and len(title) <= 50

user_date_input = input("Which year do you want to Time Travel to? Please type the date in this format: YYYY-MM-DD: ")
print(user_date_input)

response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_date_input}/")
if response.status_code != 200:
    print("Failed to retrieve data")
    exit()

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

# initialize lists to hold song titles and artist names:
songs_and_artists = []

# fetching all elements that could potentially contain song titles or artist names:
song_elements = soup.find_all(["h3", "span"], class_=["c-title", "c-label"])

# initialize placeholders:
current_title = None

for element in song_elements:
    if 'c-title' in element['class']:
        title_text = element.get_text(strip=True)
        if is_valid_title(title_text):
            current_title = title_text  # valid title found, proceed to find the corresponding artist:
    elif 'c-label' in element['class'] and current_title:
        artist_name_text = element.get_text(strip=True)
        if not any(char.isdigit() for char in artist_name_text):
            songs_and_artists.append((current_title, artist_name_text))
            current_title = None  # reset current_title after pairing:

# print the list of songs and artists:
print(f"\nSongs and Artists from {user_date_input}:")
for song, artist in songs_and_artists:
    print(f"Song: {song}, Artist: {artist}")
