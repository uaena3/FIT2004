# Author: Xinyu Ma

class Trie(object):
    class TrieNode(object):
        # We need a TrieNode class to build a Trie
        def __init__(self):
            # Parent node
            # have 26 child nodes
            # strfreq: the number of strings that ending with the characters that stored in current node
            # abprefreq: the number of strings that are prefixed with current string and not equal to current string
            # letter: letters stored in current node
            # father: parent node
            # time complexity: O(1)
            # space complexity: O(1)
            self.son = [None for _ in range(26)]
            self.strfreq = 0
            self.abprefreq = 0
            self.letter = None
            self.father = None

        def add_node(self, chara):
            # use self node as parent node, if there is no node that stores chara as a child node, add the child node
            # chara: input string, use this string to create a node and put it in the child node
            # time complexity: O(1)
            # space complexity: O(1)
            if self.son[ord(chara) - 97] == None:
                self.son[ord(chara) - 97] = Trie.TrieNode()
                self.son[ord(chara) - 97].father = self
                self.son[ord(chara) - 97].letter = chara

        def get_son(self, chara):
            # return the child node represented by chara
            # chara: a string
            # time complexity: O(1)
            # space complexity: O(0)
            return self.son[ord(chara) - 97]


            
    
    def __init__(self, text): # task1 building a Trie
        # initialize a root node without storing any strings
        # build a Trie based on the content of text
        # time complexity: O(T)
        # space complexity: O(26^S) S is the length of longest word in text
        self.root = Trie.TrieNode()
        for word in text:
            node = self.root
            for chara in word:
                node.add_node(chara)
                node = node.get_son(chara)
            node.strfreq += 1
            while node != self.root:
                node = node.father
                node.abprefreq += 1


    def string_freq(self, query_str): # task2
        # reach the node corresponding to query_str and return the corresponding strfreq
        # time complexity: O(q)
        # space complexity: O(1)
        node = self.root
        for chara in query_str:
            node = node.get_son(chara)
            if node == None:
                return 0
        return node.strfreq
        pass

    def prefix_freq(self, query_str): # task3
        # reach the node corresponding to query_str and return the sum of strfreq and abprefreq
        # time complexity: O(q)
        # space complexity: O(1)
        node = self.root
        for chara in query_str:
            node = node.get_son(chara)
            if node == None:
                return 0
        return node.abprefreq + node.strfreq
        pass

    def wildcard_prefix_freq(self, query_str): # task4
        # return all strings that prefixed with query_str
        # we can build a matchstr to perform depth first search(dfs) for our Trie
        # for example:
        # assume we want to search 'aa?', when we reach first 'a', pos = 0, then we add 'a' to the end of matchstr and dfs 'a' node of first layer in the tree
        # when pos = 1, we reach second 'a' and add it to the end of matchstr, dfs 'a' node in the child node of the 'a' node of first layer
        # when pos = 2, we reach '?', dfs will search all the child nodes of 'a' node, the letters corresponding to all child nodes will be added to the end of matchstr, and the letters at the end will be deleted after the search
        # when pos = 3, we reach an empty string, pos >= qstrlen, if strfreq of current node is > 0, then the current matchstr is constructed into the corresponding numbers of strings and added to the list
        # we will only search the nodes that match query_str, so time complexity is O(q+S)
        # space complexity: O(s) where s is the length of longest word
        matchstr = ''
        matchlist = []
        qstrlen = len(query_str)
        pos = 0
        def dfs(node):
            nonlocal pos
            nonlocal matchstr
            nonlocal matchlist
            if pos >= qstrlen and node.strfreq > 0:
                matchlist += ([matchstr]*node.strfreq)
            if pos >= qstrlen or query_str[pos] == '?':
                for s in node.son:
                    if s != None:
                        matchstr += s.letter
                        pos += 1
                        dfs(s)
                        pos -= 1
                        matchstr = matchstr[:-1]
            else:
                matchstr += query_str[pos]
                pos += 1
                dfs(node.get_son(query_str[pos-1]))
                pos -= 1
                matchstr = matchstr[:-1]
        dfs(self.root)
        return matchlist






def main():
    text = ['aa',
        'aab',
        'aaab',
        'abaa',
        'aa',
        'abba',
        'aaba',
        'aaa',
        'aa',
        'aaab',
        'abbb',
        'baaa',
        'baa',
        'bba',
        'bbab']
    student_trie = Trie(text)
    string_frequency = student_trie.string_freq('aa')
    print(string_frequency)
    string_frequency = student_trie.string_freq('abc')
    print(string_frequency)
    prefix_frequency = student_trie.prefix_freq('aa')
    print(prefix_frequency)
    prefix_frequency = student_trie.prefix_freq('abb')
    print(prefix_frequency)
    wildcard_prefix_frequency = student_trie.wildcard_prefix_freq('ab?')
    print(wildcard_prefix_frequency)
    wildcard_prefix_frequency = student_trie.wildcard_prefix_freq('aa?')
    print(wildcard_prefix_frequency)
    wildcard_prefix_frequency = student_trie.wildcard_prefix_freq('?aa')
    print(wildcard_prefix_frequency)
    wildcard_prefix_frequency = student_trie.wildcard_prefix_freq('a?a')
    print(wildcard_prefix_frequency)
    wildcard_prefix_frequency = student_trie.wildcard_prefix_freq('?b')
    print(wildcard_prefix_frequency)

if __name__ == '__main__':
    main()
