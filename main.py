import json,os,re

def app_menu():
    
    menu = """Welcome to Mooziq!
    Choose one of the options bellow:


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
        menu_choice = int(input("Type your option: "))
    
        match menu_choice:
            case 1:
                print_all_artists() 
                app_menu()
            case 2:
                all_albums_artist() 
                app_menu()
            case 3:
                get_top_tracks() 
                app_menu()
            case 4:
                export_artist_data() 
                app_menu()
            case 5:
                get_albums_by_year() 
                app_menu()
            case 6:
                creativity_score() 
                app_menu()
            case 7:
                get_longest_uniq_seq() 
                app_menu()
            case 8:
                forecast_upcoming_concerts() 
                app_menu()
            case 9:
                search_by_lyrics() 
                app_menu()
            case 10:
                print("Thank you for using Mooziq! Have a nice day :)")
            case _:
                print("Error - Invalid option. Please input a number between 1 and 10.")
                app_menu()
    except ValueError:
        print("Invalid input: ValueError")




# tast 1



artists_name_idname = {} # dict with name.lower as key and value (id,name)
artist_genre = {}

def get_artists_name_id():
   
    list_json = sorted(os.listdir("dataset/artists/"))
    
    for file in list_json:
        file_name = "dataset/artists/" + file
        with open(file_name, 'r',encoding = "utf-8") as f:
            artist_info = json.load(f)
            artists_name_idname[artist_info["name"].lower()] = (artist_info["id"],artist_info["name"])


            artist_genre[artist_info["id"]] = artist_info["genres"]

def print_all_artists():
    get_artists_name_id()
    print_all_artists()
    
    print("Artists found in the database:")
    for value in artists_name_idname.values():
        print(f"- {value[1]}")


# task 2 - gotta do the date thing
def all_albums_artist():
    get_artists_name_id()

    l_artists_name_id = {key.lower(): value for key, value in artists_name_id.items()}
    user_input = input("Please input the name of an artist: ")
    
    #check if artist exists
    if user_input.lower() in l_artists_name_id:
        chosen_id = ({l_artists_name_id[user_input.lower()]})
        print(chosen_id)
    else:
        print("Artist not found in the database.")

    
    albums_json = sorted(os.listdir("dataset/albums"))
    chosen_id_str = next(iter(chosen_id))
    if chosen_id_str + ".json" in albums_json:
        
        file_name_2 = "dataset/albums/" + chosen_id_str + ".json"
        
    else:
        print("Couldn't find any albums.")

    print(f"Listing all available albums from {user_input}:")
    with open(file_name_2, encoding="utf8") as f:
         album_info = json.load(f)
         for item in album_info["items"]:
            name = item.get('name', 'Name Not Found')
            release_date = item.get('release_date', 'Date Not Found')
            
            print(f"“{name}” was released in {release_date}")

# task 2 - gotta do the date thing
def all_albums_artist():
    get_artists_name_id()

    l_artists_name_id = {key.lower(): value for key, value in artists_name_id.items()}
    user_input = input("Please input the name of an artist: ")
    
    #check if artist exists
    if user_input.lower() in l_artists_name_id:
        chosen_id = ({l_artists_name_id[user_input.lower()]})
        print(chosen_id)
    else:
        print("Artist not found in the database.")

    
    albums_json = sorted(os.listdir("dataset/albums"))
    chosen_id_str = next(iter(chosen_id))
    if chosen_id_str + ".json" in albums_json:
        
        file_name_2 = "dataset/albums/" + chosen_id_str + ".json"
        
    else:
        print("Couldn't find any albums.")

    print(f"Listing all available albums from {user_input}:")
    with open(file_name_2, encoding="utf8") as f:
         album_info = json.load(f)
         for item in album_info["items"]:
            name = item.get('name', 'Name Not Found')
            release_date = item.get('release_date', 'Date Not Found')
            
            print(f"“{name}” was released in {release_date}")

# task 3
def get_top_tracks():
    print_all_artists()

    chosen_art = input("Please input the name of an artist: ")
    artist_id = ""
    list_all_art = []

    for key,value in artists_name_idname.items():
        if key == chosen_art.lower():
            artist_id = value[0]
    
    for value in artists_name_idname.values():
        list_all_art.append(value[1])

    list_json = sorted(os.listdir("dataset/top_tracks/"))
    top_tracks_path = "dataset/top_tracks/"

    for file_name in list_json:
        if file_name[:-5] == artist_id:
            top_tracks_path += file_name
    
    dict_tracks = {}

    with open(top_tracks_path) as f:
        dict_top_tracks = json.load(f)
        list_tracks = dict_top_tracks["tracks"]
        for track in list_tracks:
            dict_tracks[track["name"]] = track["popularity"]
    
    print(f"Listing top tracks for {artists_name_idname[chosen_art.lower()][1]}…")
    for key,value in dict_tracks.items():
        if value <= 30:
            print(f"- \"{key}\" has a popularity score of {value}. No one knows this song.")
        elif value <= 50:
            print(f"- \"{key}\" has a popularity score of {value}. Popular song.")
        elif value <= 70:
            print(f"- \"{key}\" has a popularity score of {value}. It is quite popular now!")
        elif value > 70:
            print(f"- \"{key}\" has a popularity score of {value}. It is made for the charts!")

 
#task 4
def export_artist_data():
    get_artists_name_id()
    print_all_artists()
    
    header = "artist_id,artist_name,number_of_albums,top_track_1,top_track_2,genres\n"
    csv_path = "artists-data.csv"

    l_artists_name_id = {key.lower(): value for key, value in artists_name_id.items()}
    artist_name = input("Please input the name of an artist: ")

    if artist_name.lower() in l_artists_name_id:
        artist_id = l_artists_name_id[artist_name.lower()]
    else:
        print("Artist not found in the database.")
        return

    #count albums
    albums_json = sorted(os.listdir("dataset/albums"))
    num_albums = 0
    album_file = artist_id + ".json"
    if album_file in albums_json:
        with open(f"dataset/albums/{album_file}", encoding="utf8") as f:
            album_info = json.load(f)
            num_albums = len(album_info.get("items", []))

    #get top tracks
    top_tracks_file = f"dataset/top_tracks/{artist_id}.json"
    top_track_1 = ""
    top_track_2 = ""
    if os.path.exists(top_tracks_file):
        with open(top_tracks_file, encoding="utf8") as f:
            tracks_info = json.load(f)
            tracks = sorted(tracks_info.get("tracks", []), key=lambda x: x.get("popularity", 0), reverse=True)
            if len(tracks) > 0:
                top_track_1 = tracks[0].get("name", "")
            if len(tracks) > 1:
                top_track_2 = tracks[1].get("name", "")

    genres_list = artist_genre.get(artist_id, [])
    if genres_list:
        genres_str = '"' + ", ".join(genres_list) + '"'
    else:
        genres_str = ""

    #le CSV
    row = f"{artist_id},{artist_name},{num_albums},{top_track_1},{top_track_2},{genres_str}\n"

    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0: #append
        with open(csv_path, "w", encoding="utf8") as csvfile:
            csvfile.write(header)
            csvfile.write(row)
    else: #create
        with open(csv_path, "a", encoding="utf8") as csvfile:
            csvfile.write(row) 


# task 5

def get_albums_by_year():
    get_artists_name_id()

    chosen_year = int(input("Please enter a year: "))

    list_json = sorted(os.listdir("dataset/albums/"))
    list_albums = []
    list_album_artist = []

    for file in list_json:
        file_album = "dataset/albums/" + file
        with open(file_album, 'r',encoding="utf-8") as f:
            albums = json.load(f)
            list_albums = albums["items"]
            for album in list_albums:
                if int(album["release_date"][:4]) == chosen_year:
                    for key,value in artists_name_idname.items():
                        if value[0] == file[:-5]:
                           album_artist = (album["name"],value[1])
                           list_album_artist.append(album_artist) 
    list_album_artist.sort()
    if len(list_album_artist) == 0:
        print(f"No albums released in the year {chosen_year}")
    else:
        print(f"Albums released in the year: {chosen_year}")
        for album_artist in list_album_artist:
            print(f"- \"{album_artist[0]}\" by {album_artist[1]}")
    

# task 7

def get_longest_uniq_seq():
    
    list_json = sorted(os.listdir("dataset/songs/"))
    list_dict_title_artist_lyrics = []

    for file in list_json:
        file_name = "dataset/songs/" + file
        with open(file_name, 'r',encoding = "utf-8") as f:
            song_info = json.load(f)
            list_dict_title_artist_lyrics.append(song_info)
    

    print("Available songs: ")
    
    x = 0
    for song in list_dict_title_artist_lyrics:
        x += 1
        print(f"{x}. {song["title"]} by {song["artist"]}")

    try:
        choice = int(input("Please select one of the following songs (number): ")) - 1
    

        lyrics = re.sub("[\n\r]"," ",list_dict_title_artist_lyrics[choice]["lyrics"].lower())
        lyrics = re.sub(" +"," ",lyrics)
        lyrics_word_list = re.sub(r"[!?.,'()]","",lyrics).split(" ")

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
        
        max_length = 0

        for length in all_length:
            if max_length < length:
                max_length = length

        print(f"The length of the longest unique sequence in {list_dict_title_artist_lyrics[choice]["title"]} is {max_length}")
    except (IndexError , ValueError):
        print("Error")



app_menu()
        
            
        
    
    


