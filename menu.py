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
10.Exit

Type your option:"""

    print(menu)
    menu_choice = int(input())

    match menu_choice:
        case 1:
            get_all_artists() 
            app_menu()
        case 2:
            all_albums_artist() 
            app_menu()
        case 3:
            top_tracks_artist() 
            app_menu()
        case 4:
            export_artist_data() 
            app_menu()
        case 5:
            relesed_album_year() 
            app_menu()
        case 6:
            creativity_score() 
            app_menu()
        case 7:
            longest_uniq_seq() 
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

app_menu()