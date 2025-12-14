# read the CSV and do data analytics with it
# format: timestamp,text,cid
# have a global counter of number of posts
import time
import pandas as pd
import blueskyListener as bl
import numpy as np
import matplotlib.pyplot as plt
import string
from collections import Counter
import tkinter as tk
from tkinter import simpledialog
from functools import partial

stopwords = {"able", "about", "above", "abroad", "according", "accordingly", "across", "actually", "adj", "after",
             "afterwards", "again", "against", "ago", "ahead", "ain't", "all", "allow", "allows", "almost", "alone",
             "along", "alongside", "already", "also", "although", "always", "am", "amid", "amidst", "among", "amongst",
             "an", "and", "another", "any", "anybody", "anyhow", "anyone", "anything", "anyway", "anyways", "anywhere",
             "apart", "appear", "appreciate", "appropriate", "are", "aren't", "around", "as", "a's", "aside", "ask",
             "asking", "associated", "at", "available", "away", "awfully", "back", "backward", "backwards", "be",
             "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "behind",
             "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "both", "brief",
             "but", "by", "came", "can", "cannot", "cant", "can't", "caption", "cause", "causes", "certain",
             "certainly", "changes", "clearly", "c'mon", "co", "co.", "com", "come", "comes", "concerning",
             "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could",
             "couldn't", "course", "c's", "currently", "dare", "daren't", "definitely", "described", "despite", "did",
             "didn't", "different", "directly", "do", "does", "doesn't", "doing", "done", "don't", "down", "downwards",
             "during", "each", "edu", "eg", "eight", "eighty", "either", "else", "elsewhere", "end", "ending", "enough",
             "entirely", "especially", "et", "etc", "even", "ever", "evermore", "every", "everybody", "everyone",
             "everything", "everywhere", "ex", "exactly", "example", "except", "fairly", "far", "farther", "few",
             "fewer", "fifth", "first", "five", "followed", "following", "follows", "for", "forever", "former",
             "formerly", "forth", "forward", "found", "four", "from", "further", "furthermore", "get", "gets",
             "getting", "given", "gives", "go", "goes", "going", "gone", "got", "gotten", "greetings", "had", "hadn't",
             "half", "happens", "hardly", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "hello",
             "help", "hence", "her", "here", "hereafter", "hereby", "herein", "here's", "hereupon", "hers", "herself",
             "he's", "hi", "him", "himself", "his", "hither", "hopefully", "how", "howbeit", "however", "hundred",
             "i'd", "ie", "if", "ignored", "i'll", "i'm", "immediate", "in", "inasmuch", "inc", "inc.", "indeed",
             "indicate", "indicated", "indicates", "inner", "inside", "insofar", "instead", "into", "inward", "is",
             "isn't", "it", "it'd", "it'll", "its", "it's", "itself", "i've", "just", "k", "keep", "keeps", "kept",
             "know", "known", "knows", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let",
             "let's", "like", "liked", "likely", "likewise", "little", "look", "looking", "looks", "low", "lower",
             "ltd", "made", "mainly", "make", "makes", "many", "may", "maybe", "mayn't", "me", "mean", "meantime",
             "meanwhile", "merely", "might", "mightn't", "mine", "minus", "miss", "more", "moreover", "most", "mostly",
             "mr", "mrs", "much", "must", "mustn't", "my", "myself", "name", "namely", "nd", "near", "nearly",
             "necessary", "need", "needn't", "needs", "neither", "never", "neverf", "neverless", "nevertheless", "new",
             "next", "nine", "ninety", "no", "nobody", "non", "none", "nonetheless", "noone", "no-one", "nor",
             "normally", "not", "nothing", "notwithstanding", "novel", "now", "nowhere", "obviously", "of", "off",
             "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "one's", "only", "onto", "opposite", "or",
             "other", "others", "otherwise", "ought", "oughtn't", "our", "ours", "ourselves", "out", "outside", "over",
             "overall", "own", "particular", "particularly", "past", "per", "perhaps", "placed", "please", "plus",
             "possible", "presumably", "probably", "provided", "provides", "que", "quite", "qv", "rather", "rd", "re",
             "really", "reasonably", "recent", "recently", "regarding", "regardless", "regards", "relatively",
             "respectively", "right", "round", "said", "same", "saw", "say", "saying", "says", "second", "secondly",
             "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent",
             "serious", "seriously", "seven", "several", "shall", "shan't", "she", "she'd", "she'll", "she's", "should",
             "shouldn't", "since", "six", "so", "some", "somebody", "someday", "somehow", "someone", "something",
             "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify", "specifying",
             "still", "sub", "such", "sup", "sure", "take", "taken", "taking", "tell", "tends", "th", "than", "thank",
             "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them",
             "themselves", "then", "thence", "there", "thereafter", "thereby", "there'd", "therefore", "therein",
             "there'll", "there're", "theres", "there's", "thereupon", "there've", "these", "they", "they'd", "they'll",
             "they're", "they've", "thing", "things", "think", "third", "thirty", "this", "thorough", "thoroughly",
             "those", "though", "three", "through", "throughout", "thru", "thus", "till", "to", "together", "too",
             "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "t's", "twice", "two", "un",
             "under", "underneath", "undoing", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "up",
             "upon", "upwards", "us", "use", "used", "useful", "uses", "using", "usually", "v", "value", "various",
             "versus", "very", "via", "viz", "vs", "want", "wants", "was", "wasn't", "way", "we", "we'd", "welcome",
             "well", "we'll", "went", "were", "we're", "weren't", "we've", "what", "whatever", "what'll", "what's",
             "what've", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "where's",
             "whereupon", "wherever", "whether", "which", "whichever", "while", "whilst", "whither", "who", "who'd",
             "whoever", "whole", "who'll", "whom", "whomever", "who's", "whose", "why", "will", "willing", "wish",
             "with", "within", "without", "wonder", "won't", "would", "wouldn't", "yes", "yet", "you", "you'd",
             "you'll", "your", "you're", "yours", "yourself", "yourselves", "you've", "zero", "a", "how's", "i",
             "when's", "why's", "b", "c", "d", "e", "f", "g", "h", "j", "l", "m", "n", "o", "p", "q", "r", "s", "t",
             "u", "uucp", "w", "x", "y", "z", "I", "www", "amount", "bill", "bottom", "call", "computer", "con",
             "couldnt", "cry", "de", "describe", "detail", "due", "eleven", "empty", "fifteen", "fifty", "fill", "find",
             "fire", "forty", "front", "full", "give", "hasnt", "herse", "himse", "interest", "itse”", "mill", "move",
             "myse”", "part", "put", "show", "side", "sincere", "sixty", "system", "ten", "thick", "thin", "top",
             "twelve", "twenty", "abst", "accordance", "act", "added", "adopted", "affected", "affecting", "affects",
             "ah", "announce", "anymore", "apparently", "approximately", "aren", "arent", "arise", "auth", "beginning",
             "beginnings", "begins", "biol", "briefly", "ca", "date", "ed", "effect", "et-al", "ff", "fix", "gave",
             "giving", "heres", "hes", "hid", "home", "id", "im", "immediately", "importance", "important", "index",
             "information", "invention", "itd", "keys", "kg", "km", "largely", "lets", "line", "'ll", "means", "mg",
             "million", "ml", "mug", "na", "nay", "necessarily", "nos", "noted", "obtain", "obtained", "omitted", "ord",
             "owing", "page", "pages", "poorly", "possibly", "potentially", "pp", "predominantly", "present",
             "previously", "primarily", "promptly", "proud", "quickly", "ran", "readily", "ref", "refs", "related",
             "research", "resulted", "resulting", "results", "run", "sec", "section", "shed", "shes", "showed", "shown",
             "showns", "shows", "significant", "significantly", "similar", "similarly", "slightly", "somethan",
             "specifically", "state", "states", "stop", "strongly", "substantially", "successfully", "sufficiently",
             "suggest", "thered", "thereof", "therere", "thereto", "theyd", "theyre", "thoughh", "thousand", "throug",
             "til", "tip", "ts", "ups", "usefully", "usefulness", "'ve", "vol", "vols", "wed", "whats", "wheres",
             "whim", "whod", "whos", "widely", "words", "world", "youd", "youre", "people", "&", "-", "it's", "i'm",
             "time", "la", "el", "en", "es", "del", "ich", "yo", "moi","este","fui","soy","eso","ere","era", "esta", "estas", "!", "$", "%", "^", "*", "(", ")", "_",
             "-", "=", "+", ".", ",", "\"", "\'", "1", "2", "3", "4",
             "5", "6", "7", "8", "9", "0", "?", "<", ">", "/", ":", ";", "la", "le", "de", "du", "aux", "au", "en",
             "les", "des", "je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "https", "bsky", "social", "good", "don","ch" "it","its"}


def search(dur):
    global postTexts
    global postTimestamps
    global postTags
    global textStamps
    global tagStamps
    global tagFreq
    global wordFreq
    bl.DURATION_SECONDS = dur

    bl.spy()

    try:
        df = pd.read_csv("bluesky_data.csv")
    except FileNotFoundError:
        print("Error: bluesky_data.csv not found.")
        exit()

    # data frames for texts, tags, and stamps
    postTexts = df['text'].fillna("").tolist()
    postTimestamps = df['timestamp'].tolist()
    postTags = df['tags'].fillna("").tolist()

    # dict for time vs text
    textStamps = {}
    for i in range(len(postTimestamps)):
        textStamps.update({postTimestamps[i]: postTexts[i]})

    tagStamps = {}
    for i in range(len(postTimestamps)):
        tagStamps.update({postTimestamps[i]: postTags[i]})

    # freq dicts for tags and words
    tagList = []
    for i in postTags:
        tagList.extend(set(i.split('#')))
    tagList = list(filter(lambda x: x != "", tagList))
    tagFreq = Counter(tagList)

    wordList = []
    for text in postTexts:
        # remove all punctuation and make word lower case for searching
        #punctuation = "'!#$%&\'()*+,./:;<=>?@[\\]^_`{|}~"
        translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        print(translator)
        filtered = ' ' + text.lower().translate(translator) + ' '
        print(filtered)
        words = filtered.split()
        print(words)
        unique_words = set(words)
        filtered_words = unique_words - stopwords
        wordList.extend(filtered_words)

    wordFreq = Counter(wordList)




def postFreq():
    print("Avg posts per second: ", len(postTexts) / bl.DURATION_SECONDS)


def getTagStamps(word):
    tagStamp = {}
    for i in range(len(postTimestamps)):
        tagStamp.update({postTimestamps[i]: postTags[i]})

    filteredTag = []
    for x, y in tagStamp.items():

        if word in y:
            filteredTag.append(x)
    return filteredTag


def getTextStamps(word):
    filteredText = []
    for x, y in textStamps.items():

        if word in y:
            filteredText.append(x)
    return filteredText


def GraphTimeVsWord(target, numIntervals, dict, dataType):
    # create x-axis time labels for graph
    startTime = pd.to_datetime(postTimestamps[0], utc=True)
    intervalDuration = bl.DURATION_SECONDS / numIntervals
    intervalLabels = []

    # calculate the change in time for each interval
    deltaTime = pd.Timedelta(seconds=intervalDuration)

    for i in range(numIntervals):
        # Calculate the time for the current interval
        intervalTime = startTime + (deltaTime * i)

        # Format the time into 24hr (H:M:S) format in UTC and store it
        intervalLabels.append(intervalTime.strftime('%H:%M:%S') + ' UTC')

    print(f"Analysis start time determined from first post: {startTime}")
    print(f"Total duration: {bl.DURATION_SECONDS}s, Interval duration: {intervalDuration:.2f}s")

    intervalCounts = np.zeros(numIntervals)
    totalFound = 0

    # remove all punctuation and make word lower case for searching
    #punctuation = "'!#$%&\'()*+,./:;<=>?@[\\]^_`{|}~"
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    toSearch = ' ' + target.lower().translate(translator) + ' '

    # loop Through All Posts and find frequency and interval of target word
    for timeStamp, text in dict.items():

        # Clean the post text and pad with spaces for accurate word search
        text = ' ' + text.lower().translate(translator) + ' '

        if toSearch in text:

            try:
                # Convert the timestamp string to datetime
                current_time = pd.to_datetime(timeStamp, utc=True)
            except Exception:
                continue

            timeElapsed = (current_time - startTime).total_seconds()
            interval_index = int(timeElapsed / intervalDuration)

            # assign to nearest index if overflow or underflow occurs
            if interval_index < 0:
                intervalCounts[0] += 1

            elif interval_index >= numIntervals:
                intervalCounts[len(intervalCounts) - 1] += 1

            else:
                intervalCounts[interval_index] += 1

            totalFound += 1

    if totalFound == 0:
        print(f"The word '{target}' was not found in any {dataType.lower()}s during the listening period.")
        return

    #configure chart
    plt.figure(figsize=(12, 7))

    plt.bar(range(numIntervals), intervalCounts, color='skyblue')

    plt.title(f'Frequency of {dataType}s Containing "{target}" over {numIntervals} Intervals (Total: {totalFound})')
    plt.xlabel(f'Time Interval (Total Duration: {bl.DURATION_SECONDS} seconds)')
    plt.ylabel('Count of Occurrences')

    plt.xticks(ticks=range(numIntervals), labels=intervalLabels, rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

#plot most frequently appearing words/tags
def plotFreq(data, size, label):
    data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

    df = pd.DataFrame(
        list(data.values())[:size],
        columns=['freq'],
        index=list(data.keys())[:size]
    )

    print(df.head())

    #configure chart
    df.plot(kind='bar', legend=False, rot=45, color='skyblue')
    plt.title(f"Frequencies by {label}")
    plt.xlabel(label)
    plt.ylabel("Frequency")
    plt.xticks()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


root = tk.Tk()
root.title("Data Visualization Menu")


# UI Button actions
def action_graph_tag():
    tagName = simpledialog.askstring("Input", "Tag to search for: ")

    if not(tagName is None or tagName == ""):
        intervalCount = simpledialog.askinteger("Input", "How many intervals? (We recommend 10): ")

        if not(intervalCount is None or intervalCount <= 0):
            GraphTimeVsWord(tagName, intervalCount, tagStamps, dataType="Tag")

def action_plot_words():
    wordCount = simpledialog.askinteger("Input", "How many words (We recommend 10)? ")
    if not(wordCount is None or wordCount <= 0):
        plotFreq(wordFreq, wordCount, "words")


def action_graph_post():
    wordName = simpledialog.askstring("Input", "Enter word to search for: ")
    
    if not(wordName is None or wordName == ""):
        intervalCount = simpledialog.askinteger("Input", "How many intervals? (We recommend 10): ")

        if not(intervalCount is None or intervalCount <= 0):
            GraphTimeVsWord(wordName, intervalCount, textStamps, dataType="Post")


def action_plot_tags():
    tagCount = simpledialog.askinteger("Input", "How many tags? (We recommend 10): ")
    if not(tagCount is None or tagCount <= 0):
        plotFreq(tagFreq, tagCount, "tags")


def action_search():
    dur = simpledialog.askinteger("Input", "How many seconds should we read the data for? ")
    if not(dur is None or dur <= 0):
        search(dur)


#setup main gui
tk.Label(root, text="DASHBOARD", font=("Arial", 16, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Graph time vs specific tag", width=30, command=action_graph_tag).pack(pady=5)
tk.Button(frame, text="Graph time vs specific word", width=30, command=action_graph_post).pack(pady=5)
tk.Button(frame, text="Plot tag frequency", width=30, command=action_plot_tags).pack(pady=5)
tk.Button(frame, text="Plot word frequency", width=30, command=action_plot_words).pack(pady=5)
tk.Button(frame, text="listen", width=30, command=action_search).pack(pady=5)

tk.Button(root, text="Exit", width=30, command=root.quit, bg="red", fg="white").pack(pady=20)

root.mainloop()
