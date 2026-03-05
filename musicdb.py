#!/usr/bin/env python3
"""
musicdb - A very simple music search tool

This program searches a small music database stored
in a JSON file on your computer.
"""

import json
import argparse
import os
import sys


class MusicDatabase:
    """Loads and searches the music database"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.songs = self.load_database()

    def load_database(self):
        """Load the music file"""

        try:
            with open(self.filepath) as file:
                return json.load(file)

        except FileNotFoundError:
            print("Database file not found.")
            sys.exit(1)

        except json.JSONDecodeError:
            print("Database file is broken.")
            sys.exit(1)

    def search(self, word):
        """Search songs by title, artist, or genre"""

        word = word.lower()
        results = []

        for song in self.songs:

            title = song.get("title", "").lower()
            artist = song.get("artist", "").lower()
            genre = song.get("genre", "").lower()

            if word in title or word in artist or word in genre:
                results.append(song)

        return results


class Screen:
    """Handles printing results to the screen"""

    def show_results(self, songs):

        if not songs:
            print("No songs found.")
            return

        print("\nFound", len(songs), "song(s)\n")

        for song in songs:

            title = song.get("title", "Unknown")
            artist = song.get("artist", "Unknown")
            year = song.get("year", "?")
            genre = song.get("genre", "?")

            print(f"Title : {title}")
            print(f"Artist: {artist}")
            print(f"Year  : {year}")
            print(f"Genre : {genre}")
            print("-" * 30)


def main():
    """Main program"""

    parser = argparse.ArgumentParser(
        description="Search your local music database"
    )

    parser.add_argument(
        "query",
        help="word to search for (title, artist, genre)"
    )

    parser.add_argument(
        "-f",
        "--file",
        default=os.path.expanduser("~/.musicdb.json"),
        help="location of the music database file"
    )

    args = parser.parse_args()

    database = MusicDatabase(args.file)
    results = database.search(args.query)

    screen = Screen()
    screen.show_results(results)


if __name__ == "__main__":
    main()
