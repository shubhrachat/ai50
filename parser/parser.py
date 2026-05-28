import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> N V
S -> NP VP | NP VP Conj NP VP | NP VP Conj VP
NP -> N | Det N | P NP | Det Adj | Adj NP | Adv NP | Conj NP | Adv
NP -> Conj NP | Conj S | P S | NP NP
VP -> V | Adv VP | V Adv | VP NP | V NP Adv
AP -> Adj NP | Adj AD
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # obtaining all the tokens in the given sentence
    tokens = nltk.word_tokenize(sentence)

    # Your function should return a list of words, where each word is a lowercased string.
    # this is the current empty list of words
    words = []

    # for every character in sentence - words, characters etc.
    for ch in tokens:

        # Checking for at least one alphabetic character
        # setting condition to False as of now
        flag = 0

        # checking each character under each token
        for letter in ch:

            # checking for alphabetic literal
            if letter.isalpha():
                # if present
                # change condition to True
                # append to list of valid words
                flag = 1

            # else excluded from list

        if flag == 1:
            # adding valid character
            words.append(ch)

        # scanning all relevant words and converting to lowercase
        for i in range(0, len(words)):
            # Pre-process sentence by converting all characters to lowercase
            words[i] = words[i].lower()

    # returning list of valid words
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    # return a list of all noun phrase chunks in the sentence tree which itself does not conatin noun phrases
    return tree.subtrees(

        # for every tree in original tree
        # checking label
        #  A noun phrase chunk is defined as any subtree of the sentence whose label is "NP"
        lambda original_tree: original_tree.label() == "NP"
        and not list(
            # checking whether secondary trees under original trees contains any other noun phrases
            # checking whether original tree itself consists of noun phrases
            original_tree.subtrees(
                # if it does contain NP
                # it is not added ot the list to be returned
                lambda secondary_tree: original_tree != secondary_tree and secondary_tree.label() == "NP"
            )
        )
        # else added to list
    )


if __name__ == "__main__":
    main()
