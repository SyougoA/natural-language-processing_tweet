import sqlite3


class SqliteTweet(object):
    def __init__(self, name):
        db_name = name + ".db"
        self.conn = sqlite3.connect(db_name)
        cur = self.conn.cursor()

        cur.execute("""
                           CREATE TABLE IF NOT EXISTS streaming_tweet(
                           comment_id INTEGER PRIMARY KEY,
                           tweet_name TEXT,
                           comment TEXT,
                           reply_name TEXT
                           );
                           """)

        self.conn.commit()

    def insert_tweet(self, tweet_data):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO streaming_tweet(tweet_name,comment,reply_name) VALUES (?,?,?);",
            tweet_data
        )

        self.conn.commit()
