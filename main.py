# tast 1
import json,os

artists_name_id = {}

def get_artists_name_id():
   
    list_json = sorted(os.listdir("dataset/artists/"))
    
    for file in list_json:
        file_name = "dataset/artists/" + file
        with open(file_name, 'r') as f:
            artist_info = json.load(f)
            artists_name_id[artist_info["name"]] = artist_info["id"]

def get_all_artists():
    get_artists_name_id()
    
    print("Artists found in the database:")
    for key in artists_name_id.keys():
        print(f"- {key}")


# task 3
def get_top_tracks():
    get_all_artists()

    chosen_art = input("Please input the name of an artist: ")
    artist_id = ""
    for key in artists_name_id.keys():
        if key == chosen_art:
            artist_id = artists_name_id[key]
    
    list_json = sorted(os.listdir("dataset/top_tracks/"))
    artist_top_tracks = "dataset/top_tracks/"

    for file in list_json:
        if file[:-5] == artist_id:
            artist_top_tracks += file
    
    dict_tracks = {}

    with open(artist_top_tracks) as f:
        dict_top_tracks = json.load(f)
        list_tracks = dict_top_tracks["tracks"]
        for track in list_tracks[:2]:
            dict_tracks[track["name"]] = track["popularity"]
   
    for key,value in dict_tracks.items():
        if value <= 30:
            print(f"{key} has a popularity score of {value}. No one knows this song.")
        elif value <= 50:
            print(f"{key} has a popularity score of {value}. Popular song.")
        elif value <= 70:
            print(f"{key} has a popularity score of {value}. It is quite popular now!")
        elif value > 70:
            print(f"{key} has a popularity score of {value}. It is made for the charts!")



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
                    for key,value in artists_name_id.items():
                        if value == file[:-5]:
                           artist_album = (album["name"],key)
                           list_album_artist.append(artist_album) 
    print(f"Albums released in the year: {chosen_year}")
    for album_artist in list_album_artist:
        print(f"- \"{album_artist[0]}\" by {album_artist[1]}")
    
