import requests
import random
import time

# gets a random 5-letter word from the Datamuse API
# ChatGPT helped me with formatting this function to properly handle the API response
def get_random_5_letter_word():
    try:
        response = requests.get("https://api.datamuse.com/words?sp=?????")
        response.raise_for_status()
        
        word_objects = response.json()
        words = [obj['word'] for obj in word_objects if 'word' in obj]
        
        if not words:
            print("No 5-letter words found in the API response.")
            return None
        
        return random.choice(words)
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except ValueError:
        print("Failed to parse JSON from the API response.")
        return None

# starts the game and handles user input
def start_game(word):
    
    is_correct = False
    start_time = time.time()
    
    # there are 6 guesses
    for _ in range(6):
        
        guess = input().strip().lower()
        
        # ensure the word has 5 letters
        if len(guess) != 5:
            
            print("Please enter a 5-letter word.")
            continue
        
        # check if the word is the correct word
        elif guess == word:
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            
            print("Congrats! You solved it in " + str(minutes) + " minutes and " + str(seconds) + " seconds.")
            is_correct = True
            return
        
        # give feedback on the guess
        else:
            
            feedback = []
            for i in range(5):
                if guess[i] == word[i]:
                    feedback.append('🟩')
                elif guess[i] in word:
                    feedback.append('🟨')
                else:
                    feedback.append('🔲')
            print(''.join(feedback))
    
    # if after all attempts the word is not guessed
    if not is_correct:

        print("Sorry, you've used all attempts. The word was: " + word)

# repeats until the user decides to stop playing
while True:  
    start_game(get_random_5_letter_word())
    
    if input("Do you want to play again? (y/n): ").strip().lower() not in ['y', 'yes']:
        break