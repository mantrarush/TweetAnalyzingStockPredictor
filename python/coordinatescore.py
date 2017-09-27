__author__ = 'Amrutha'


import sys
import json
import csv

tweet_list=[]
tweet_text=[]
dict_data = {}
state_dict ={}
tweet_dict_coordinate = {}
coordinate_score_dict = {}

def make_dict (afinn_fp):

    afinn_data = open (afinn_fp)
    word_count = 0

    for line in afinn_data:
        term, score = line.split("\t")
        dict_data[term]=int(score)
        word_count = word_count + 1


def parse_tweet (tweet_fp):

    json_data = open(str(tweet_fp))
    tweet_count = 0
    pop_tweet_count = 0
    tweet_txt_num =0

    # CONVERT STREAM FILE TO DICTIONARY
    for line in json_data:
        data =json.loads(line)
        tweet_list.append(data)
        tweet_count = tweet_count + 1
    print ">>>>> Total Twitter = %i" %tweet_count + " <<<<<"

    # FILTER OUT TWEET MSG -> CONSTRUCT A FULL TWEET LIST AND US TWEET LIST
    for i in range(0, tweet_count):

        if str(tweet_list[i].keys()) != "[u'delete']" and tweet_list[i]['lang']=="en":  #get rid of Delete msg and non-English tweet

            #EXTRACT ONLY TWEET MSG PART AND MAKE A LIST OF TWEETS MSG
            x = tweet_list[i]["text"].encode("ascii", 'ignore') #error handling for ascii encoding for special char.
            tweet_text.append(x)
            tweet_txt_num = tweet_txt_num +1

            #CHECK TWEET LOCATION AND MAKE A LIST FOR US TWEETS, 3 WAYS TO CHECK
            if tweet_list[i]['coordinates'] != None:

                coordinate = tweet_list[i]["coordinates"]["coordinates"]  # EXTRACT COORDINATE THAT IS A LIST

                coordinate_str = str(coordinate).strip('[]') #FORMAT COORDINATE TO STRING AND REMOVE []

                tweet_msg = tweet_list[i]['text'].encode("ascii", 'ignore')
                tweet_msg =tweet_msg.lower()
                tweet_msg =tweet_msg.replace('\n', ' ')

                if tweet_msg != None:
                    tweet_dict_coordinate[tweet_msg] = coordinate_str
                    pop_tweet_count = pop_tweet_count + 1

    print ">>>>> total tweets with populated text and coordinate = %i" %pop_tweet_count + " <<<<<"


def tweet_sentiment_chk(tweet_msg, dict_data):

        tweet_word = []
        tweet_score = []

        #extract words from each tweet
        tweet_word = tweet_msg.split(" ")

        #sum sentiment score for the tweet
        for n in range (0 , len(tweet_word)):
            tweet_word[n] = tweet_word[n].strip ('!@#$%^&*(),./<>?;\':\""[]\{}|\'')
            score = dict_data.get(str(tweet_word[n]))
            if score == None:         #for words not in the word bank
                score = 0
            tweet_score.append(score) #constract a score list for this tweet

        total_score = 0

        for n1 in range(0, len( tweet_score)):
            total_score = total_score + tweet_score[n1]

        return total_score


def update_coordinate_score (score, coordinate):

    coordinate_score_dict[coordinate] = score



def sentiment_chk_coordinate (tweet_dict_coordinate):

    for tweet_msg, coordinate in tweet_dict_coordinate.iteritems():

        score = tweet_sentiment_chk(tweet_msg, dict_data)
        update_coordinate_score (score, coordinate)




def main():

    make_dict(sys.argv[1])
    parse_tweet(sys.argv[2])

    #sentiment_chk(tweet_text, dict_data)

    sentiment_chk_coordinate(tweet_dict_coordinate)


    #OUTPUT STATE_SCORE DICTS TO CSV file
    writer = csv.writer (open('coordinate_score.csv', 'wb'))
    for key, value in coordinate_score_dict.items():
        lon_lat = key.split(',')
        lon = lon_lat[0]
        lat = lon_lat[1]
        writer.writerow([lon, lat, value])
    print (">>>>> CSV Export Completed <<<<<")




if __name__ == '__main__':
    main()
