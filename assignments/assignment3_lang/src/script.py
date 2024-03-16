import argparse
import os
import gensim.downloader as api
import pandas as pd
import re
import sys


def load_data():
    file_path = os.path.join(
        "..", 
        "in",
        "Spotify Million Song Dataset_exported.csv")

    df = pd.read_csv(file_path, encoding="latin-1")
    return df


def clean_text(text):
    '''
    This function makes all characters lowercase, removes all non-alphanumeric characters (\W+), and extra white spaces "\n" using the "re" module. 
    '''
    cleaned_text = re.sub(r'\n|\W+', ' ', text).strip().lower()
    return cleaned_text


def word_embed(keyword):
    '''
    This function uses word embedding to return a list of the most similar words based a the keyword. 
    '''
    model = api.load("glove-wiki-gigaword-50")
    similar_words = []
    for word, _ in model.most_similar(keyword):
        similar_words.append(word)
    return similar_words



def process(artist, keyword):
    df = load_data()
    df['text'] = df['text'].apply(clean_text) # clean the text column
    # find similar words
    keywords = word_embed(keyword)
    # filter based on artist name - make subset of songs 
    artist_df = df[df['artist'] == artist]
    # filter rows where "text" column contains any word from the word embed list
    keyword_df = artist_df[artist_df['text'].str.contains('|'.join(keywords))]
    key_count = len(keyword_df)  
    all_count = len(artist_df)
    percentage = key_count/all_count*100
    print(f"{percentage}% of {artist}'s songs contain words related to: {keyword}")



def print_possible_artists():
    '''
    I want to print the possible artist options to the console, so whoever is running the script, can get an overview of the options.
    This goes through the df and lists all the unique artists. 
    '''
    df = load_data()
    artists = df['artist'].unique().tolist() # extracts the unique artists and convert to list
    print("List of possible artists:")
    for artist in artists:
        print(artist)
    sys.exit()  # exit the script after printing the list of artists


def input():
    '''
    This sets 3 different arguments: artist, keyword and list_artists to display possible options in the artists category.
    If an artist that is not present in the data is passed in the console, it should throw an error, stating that it is not in the list of possible artists.  
    '''
    parser = argparse.ArgumentParser(description="Query expansion with word embeddings")
    parser.add_argument("--list-artists", action="store_true", help="Display the list of possible artists")
    parser.add_argument("--artist", "-a", help="Name of the artist")
    parser.add_argument("--keyword", "-k", help="Keyword to classify")
    args = parser.parse_args()

    if args.list_artists:
        print_possible_artists()
    elif not args.artist or not args.keyword:
        parser.error("the following arguments are required: --artist/-a, --keyword/-k")
    
       # check if the provided artist is in the list of possible artists - if not, it should throw an error
    if args.artist:
        df = load_data()
        if args.artist not in df['artist'].unique():
            parser.error(f"The artist '{args.artist}' is not in the list of possible artists. To list possible artists use: --list-artists")

    return args


def main():
    args = input()
    artist = args.artist
    keyword = args.keyword
    process(artist, keyword)

if __name__ == "__main__":
    main()