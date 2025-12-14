import time
import pandas as pd
from atproto import FirehoseSubscribeReposClient, parse_subscribe_repos_message, CAR, models

# SETTINGS
DURATION_SECONDS = 10  # How long to listen (in seconds)
OUTPUT_FILE = "bluesky_data.csv"
KEYWORDS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
            "v", "w", "x", "y", "z"]  # Leave empty to grab EVERYTHING, or add terms like ["tech", "ai", "cat"]
CLIENT = FirehoseSubscribeReposClient()
# List to store data before saving
collectedPosts = []
startTime = time.time()

print("running listener")


def on_message_handler(message) -> None:
    # Stop if time is up
    if time.time() - startTime > DURATION_SECONDS:
        print("Time limit reached. Stopping...")
        CLIENT.stop()
        return

    # Parse the message from the firehose into a commit object
    commit = parse_subscribe_repos_message(message)

    # Only move forward if the message passed in was a commit object, not any other like an account update
    if not isinstance(commit, models.ComAtprotoSyncSubscribeRepos.Commit):
        return

    # If the commit has data blocks (CAR file), decode them
    if not commit.blocks:
        return

    car = CAR.from_bytes(commit.blocks)

    for op in commit.ops:
        # only get posts added in live during the listening period (action == 'create')
        if op.action == 'create' and op.path.startswith('app.bsky.feed.post'):

            # extract the raw data for this post
            rawRecord = car.blocks.get(op.cid)

            # The record is a dict with post text and timestamp
            if rawRecord and 'text' in rawRecord:
                postText = rawRecord['text']
                createdAt = rawRecord['createdAt']

                # create a separate list for hashtags and non-hashtag text in the post
                words = postText.split()
                filteredWords = []
                hashtags = []
                punctuation = '.,!?:;()[]{}<>"\'\n'
                for word in words:
                    if word.startswith("#"):
                        for p in punctuation:
                            word = word.rstrip(p)
                        hashtags.append(word)
                    else:
                        filteredWords.append(word)

                # combine all the text into one string to send to the csv file
                filteredText = " ".join(filteredWords)
                hashtags = "".join(hashtags)

                # filter posts so that every post is in english script(optional) 
                if KEYWORDS and not any(k.lower() in postText.lower() for k in KEYWORDS):
                    continue

                print(f"Captured: {postText[:50]}...")  # Print preview

                collectedPosts.append({
                    "timestamp": createdAt,
                    "text": filteredText,
                    "tags": hashtags,
                    "cid": str(op.cid)
                })


def spy():
    global CLIENT, collectedPosts, startTime
    CLIENT = FirehoseSubscribeReposClient()
    collectedPosts = []
    startTime = time.time()

    print(f"Listening to Bluesky Firehose for {DURATION_SECONDS} seconds...")

    try:
        CLIENT.start(on_message_handler)
    except KeyboardInterrupt:
        print("Terminating search manually.")
    except Exception as e:
        print(f"Something went wrong on the server side: {e}")

    # save to CSV when finished
    if collectedPosts:
        df = pd.DataFrame(collectedPosts)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Success! Saved {len(collectedPosts)} posts to {OUTPUT_FILE}")
    else:
        print("No posts matching your criteria were found.")
