from typing import List, Tuple

from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.tokenize import MWETokenizer

from instance import Instance


def extract_label(tok_w_label: List[str]) -> Tuple[List[str], List[bool]]:
    """
    Extract labels from a list of marked tokens

    :param tok_w_label: a list of tokens where each marked entity is surrounded by <p>...</p>
    :return: a list of raw tokens and the label of each token
    """
    tok_raw = []
    label = []
    i = 0
    while i < len(tok_w_label):
        if tok_w_label[i] == '<p>':
            i += 1
            while tok_w_label[i] != '</p>':
                tok_raw.append(tok_w_label[i])
                label.append(True)
                i += 1
        else:
            tok_raw.append(tok_w_label[i])
            label.append(False)
        i += 1

    return tok_raw, label


def is_candidate_term(term: List[str]) -> bool:
    """Returns true if the term is title-cased."""
    first_chars = ''.join([t[0] for t in term])
    all_chars = ''.join(term)
    return first_chars.isupper() and first_chars.isalpha() and not all_chars.isupper()


def _get_instances(tok: List[str], pos: List[str], label: List[bool], file_idx: int = -1) -> List[Instance]:
    """
    Return all candidate instances given a tokenized sentence.

    :param tok: a list of tokens (tokenized from a sentence)
    :param pos: a list of pos tags
    :param label: a list of labels
    :param file_idx: the index of the text file
    :return: a list of instances
    """
    instances = []

    # instance with 1 word
    for i in range(len(tok)):
        term = [tok[i]]
        if not is_candidate_term(term) and not label[i]:
            continue
        instances.append(Instance(term=term, pre=tok[:i], post=tok[i + 1:],
                                  term_pos=[pos[i]], pre_pos=pos[:i], post_pos=pos[i + 1:],
                                  label=label[i], file_idx=file_idx))

    # instance with 2 words
    for i in range(len(tok) - 1):
        term = tok[i:i + 2]
        if not is_candidate_term(term) and not all(label[i:i + 2]):
            continue
        instances.append(Instance(term=term, pre=tok[:i], post=tok[i + 2:],
                                  term_pos=pos[i:i + 2], pre_pos=pos[:i], post_pos=pos[i + 2:],
                                  label=all(label[i:i + 2]), file_idx=file_idx))

    # instance with 3 words
    for i in range(len(tok) - 2):
        term = tok[i:i + 3]
        if not is_candidate_term(term) and not all(label[i:i + 3]):
            continue
        instances.append(Instance(term=term, pre=tok[:i], post=tok[i + 3:],
                                  term_pos=pos[i:i + 3], pre_pos=pos[:i], post_pos=pos[i + 3:],
                                  label=all(label[i:i + 3]), file_idx=file_idx))

    return instances


def get_simple_pos(tag):
    """Simplify the nltk pos tags into just VERB, NOUN, and OTHER"""
    if tag.startswith('V'):
        return 'VERB'
    elif tag.startswith('N'):
        return 'NOUN'
    else:
        return 'OTHER'


def get_instances(text: str, idx: int = -1) -> List[Instance]:
    """
    Return all candidate instances from the given marked text.
    A candidate instance must either be directly marked or (contain only titled-case words and have <= 3 words)

    :param text: marked text, each entity is marked by <p>...</p>
    :param idx: file index
    :return: a list of instances
    """
    instances = []

    tokenizer = MWETokenizer([('<', 'p', '>'), ('<', '/p', '>')], separator='')

    for sent in sent_tokenize(text):
        tok_w_label = tokenizer.tokenize(word_tokenize(sent))
        tok, label = extract_label(tok_w_label)
        pos = [get_simple_pos(t[1]) for t in pos_tag(tok)]

        assert len(pos) == len(tok)

        instances += _get_instances(tok, pos, label, idx)

    return instances
