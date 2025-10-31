import string
import random
import matplotlib.pyplot as plt

comparisons = 0

# User menu. Calls for selected chart functions
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

# Gets lengths of pattern |W| and text |T| from user input
def get_lengths():
    try:
        print("How long should be the pattern |W|?")
        pattern_len = int(input())
        print("How long should be the text |T|?")
        text_len = int(input())
    
        if pattern_len > text_len: raise Exception("\nPattern shouldn't be longer than text itself! Try again\n")
        
        return pattern_len, text_len
    except ValueError:
        print("\nLength should be a numeric value! Try again\n")
        menu()

# Gets alphabet |A| length from user input 
def get_alphabet():
    try:
        print("How big should be the alphabet |A|?")
        alphabet_len = int(input())
        
        if alphabet_len > len(list(string.ascii_lowercase)): raise Exception("\nWhole alphabet is smaller than the provided length! Try again\n")
        
        return alphabet_len
    except ValueError:
        print("\nLength should be a numeric value! Try again\n")
        menu()
    
# Calculates information for X = |T|, Y = Comparisons
def chart_text_comparisons(alphabet, pattern_len, text_len):
        global comparisons
        i = 0
        pattern = ""
        
        while i < pattern_len:
            pattern += random.choice(alphabet)
            i += 1

        i = 0
        text = ""
        text_lengths_naive = []
        comparisons_naive = []
        text_lengths_sunday = []
        comparisons_sunday = []
        text_lengths_karp_rabin = []
        comparisons_karp_rabin = []
        
        # Loop execution of algorithms for growing text |T|
        while i < text_len:
            text += random.choice(alphabet)
            # Naive search
            found_patterns = naive_search(pattern, text)
            text_lengths_naive.append(len(text))
            comparisons_naive.append(comparisons)
            comparisons = 0
            # Sunday search
            found_patterns = sunday_search(pattern, text)
            text_lengths_sunday.append(len(text))
            comparisons_sunday.append(comparisons)
            comparisons = 0
            # Karp-Rabin search
            found_patterns = karp_rabin_search(pattern, text, alphabet)
            text_lengths_karp_rabin.append(len(text))
            comparisons_karp_rabin.append(comparisons)
            comparisons = 0
            i += 1
        
        draw_chart(text_lengths_naive, comparisons_naive, text_lengths_sunday, comparisons_sunday, text_lengths_karp_rabin, comparisons_karp_rabin, chart_title = "Text length against comparisons", x_title = "Text length")

# Calculates information for X = |W|, Y = Comparisons
def chart_pattern_comparisons(alphabet, pattern_len, text_len):
    global comparisons
    i = 0
    text = ""
    
    while i < text_len:
        text += random.choice(alphabet)
        i += 1
    
    i = 0
    pattern = ""
    pattern_lengths_naive = []
    comparisons_naive = []
    pattern_lengths_sunday = []
    comparisons_sunday = []
    
    # Loop execution of algorithms for growing pattern |W|
    while i < pattern_len:
        pattern += random.choice(alphabet)
        # Naive search
        found_patterns = naive_search(pattern, text)
        pattern_lengths_naive.append(len(pattern))
        comparisons_naive.append(comparisons)
        comparisons = 0
        # Sunday search
        found_patterns = sunday_search(pattern, text)
        pattern_lengths_sunday.append(len(pattern))
        comparisons_sunday.append(comparisons)
        comparisons = 0
        i += 1

    draw_chart(pattern_lengths_naive, comparisons_naive, pattern_lengths_sunday, comparisons_sunday, chart_title = "Pattern length against comparisons", x_title = "Pattern length")
    
# Calculates information for X = |A|, Y = Comparisons
def chart_alphabet_comparisons(alphabet_len, pattern_len, text_len):
    global comparisons
    i = 1
    alphabet = ""
    alphabet_lengths = []
    comparisons_naive = []
    comparisons_sunday = []
    
    # Loop execution of algorithms for growing alphabet |A|
    # Each new loop / alphabet letter requires new text |T| and pattern |W| to be made 
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

        # Naive search
        found_patterns = naive_search(pattern, text)
        alphabet_lengths.append(len(alphabet))
        comparisons_naive.append(comparisons)
        comparisons = 0
        # Sunday search
        found_patterns = sunday_search(pattern, text)
        comparisons_sunday.append(comparisons)
        comparisons = 0
    
    draw_chart(alphabet_lengths, comparisons_naive, alphabet_lengths, comparisons_sunday, chart_title = "Alphabet length against comparisons", x_title = "Alphabet length")

# Checks if letter from text |T| matches corresponding pattern |W| letter
def matches_at(pattern, text, p):
    global comparisons
    i = 0
    while i < len(pattern):
        comparisons += 1
        if pattern[i] != text[p+i]:
            return False
        i += 1
    
    return True

# Naive search algorithm. Compares each letter from text |T| to pattern |W|
def naive_search(pattern, text):
    global comparisons
    found_patterns = 0
    p = 0
    
    while p <= len(text) - len(pattern):
        if matches_at(pattern, text, p):
            found_patterns += 1
        comparisons += 1
        p += 1

# Sunday search algorithm. Skips chunks of text |T| by checking neighbouring letter
def sunday_search(pattern, text):
    global comparisons
    found_patterns = 0
    p = 0
    i = 0
    pattern_len = len(pattern)
    text_len = len(text)
    
    lastp = {}
    while i <= pattern_len - 1:
        lastp.update({pattern[i]:i})
        i += 1
    
    
    while p <= text_len - pattern_len:
        if matches_at(pattern, text, p):
            found_patterns += 1
        
        p += pattern_len
        
        if p < text_len:
            p -= lastp.get(text[p], -1)

# Hashes given string to a number in accordance to alphabet order
def hash_string(pre_hash, alphabet):
    i = len(pre_hash) - 1
    post_hash = 0
    
    while i >= 0:
        post_hash += (alphabet.index(pre_hash[i]) + 1) * (len(alphabet)**i)
        i -= 1
    
    return post_hash

# Karp-Rabin search calculates hashes, then compares them with text |T| window hashes
def karp_rabin_search(pattern, text, alphabet):
    global comparisons
    found_patterns = 0
    p = 0
    pattern_len = len(pattern)
    text_len = len(text)
    alphabet_len =  len(alphabet)
    
    pattern_hash = hash_string(pattern, alphabet)
    text_hash = hash_string(text[0:pattern_len], alphabet)
    highest_power = alphabet_len ** (pattern_len - 1)
    
    while p <= text_len  - pattern_len:
        if (pattern_hash == text_hash):
            if (matches_at(pattern, text, p)):
                found_patterns += 1
        
        if p < text_len - pattern_len:
            left_char_value = (alphabet.index(text[p]) + 1) * highest_power
            right_char_value = (alphabet.index(text[p + pattern_len]) + 1)
            text_hash = (text_hash - left_char_value) * alphabet_len + right_char_value
        
        p += 1
        comparisons += 1
        
# Draws chart based on provided information during calls
def draw_chart(x1, y1, x2, y2, x3, y3, chart_title, x_title):
    plt.plot(x1, y1, label="naive")
    plt.plot(x2, y2, label="sunday")
    plt.plot(x3, y3, 'y', label="karp-rabin")
    plt.title(chart_title)
    plt.xlabel(x_title)
    plt.ylabel("Comparisons")
    plt.grid(True)
    plt.legend()
    plt.show()

# Starts the program
menu()