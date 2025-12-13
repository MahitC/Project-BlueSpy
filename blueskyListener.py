import time
import pandas as pd
from atproto import FirehoseSubscribeReposClient, parse_subscribe_repos_message, CAR, models

# SETTINGS
DURATION_SECONDS = 60  # How long to listen (in seconds)
OUTPUT_FILE = "bluesky_data.csv"
KEYWORDS = []  # Leave empty to grab EVERYTHING, or add terms like ["tech", "ai", "cat"]

# List to store data before saving
collected_posts = []
start_time = time.time()

print("running listener")

def on_message_handler(message) -> None:
    # Stop if time is up
    if time.time() - start_time > DURATION_SECONDS:
        print("Time limit reached. Stopping...")
        client.stop()
        return

    # Parse the message from the firehose
    commit = parse_subscribe_repos_message(message)
    
    # We only care about 'Commit' messages (actual data updates)
    if not isinstance(commit, models.ComAtprotoSyncSubscribeRepos.Commit):
        return

    # If the commit has data blocks (CAR file), decode them
    if not commit.blocks:
        return

    car = CAR.from_bytes(commit.blocks)

    for op in commit.ops:
        # We only want NEW posts (action == 'create')
        if op.action == 'create' and op.path.startswith('app.bsky.feed.post'):
            # Extract the raw data for this post
            raw_record = car.blocks.get(op.cid)
            
            # The record is a dictionary, key data is in 'text' and 'createdAt'
            if raw_record and 'text' in raw_record:
                post_text = raw_record['text']
                created_at = raw_record['createdAt']
                
                # Simple keyword filter (optional)
                if KEYWORDS and not any(k.lower() in post_text.lower() for k in KEYWORDS):
                    continue
                
                print(f"Captured: {post_text[:50]}...") # Print preview
                
                collected_posts.append({
                    "timestamp": created_at,
                    "text": post_text,
                    "cid": str(op.cid)
                })

if __name__ == '__main__':
    print(f"Listening to Bluesky Firehose for {DURATION_SECONDS} seconds...")
    
    # Initialize the client (No login required for public firehose)
    client = FirehoseSubscribeReposClient()
    
    try:
        client.start(on_message_handler)
    except KeyboardInterrupt:
        print("Stopped manually.")
    
    # Save to CSV when finished
    if collected_posts:
        df = pd.DataFrame(collected_posts)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Success! Saved {len(collected_posts)} posts to {OUTPUT_FILE}")
    else:
        print("No posts matching your criteria were found.")