class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.isEnd = False


class Trie:
    def __init__(self):
        self._root = TrieNode()

    def toIndex(self, ch):
        # Map chars to integer index
        return ord(ch) - ord('a')

    def insert(self, key):
        # Insert key into trie
        # Start at root of trie
        current_node = self._root

        # Traverse characters and add nodes that arent inside
        for char in key.lower():
            index = self.toIndex(char)
            if not current_node.children[index]:
                current_node.children[index] = TrieNode()
            current_node = current_node.children[index]

        # Flip the end flag for leaf of key
        current_node.isEnd = True

    def search(self, key):
        # Search for key in trie
        # Start at the root of the tree
        current_node = self._root

        # Traverse characters
        for char in key.lower():
            index = self.toIndex(char)
            # If node doesnt exist, string cannot be in trie
            if not current_node.children[index]:
                return False
            current_node = current_node.children[index]

        # Check if current node is has end flag and exists
        return current_node != None and current_node.isEnd

    def search_print(self, key):
        print(f'{key} is {"" if self.search(key) else "not "}in trie')


def clean_file(file_name):  # to clean the article - remove digit, punctuations and lowercase all letters
    file1 = open(file_name + ".txt", "r", encoding="utf8")
    cfile1 = file1.readlines()

    file2 = open(file_name + "_clean.txt", "a", encoding="utf8")

    for line in cfile1:
        string = ""
        for char in line:
            if char.isalpha() or char == " ":
                string = string + char
        file2.write(string.lower() + "\n")

    file1.close()


def count_words(file_name):  # to count the num of words in the file
    file = open(file_name + ".txt", "r", encoding="utf8")
    cfile = file.readlines()
    wordcount = 0
    for line in cfile:
        wordlist = line.split()
        wordcount = wordcount + len(wordlist)
    file.close()
    return wordcount


def filter_stop_words(file_name):
    file2 = open(file_name + ".txt", "r", encoding="utf8")
    cfile2 = file2.readlines()
    string = []
    for line in cfile2:
        temp = ' '.join(i for i in line.split() if not stop_trie.search(i)) + " "
        string.append(temp)

    file2 = open(file_name + ".txt", "w", encoding="utf8")
    file2.writelines(string)
    file2.close()


if __name__ == '__main__':
    stop_trie = Trie()

    clean_file("stopwords")
    stop_clean = open("stopwords_clean.txt", "r", encoding="utf8")
    cstop_clean = stop_clean.readlines()

    # to store the stop words into the trie
    for i in cstop_clean:
        keys = i.split()
    for key in keys:
        stop_trie.insert(key)

    stop_clean.close()

    file_list = [["citylink1", "citylink2", "citylink3"], ["DHL1", "DHL2", "DHL3"], ["GDEX1", "GDEX2", "GDEX3"],
                 ["J&T1", "J&T2", "J&T3"], ["poslaju1", "poslaju2", "poslaju3"]]

    # to count the total word count and total stop words of all articles for each courier company to create graph
    total_words_arr = []  # total word count of all articles for each courier company
    total_stop_words_arr = []  # total stop word of all articles for each courier company
    courier_company = ["City-Link Express", "DHL", "GDEX", "J&T", "Pos Laju"]
    for i in file_list:
        total_no_of_words = 0
        total_no_of_stopwords = 0
        for j in i:
            clean_file(j)
            # before removing stop words
            no_of_words = count_words(j + "_clean")
            total_no_of_words = total_no_of_words + no_of_words
            filter_stop_words(j + "_clean")
            # no of stop words
            no_of_stopwords = no_of_words - count_words(j + "_clean")
            total_no_of_stopwords = total_no_of_stopwords + no_of_stopwords

        total_words_arr.append(total_no_of_words)
        total_stop_words_arr.append(total_no_of_stopwords)

    positive_trie = Trie()
    clean_file("positiveWords")
    positive_clean = open("positiveWords_clean.txt", "r", encoding="utf8")
    positiveWords_clean = positive_clean.readlines()

    # to store positive words into the trie
    for i in positiveWords_clean:
        keys = i.split()
    for key in keys:
        positive_trie.insert(key)

    positive_clean.close()

    negative_trie = Trie()
    clean_file("negativeWords")
    negative_clean = open("negativeWords_clean.txt", "r", encoding="utf8")
    negativeWords_clean = negative_clean.readlines()

    # to store negative words into the trie
    for i in negativeWords_clean:
        keys = i.split()

    for key in keys:
        negative_trie.insert(key)

    negative_clean.close()

    total_positive_words_arr = []  # total posititive words of all articles for each courier company
    total_negative_words_arr = []  # total negative words of all articles for each courier company
    total_neutral_words_arr = []  # total neutral words of all articles for each courier company
    for i in file_list:
        total_no_of_positive_words = 0
        total_no_of_negative_words = 0
        total_no_of_neutral_words = 0
        for j in i:
            filename = j + "_clean.txt"
            file = open(filename, "r", encoding="utf8")
            cfile = file.readlines()

            for line in cfile:
                wordlist = line.split()
                for word in wordlist:
                    if positive_trie.search(word):
                        total_no_of_positive_words = total_no_of_positive_words + 1
                    elif negative_trie.search(word):
                        total_no_of_negative_words = total_no_of_negative_words + 1
                    else:
                        total_no_of_neutral_words = total_no_of_neutral_words + 1
            file.close()

        total_positive_words_arr.append(total_no_of_positive_words)
        total_negative_words_arr.append(total_no_of_negative_words)
        total_neutral_words_arr.append(total_no_of_neutral_words)

    print("total word count: ", total_words_arr)
    print("total stop words: ", total_stop_words_arr)
    print("total positive words: ", total_positive_words_arr)
    print("total negative words: ", total_negative_words_arr)
    print("total neutral words: ", total_neutral_words_arr)

