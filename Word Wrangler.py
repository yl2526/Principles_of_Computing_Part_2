"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_list = list(list1)
    for poi in xrange(len(new_list)):
        try:
            while new_list[poi] == new_list[poi+1]:
                del new_list[poi+1]
        except IndexError:
            return new_list
    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    clist1 = list(list1)
    clist2 = list(list2)
    new_list = []
    while clist1 and clist2:
        if clist1[0] < clist2[0]:
            del clist1[0]
        elif clist1[0] > clist2[0]:
            del clist2[0]
        else:
            del clist1[0]
            new_list.append(clist2.pop(0))
    return new_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    clist1 = list(list1)
    clist2 = list(list2)
    new_list = []
    while clist1 or clist2:
        if clist1 and clist2:
            if clist1[0] < clist2[0]:
                new_list.append(clist1.pop(0))
            elif clist1[0] > clist2[0]:
                new_list.append(clist2.pop(0))
            else:
                new_list.append(clist1.pop(0))
                new_list.append(clist2.pop(0))
        elif clist1 and not clist2:
            while clist1:
                new_list.append(clist1.pop(0))
        elif not clist1 and clist2:
            while clist2:
                new_list.append(clist2.pop(0))
    return new_list
                                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    #base case
    if len(list1) == 1:
        return list1
    elif len(list1) == 0:
        return []
    # induction case
    else:
        mid = len(list1)//2
        left = list1[:mid]
        right = list1[mid:]
        return merge(merge_sort(left), merge_sort(right))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    #base case
    if len(word)==0:
        return [""]
    # induction case
    else:
        first = word[0]
        rest = word[1:]
        add = lambda letter, word: [word[:poi] + letter + word[poi:] for poi in xrange(len(word)+1)]
        rest_all_word = gen_all_strings(rest)
        word_for_first = []
        for word in rest_all_word:
            word_for_first += add(first, word) 
        return rest_all_word + word_for_first

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(WORDFILE )
    netfile = urllib2.urlopen(url)
    string_list = []
    for word in netfile.readlines():
        string_list.append(word)
    return string_list

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()


import poc_simpletest

function_to_test = [remove_duplicates, intersect
                   ,merge, merge_sort
                   ,gen_all_strings]

def run_suite(function):
    """
    test the functions
    """
    suite = poc_simpletest.TestSuite()
    print function[0]
    suite.run_test(function[0]([]), [])
    suite.run_test(function[0]([1,2,2,3]), [1,2,3])
    suite.run_test(function[0]([1,2,3,2]), [1,2,3,2])
    suite.report_results()
    
    suite = poc_simpletest.TestSuite()
    print function[1]
    suite.run_test(function[1]([], [1,2,3]), [])
    suite.run_test(function[1]([1,2,3], []), [])
    suite.run_test(function[1]([1], [1,2,3]), [1])
    suite.run_test(function[1]([3], [1,2,3]), [3])
    suite.run_test(function[1]([1,3,5], [4,5]), [5])
    suite.run_test(function[1]([1,3,5], [3]), [3])
    suite.run_test(function[1]([1,3,5], [1,3,5]), [1,3,5])
    suite.run_test(function[1]([8, 19, 32, 47], [1, 5, 7, 8]), [8])
    suite.report_results()
    
    suite = poc_simpletest.TestSuite()
    print function[2]
    suite.run_test(function[2]([], [1,2,3]), [1,2,3])
    suite.run_test(function[2]([1,2,3], []), [1,2,3])
    suite.run_test(function[2]([2,3,4], [1,2,3]), [1,2,2,3,3,4])
    suite.run_test(function[2]([3,5,7], [3,3,3]), [3,3,3,3,5,7])
    suite.report_results()
    
    suite = poc_simpletest.TestSuite()
    print function[3]
    suite.run_test(function[3]([]), [])
    suite.run_test(function[3]([1,1]), [1,1])
    suite.run_test(function[3]([2,1]), [1,2])
    suite.run_test(function[3]([3,4,1,5]), [1,3,4,5])
    suite.run_test(function[3]([2,2,3,3,5]), [2,2,3,3,5])
    suite.report_results()
    
    suite = poc_simpletest.TestSuite()
    print function[4]
    suite.run_test(function[4]('a'), ['', 'a'])
    suite.run_test(function[4]('ab'), ['', 'b', 'a', 'ab', 'ba'], '#2')
    suite.run_test(function[4]('aa'), ['', 'a', 'a', 'aa', 'aa'], '#3')
    suite.report_results()

run_suite(function_to_test)