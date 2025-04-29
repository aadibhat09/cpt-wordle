import requests
import random
import time

# gets a random 5-letter word from the Datamuse API
# returns a string of the lowercase 5-letter word
# this code was co-developed with help from ChatGPT (used for guidance in handling the API response)
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

# generates visual feedback for a guess
# accepts two strings: guess and word
# returns a string of emojis representing the feedback
def generate_feedback(guess, word):
    feedback = []
    for i in range(5):
        if guess[i] == word[i]:
            feedback.append('🟩')
        elif guess[i] in word:
            feedback.append('🟨')
        else:
            feedback.append('🔲')
    return ''.join(feedback)

# starts the game and handles user input
def start_game(word):
    if not word:
        print("Cannot start the game without a word.")
        return

    is_correct = False
    start_time = time.time()
    
    guess_history = []

    # there are 6 attempts maximum
    for _ in range(6):
        guess = input("Enter your 5-letter guess: ").strip().lower()

        # checks if the guess is a 5-letter word
        if len(guess) != 5:
            print("Please enter a 5-letter word.")
            continue
        
        # checks if the guess has already been made
        if guess in guess_history:
            print("You've already guessed that word. Try something else.")
            continue

        guess_history.append(guess)
        
        # checks if the guess is correct and logs time
        if guess == word:
            end_time = time.time()
            elapsed_time = end_time - start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            
            print("Congrats! You solved it in " + str(minutes) + " minutes and " + str(seconds) + " seconds.")
            is_correct = True
            break

        else:
            feedback = generate_feedback(guess, word)
            print(feedback)

    # if all 6 attempts are up and the word is still not guessed
    if not is_correct:
        print("Sorry, you've used all attempts. The word was: " + word)

    # prints the history of guesses
    print("Your guesses were:")
    for g in guess_history:
        print("-", g)

# repeats until the user decides to stop playing
while True:  
    start_game(get_random_5_letter_word())

    if input("Do you want to play again? (y/n): ").strip().lower() not in ['y', 'yes']:
        break