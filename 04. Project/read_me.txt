My search engine simply allows a user to search single words and returns a list of the pages that contain those words. The pages are ranked by the frequency that the given word occurs in the page. I chose to do this in python.

Static Data:
	myPath:	This is simply a string containing the path to the html documents that will be crawled for information.
	links:	This is simply a list of the files in the directory specified by myPath
	stopWords: this is a list of stop words which don't contribute to a document's meaning.

Methods:
	retrieveLocalHtml: This method simply opens the html files specified by myPath and links.
	parseText:	This method removes punctuation and non-alphabet characters from a string, breaks the string into individual words, and remove stop words. It returns a list of words.
	createRank:	This method creates and returns a dictionary from a list of words. It uses the words as keys and the frequency that the word appears in the input list as values.
	

Data Structures:
	Node:	I created a node data structure that contains the character or substrnig within a given word, 
		a link to it's parent node, 
		a dictionary containing the children of a given node, 
		a boolean identifier representing whther the node is a prefix or not,
		a boolean identifier representing whther a ndoe is an indexTerm or not, 
		an occurence list represented by a dictionary, 
		and a redundant rank list represented by a dictionary.
		The rank list uses file names as keys and the frequency that the index term appears in the file as values.
		The occurence list uses integers as keys and a list of file names as values. The integer represents the frequency that the index term appears in each the links in the value list. It was implemented this way to make ranking based on frequency easier.

	Trie:	I created a trie data structure that simply contains one attribute, a link to it's root node, who's char is blank.
		I created an addWord method that creates all the nodes necessary to create an index term within the trie, and initiates all the index terms attributes like isIndexTerm, rank, and occurenceList.
		
	SearchEngine:	I created a search engine object that initializes with a trie.
		Methods: 
			crawlPage:	This method crawls a page or an html file and adds all the words in that file to the trie as index terms.
			compressTrie:	This method compresses the trie, making searching more efficient.
			searchWord:	This method searches a word in the compressed trie and returns the occurence list of that index term if it exists, otherwise it returns "None"

Main Function:
	The main function generates the search engine object, 
	crawls the pages in the path directory specified, 
	compresses the search engine's trie, 
	then runs a search loop allowing the user to search for whatever terms they'd like.
		