import os,json,re,csv

# task 1 
      
def get_artists_info():
    folder_path = "dataset/artists"
    artists_low_idnamegenre = {}
    for artist_info in read_jsons(folder_path).values():
        artists_low_idnamegenre[artist_info["name"].lower()] = {"id":artist_info["id"],"name":artist_info["name"],"genres":artist_info["genres"]}
    return artists_low_idnamegenre

#task 2

def format_release_date(release_date, precision):
    if not release_date:
        return "Date Not Found"
    months = ["January","February","March","April","May","June"]
    months += ["July","August","September","October","November","December"]
    if precision == "day":
        year, month, day = release_date.split('-')
        month_name = months[int(month) - 1]
        day_int = int(day)
        if 11 <= day_int <= 13:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day_int % 10, "th")
        return f"{month_name} {day_int}{suffix} {year}"
    if precision == "month":
        year, month = release_date.split('-')[:2]
        month_name = months[int(month) - 1]
        return f"{month_name} {year}"
    return release_date

# task 3

def find_artist(chosen_art,artists_name_idnamegenre):    
        artist_found = False
        for key in artists_name_idnamegenre.keys():
            if key == chosen_art.lower():
                artist_found = True
                return artist_found
        return False

def read_jsons(folder_path):
    list_json = sorted(os.listdir(folder_path))
    
    file_name_data = {}

    for file_name in list_json:
        with open(f"{folder_path}/{file_name}", 'r',encoding = "utf-8") as file:
            file_content = json.load(file)
            file_name_data[file_name] = file_content
    return file_name_data

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

#task 4

def write_csv_rows(path, header, rows):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline='', encoding="utf8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

def update_or_append_csv(path, header, row, key_field):
    rows = read_csv_rows(path)
    updated = False
    for r in rows:
        if r.get(key_field) == row.get(key_field):
            r.update(row)
            updated = True
            break
    if not updated:
        rows.append(row)
    write_csv_rows(path, header, rows)
    return updated


# task 5

def sanitize_text(text):
    if text is None:
        return ""
    txt = text
    txt = re.sub(r"[.,!?\"'()\/:;]", "", txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    return txt

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

#task 6

def get_song_entries():
    out = []
    folder = os.path.join("dataset", "songs")
    for fname in sorted(os.listdir(folder)):
        full = os.path.join(folder, fname)
        data = safe_load_json(full)
        if not data:
            continue
        out.append((data.get("title", "Unknown Title"), data.get("artist", "Unknown Artist"), data.get("lyrics", "")))
    return out

# task 7

def get_available_songs():
    list_dict_title_artist_lyrics = []
    file_name_data = read_jsons("dataset/songs")

    for data in file_name_data.values():
        list_dict_title_artist_lyrics.append(data) 
    
    return list_dict_title_artist_lyrics

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

    artists_ctcode_date = {}
    for concert in concerts_info: 

        

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

    months = ["January","February","March","April","May","June"]
    months += ["July","August","September","October","November","December"]

    for concert in concerts_weather:  
        date_str = concert["date"]
        
        year = int(date_str[:4])    
        month = int(date_str[5:7])     
        day = int(date_str[-2:])         
        if 11 <= day <= 13:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        
        month_str = months[int(month) - 1]
        
        dates.append(f"{month_str} {day}{suffix} {year}")
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

# task 9

def safe_load_json(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

def read_csv_rows(file_path):
    if not os.path.exists(file_path):
        open(file_path, "w", encoding="utf-8").close()
    csv_rows = []
    with open(file_path,"r",encoding = "utf-8") as file:
        files_content = csv.DictReader(file)
        for row in files_content:
            csv_rows.append(row)
    return csv_rows

def save_inverted_index(path, index):
    to_save = {w: [[t, a] for (t, a) in lst] for w, lst in index.items()}
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf8") as f:
        json.dump(to_save, f, ensure_ascii=False, indent=2)

def load_inverted_index(path):
    data = safe_load_json(path)
    if not data:
        return {}
    index = {}
    for word, items in data.items():
        tuples_list = []
        for item in items:
            tuples_list.append(tuple(item))
        index[word] = tuples_list
    return index
