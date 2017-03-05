"""Usage: python wordsquares.py vocab.txt squares.txt
Format of `vocab.txt`: one word per line, lower case.
Hunts for every possible word square buildable from that vocab, and saves them
to `squares.txt`, one square per line (separated by a ' ').
"""

import collections
import sys


class WordList(object):

    def __init__(self, words):
        self._words = sorted(words)
        self._num_words = len(words)

    def words(self):
        return self._words

    def find_first_prefix_position(self, prefix):
        if self._words[0].startswith(prefix):
            return 0
        prefix_len = len(prefix)
        lower = 1
        upper = self._num_words - 1
        while lower <= upper:
            mid = (upper + lower) / 2
            mid_prefix = self._words[mid][:prefix_len]
            lesser_prefix = self._words[mid - 1][:prefix_len]
            if mid_prefix == prefix and lesser_prefix < prefix:
                return mid
            if mid_prefix < prefix:
                lower = mid + 1
            else:
                upper = mid - 1
        return None

    def find_last_prefix_position(self, prefix):
        if self._words[-1].startswith(prefix):
            return self._num_words - 1
        prefix_len = len(prefix)
        lower = 0
        upper = self._num_words - 2
        while lower <= upper:
            mid = (upper + lower) / 2
            mid_prefix = self._words[mid][:prefix_len]
            greater_prefix = self._words[mid + 1][:prefix_len]
            if mid_prefix == prefix and greater_prefix > prefix:
                return mid
            if mid_prefix <= prefix:
                lower = mid + 1
            else:
                upper = mid - 1
        return None

    def find_prefixes(self, prefix):
        first = self.find_first_prefix_position(prefix)
        last = self.find_last_prefix_position(prefix)
        if first is not None and last is not None:
            return self._words[first : last + 1]
        else:
            return []


def PrefixFromGrid(grid):
    if not grid:
        raise ValueError("grid can't be empty")
    n = len(grid[0])
    num_words = len(grid)
    if num_words >= n:
        raise "Too many entries in grid"
    if not all([len(w) == n for w in grid]):
        raise ValueError("all words in grid must be same length")
    return "".join([word[num_words] for word in grid])


def BuildGrid(starting_word, wordlist):
    """Depth first search through possible grid extensions."""
    actual_grids = []

    grid_stack = [[starting_word,]]
    num_char = len(starting_word)

    while grid_stack:
        grid = grid_stack[-1]
        grid_stack = grid_stack[:-1]
        if len(grid) == num_char:
            actual_grids.append(grid)
            continue
        prefix = PrefixFromGrid(grid)
        for candidate in wordlist.find_prefixes(prefix):
            grid_stack.append(grid + [candidate,])
    return actual_grids


def WordListsFromFile(filename):
    len_to_words = collections.defaultdict(list)
    with open(filename, 'r') as infile:
        for word in infile.xreadlines():
            if word.islower():
                len_to_words[len(word)].append(word.strip())
    return [WordList(words) for words in len_to_words.values()]


if __name__ == "__main__":
    wordlists = WordListsFromFile(sys.argv[1])
    print "done building wordlists"

    all_grids = []
    for wordlist in wordlists:
        print "\nWordList starting with", wordlist.words()[0]
        if len(wordlist.words()[0]) >= 8:
            break
        print '\t', "Current length:", len(all_grids)
        for word in wordlist.words():
            all_grids.extend(BuildGrid(word, wordlist))
        PrintSquare(all_grids[-1])
    print len(all_grids), "grids found"

    with open(sys.argv[2], 'w') as outfile:
        for grid in all_grids:
            outfile.write(" ".join(grid) + "\n")
