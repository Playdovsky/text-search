import string
import random
import matplotlib.pyplot as plt

# Calls for chart functions
def menu():
    try:
        print("What do you want to do?\n1. Plot a text length against comparisons chart\n2. Plot a pattern length against comparisons chart\n3. Plot an alphabet length against comparisons chart\n4. Plot all charts\n5. Exit\n")
        option = int(input())
        pattern_len, text_len = get_lengths()
        alphabet_len = get_alphabet()

        match option:
            case 1:
                alphabet = string.ascii_lowercase[:alphabet_len]
                chart_text_comparisons(alphabet, pattern_len, text_len)
            case 2:
                alphabet = string.ascii_lowercase[:alphabet_len]
                chart_pattern_comparisons(alphabet, pattern_len, text_len)
            case 3:
                chart_alphabet_comparisons(alphabet_len, pattern_len, text_len)
            case 4:
                alphabet = string.ascii_lowercase[:alphabet_len]
                chart_text_comparisons(alphabet, pattern_len, text_len)
                chart_pattern_comparisons(alphabet, pattern_len, text_len)
                chart_alphabet_comparisons(alphabet_len, pattern_len, text_len)
            case 5:
                exit()
            case _:
                print("Something went wrong, please try again")
                
    except ValueError:
        print("\nLength should be a numeric value! Try again\n")


def get_lengths():
    try:
        # Get lengths of pattern |W| and text |T|
        print("How long should be the pattern |W|?")
        pattern_len = int(input())
        print("How long should be the text |T|?")
        text_len = int(input())
    
        if pattern_len > text_len: raise Exception("\nPattern shouldn't be longer than text itself! Try again\n")
        
        return pattern_len, text_len
    except ValueError:
        print("\nLength should be a numeric value! Try again\n")
        menu()

def get_alphabet():
    try:
        # Get desired alphabet |A| length
        print("How big should be the alphabet |A|?")
        alphabet_len = int(input())
        
        # Alphabet length can't be longer than alphabet itself (26 characters)
        if alphabet_len > len(list(string.ascii_lowercase)): raise Exception("\nWhole alphabet is smaller than the provided length! Try again\n")
        
        return alphabet_len
    except ValueError:
        print("\nLength should be a numeric value! Try again\n")
        menu()
    
# Calculates information for X = |T|, Y = Comparisons
def chart_text_comparisons(alphabet, pattern_len, text_len):
        i = 0
        pattern = ""
        
        while i < pattern_len:
            pattern += random.choice(alphabet)
            i += 1

        i = 0
        text = ""
        text_lengths = []
        comparisons_list = []
        
        while i < text_len:
            text += random.choice(alphabet)
            # With each iteration, naive_search function tries to find pattern |W| in the slowly growing text |T|
            # Text |T| grows with each iteration
            found_patterns, comparisons = naive_search(pattern, text)
            text_lengths.append(len(text))
            comparisons_list.append(comparisons)
            
            i += 1
        
        #print("\nNaive search found: " + str(found_patterns) + " matching patterns in the text with " + str(comparisons) + " comparisons\n")
        draw_chart(text_lengths, comparisons_list, chart_title = "Text length against comparisons", x_title = "Text length")

# Calculates information for X = |W|, Y = Comparisons
def chart_pattern_comparisons(alphabet, pattern_len, text_len):
    i = 0
    text = ""
    
    while i < text_len:
        text += random.choice(alphabet)
        i += 1
    
    i = 0
    pattern = ""
    pattern_lengths = []
    comparisons_list = []
    
    while i < pattern_len:
        pattern += random.choice(alphabet)
        # With each iteration, naive_search function tries to find pattern |W| in text |T| while also slowly increasing the length of pattern
        # Pattern |W| grows with each iteration
        found_patterns, comparisons = naive_search(pattern, text)
        pattern_lengths.append(len(pattern))
        comparisons_list.append(comparisons)
        i += 1

    draw_chart(pattern_lengths, comparisons_list, chart_title = "Pattern length against comparisons", x_title = "Pattern length")
    
# Calculates information for X = |A|, Y = Comparisons
def chart_alphabet_comparisons(alphabet_len, pattern_len, text_len):
    i = 1
    alphabet = ""
    alphabet_lengths = []
    comparisons_list = []
    while i <= alphabet_len:
        alphabet = string.ascii_lowercase[:i]
        i += 1
        
        n = 0
        text = ""
        while n < text_len:
            text += random.choice(alphabet)
            n += 1
        
        m = 0
        pattern = ""
        while m < pattern_len:
            pattern += random.choice(alphabet)
            m += 1
        
        # With each iteration, naive_search function tries to find pattern |W| in text |T|
        # Alphabet |A| grows with each iteration which requires new text |T| and pattern |W| generation with each cycle
        found_patterns, comparisons = naive_search(pattern, text)
        alphabet_lengths.append(len(alphabet))
        comparisons_list.append(comparisons)
    
    draw_chart(alphabet_lengths, comparisons_list, chart_title = "Alphabet length against comparisons", x_title = "Alphabet length")
    
# Starts the naive search algorithm
# Returns number of found patterns |W| in provided text |T|
# Returns number of comparisons made during execution of an algorithm
def naive_search(pattern, text):
    comparisons = 0
    found_patterns = 0
    
    # In the range of text |T|, search for the pattern |W| comparing letter after letter
    # len(text) - len(pattern) prevents "out of index" exception, + 1 skips index 0
    for n in range(len(text) - len(pattern) + 1):
        match = True
        
        # In the length of pattern |W| compare letters. Add 1 for each comparison iteration
        for m in range(len(pattern)):
            comparisons += 1
            
            # Comparison between value at the text |T| index and value at the patterns |W| respective position
            if text[n + m] != pattern[m]:
                match = False
                break
        
        # If match was True after whole pattern |W| check, increase number of found patterns |W| in the text |T|
        if match:
            found_patterns += 1
    
    return found_patterns, comparisons

# Draws chart based on provided information during calls
def draw_chart(x, y, chart_title, x_title):
    plt.plot(x, y)
    plt.title(chart_title)
    plt.xlabel(x_title)
    plt.ylabel("Comparisons")
    plt.grid(True)
    plt.show()

# Starts the program
menu()