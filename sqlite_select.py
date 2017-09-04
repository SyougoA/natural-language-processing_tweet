import sqlite3


class SelectTweet(object):
    def __init__(self):
        self.dbname = "tl_streaming.db"
        self.conn = sqlite3.connect(self.dbname)

    def export_tweet(self):
        cur = self.conn.cursor()
        cur.execute(
            "select comment from streaming_tweet;"
        )
        tweet = cur.fetchall()

        return tweet

if __name__ == "__main__":
    sl = SelectTweet()
    print(sl.export_tweet())
