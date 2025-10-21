import json,os,re,csv
import helper_functions as hf


albums_name_release = {}
artist_genre = {}
search_by_lyrics_dict = {}
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


artists_low_idnamegenre = hf.get_artists_info() # dict with artist.lower as key and value as dict with keys: id, name, genre

def list_all_artists():

    for value in artists_low_idnamegenre.values():
        print(f"- {value["name"]}")

# task 1

def print_all_artists():
    
    print("Artists found in the database:")

    for value in artists_low_idnamegenre.values():
        print(f"- {value["name"]}")


# task 2
def all_albums_artist():
    if not artists_low_idnamegenre:
        hf.get_artists_info()
    print_all_artists()

    l_artists_name_id = artists_low_idnamegenre
    user_input = input("Please input the name of an artist: ")
    

    if user_input.lower() in l_artists_name_id:
        chosen_id = {l_artists_name_id[user_input.lower()][0]}

    else:
        print("Artist not found in the database.")
        return

    
    albums_json = sorted(os.listdir("dataset/albums"))
    chosen_id_str = str(next(iter(chosen_id)))

    if (chosen_id_str+".json") in albums_json:
        
        file_name_2 = "dataset/albums/" + chosen_id_str + ".json"

    else:
        print("Couldn't find any albums.")
        return
    
    x = l_artists_name_id[user_input.lower()][1]
    print(f"Listing all available albums from {x}...")
    with open(file_name_2, encoding="utf8") as f:
         album_info = json.load(f)
         for item in album_info["items"]:
            name = item.get('name', 'Name Not Found')
            release_date = item.get('release_date', 'Date Not Found')
            release_date_precision = item.get('release_date_precision', 'Precision Not Found')

            if release_date_precision == "day":
                year, month, day = release_date.split('-')
                month_name = months[int(month) - 1]
                day_int = int(day)

                if 11 <= day_int <= 13:
                    suffix = "th"
                else:
                    suffix = {1: "st", 2: "nd", 3: "rd"}.get(day_int % 10, "th")
                release_date = f"{month_name} {day_int}{suffix} {year}"
            
            elif release_date_precision == "month":
                year, month = release_date.split('-')
                month_name = months[int(month) - 1]
                release_date = f"{month_name} {year}"


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
 
