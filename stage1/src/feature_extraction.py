from typing import List, Optional

from nltk.corpus import stopwords, words

from instance import Instance

EN_ARTICLES = ['the', 'a', 'an']
EN_WH_WORDS = ['who', 'whose', 'whom', 'which', 'what',
               'that', 'where', 'when', 'why', 'how']
EN_PREPOSITIONS = ['of', 'in', 'to', 'for', 'with', 'on', 'at', 'from', 'by',
                   'about', 'as', 'into', 'like', 'through', 'after', 'over',
                   'between', 'out', 'against', 'during', 'without', 'before',
                   'under', 'around', 'among']
EN_TITLES = ['Mr.', 'Dr.', 'Mrs.', 'Miss', 'Lt.', 'Captain', 'Lord', 'Sir',
             'Jr.', 'Dr', 'King', 'Detective']
EN_DICTIONARY = words.words()
EN_STOPWORDS = stopwords.words('english')


def _prev_non_title_cased_word(tok: List[str]) -> Optional[str]:
    """Return the last non title-cased token given a list of tokens, ignoring commas."""
    for w in reversed(tok):
        if not w[0].isupper() and w != ',':
            return w
    return None


def _next_non_title_cased_word(tok: List[str]) -> Optional[str]:
    """Return the first non title-cased token given a list of tokens, ignoring commas."""
    for w in tok:
        if not w[0].isupper() and w != ',':
            return w
    return None


def feature_n_words(ins: Instance) -> int:
    """Return the number of words."""
    return len(ins.term)


def feature_avg_word_len(ins: Instance) -> int:
    """Return the average length of words."""
    return sum([len(w) for w in ins.term]) // len(ins.term)


def feature_preceding_preposition(ins: Instance) -> str:
    """Return the preceding preposition (on, at, in, ...) if exists."""
    w = _prev_non_title_cased_word(ins.pre)
    if w in EN_PREPOSITIONS:
        return w
    else:
        return ''
    # if ins.pre and ins.pre[-1].lower() in EN_PREPOSITIONS:
    #     return ins.pre[-1].lower()
    # else:
    #     return ''


def feature_has_title_prefix(ins: Instance) -> bool:
    """Return true if there is a title (Mr., Dr., ...) before the term."""
    return bool(ins.pre) and ins.pre[-1] in EN_TITLES


def feature_contains_title(ins: Instance) -> bool:
    """Return true if the term contains a title."""
    return any(title in ins.term for title in EN_TITLES)


def feature_has_possessive_suffix(ins: Instance) -> bool:
    """Return true if the term is followed by a possessive suffix ('s)."""
    w = _next_non_title_cased_word(ins.post)
    return w in ["'s", "'"]


def feature_has_preceding_article(ins: Instance) -> bool:
    """Return true if the term is preceded by an article (a, the)."""
    return any([w.lower() in EN_ARTICLES for w in ins.pre[-4:]])
    # return bool(ins.pre) and ins.pre[-1].lower() in ENGLISH_ARTICLES


def feature_has_preceding_named(ins: Instance) -> bool:
    """Return true if the previous word is 'named'."""
    w = _prev_non_title_cased_word(ins.pre)
    return w == 'named'


def feature_prev_word_suffix(ins: Instance) -> str:
    """Return the previous word's suffix (last two characters)."""
    w = _prev_non_title_cased_word(ins.pre)
    return w[-2:] if w else ''


def feature_contains_article(ins: Instance) -> bool:
    """Return true if the term contains an article."""
    return any(w.lower() in EN_ARTICLES for w in ins.term)


def feature_following_wh_word(ins: Instance) -> str:
    """Return the following WH-word (who, which, ...) if exists."""
    w = _next_non_title_cased_word(ins.post)
    return w if w in EN_WH_WORDS else ''


def feature_has_following_article(ins: Instance) -> bool:
    """Return true if the term is followed by an article."""
    w = _next_non_title_cased_word(ins.post)
    return w in EN_ARTICLES


