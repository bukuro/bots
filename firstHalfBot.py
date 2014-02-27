import feedparser
import praw
import time


def submit_comment(url):
    try:
        submission.add_comment('[First half highlights](' + url + ')')
    except praw.errors.RateLimitExceeded as e:
        #sleep until the rate limit let the bot comment again
        time.sleep(e.sleep_time)
        submit_comment(url)

try:
    r = praw.Reddit('NBA first half highlights bot')
    r.login('', '')
except Exception as e:
    print("Error", e)
    exit(1)

teams_dictionary = {
    "celtics": "Boston Celtics",
    "nets": "Brooklyn Nets",
    "knicks": "New York Knicks",
    "sixers": "Philadelphia 76ers",
    "raptors": "Toronto Raptors",
    "bulls": "Chicago Bulls",
    "cavaliers": "Cleveland Cavaliers",
    "pistons": "Detroit Pistons",
    "pacers": "Indiana Pacers",
    "bucks": "Milwaukee Bucks",
    "hawks": "Atlanta Hawks",
    "bobcats": "Charlotte Bobcats",
    "heat": "Miami Heat",
    "magic": "Orlando Magic",
    "wizards": "Washington Wizards",
    "mavericks": "Dallas Mavericks",
    "rockets": "Houston Rockets",
    "grizzlies": "Memphis Grizzlies",
    "pelicans": "New Orleans Pelicans",
    "spurs": "San Antonio Spurs",
    "nuggets": "Denver Nuggets",
    "timberwolves": "Minnesota Timberwolves",
    "thunder": "Oklahoma City Thunder",
    "blazers": "Portland Trail Blazers",
    "jazz": "Utah Jazz",
    "warriors": "Golden State Warriors",
    "clippers": "Los Angeles Clippers",
    "lakers": "Los Angeles Lakers",
    "suns": "Phoenix Suns",
    "kings": "Sacramento Kings"}

lastEntry = None
nba_mod = None
index_list = 0
links = []

while True:
    nbaFeed = feedparser.parse('http://www.nba.com/topvideo/rss.xml', modified=nba_mod)
    if nbaFeed.status is 200:
        nba_mod = nbaFeed.modified
        firstEntry = None
        for entry in nbaFeed.entries:
            if not firstEntry:
                firstEntry = entry.id
            if lastEntry == entry.id:
                break
            elif entry['title'].find(': First half') is not -1 and not entry.id in links:
                links.append(entry.id)
                if len(links) > 15:
                    del links[:5]
                team_playing = entry['category'][6:]
                video_link = entry['link']
                submissions = r.search('title:\"Game Thread ' + teams_dictionary[team_playing] + '\"', 'nba', 'new',
                                       None, 'day')
                for submission in submissions:
                    submit_comment(video_link)
                    break
        lastEntry = firstEntry
    time.sleep(60)