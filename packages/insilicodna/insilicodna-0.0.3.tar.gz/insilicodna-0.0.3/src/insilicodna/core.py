"""Core functions which are call throughout.

Core functions which are call throughout.

"""

import random
import uuid
import sys


def chunks(sequence_list, chunk_length):
    """Yields successive n-sized chunks from a list.

    Yields successive n-sized chunks from a list. If list is not
    evenly split into equal chunks, the last chunk will contain
    the uneven chunk.

    Args:
        l:
          A single list of values to create chunks from.
        n:
          An integer which specifies the desired length of each chunk.

    Yields:
        A generator with equally sized chunks derived from the original
        list of values. Returned lists will always be equal to, or less
        than the specified input, n.

    Raises:
        IOError:
          An error occured if n is greater than the length of the
          supplied list.
    """
    for i in range(0, len(sequence_list), chunk_length):
        yield sequence_list[i:i + chunk_length]

def generate_sequence(length, upper=True):
    """Generates a sequence of base pairs.

    Generates a sequence of base pairs, randomly selecting
    from ('A', 'C', 'T', 'G').

    Args:
        length:
          Desired length of sequence.

    Returns:
        A list of base pairs

    """
    base_pairs = ['A', 'C', 'T', 'G']
    if upper is not True:
        base_pairs = [a.lower() for a in base_pairs]
    return random.choices(base_pairs, k=length)

def generate_uuid4():
    """Generates a unique id.

    Generates a unique id.

    Returns:
        An uppercase UUID of numbers (0-9) and letters (A-Z).

    """
    id_ = str(uuid.uuid4()).upper()
    id_ = id_.replace('-', '')
    return id_

def print_fasta(sequence_dict_list, line_length=60):
    """Prints a sequence in FASTA format.

    Prints a sequence in FASTA format.

    Args:
        sequence_dict_list:
          A dict where the key is an ID and the value is
          a list of base pairs.
        line_length:
          Desired line length for FASTA output.

    Returns:
        A FASTA formatted sequence.

    """
    for item in sequence_dict_list:
        header = list(item.keys())[0]
        body = list(item.values())[0]
        print(f">{header}")
        chunk_list = chunks(body, line_length)
        for line in chunk_list:
            print("".join(line))

def generate_fasta_file(filename, sequence_dict_list, line_length=60):
    """Creates a FASTA file.

    Creates a FASTA file.

    Args:
        filename:
          Name of the output file.
        sequence_dict_list:
          A dict where the key is an ID and the value is
          a list of base pairs.
        line_length:
          Desired line length for FASTA output.

    Returns:
        A FASTA formatted file.

    """
    original_stdout = sys.stdout
    filename = f"{filename}.fasta"
    with open(filename, 'w', encoding="utf-8") as fileout:
        sys.stdout = fileout
        print_fasta(sequence_dict_list, line_length=line_length)
        sys.stdout = original_stdout
