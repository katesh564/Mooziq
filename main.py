import json,os,re,csv
import helper_functions as hf

artists_name_idname = {}
artist_genre = {}
search_by_lyrics_dict = {}
inverted_index = {}
albums_name_release = {}

months = ["January","February","March","April","May","June"]
months += ["July","August","September","October","November","December"]
 

ascii_art = r''' ___            ___
/   \          /   \
\_   \        /  __/
 _\   \      /  /__
 \___  \____/   __/
     \_       _/
       | @ @  \__
       |32
     _/     /\
    /o)  (o/\ \__
    \_____/ /
      \____/
'''
# task 1

artists_low_idnamegenre = hf.get_artists_info() # dict with artist.lower as key and value as dict with keys: id, name, genre

def list_all_artists():

    for value in artists_low_idnamegenre.values():
        print(f"- {value["name"]}")
# task 2
def get_all_albums_by_artist():

    artist_name_input = input("Please input the name of one of the following artists: ")

    if artist_name_input.lower() in artists_name_idname:
        chosen_id = artists_name_idname[artist_name_input.lower()][0]
    else:
        print("Artist not found in the database.")
        return

    chosen_id_str = str(chosen_id)
    album_path = os.path.join("dataset", "albums", f"{chosen_id_str}.json")
    if not os.path.exists(album_path):
        print("Couldn't find any albums.")
        return

    print(f'Listing all available albums from {artists_name_idname[artist_name_input.lower()][1]}...')
    album_info = hf.safe_load_json(album_path)
    if not album_info:
        print("Couldn't read album info.")
        return

    for item in album_info.get("items", []):
        name = item.get('name', 'Name Not Found')
        release_date = item.get('release_date', '')
        precision = item.get('release_date_precision', '')
        if precision in ("day", "month"):
            release_date = hf.format_release_date(release_date, precision)
        else:
            release_date = release_date or "Date Not Found"
        print(f'- "{name}" was released in {release_date}.')

# task 3
   
def get_top_tracks():
    list_all_artists()

    chosen_art = input("Please input the name of an artist: ").lower()
    artist_found = hf.find_artist(chosen_art,artists_low_idnamegenre)

    if artist_found:

        artist = artists_low_idnamegenre[chosen_art]["name"]
        artist_id = artists_low_idnamegenre[chosen_art]["id"]
    
        print(f"Listing top tracks for {artist}...")
    
        top_track_files = hf.read_jsons("dataset/top_tracks")
        all_tracks = top_track_files[f"{artist_id}.json"]["tracks"]
       
        track_popul = []
        for track in all_tracks:
            track_popul.append((track["name"],track["popularity"]))
        
        hf.print_tracks_popularity(track_popul)
    else:
        print("Artist Not Found")

    
# task 4
def export_artist_data():
    if not artists_low_idnamegenre:
        hf.get_artists_name_id()
    
    for value in artists_low_idnamegenre.values():
        print(f"- {value[1]}")

    header = ["artist_id","artist_name","number_of_albums","top_track_1","top_track_2","genres"]
    os.makedirs("dataset", exist_ok=True)
    csv_path = os.path.join("dataset", "artist-data.csv")

    artist_name = input("Please input the name of one of the following artists: ").strip()
    if artist_name.lower() not in artists_name_idname:
        print("Artist not found in the database.")
        return
    artist_info = artists_name_idname[artist_name.lower()]
    artist_id_str = str(artist_info[0])

    # count albums
    album_file = os.path.join("dataset","albums", f"{artist_id_str}.json")
    num_albums = 0
    album_info = hf.safe_load_json(album_file)
    if album_info:
        num_albums = len(album_info.get("items", []))

    top1 = top2 = ""
    top_path = os.path.join("dataset", "top_tracks", f"{artist_id_str}.json")
    top_data = hf.safe_load_json(top_path)
    if top_data:
        tracks = top_data.get("tracks", [])
        if len(tracks) > 0:
            top1 = tracks[0].get("name", "")
        if len(tracks) > 1:
            top2 = tracks[1].get("name", "")

    # genres
    genres_list = artist_genre.get(artist_id_str, [])
    genres_str = ", ".join(genres_list) if genres_list else ""

    row_dict = {
        "artist_id": artist_id_str,
        "artist_name": artist_info[1],
        "number_of_albums": str(num_albums),
        "top_track_1": top1,
        "top_track_2": top2,
        "genres": genres_str
    }

    updated = hf.update_or_append_csv(csv_path, header, row_dict, "artist_id")
    if updated:
        print(f'Exporting "{artist_name}" data to CSV file...Data successfully updated.')
    else:
        print(f'Exporting "{artist_name}" data to CSV file...Data successfully appended.')

# task 5
def get_albums_by_year():
    hf.get_artists_info()

    artist_found = hf.find_artist()

    if artist_found:
        

        try:
            chosen_year = int(input("Please enter a year: "))
        except ValueError:
            print("Invalid year.")
            return

    all_albums = []
    album_artist = []

    folder_path = "dataset/albums"

    for file_name, data in hf.read_jsons(folder_path):
        all_albums = data["items"]
        artist_name = hf.find_artist_by_id(file_name[:-5],artists_low_idnamegenre)

        for album in all_albums:          
            if int(album["release_date"][:4]) == chosen_year:
                album_artist.append((album["name"],artist_name))
    
    hf.print_all_albums(album_artist,chosen_year)
        