def feature_has_following_parenthesis(ins: Instance) -> bool:
    """Return true if the term is followed by a parenthesis."""
    w = _next_non_title_cased_word(ins.post)
    return w == '('


def feature_is_in_parenthesis(ins: Instance) -> bool:
    """Return true if the term is inside parentheses."""
    prev_w = _prev_non_title_cased_word(ins.pre)
    next_w = _next_non_title_cased_word(ins.post)
    return prev_w == '(' and next_w == ')'


def feature_is_beginning_of_sentence(ins: Instance) -> bool:
    """Return true if the term is at the beginning of a sentence."""
    return not ins.pre


def feature_prev_word_pos(ins: Instance) -> str:
    """Return the simplified pos tag (noun, verb, or other) of the previous word."""
    return ins.pre_pos[-1] if ins.pre_pos else ''


def feature_next_word_pos(ins: Instance) -> str:
    """Return the simplified pos tag (noun, verb, or other) of the next word."""
    return ins.post_pos[0] if ins.post_pos else ''


def feature_term_pos(ins: Instance) -> str:
    """Return the simplified pos tag of the term if every word has the same tag."""
    if len(set(ins.term_pos)) <= 1:
        return ins.term_pos[0]
    else:
        return ''


def feature_has_punctuation(ins: Instance) -> bool:
    """Return true if the terms contains '.' or '-'"""
    all_chars = ''.join(ins.term)
    return any(p in all_chars for p in ['.', '-'])


def feature_has_stopwords(ins: Instance) -> bool:
    """Return true if the terms contains common English stopwords (nltk.corpus.stopwords)."""
    return any(w.lower() in EN_STOPWORDS for w in ins.term)


def feature_has_verb_nearby(ins: Instance) -> bool:
    """Return true if there is a nearby verb."""
    return 'VERB' in ins.post_pos[:4]


def feature_has_pronoun_nearby(ins: Instance) -> bool:
    """Return true if there is a nearby 'his' or 'her'."""
    return 'his' in ins.post_pos[:4] or 'her' in ins.post_pos[:4]


def feature_has_dictionary_word(ins: Instance) -> bool:
    """Return true if the term contains a common English word (nltk.corpus.words)."""
    return any(w.lower() in EN_DICTIONARY for w in ins.term)


def feature_is_all_dictionary_words(ins: Instance) -> bool:
    """Return true if the term contains a common English word (nltk.corpus.words)."""
    return all(w.lower() in EN_DICTIONARY for w in ins.term)


def get_feature_names() -> List[str]:
    return ['n_words', 'avg_word_len', 'has_title_prefix', 'contains_title', 'has_preceding_article',
            'contains_article', 'has_possessive_suffix', 'has_following_parenthesis', 'is_in_parenthesis',
            'is_beginning_of_sentence', 'has_preceding_named', 'has_punctuation', 'has_stopwords',
            'has_following_article', 'has_verb_nearby', 'has_pronoun_nearby', 'has_dictionary_word',
            'is_all_dictionary_words', 'preceding_preposition', 'following_wh_word', 'prev_word_suffix',
            'term_pos', 'next_word_pos', 'prev_word_pos', 'label']


def extract_features(ins: Instance) -> List[object]:
    feature_func = [feature_n_words,
                    feature_avg_word_len,
                    feature_has_title_prefix,
                    feature_contains_title,
                    feature_has_preceding_article,
                    feature_contains_article,
                    feature_has_possessive_suffix,
                    feature_has_following_parenthesis,
                    feature_is_in_parenthesis,
                    feature_is_beginning_of_sentence,
                    feature_has_preceding_named,
                    feature_has_punctuation,
                    feature_has_stopwords,
                    feature_has_following_article,
                    feature_has_verb_nearby,
                    feature_has_pronoun_nearby,
                    feature_has_dictionary_word,
                    feature_is_all_dictionary_words,
                    feature_preceding_preposition,
                    feature_following_wh_word,
                    feature_prev_word_suffix,
                    feature_term_pos,
                    feature_next_word_pos,
                    feature_prev_word_pos]
    features = [f(ins) for f in feature_func]
    features.append(ins.label)
    return features
