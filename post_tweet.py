""" Usage: python tweet_square.py squares.db auth.config

Grab the next untweeted wordsquare out of the given `squares.db` database from
its `wordsquares` table.  If `test` is in the arguments, just print the tweet
to stdout.  Loads the necessary Twitter auth info from the `auth.config` file.
Format that auth file as:
    CONSUMER_KEY = [...]
    CONSUMER_SECRET = [...]
    ACCESS_SECRET = [...]
    ACCESS_KEY = [...]
"""

import sqlite3
import sys
import tweepy


NORMAL_TO_UNICODE = {
    'a': u'\uFF21',    'b': u'\uFF22',    'c': u'\uFF23',    'd': u'\uFF24',
    'e': u'\uFF25',    'f': u'\uFF26',    'g': u'\uFF27',    'h': u'\uFF28',
    'i': u'\uFF29',    'j': u'\uFF2A',    'k': u'\uFF2B',    'l': u'\uFF2C',
    'm': u'\uFF2D',    'n': u'\uFF2E',    'o': u'\uFF2F',    'p': u'\uFF30',
    'q': u'\uFF31',    'r': u'\uFF32',    's': u'\uFF33',    't': u'\uFF34',
    'u': u'\uFF35',    'v': u'\uFF36',    'w': u'\uFF37',    'x': u'\uFF38',
    'y': u'\uFF39',    'z': u'\uFF3A'
}


def GetNextSquare(cur):
    cur.execute("""SELECT id, square from wordsquares
                   where tweet_id = '' order by id limit 1""")
    return cur.fetchone()


def SquareToUnicode(square):
    """Replace ASCII with monospace Unicode equivalent, and add line breaks."""
    unicoded = "".join([NORMAL_TO_UNICODE.get(ch, ch) for ch in square])
    return "\n".join(unicoded.split())


def GetTweepyConfig(config_filename):
    """Returns dictionary with auth details for building a Tweepy API object."""
    print 'gtc', config_filename
    with open(config_filename, "r") as infile:
        config = {}
        for line in infile:
            spline = line.split(" = ")
            config[spline[0]] = spline[1].strip()
    print config
    return config


def GetTweepyAuth(config_file):
    config = GetTweepyConfig(config_file)
    ckey = config["CONSUMER_KEY"]
    csec = config["CONSUMER_SECRET"]
    akey = config["ACCESS_KEY"]
    asec = config["ACCESS_SECRET"]
    auth = tweepy.OAuthHandler(ckey, csec)
    auth.set_access_token(akey, asec)
    return auth


def TweetSquare(raw_square, tweepy_config_filename):
    """Transform square text from DB form to Unicode, then tweet it out."""
    tweet_text = SquareToUnicode(raw_square)
    auth = GetTweepyAuth(tweepy_config_filename)
    api = tweepy.API(auth)
    status = api.update_status(status=tweet_text)
    return status.id_str


def MarkAsTweeted(cur, square_id, tweet_id):
    cur.execute("UPDATE wordsquares SET tweet_id = ? where id = ?",
                (tweet_id, square_id))


def main(args):
    db_filename = args[1]
    twconfig_filename = args[2]

    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    sq_id, square = GetNextSquare(cur)
    print square
    tw_id = TweetSquare(square, twconfig_filename)
    MarkAsTweeted(cur, sq_id, tw_id)

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main(sys.argv)
