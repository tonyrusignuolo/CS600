from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from os import listdir
from os.path import isfile, join

myPath  = r"C:\Users\Tony the Potato\Google Drive\My Drive\3. Academics\1. Stevens\2. Masters (Computer Science)\1. Courses\'18 S3\CS600WS (Advanced Algorithms)\4. Project\html"
# list of web pages to crawl
links = [f for f in listdir(myPath) if isfile(join(myPath, f))]
links.remove('desktop.ini')

stopWords = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

def retrieveHtml(link: str):
    """Opens a local html file and returns it as text."""
    html = open(join(myPath, link), 'r', encoding = 'utf-8').read()
    return html

def parseText(text: str):
    """Breaks long strings of text into a list of individual words. Returns a list of the words"""
    words = re.sub("[^\w]", " ", text.lower()).split()
    words = [word for word in words if word not in stopWords]
    return words

def createRank(wordList):
    """Creates a dictionary from a list of words with the words as keys and 
    the frequency that those words appear in the list as values. Returns the dictionary."""
    dictionary = {}
    for word in wordList:
        try:
            dictionary[word] += 1
        except:
            dictionary[word] = 1
    return dictionary

class Node(object):
    def __init__(self, char: str):
        """Creates a node object in a trie."""
        """char is the character of the word"""
        self.char = char
        """Parent links back to the parent node making tree traversal significantly easier."""
        self.parent = None
        """children is a dictionary with links
        to other nodes representing the characters
        that follow in a given word"""
        self.children = {}
        """isPrefix represents whether a node is
        the prefix of another word."""
        self.isPrefix = False
        """isIndexTerm represents whether a node is
        the last character of a word."""
        self.isIndexTerm = False
        self.counter = 1
        """occurenceList is a dictionary with
        integers as keys and a list of file link 
        strings as values. The integers represent
        the frequency that the index term occurs
        in all the links in the list. A node only
        has an occurenceList if it is an index
        term"""
        self.occurenceList = None
        """rank is a dictionary with file link 
        strings as keys and integers representing
        the frequency the index term appears in
        the link as the value. It can simply be
        thought of as the opposite of an
        occurenceList."""
        self.rank = None

    def __str__(self):
        """Returs a string output for a node."""
        return """Node:\tchar: "%s",
\tchildren: %s
\tisPrefix: %s
\tisIndexTerm: %s
\tcounter: %s
\toccureneceList: %s
\trank: %s""" % (self.char, self.children, self.isPrefix, self.isIndexTerm, self.counter, self.occurenceList, self.rank)
        

class Trie(object):
    def __init__(self):
        """Creates a Trie object consisting of nodes."""
        self.root = Node(" ")

    def addWord(self, word: str, link: str, rank: int):
        """Adds a word to the trie by creating nodes
        with the word's characters."""
        # print(link)
        node = self.root
        for char in word:
            # iterate through characters in the word
            try:
                # if the character already exists as a node traverse the tree to that node
                child = node.children[char]
                child.counter += 1
                node = child
            except:
                # if that character doesn't exist as a node create a new node with the appropriate links and traverse to it to finish the word
                newNode = Node(char)
                newNode.parent = node
                node.children[char] = newNode
                node = newNode
        # set the node to an index terms
        node.isIndexTerm = True
        if node.children:
            # if the node has children, that means it is a prefix
            node.isPrefix = True
        """Everything below is very complicated. Basically it creates and updates the rank and occurenceList for each node."""
        if node.rank:
            try:
                linkRankOld = node.rank[link]
                if linkRankOld != rank:
                    if node.occurenceList:
                        try:
                            linkList = node.occurenceList[linkRankOld]
                            if link in linkList:
                                linkList.remove(link)
                                linkList = node.occurenceList[rank]
                                if link not in linkList:
                                    linkList.append(link)
                        except:
                            node.occurenceList[rank] = [link]
                    else:
                        node.occurenceList = {rank: [link]}
            except:
                node.rank[link] = rank
                if node.occurenceList:
                    try:
                        linkList = node.occurenceList[rank]
                        if link not in linkList:
                            linkList.append(link)
                    except:
                        node.occurenceList[rank] = [link]
        else:
            node.rank = {link: rank}
            if node.occurenceList:
                try:
                    linkList = node.occurenceList[rank]
                    if link not in linkList:
                        linkList.append(link)
                except:
                    node.occurenceList[rank] = [link]
            else:
                node.occurenceList = {rank: [link]}

    # def isPrefix(self, word: str):

    #     if not self.root.children:
    #         return False, 0
    #     node = self.root
    #     for char in word:
    #         foundInChildren = False
    #         try:
    #             child = node.children[char]
    #             foundInChildren = True
    #             node = child
    #             break
    #         except:
    #             if not foundInChildren:
    #                 return False, 0
    #     return True, node.counter


class SearchEngine(object):
    def __init__(self):
        """Creates a SearchEngine object."""
        self.trie = Trie()
        self.compressedTrie = Trie()

    def crawlPage(self, trie: Trie, link: str):
        """Crawls an html document for text to add to the search engine."""
        pageHtml = retrieveHtml(link)
        pageSoup = BeautifulSoup(pageHtml, 'html.parser')
        pageText = pageSoup.get_text()
        pageWords = parseText(pageText)
        pageRank = createRank(pageWords)
        for word, rank in pageRank.items():
            trie.addWord(word, link, rank)

    def compressTrie(self):
        """Compresses the trie to make search more efficient."""
        node = self.compressedTrie.root
        def compressTrieHelper(node):
            children = list(node.children.values())
            if len(children) == 1 and node.isPrefix == 0:
                # Node is compressable, compress node
                child = children[0]
                child.parent = None
                del node.parent.children[node.char]
                node.char += child.char
                node.parent.children[node.char] = node
                node.children = child.children
                node.isPrefix = child.isPrefix
                node.isIndexTerm = child.isIndexTerm
                node.occurenceList = child.occurenceList
                node.rank = child.rank
                compressTrieHelper(node)
            elif len(children) > 1:
                # node is not compressable, recursively traverse to children
                for child in children:
                    compressTrieHelper(child)
        for child in list(node.children.values()):
            # iterate through children, so root node isn't compressed
            compressTrieHelper(child)

    def searchWord(self, word: str):
        """Searches a given word in the the SearchEngine's compressedTrie."""
        root = self.compressedTrie.root
        def searchWordHelper(node: Node, string: str):
            children = list(node.children.items())
            for child in children:
                if child[0] == string and child[1].isIndexTerm == 1:
                    return child[1].occurenceList
                elif string.find(child[0]) == 0:
                    return searchWordHelper(child[1], string.replace(child[0], "", 1))
            return None
        return searchWordHelper(root, word)
    
if __name__ == "__main__":
    # print(links)
    SE = SearchEngine()
    # generates a search engine
    for link in links:
        # crawls all available pages for the search engine
        # SE.crawlPage(SE.trie, link)
        SE.crawlPage(SE.compressedTrie, link)
    SE.compressTrie()
    # compresses the trie for more efficient searching.
    print("\n")
    print("Welcome to Tony's CS600 PySearch!\n")
    x = True
    while x:
        # main loop allowing a user to search single word input terms
        search = re.sub("[^\w]", "", input("search >>> ").lower())        
        if search == "q":
            x = False
        else:
            results = SE.searchWord(search)
            if results:
                results = sorted(list(results.items()), key = lambda tup: tup[0], reverse = True)
                for tup in results:
                    for result in tup[1]:
                        print(result)
                print("\n")
            else:
                print("None\n")
    print("Thanks for searching!")