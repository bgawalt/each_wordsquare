"""Usage: python create_db.py squares.txt squares.db
Format of `squares.txt`: one square per line (separated by a ' ')
Creates (or deletes, then creates) a table `wordsquares` inside `squares.db`
that has columns (id integer, square text, square_size integer, tweet_id text).
Builds indices on id and tweet_id.  tweet_id is populated with all empty strings
and id is populated with a random shuffle of the given squares.  square_size
provides the number of characters in each word of the square.
"""

import random
import sqlite3
import sys


LINE_LEN_TO_SIZE = {
    2: 1,
    6: 2,
    12: 3,
    20: 4,
    30: 5,
    42: 6,
    56: 7,
    72: 8
}


def MakeTable(cur):
    cur.execute("DROP TABLE IF EXISTS wordsquares")
    cur.execute(
        """CREATE TABLE IF NOT EXISTS wordsquares
           (id integer, square text, square_size integer, tweet_id text)"""
    )


def PopulateTable(lines, cur):
    random.shuffle(lines)
    rows = [(id_, line.strip(), LINE_LEN_TO_SIZE[len(line)], "")
             for id_, line in enumerate(lines)]
    cur.executemany(
        """INSERT INTO wordsquares (id, square, square_size, tweet_id)
           VALUES (?, ?, ?, ?)""", rows)


def MakeIndicies(cur):
    cur.execute("""CREATE INDEX IF NOT EXISTS wordsquares_id on
                   wordsquares (id)""")
    cur.execute("""CREATE INDEX IF NOT EXISTS wordsquares_tweet_id on
                   wordsquares (tweet_id)""")


def main(args):
    square_filename = args[1]
    db_name = args[2]
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    MakeTable(cur)

    infile = open(square_filename, "r")
    lines = infile.readlines()
    infile.close()

    PopulateTable(lines, cur)
    MakeIndicies(cur)

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main(sys.argv)
