import typing

GAMEWORD_LIST_FNAME = "gamewords.txt"

def filter_word(word: str, length: int) -> str:
    if len(word.strip()) == length:
        return word.strip().upper()
    return None

def create_wordlist(fname: str, length: int) -> typing.List[str]:
    with open(fname, "r") as f:
        lines = f.readlines()
    return list(map(lambda word: filter_word(word, length), lines))

def validate(guess: str, wordlen: int, wordlist: typing.Set[str]) -> typing.Tuple[str, str]:
    guess_upper = guess.upper()
    if len(guess_upper) != wordlen:
        return f"Guess must be of length {wordlen}", guess_upper
    if guess_upper not in wordlist:
        return f"Unknown word", guess_upper
    return None, guess_upper

def get_user_guess(wordlen: int, wordlist: typing.Set[str]) -> str:
    while True:
        guess = input("Guess: ")
        error, guess = validate(guess=guess, wordlen=wordlen,
                                wordlist=wordlist)
        if error is None:
            break
        print(error)
    return guess

def find_all_char_positions(word: str, char: str) -> typing.List[int]:
    positions = []
    pos = word.find(char)
    while pos != -1:
        positions.append(pos)
        pos = word.find(char, pos + 1)
    return positions

def compare(expected: str, guess: str) -> typing.List[str]:
    output = ["_"] * len(expected)
    counted_pos = set()
    for index, (expected_char, guess_char) in enumerate(zip(expected, guess)):
        if expected_char == guess_char:
            output[index] = "X"
            counted_pos.add(index)

    for index, guess_char in enumerate(guess):
        if guess_char in expected and \
                output[index] != "X":
            positions = find_all_char_positions(word=expected, char=guess_char)
            for pos in positions:
                if pos not in counted_pos:
                    output[index] = "?"
                    counted_pos.add(pos)
                    break

    if(expected == ""):
        output = ["_"] * 5

    return output

if __name__ == '__main__':
    WORDLEN = 5
    GAMEWORD_WORDLIST = create_wordlist(
        GAMEWORD_LIST_FNAME, length=WORDLEN)
    
    GUESSWORD_WORDLIST = set(create_wordlist(
        GAMEWORD_LIST_FNAME, length=WORDLEN))

    GAME_WORD_LENGTH = 5
    NUM_GUESSES = 0

    print("""

██╗░░██╗░█████╗░░█████╗░██╗░░██╗  ░██╗░░░░░░░██╗░█████╗░██████╗░██████╗░██╗░░░░░███████╗
██║░░██║██╔══██╗██╔══██╗╚██╗██╔╝  ░██║░░██╗░░██║██╔══██╗██╔══██╗██╔══██╗██║░░░░░██╔════╝
███████║██║░░██║███████║░╚███╔╝░  ░╚██╗████╗██╔╝██║░░██║██████╔╝██║░░██║██║░░░░░█████╗░░
██╔══██║██║░░██║██╔══██║░██╔██╗░  ░░████╔═████║░██║░░██║██╔══██╗██║░░██║██║░░░░░██╔══╝░░
██║░░██║╚█████╔╝██║░░██║██╔╝╚██╗  ░░╚██╔╝░╚██╔╝░╚█████╔╝██║░░██║██████╔╝███████╗███████╗
╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝  ░░░╚═╝░░░╚═╝░░░╚════╝░╚═╝░░╚═╝╚═════╝░╚══════╝╚══════╝

You have to guess the Word in six tries or less

‘X’ means Hit (letter is in the target word, and correct position)
‘?’ means Near hit (letter is in the target word, but not in correct position)
‘_’ means Miss (letter is not in the target word).

To quit, press CTRL-C.
""")

    # start of the user name interaction
    print("_ " * GAME_WORD_LENGTH)

    try:
        while True:
            # set word to "" until a word can be generated
            WORD=""
            GUESS = get_user_guess(
                wordlen=GAME_WORD_LENGTH, wordlist=GAMEWORD_WORDLIST)
            NUM_GUESSES += 1

            # Trying to remove letters from the list to then generate a final word to guess
            letters = (list(GUESS))

            # This checks the first pair of the word  
            result = compare(expected=WORD, guess=GUESS)

            if (result.count("X") == 0 and result.count("?") == 0 and len(GUESSWORD_WORDLIST)>2):
                GUESSWORD_WORDLIST = [ele for ele in GUESSWORD_WORDLIST if all(ch not in ele for ch in letters)]

            wordlist = []
            
            for i in GUESSWORD_WORDLIST:
                wordlist1 = []
                resultX = compare(expected=i,guess=GUESS)
                hit = resultX.count("X")
                nearhit = resultX.count("?")
                wordlist1.append(i)
                wordlist1.append(hit)
                wordlist1.append(nearhit)
                wordlist.append(wordlist1)

            sorted_data = sorted(wordlist, key=lambda x: (-x[2],-x[1]))
            WORD = sorted_data[0][0]
            for j in range(len(sorted_data)):
                if(sorted_data[j][1] == 5):
                    WORD = sorted_data[j][0]
            print(sorted_data)
                
            result = compare(expected=WORD, guess=GUESS)
            print(" ".join(result))

            if WORD == GUESS:
                print(f"{WORD.upper()} in {NUM_GUESSES} rounds.")
                break
            elif NUM_GUESSES == 6:
                print(f"the correct answer was {WORD.upper()}.")
                break

    except KeyboardInterrupt:
        print(f"""
You quit
""")