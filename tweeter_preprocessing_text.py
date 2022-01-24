
from nltk.tokenize import word_tokenize
import re
from nltk.stem.isri import ISRIStemmer


# Open Stopwords and special words file
import special_stop_words

# get stop words list
stopwords = special_stop_words.stop_words


# get special words list

special_words_data = special_stop_words.special_words


#to do preprocess for any text it takes some steps
def preprocessing_tweets(dataset):
    # Make Tokenization for this dataset

    tokens = [word_tokenize(tweet) for tweet in dataset['Tweets']]
    
    # remove all words that contain any non alphabitic words 
    p_text = []
    for token in tokens:
        alpha_words = []
        for word in token:
            if word.isalpha():
                alpha_words.append(word)
        p_text.append(alpha_words)
    
    # Cleanning Text from ==>> stopwords , special words , punctuation , diacritics ,
    # nummber , links , duplicates characters , english words , @ , #
    
    pre_text = []
    preprocessed_text = []
    arabic_diacritics = re.compile("""
    
                                 ّ    | # Tashdid
                                 َ    | # Fatha
                                 ً    | # Tanwin Fath
                                 ُ    | # Damma
                                 ٌ    | # Tanwin Damm
                                 ِ    | # Kasra
                                 ٍ    | # Tanwin Kasr
                                 ْ    | # Sukun
                                -      # Tatwil
                             """, re.VERBOSE)
    
    for words in p_text:
        for word in words:
            # remove english words
            word = re.sub(r'([A-Za-z0-9?])', "", word)
            # Diacritics 
            word = re.sub(arabic_diacritics, "", word)
            # Normalize words
            word = re.sub("[إأٱآا]", "ا", word)
            word = re.sub("ؤ", "ء", word)
            word = re.sub("ئ", "ء", word)
            word = re.sub("ة", "ه", word)
            word = re.sub("ى", "ي", word)
            # remove Stop words
            if word in stopwords:
                continue
            # remove duplicate words
            word = re.sub(r'(.)\1+', r'\1', word)
            # remove special arabic words
            if word in special_words_data:
                continue
            
            pre_text.append(word)
        preprocessed_text.append(pre_text)
        pre_text = []
    
    cleaned_stem_list = steming_words(preprocessed_text)
    return cleaned_stem_list
    
    


# Stem with ISRIStemmer
def steming_words(preprocessed_text):

    isri_stem = ISRIStemmer()
    stem_words = ''
    cleaned_stem_list = []
    for cleaned_word in preprocessed_text:
        for stem_word in cleaned_word:
            stem_w = isri_stem.stem(stem_word)
            stem_words += stem_w + ' '
        cleaned_stem_list.append(stem_words)
        stem_words = ''
    return cleaned_stem_list