# task 6
def moosefy_song():
    songs = hf.get_song_entries()
    if not songs:
        print("No songs available.")
        return

    print("Available songs:")
    for i, (t, a, _) in enumerate(songs, start=1):
        print(f"{i}. {t} by {a}")

    try:
        song_choice = int(input("Please select one of the following songs (number): ").strip())
    except ValueError:
        print("Error: Invalid song number.")
        return
    if song_choice < 1 or song_choice > len(songs):
        print("Error: Invalid song number.")
        return

    title, artist, lyrics = songs[song_choice - 1]
    lyrics2 = re.sub(r'mo', 'moo', lyrics, flags=re.IGNORECASE)
    lyrics2 = re.sub(r'\b\w+(!|\?)', r'moo\1', lyrics2)

    if lyrics == lyrics2:
        print(f"{title} by {artist} is not moose-compatible!")
        return

    moosified_dir = "moosified"
    os.makedirs(moosified_dir, exist_ok=True)
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    filename = f"{safe_title} Moosified.txt"
    filepath = os.path.join(moosified_dir, filename)
    with open(filepath, "w", encoding="utf8") as f:
        f.write(lyrics2)

    print(f"{title} by {artist} has been moos-ified!\nFile saved at ./{filepath}\n{ascii_art}")

# task 7
def get_longest_uniq_seq():
    
    print("Available songs: ")
#----------------------task 6
    list_dict_title_artist_lyrics = hf.get_available_songs()

    song_number = 0
    for song in list_dict_title_artist_lyrics:
        song_number += 1
        print(f"{song_number}. {song["title"]} by {song["artist"]}")
#--------------------------------------------
    try:
        choice = int(input("Please select one of the following songs (number): ")) - 1

        if choice in range(len(list_dict_title_artist_lyrics) + 1):
            lyrics_word_list = hf.remove_punctuation(choice ,list_dict_title_artist_lyrics)

            all_lengths = hf.get_all_lenghts(lyrics_word_list)

            max_length = hf.find_max_length(all_lengths)
            song_title = list_dict_title_artist_lyrics[choice]["title"]

            print(f"The length of the longest unique sequence in {song_title} is {max_length}")
        else:
            print("Song Not Found")
    except ValueError:
        print("Error")
# task 8
def get_for_forecast_upcoming_concerts():
    if not artists_name_idname:
        get_artists_name_id()

def forecast_upcoming_concerts():
    hf.get_artists_info()

    concerts_file_path = "dataset/concerts/concerts.csv"
    concerts_info = hf.read_csv(concerts_file_path)
    artists_ctcode_date = hf.get_artists_ctcode_date(concerts_info)

    print("Upcoming artists:")
    for key in artists_ctcode_date.keys():
        print(f"- {key}")

    user_choice = input("Please input the name of one of the following artists: ").lower()
    
    artist_found = hf.find_artist(user_choice)

    if artist_found:

        chosen_art = artists_low_idnamegenre[user_choice]["name"]
        weather_file_path = "dataset/weather/weather.csv"

        weather_info = hf.read_csv(weather_file_path)
        concerts_weather = hf.get_concerts_weather(weather_info, artists_ctcode_date)

        dates = hf.get_date_suffix(concerts_weather)
        weather_recom = hf.get_recommendations(concerts_weather)

        print_recom(weather_recom, concerts_weather, dates)

                
        def print_recom(weather_recom, concerts_weather, dates):

            if len(concerts_weather) > 1:
                print(f"Fetching weather forecast for {chosen_art} concerts...")
                print(f"{chosen_art} has {len(concerts_weather)} upcoming concerts:")
            else:
                print(f"Fetching weather forecast for \"{chosen_art}\" concerts...")
                print(f"{chosen_art} has 1 upcoming concert:")

            index = 0
            for concert in concerts_weather:
                date = dates[index]
                recom = weather_recom[index]
                print(f"- {concert["city"]}, {date}. {recom}")
                index += 1
    else:
        print("Artist Not Found")




