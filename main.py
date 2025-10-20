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
       |
     _/     /\
    /o)  (o/\ \__
    \_____/ /
      \____/
'''

def read_jsons(folder_path):
    list_json = sorted(os.listdir(folder_path))
    
    file_name_data = {}

    for file_name in list_json:
        with open(f"{folder_path}/{file_name}", 'r',encoding = "utf-8") as file:
            file_content = json.load(file)
            file_name_data[file_name] = file_content
    return file_name_data

def get_artists_name_id():
    folder_path = "dataset/artists"
    artists_low_idnamegenre = {}
    for artist_info in read_jsons(folder_path).values():
        artists_low_idnamegenre[artist_info["name"].lower()] = (artist_info["id"],artist_info["name"],artist_info["genres"])
    return artists_low_idnamegenre

artists_low_idnamegenre = get_artists_name_id() # dict with name.lower as key and value (id,name,genre)

def list_all_artists():

    for value in artists_low_idnamegenre.values():
        print(f"- {value[1]}")

# task 1

def print_all_artists():
    
    print("Artists found in the database:")

    for value in artists_low_idnamegenre.values():
        print(f"- {value[1]}")


# task 2
def all_albums_artist():
    if not artists_low_idnamegenre:
        get_artists_name_id()
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

                if 11 <= day_int % 100 <= 13:
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
    artist_id = ""
    artist_found = hf.find_artist(chosen_art,artists_low_idnamegenre)

    if artist_found:

        artist = artists_low_idnamegenre[chosen_art][1]
        artist_id = artists_low_idnamegenre[chosen_art][0]
    
        print(f"Listing top tracks for {artist}...")
    
        top_track_files = read_jsons("dataset/top_tracks")
        list_tracks = top_track_files[f"{artist_id}.json"]["tracks"]
       
        list_track_popul = []
        for track in list_tracks:
            list_track_popul.append((track["name"],track["popularity"]))
        
        hf.print_tracks_popularity(list_track_popul)
    else:
        print("Artist Not Found")
 
#task 4
def export_artist_data():

    if not artists_low_idnamegenre:
        get_artists_name_id()
    
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
        print(f'exporting"{artist_name}"datatocsvfile...datasuccessfullyupdated.')
    else:
        print(f'exporting"{artist_name}"datatocsvfile...datasuccessfullyappended.')


# task 5

def get_albums_by_year():
    get_artists_name_id()

    chosen_year = int(input("Please enter a year: "))

   
    list_albums = []
    list_album_artist = [] # def list_album_artist(file_name_data)

    folder_path = "dataset/albums"

    list_json = sorted(os.listdir("dataset/albums/")) # def read_json(folder_path)
    for file_name in list_json:      
        with open(f"dataset/albums/{file_name}", 'r',encoding="utf-8") as file:
            albums_info = json.load(file)
            list_albums = albums_info["items"] # def list_albums(file_name_data)
            for album in list_albums:           # def list_album_artist(list_albums)
                if int(album["release_date"][:4]) == chosen_year:
                    for value in artists_low_idnamegenre.values():
                        if value[0] == file_name[:-5]:
                            list_album_artist.append((album["name"],value[1])) 
    
    list_album_artist.sort()
    
# def print_albums

    if len(list_album_artist) == 0:
        print(f"No albums released in the year {chosen_year}")
    else:
        print(f"Albums released in the year: {chosen_year}")
        for album_artist in list_album_artist:
            print(f"- \"{album_artist[0]}\" by {album_artist[1]}.")
    

#task 6 

def moosefy_song():

    list_json = sorted(os.listdir("dataset/songs"))
    
    title = []
    artist = []
    lyrics = []

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
    
   
    list_dict_title_artist_lyrics = []

    folder_path = "dataset/songs"

    list_json = sorted(os.listdir("dataset/songs/")) # def read_json
    for file_name in list_json:
        with open(f"dataset/songs/{file_name}", 'r',encoding = "utf-8") as file:
            song_info = json.load(file)
            list_dict_title_artist_lyrics.append(song_info) # def list_songs_info(fale_name_data)
    

    print("Available songs: ")
    # def print_available_songs(list_dict_title_artist_lyrics)
    x = 0
    for song in list_dict_title_artist_lyrics:
        x += 1
        print(f"{x}. {song["title"]} by {song["artist"]}")

    try:
        choice = int(input("Please select one of the following songs (number): ")) - 1
    
        # def remove_punctuation(choice ,list_dict_title_artist_lyrics)
        lyrics = re.sub("[\n\r]"," ",list_dict_title_artist_lyrics[choice]["lyrics"].lower())
        lyrics = re.sub(" +"," ",lyrics)
        lyrics_word_list = re.sub(r"[!?.,'()]","",lyrics).split(" ")

        # def get_unique_sequence(lyrics_word_list)
        unique_sequence = []
        all_length = []
       
        for word in lyrics_word_list:
            if word in unique_sequence: 
                word_index = unique_sequence.index(word) + 1
                all_length.append(len(unique_sequence))
                unique_sequence = unique_sequence[word_index:]
                unique_sequence.append(word)
            else:
                unique_sequence.append(word)
        
        # def get_max_length(all_length)
        max_length = 0

        for length in all_length:
            if max_length < length:
                max_length = length

        # return max_length

        song_title = list_dict_title_artist_lyrics[choice]["title"]

        print(f"The length of the longest unique sequence in {song_title} is {max_length}")
    except (IndexError , ValueError):
        print("Error")

# task 8

def forecast_upcoming_concerts():
    get_artists_name_id()

    with open("dataset/concerts/concerts.csv","r",encoding = "utf-8") as f: # def read_csv
        list_dict_concert_info = csv.DictReader(f)
        for dict in list_dict_concert_info:   
    
     # def get_artists_ctcode_date()
            dict_artists_ctcode_date = {}
            day = f"{int(dict["day"]):02d}"
            month = f"{int(dict["month"]):02d}"
            year = dict["year"]


            if dict["artist"] not in dict_artists_ctcode_date.keys():
                date = f"{year}-{month}-{day}"
                dict_artists_ctcode_date[dict["artist"]] = [(dict["city_code"],date)]
            else:
                date = date = f"{year}-{month}-{day}"
                dict_artists_ctcode_date[dict["artist"]].append((dict["city_code"],date))
        # return dict_artists_ctcode_date

    print("Upcoming artists:")

    for key in dict_artists_ctcode_date.keys():
        print(f"- {key}")

    try:
        user_choice = input("Please input the name of one of the following artists: ").lower()
        chosen_art = ""
        
        for key,value in artists_low_idnamegenre.items(): # def find_artist(user_choise, artists_low_idnamegenre)
            if key == user_choice.lower():
                chosen_art = value[1]
            elif user_choice.lower() not in artists_low_idnamegenre.keys():
                print("Artist Not Found")
                return

        with open("dataset/weather/weather.csv","r",encoding = "utf-8") as f: # def read_csv
            list_dict_weather_info = csv.DictReader(f)
            for dict in list_dict_weather_info:

            # def get_weather_info()
           
                weather_concerts = []

            for city_code, date in dict_artists_ctcode_date[chosen_art]:
                if city_code == dict["city_code"] and date == dict["date"]:
                    weather_concerts.append(dict)

        list_city_dates = []

          # def get_date_suffix(weather_concerts,list_city_dates)
        for concert in weather_concerts:  
            date_str = concert["date"]  # e.g. '2025-09-25'
            
            year = int(date_str[:4])    
            month = int(date_str[5:7])     
            day = int(date_str[-2:])         
            if 11 <= day <= 13:
                suffix = "th"
            else:
                suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
            
            month_name = months[int(month) - 1]
            
            list_city_dates.append((concert["city"],f"{month_name} {day}{suffix} {year}"))

        # def get_recommendations
        weather_recom = []

        for concert in weather_concerts:
            recommend = ""
            if int(concert["temperature_min"]) > 10 and float(concert["precipitation"]) < 2.3:
                recommend += "Perfect weather!"

            if int(concert["temperature_min"]) <= 10:
                recommend += "Wear warm clothes. "

            if float(concert["precipitation"]) >= 2.3:
                if int(concert["wind_speed"]) < 15:
                    recommend += "Bring an umbrella."
                else:
                    recommend += "Bring a rain jacket."
           
            weather_recom.append(recommend)
                
        # def print_recom

        if len(weather_concerts) > 1:
            print(f"Fetching weather forecast for {chosen_art} concerts...")
            print(f"{chosen_art} has {len(weather_concerts)} upcoming concerts:")
        else:
            print(f"Fetching weather forecast for \"{chosen_art}\" concerts...")
            print(f"{chosen_art} has {len(weather_concerts)} upcoming concert:")

        index = 0
        for concert in weather_concerts:
            date = list_city_dates[index][1]
            recom = weather_recom[index]
            print(f"- {concert["city"]}, {date}. {recom}")
            index += 1

    except TypeError :
        print("TypeError")




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
        
