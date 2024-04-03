"""CSC111 Project 2 - PDF Loader

Module Description: Contains a function to create a song recommendation PDF based on an inputted
song and recommendations.

This file is Copyright (c) 2024 Aakaash Rohra, Daniel Xie, Ethan Chiu, and Jackie Chen.
"""
from __future__ import annotations
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


def create_pdf(given: str, recs: list[str]) -> None:
    """
    Create a PDF displaying the songs in recs as the most similar songs to the given track,
    using the ReportLab library. This PDF is located in the same file as pdf_loader.py.
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
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['reportlab.pdfgen', 'reportlab.lib.pagesizes', 'reportlab.lib.units'],
    })