#task 9
    concerts_path = "dataset/concerts/concerts.csv"
    if not os.path.exists(concerts_path := concerts_path):
        print("No concerts data.")
        return

    dict_artists_ctcode_date = {}
    with open(concerts_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            day = f"{int(row['day']):02d}"
            month = f"{int(row['month']):02d}"
            year = row["year"]
            date = f"{year}-{month}-{day}"
            dict_artists_ctcode_date.setdefault(row["artist"], []).append((row["city_code"], date))

    print("Upcoming artists:")
    for key in dict_artists_ctcode_date.keys():
        print(f"- {key}")

    user_choice = input("Please input the name of one of the following artists: ").strip().lower()
    if user_choice not in artists_low_idnamegenre:
        print("Artist Not Found")
        return
    chosen_art = artists_low_idnamegenre[user_choice][1]

    weather_path = "dataset/weather/weather.csv"
    if not os.path.exists(weather_path):
        print("No weather data.")
        return

    weather_rows = []
    with open(weather_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        weather_rows = list(reader)

    weather_concerts = []
    for city_code, date in dict_artists_ctcode_date.get(chosen_art, []):
        for w in weather_rows:
            if w.get("city_code") == city_code and w.get("date") == date:
                weather_concerts.append(w)

    if not weather_concerts:
        print(f"No weather info for {chosen_art} concerts.")
        return

    list_city_dates = []
    for concert in weather_concerts:
        date_str = concert["date"]
        # use helper for formatting day precision
        list_city_dates.append((concert["city"], hf.format_release_date(date_str, "day")))

    weather_recom = []
    for concert in weather_concerts:
        recommend = ""
        if int(concert.get("temperature_min", 0)) > 10 and float(concert.get("precipitation", 0)) < 2.3:
            recommend += "Perfect weather!"
        if int(concert.get("temperature_min", 0)) <= 10:
            recommend += "Wear warm clothes. "
        if float(concert.get("precipitation", 0)) >= 2.3:
            if int(concert.get("wind_speed", 0)) < 15:
                recommend += "Bring an umbrella."
            else:
                recommend += "Bring a rain jacket."
        weather_recom.append(recommend)

    if len(weather_concerts) > 1:
        print(f"Fetching weather forecast for {chosen_art} concerts...")
        print(f"{chosen_art} has {len(weather_concerts)} upcoming concerts:")
    else:
        print(f"Fetching weather forecast for \"{chosen_art}\" concerts...")
        print(f"{chosen_art} has {len(weather_concerts)} upcoming concert:")

    for idx, concert in enumerate(weather_concerts):
        date = list_city_dates[idx][1]
        recom = weather_recom[idx]
        print(f"- {concert['city']}, {date}. {recom}")

# task 9
def create_lyrics_dict():
    global inverted_index
    os.makedirs("dataset", exist_ok=True)
    inverted_path = os.path.join("dataset", "inverted_index.json")

    loaded = hf.load_inverted_index(inverted_path)
    if loaded:
        inverted_index = loaded
        return

    temp_index = {}
    for title, artist, lyrics in hf.get_song_entries():
        if not lyrics:
            continue
        txt = hf.sanitize_text(lyrics)
        for word in txt.split():
            temp_index.setdefault(word, set()).add((title, artist))

    # convert to list-of-lists for JSON and save via helper
    to_save = {w: [[t, a] for (t, a) in sorted(lst)] for w, lst in temp_index.items()}
    hf.save_inverted_index(inverted_path, {w: lst for w, lst in to_save.items()})
    # set internal inverted_index as tuples
    inverted_index = {w: [tuple(item) for item in lst] for w, lst in to_save.items()}

def search_by_lyrics():
    if not inverted_index:
        create_lyrics_dict()

    search_phrase = input("Please input a word or phrase to search for: ").lower()
    search_phrase = hf.sanitize_text(search_phrase)
    words = search_phrase.split()
    if not words:
        print("No valid input provided.")
        return

    score_map = {}
    for word in words:
        if word in inverted_index:
            for song in set(inverted_index[word]):
                score_map[song] = score_map.get(song, 0) + 1

    if not score_map:
        print(f"No songs found containing the phrase '{search_phrase}'.")
        return

    sorted_songs = sorted(score_map.items(), key=lambda kv: (-kv[1], kv[0][0].lower()))
    print(f"Songs matching '{search_phrase}':")
    for (title, artist), score in sorted_songs:
        print(f"- {title} with a score of {score}")

# main
def main():
    try:
        menu_choice = 0
        while menu_choice != 10:
            menu = """
            1.Get All Artists
            2.Get All Albums By An Artist
            3.Get Top Tracks By An Artist
            4.Export Artist Data
            5.Get Released Albums By Year
            6.Analyze Song Lyrics
            7.Calculate Longest Unique Word Sequence In A Song
            8.Weather Forecast For Upcoming Concerts
            9.Search Song By Lyrics
            10.Exit"""
            print(menu)
            try:
                menu_choice = int(input("Type your option: ").strip())
            except ValueError:
                print("Invalid input: please enter a number.")
                continue

            match menu_choice:
                case 1:
                    print_all_artists()
                case 2:
                    get_all_albums_by_artist()
                case 3:
                    get_top_tracks()
                case 4:
                    export_artist_data()
                case 5:
                    get_albums_by_year()
                case 6:
                    moosefy_song()
                case 7:
                    get_longest_uniq_seq()
                case 8:
                    get_for_forecast_upcoming_concerts()
                case 9:
                    search_by_lyrics()
                case 10:
                    print("Thank you for using Mooziq! Have a nice day :)")
                case _:
                    print("Error - Invalid option. Please input a number between 1 and 10.")
    except ValueError:
        print("Invalid input: ValueError")

if __name__ == '__main__':
    print("Welcome to Mooziq!")
    print("Choose one of the options bellow:")
    main()
        