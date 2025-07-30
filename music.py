music = {
    "jhol": "https://www.youtube.com/watch?v=-2RAq5o5pwc",
    "wavy": "https://www.youtube.com/watch?v=XTp5jaRU3Ws",
    "saxophone": "https://www.youtube.com/watch?v=YqN0ZOEO9oI",
    "drums": "https://www.youtube.com/watch?v=lserNww6WPk",
    "piano": "https://www.youtube.com/watch?v=_mVW8tgGY_w",
    "guitar": "https://www.youtube.com/watch?v=jdYJf_ybyVo",
    "naat": "https://www.youtube.com/watch?v=EarxkHbpWQE"
}

def play(song):
    """
    Returns the URL of the song if found in the music dictionary.
    If the song is not found, returns a default message or URL.
    """
    song = song.lower()
    if song in music:
        return music[song]
    else:
        return "https://www.youtube.com/results?search_query=" + song
