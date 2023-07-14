#Importing predefined modules
import random
import requests



def check(guess,coloring):
    '''
    This function returns the lists of dictionaries correct_position and incorrect_position which contains the correct and incorrect positions of letters in guessed word with respect to the actual word and a list of invalid_words which contains the letters that are not present in the actual word
    '''

    #defines the ANSI codes of colors 
    yellow="\033[0;33m"
    green="\033[0;32m"
    red="\033[0;31m"

    #lists of dictionaries for storing correct and incorrect positions of letters in the guessed word
    correct_postition=[]
    incorrect_position=[]

    #list of letters of guessed words which are not the part of actual word
    invalid_letters=[]

    #iterating over every position of guessed word
    for i in range(5):

        #if letter is present and is in correct position, then append it to correct_position dictionary
        if(coloring[i]==green):
            correct_postition.append({'letter':guess[i],'position':i})

        #if the letter is not in the actual word then add that letter to invalid_letters list
        elif(coloring[i]==red):
            invalid_letters.append(guess[i])
            #If a letter is present in the actual word and the same letter is also in the invalid_letters list, then remove that letter from the invalid_letters list
            for j in range(5):
                if(i!=j and guess[i]==guess[j] and coloring[j] !=red):
                    invalid_letters.remove(guess[i])
                    break

        #if the letter is present in that word but is not in correct position, add a question mark at that position in correct_position dictionary and that position in incorrect_position dictionary
        else:
            correct_postition.append({'letter':guess[i],'position':'?'})
            incorrect_position.append({'letter':guess[i],'position':i})

    #function returns the correct_position, incorrect_positions and list of set of invalid_letters in order to avoid repetitions
    return correct_postition,incorrect_position,list(set(invalid_letters))




# These are the ANSI codes of the colours yellow, green, red
yellow="\033[0;33m"
green="\033[0;32m"
red="\033[0;31m"



def filter(words,correct_position,incorrect_position,invalid_letters):
    '''
    This function filters out the remaining list of words by the use of correct/incorrect position and invalid letters
    '''
    
    # If any word contains any invalid letter which is not present in the actual word, remove that word form the list of remaining words
    for letter in invalid_letters:
        for word in words[:]:
            if letter in word:
                words.remove(word)
    
    for items in correct_position:
        #If any letter is present in the actual word of which the position is not known, then remove all words from the list which does not contain that letter
        if(items['position']=='?'):
            for word in words[:]:
                if items['letter'] not in word:
                    words.remove(word)
        else:
        # If any letter in the actual word is known with its position, then remove words which deos not contain that letter at that position
            for word in words[:]:
                if (items['letter']!=word[items['position']]):
                    words.remove(word)
    #If a letter is present at incorrect position in the actual word then remove all words in which that letter is present at that position      
    for items in incorrect_position:
        for word in words[:]:
            if(items['letter']==word[items['position']]):
                words.remove(word)
    
    #Return the filtered list of remaining words
    return words



def score(cwords):
    '''This is the function to assign some score to all the words in the given list 
    based on the frequency of occourence of the letters in it in the english language'''

    # This dictionary contains the frequency of letters in english language
    letter_value = {'a':8.2, 'b':1.5, 'c':2.8, 'd':4.3, 'e':13, 'f':2.2, 'g':2, 'h':6.1, 'i':7, 'j':0.15, 'k':0.77, 'l':4, 'm':2.4, 'n':6.7, 'o':7.5, 'p':1.9, 'q':0.095, 'r':6, 's':6.3, 't':9.1, 'u':2.8, 'v':0.98, 'w':2.4, 'x':0.15, 'y':2, 'z':0.074}
    
    # This dictionary will be having scores corresponding to the words with score as key and word as the value
    scores={}

    # We assign score by adding the frequency of all the distinctly occouring letters in it
    for word in cwords:
        score=0
        for letter in set(word):
            score+=letter_value[letter]
        if score not in scores.keys():
            scores[score]=[word]
        else:
            scores[score].append(word)
    
    # We make a list scores_keys which will be the list of the keys in the dictionary scores 
    # and then we sort and reverse it
    scores_keys=list(scores.keys())
    scores_keys.sort()
    scores_keys.reverse()

    # Scores_list will be the final list having words in the descendin=g order of score and return it
    scores_list=[]
    for i in scores_keys:
        scores_list+=scores[i]
    return scores_list


# Getting a json of all five letter words by the get request from an API and storing it in a list
response=requests.get('https://random-word-api.herokuapp.com/word', params={"length":5,"number":10000})
words=response.json()
curr_words=list(words)


#Get the list of words that gives the most information and are most frequent to reduce the possibilities to the maximum extent
curr_score=score(curr_words)
#Use any word from this list as the guess
guess=curr_score[0]

#ANSI codes of colors
yellow="\033[0;33m"
green="\033[0;32m"
red="\033[0;31m"

#Six chances to guess the actual word
for chance in range(6):
    print(guess)
    #This will return a list containing the colors at the corresponding position according to the guessed word and the actual word
    coloring=[]
    s=input().lower()
    for i in range(5):
        if s[i]=='r':
            coloring.append(red)
        elif s[i]=='g':
            coloring.append(green)
        else:
            coloring.append(yellow)
    for i in range(5):
        #Print the guessed word with colored characters according with the coloring list
            print(coloring[i],guess[i],end="")
    #Print the ANSI code of white to make the further text white
    print("\033[0;37m")

    #If all the charcters are green then the word is guessed, so break out of the loop as the program is finished
    if red not in coloring and yellow not in coloring:
        break

    # Get the list of dictionaries containing correct position of letters and incorrect position of letters and a list containg the invalid letters that are not present in the actual word
    correct_position,incorrect_position,invalid_letters=check(guess,coloring)

    #Filter out the list of remaining words based on the correct/incorrecct positions of letters in the guesssed word and the invalid letters in the guessed word
    curr_words=filter(curr_words,correct_position,incorrect_position,invalid_letters)

    #Get the list of words that gives the most information and are most frequent to reduce the possibilities to the maximum extent
    curr_score=score(curr_words)

    #This is the previous guess
    prev_guess=guess

    #Now, if there is a case when there are multiple words(<=5) having>=3 green words 
    #then we use a different approach for our next guess
    #for an example, words like water, cater, later, hater etc.
    #if not then, we remain with our initial strategy
    if coloring.count(green)>=3 and 2<len(curr_score)<=5 and coloring.count(red)==5-coloring.count(green):

        #we take a word from words which will have the words in all the guesses that are at red positions
        for i in range(5):
            if coloring[i]==red:
                rem=[curr_score[j][i] for j in range(len(curr_score))]
                for k in words:
                    all_present=1
                    for rem_word in rem:
                        if rem_word not in k:
                            all_present=0
                            break
                    if all_present==1:
                        guess=k
                        break
            if guess!=prev_guess:
                break
        #if there doesn't exist a word having such letters, we go back to our previous strategy
        if guess==prev_guess:
            guess=curr_score[0]
    else:
        guess=curr_score[0]