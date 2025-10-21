import os,json,re,csv

def read_jsons(folder_path):
    list_json = sorted(os.listdir(folder_path))
    
    file_name_data = {}

    for file_name in list_json:
        with open(f"{folder_path}/{file_name}", 'r',encoding = "utf-8") as file:
            file_content = json.load(file)
            file_name_data[file_name] = file_content
    return file_name_data

def read_csv(file_path):
    with open(file_path,"r",encoding = "utf-8") as file:
        files_content = csv.DictReader(file)
    return files_content
           

def get_artists_info():
    folder_path = "dataset/artists"
    artists_low_idnamegenre = {}
    for artist_info in read_jsons(folder_path).values():
        artists_low_idnamegenre[artist_info["name"].lower()] = (artist_info["id"],artist_info["name"],artist_info["genres"])
    return artists_low_idnamegenre

# task 3
def find_artist(chosen_art,artists_name_idnamegenre):    
        artist_found = False
        for key in artists_name_idnamegenre.keys():
            if key == chosen_art.lower():
                artist_found = True
                return artist_found
        return False


def print_tracks_popularity(list_track_popul):
    for track_popul in list_track_popul:
        
        track = track_popul[0]
        popularity = track_popul[1]
        
        if popularity <= 30:
            print(f"- \"{track}\" has a popularity score of {popularity}. No one knows this song.")
        elif popularity <= 50:
            print(f"- \"{track}\" has a popularity score of {popularity}. Popular song.")
        elif popularity <= 70:
            print(f"- \"{track}\" has a popularity score of {popularity}. It is quite popular now!")
        elif popularity > 70:
            print(f"- \"{track}\" has a popularity score of {popularity}. It is made for the charts!")

# task 5

def find_artist_by_id(artist_id,artists_low_idnamegenre):
    for value in artists_low_idnamegenre.values():
        if value["id"] == artist_id:
            return value["name"]

def print_all_albums(list_album_artist,chosen_year):
        list_album_artist.sort()
        if len(list_album_artist) == 0:
            print(f"No albums were released in the year {chosen_year}.")
        else:
            print(f"Albums released in the year {chosen_year}:")
            for album_artist in list_album_artist:
                print(f"- \"{album_artist[0]}\" by {album_artist[1]}.")

# task 7

def get_available_songs():
    list_dict_title_artist_lyrics = []
    file_name_data = read_jsons("dataset/songs")

    for data in file_name_data.values():
        list_dict_title_artist_lyrics.append(data) 
    
    return list_dict_title_artist_lyrics

def remove_punctuation(choice ,list_dict_title_artist_lyrics):
    lyrics = re.sub("[\n\r]"," ",list_dict_title_artist_lyrics[choice]["lyrics"].lower())
    lyrics = re.sub(r"\s+"," ",lyrics)
    lyrics_word_list = re.sub(r"[!?.,'()]","",lyrics).split(" ")

    return lyrics_word_list

def get_all_lenghts(lyrics_word_list):
    unique_sequence = []
    all_lengths = []
    
    for word in lyrics_word_list:
        if word in unique_sequence: 
            word_index = unique_sequence.index(word) + 1

            all_lengths.append(len(unique_sequence))
            unique_sequence = unique_sequence[word_index:]
            unique_sequence.append(word)
        else:
            unique_sequence.append(word)
    
    return all_lengths

def find_max_length(all_length):
    max_length = 0

    for length in all_length:
        if max_length < length:
            max_length = length

    return max_length

# task 8

def get_artists_ctcode_date(concerts_info):

    for concert in concerts_info: 

        artists_ctcode_date = {}

        day = f"{int(concert["day"]):02d}"
        month = f"{int(concert["month"]):02d}"
        year = concert["year"]

    if concert["artist"] not in artists_ctcode_date.keys():
        date = f"{year}-{month}-{day}"
        artists_ctcode_date[concert["artist"]] = [(concert["city_code"],date)]
    else:
        date = date = f"{year}-{month}-{day}"
        artists_ctcode_date[concert["artist"]].append((concert["city_code"],date))

    return artists_ctcode_date

def get_concerts_weather(weather_info,artists_ctcode_date,chosen_art):
    
        concerts_weather = []
        for forecast in weather_info:
            for city_code, date in artists_ctcode_date[chosen_art]:
                if city_code == forecast["city_code"] and date == forecast["date"]:
                    concerts_weather.append(forecast)
        return concerts_weather

def get_date_suffix(concerts_weather):

    dates = []

    for concert in concerts_weather:  
        date_str = concert["date"]  # e.g. '2025-09-25'
        
        year = int(date_str[:4])    
        month = int(date_str[5:7])     
        day = int(date_str[-2:])         
        if 11 <= day <= 13:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        
        month_name = months[int(month) - 1]
        
        dates.append(f"{month_name} {day}{suffix} {year}")
    return dates

def get_recommendations(concerts_weather):
            weather_recom = []

            for weather in concerts_weather:
                recommend = ""
                if int(weather["temperature_min"]) > 10 and float(weather["precipitation"]) < 2.3:
                    recommend += "Perfect weather!"

                if int(weather["temperature_min"]) <= 10:
                    recommend += "Wear warm clothes. "

                if float(weather["precipitation"]) >= 2.3:
                    if int(weather["wind_speed"]) < 15:
                        recommend += "Bring an umbrella."
                    else:
                        recommend += "Bring a rain jacket."
            
                weather_recom.append(recommend)
                return weather_recom
            
def print_recom(weather_recom, concerts_weather, dates, chosen_art):

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