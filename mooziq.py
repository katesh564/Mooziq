# tast 1
import json,os

artists_name_id = {}

def get_all_artists():
    
    list_json = sorted(os.listdir("dataset/artists"))
    
    for file in list_json:
        file_name = "dataset/artists/" + file
        with open(file_name) as f:
            artist_info = json.load(f)
            artists_name_id[artist_info["name"]] = artist_info["id"]
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
        for track in list_tracks:
            dict_tracks[track["name"]] = track["popularity"]
   
    for key,value in dict_tracks.items():
        if key <= 30:
            print(f"{key} has a popularity score of {value}. No one knows this song.")
        elif key <= 50:
            print(f"{key} has a popularity score of {value}. Popular song.")
        elif key <= 70:
            print(f"{key} has a popularity score of {value}. It is quite popular now!")
        elif key >70:
            print(f"{key} has a popularity score of {value}. It is made for the charts!")

get_top_tracks()