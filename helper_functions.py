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