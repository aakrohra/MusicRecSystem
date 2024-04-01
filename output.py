"""desc"""
from __future__ import annotations

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

import pandas

import graph_loader


def create_pdf(given: str, recs: list[str]) -> None:
    """
    Create a PDF displaying the songs in recs as the most similar songs to the given track,
    using the ReportLab library.
    # TODO: is this a good enough docstring
    """
    c = canvas.Canvas('song_recommendations.pdf', pagesize=letter)  # set up PDF
    c.setFont("Times-Roman", 15, 18)  # set default font size
    curr_x = 1 * inch
    curr_y = 10 * inch

    c.drawString(curr_x, curr_y, f'Song Recommendations Similar to {given}')
    curr_y -= 18
    c.setFont("Times-Roman", 12, 18)  # adjust font size

    c.line(curr_x, curr_y, 8.5 * inch - curr_x, curr_y)
    curr_y -= 25

    c.drawString(curr_x, curr_y, 'The following 15 songs are ranked from most to least similar to the inputted song.')
    curr_y -= 18
    c.drawString(curr_x, curr_y, 'Click the black box next to a song to search for it on YouTube.')
    curr_y -= 25

    i = 1
    for rec in recs:
        c.rect(curr_x, curr_y - 2, 12, 12, fill=1)  # draw a rectangle
        c.linkURL(f'https://www.youtube.com/results?search_query={rec}',
                  (curr_x, curr_y - 2, curr_x + 12, curr_y + 10), relative=1)  # put link where the rectangle is
        c.drawString(curr_x + 30, curr_y, f'{i}. {rec}')  # draw in recommended song
        curr_y -= 18
        i += 1

    c.save()  # save pdf


if __name__ == '__main__':

    data = pandas.read_csv('music_genre.csv', usecols=['instance_id', 'artist_name', 'track_name'])

    input_song = 0.0
    track = ''
    artist = ''
    valid = False

    while not valid:  # loop until a valid formatted input is given
        print('What song would you like to generate recommendations for?')
        print('Please enter as follows: Track Name - Artist Name')
        try:
            track, artist = input().split(' - ')
            print("Loading...")
            valid = True
        except ValueError:
            print('Not a valid input, try again.')

    for s in data.iterrows():  # to find instance ID based on input
        if s[1]['artist_name'] == artist and s[1]['track_name'] == track:
            input_song = float(s[1]['instance_id'])

    if input_song != 0.0:  # check if the input song actually exists in the database
        # list of recommendations, with IDs
        recs_ids = graph_loader.load_graph('music_rock.csv').get_song_recommendations(input_song)  # TODO: CHANGE TO FULL CSV LATER
        # list of recommendations, track and artist names
        recs_names = [s[1]['track_name'] + ' - ' + s[1]['artist_name'] for s in data.iterrows()
                      if float(s[1]['instance_id']) in recs_ids][:15]
        create_pdf(track + ' - ' + artist, recs_names)  # call helper function to create PDF
        print("A PDF has been created in the same folder as this .py file, with 15 song recommendations\n"
              "based on similarity to your inputted song, from most to least similar!")
    else:
        print(f"There is no track called {track} by {artist} in the database!")