#task 4
def export_artist_data():

    if not artists_low_idnamegenre:
        hf.get_artists_name_id()
    
    for value in artists_low_idnamegenre.values():
        print(f"- {value[1]}")

    header = ["artist_id","artist_name","number_of_albums","top_track_1","top_track_2","genres"]
    csv_path = "artist-data.csv"

    os.makedirs("dataset", exist_ok=True)
    csv_path = os.path.join("dataset", "artist-data.csv")

    l_artists_name_id = artists_low_idnamegenre
    artist_name = input("Please input the name of one of the following artists: ")

    if artist_name.lower() in l_artists_name_id:
        artist_info = l_artists_name_id[artist_name.lower()]  
    else:
        print("Artist not found in the database.")
        return

    artist_id_str = str(artist_info[0])

    albums_json = sorted(os.listdir("dataset/albums"))
    num_albums = 0
    album_file = artist_id_str + ".json"
    if album_file in albums_json:
        with open(f"dataset/albums/{album_file}", encoding="utf8") as f:
            album_info = json.load(f)
            num_albums = len(album_info.get("items", []))


    top_tracks_file = f"dataset/top_tracks/{artist_id_str}.json"
    top_track_1 = ""
    top_track_2 = ""
    if os.path.exists(top_tracks_file):
        with open(top_tracks_file, encoding="utf8") as f:
            tracks_info = json.load(f)
            tracks = tracks_info.get("tracks", [])
            if len(tracks) > 0:
                top_track_1 = tracks[0].get("name", "")
            if len(tracks) > 1:
                top_track_2 = tracks[1].get("name", "")


    genres_list = artist_genre.get(artist_id_str, [])
    genres_str = ", ".join(genres_list) if genres_list else ""

    x = l_artists_name_id[artist_name.lower()][1]

    row_dict = {
        "artist_id": artist_id_str,
        "artist_name": x,
        "number_of_albums": str(num_albums),
        "top_track_1": top_track_1,
        "top_track_2": top_track_2,
        "genres": genres_str
    }

    rows = []
    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
        with open(csv_path, newline='', encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for r in reader:
                rows.append(r)

    updated = False
    for r in rows:
        if r.get("artist_id") == artist_id_str:
            r.update(row_dict)
            updated = True
            break
    if not updated:
        rows.append(row_dict)

    with open(csv_path, "w", newline='', encoding="utf8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

    if updated:
        print(f'Exporting"{artist_name}"data to CSV file...data successfully updated.')
    else:
        print(f'Exporting"{artist_name}"data to CSV file...data successfully appended.')


# task 5

def get_albums_by_year():
    hf.get_artists_info()

    chosen_year = int(input("Please enter a year:\n "))

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
        

#task 6 

def moosefy_song():

    list_json = sorted(os.listdir("dataset/songs"))
    
    title = []
    artist = []
    lyrics = []
#------------------task 7
    print("Songs found in the database:")
    for file in list_json:
        file_name = "dataset/songs/" + file
        with open(file_name, encoding="utf8") as f:
            song_info = json.load(f)
            title.append(song_info.get("title", "Unknown Title"))
            artist.append(song_info.get("artist", "Unknown Artist"))
            lyrics.append(song_info.get("lyrics", "No Lyrics Found"))
    
    for i in range(len(title)):
        print(f"{i+1}. {title[i]} by {artist[i]}")
#-----------------------------------
    
    song_choice = int(input("Choose a song by typing its number: "))
    if song_choice < 1 or song_choice > len(title):
        print("Error: Invalid song number.")
        return

    lyrics_chosen = lyrics[song_choice - 1]

    lyrics_chosen2 = re.sub(r'mo', 'moo', lyrics_chosen, flags=re.IGNORECASE)
    lyrics_chosen2 = re.sub(r'\b\w+(!|\?)', r'moo\1', lyrics_chosen2)

    if lyrics_chosen == lyrics_chosen2:
        print(f"{title[song_choice - 1]} by  {artist[song_choice - 1]} is not moose-compatible!")
    
    else:

        #create directory if doesnt exist
        moosified_dir = "moosified"
        os.makedirs(moosified_dir, exist_ok=True)

        #checkfilename for ?!*etc
        safe_title = re.sub(r'[\\/*?:"<>|]', "", title[song_choice - 1])
        filename = f"{safe_title} Moosified.txt"
        filepath = os.path.join(moosified_dir, filename)

        with open(filepath, "w", encoding="utf8") as f:
            f.write(lyrics_chosen2)

        titletoprint = title[song_choice - 1].lower()
        artisttoprint = artist[song_choice - 1].lower()

        print(f"{titletoprint} by {artisttoprint} has been moos-ified!\nFile saved at ./{filepath}\n{ascii_art}")

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

def create_lyrics_dict():

    list_json = sorted(os.listdir("dataset/songs/"))
    
    for file in list_json:
        file_name = "dataset/songs/" + file
        with open(file_name, encoding="utf8") as f:
            song_info = json.load(f)
            title = song_info.get("title", "Unknown Title")
            artist = song_info.get("artist", "Unknown Artist")
            lyrics = song_info.get("lyrics", "")
            
            lyrics= lyrics.lower()
            lyrics = re.sub(r'[.,!?"]', '', lyrics)
            lyrics = re.sub(r'[\']', '', lyrics)
            lyrics = re.sub(r'\s+', ' ', lyrics).strip()

            for word in lyrics.split():
                if word not in search_by_lyrics_dict:
                    search_by_lyrics_dict[word] = []
                search_by_lyrics_dict[word].append((title, artist))

def search_by_lyrics():
    if not search_by_lyrics_dict:
        create_lyrics_dict()

    user_input = input("Please input a word or phrase to search for: ").lower()
    user_input = re.sub(r'[.,!?"]', '', user_input)
    user_input = re.sub(r'\s+', ' ', user_input).strip()

    words = user_input.split()
    if not words:
        print("No valid input provided.")
        return

    score_map = {} 
    for word in words:
        if word in search_by_lyrics_dict:
            for song in set(search_by_lyrics_dict[word]):
                score_map[song] = score_map.get(song, 0) + 1

    if not score_map:
        print(f"No songs found containing the phrase '{user_input}'.")
        sorted_songs = sorted(score_map.items(), key=lambda kv: (-kv[1], kv[0][0].lower()))
        for (title, artist), score in sorted_songs:
            print(f"- {title} with a score of {score}")
    sorted_songs = sorted(score_map.items(), key=lambda kv: (-kv[1], kv[0][0].lower()))
    for (title, artist), score in sorted_songs:
        print(f"- {title} with a score of {score}")

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
                
            
            menu_choice = int(input("Type your option: "))

            match menu_choice:
                case 1:
                    print_all_artists() 
                case 2:
                    all_albums_artist() 
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
                    forecast_upcoming_concerts() 
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
        
