"""CSC111 Project 2 - Main File

Module Description: Takes input from the user and calls graph_loader.py and pdf_loader.py to
generate song recommendations for the user.

This file is Copyright (c) 2024 Aakaash Rohra, Daniel Xie, Ethan Chiu, and Jackie Chen.
"""
from __future__ import annotations
import pandas
import pdf_loader
import graph_loader


if __name__ == '__main__':

    data = pandas.read_csv('music_genre.csv',
                           usecols=['instance_id', 'artist_name', 'track_name', 'music_genre'])

    input_song = 0.0
    input_genre = ''
    valid = False

    while not valid:  # loop until a valid formatted input is given
        print('What song would you like to generate recommendations for?')
        track = input('Please enter the track name: ').lower()
        artist = input('Please enter the artist name: ').lower()
        print("Loading...")

        for s in data.iterrows():  # to find instance ID based on input
            if str(s[1]['artist_name']).lower() == artist and str(s[1]['track_name']).lower() == track:
                input_song = float(s[1]['instance_id'])
                input_genre = s[1]['music_genre']

        if input_song != 0.0 and input_genre != '':  # check if the input song actually exists in the database
            # list of recommendations, with IDs
            recs_ids = graph_loader.load_graph('music_genre.csv', input_genre).get_song_recommendations(input_song)
            # list of recommendations, track and artist names
            recs_names = [c[1]['track_name'] + ' - ' + c[1]['artist_name'] for c in data.iterrows()
                          if float(c[1]['instance_id']) in recs_ids][:15]
            pdf_loader.create_pdf(track + ' - ' + artist, recs_names)  # call helper function to create PDF
            print("A PDF has been created in the same folder as this .py file, with 15 song recommendations\n"
                  "based on similarity to your inputted song, from most to least similar!")
            valid = True
        else:
            print(f"There is no track called {track} by {artist} in the database! Do you want to try again? Y/N")
            try_again = False
            while not try_again:
                yn = input()
                if yn.upper() == 'Y':
                    valid = False
                    try_again = True
                elif yn.upper() == 'N':
                    print("Thanks for trying!")
                    valid = True
                    try_again = True
                else:
                    print("Please enter Y if you'd like to try again, or N if you'd like to exit!'")

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['pandas', 'pdf_loader', 'graph_loader'],
    })
