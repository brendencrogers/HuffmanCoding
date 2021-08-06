from ordered_list import *
from huffman_bit_reader import *
from huffman_bit_writer import *


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right
        
    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if self is None or other is None:
            return False
        else:
            return self.freq == other.freq and self.char == other.char

    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if self.freq < other.freq:
            return True
        else:
            if self.freq == other.freq:
                if self.char < other.char:
                    return True
                else:
                    return False
            else:
                return False


def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    freq = [0] * 256
    with open(filename, 'r') as file:
        for line in file:
            for j in line:
                ascii_code = ord(str(j))
                freq[ascii_code] += 1
    return freq


def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''
    lst = OrderedList()
    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            lst.add(HuffmanNode(i, char_freq[i]))
    while lst.size() > 1:
        lowest = lst.pop(0)
        second = lst.pop(0)
        root_char = min(lowest.char, second.char)
        new = HuffmanNode(root_char, lowest.freq + second.freq)
        new.left = lowest
        new.right = second
        lst.add(new)
    return lst.pop(0)


def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    codes = [''] * 256
    current = ''
    if node is None:
        return codes
    if node.left is None and node.right is None:
        return codes
    return create_code_helper(node, codes, current)


def create_code_helper(node, codes, current):
    """Recursively create list of codes"""
    if node.left is None and node.right is None:
        codes[node.char] = current
    if node.left is not None:
        current += '0'
        create_code_helper(node.left, codes, current)
    if node.right is not None:
        current = current[0:len(current) - 1]
        current += '1'
        create_code_helper(node.right, codes, current)
    return codes


def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list associated with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    header = []
    for i in range(len(freqs)):
        if freqs[i] != 0:
            freq_val = freqs[i]
            asci = i
            header.append(str(asci))
            header.append(str(freq_val))
    return ' '.join(header)


def huffman_encode(in_file, out_file):
    '''Takes input file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take note of special cases - empty file and file with only one unique character'''
    try:
        empty = [0] * 256
        freqlist = cnt_freq(in_file)
        if empty == freqlist:
            with open(out_file, 'w') as empty:
                empty.write('')
            compressed = out_file[0:-4] + '_compressed.txt'
            huff = HuffmanBitWriter(compressed)
            huff.close()
        else:
            tree = create_huff_tree(freqlist)
            coded = create_code(tree)
            with open(in_file, 'r') as _in:
                final_code = ''
                for line in _in:
                    for char in line:
                        asci = ord(char)
                        final_code += coded[asci]
            header = create_header(freqlist)
            with open(out_file, 'w') as out:
                out.write(header + '\n' + final_code)
            compressed = out_file[0:-4] + '_compressed.txt'
            huff = HuffmanBitWriter(compressed)
            huff.write_str(header + '\n')
            huff.write_code(final_code)
            huff.close()
    except Exception:
        raise FileNotFoundError


def huffman_decode(encoded_file, decode_file):
    """Reads an encoded text file and writes the decoded text into an output file. If the
    encoded file does not exist, raises FileNotFoundError"""
    try:
        huff_file = HuffmanBitReader(encoded_file)
    except Exception:
        raise FileNotFoundError
    header = huff_file.read_str()
    freq_list = parse_header(header)
    single_check = header.split()
    if len(single_check) == 2:
        with open(decode_file, 'w') as outf:
            single = ''
            while len(single) < int(single_check[1]):
                single += chr(int(single_check[0]))
            outf.write(single)
        huff_file.close()
    else:
        decoded = ''
        try:
            tree = create_huff_tree(freq_list)
            current = tree
            while len(decoded) != sum(freq_list):
                bit = huff_file.read_bit()
                if bit is True:
                    current = current.right
                    if current.left is None and current.right is None:
                        decoded += chr(current.char)
                        current = tree
                elif bit is False:
                    current = current.left
                    if current.left is None and current.right is None:
                        decoded += chr(current.char)
                        current = tree
            huff_file.close()
            with open(decode_file, 'w') as outf:
                outf.write(decoded)
        except IndexError:
            with open(decode_file, 'w') as outf:
                outf.write(decoded)
            huff_file.close()


def parse_header(header_string):
    """Takes string input (first line of the input file) and returns a list of frequencies.
    Freq_list should be in format of cnt_freq() function."""
    header_lst = header_string.split()
    freq_lst = [0] * 256
    for i in range(0, len(header_lst), 2):
        freq_lst[int(header_lst[i])] = int(header_lst[i + 1])
    return freq_lst
