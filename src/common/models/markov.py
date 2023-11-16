import re
import warnings
from sys import getsizeof
from typing import Dict, List, Tuple, TypeVar

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from sklearn.preprocessing import normalize

from src.common.interfaces.IMarkov import (
    MarkovChain,
    SequenceTokenizerInterface,
    StateSpaceInterface,
)

T = TypeVar('T', bound='NLPTextTokens')


class NLPTextTokens(SequenceTokenizerInterface[str]):
    """A class for tokenizing natural language text.

    It inherits from SequenceTokenizerInterface.

    Properties:
        raw (str): Original raw string content.
        content (str): Preprocessed string content.
        tokens (List[str]): List of tokens extracted from the content.
        mapping (Dict[str, int]): Mapping of unique tokens to their indices.

    Methods:
        preprocess: Preprocesses the raw content by handling punctuations.
        tokenize: Splits the content into tokens and creates a mapping.
        total_tokens: Returns the total number of tokens.
        total_unique_tokens: Returns the number of unique tokens.
        info: Prints information about the tokenization.
    """

    def __init__(self, content: str) -> None:
        """Initializes the NLPTextTokens instance.

        Args:
            content (str): The text content to be tokenized.

        Raises:
            TypeError: If the provided content is not a string.
        """
        if not isinstance(content, str):
            raise TypeError('content is not a string.')

        self._raw: str = content
        self._content: str = self.preprocess()
        self._tokens: List[str]
        self._mapping: Dict[str, int]
        self._tokens, self._mapping = self.tokenize(self._content)

    @property
    def raw(self) -> str:
        """Returns the original raw content."""
        return self._raw

    @property
    def content(self) -> str:
        """Returns the preprocessed content."""
        return self._content

    @property
    def tokens(self) -> List[str]:
        """Returns the list of tokens."""
        return self._tokens

    @property
    def mapping(self) -> Dict[str, int]:
        """Returns the mapping of tokens to their indices."""
        return self._mapping

    def preprocess(self) -> str:
        """Preprocesses the raw text by handling punctuations.

        Returns:
            str: The preprocessed text.
        """
        punctuation_pad = '!?.,:-;'
        punctuation_remove = '"()_\n'

        content_preprocess = re.sub(r'(\S)(\n)(\S)', r'\1 \2 \3', self._raw)
        content_preprocess = content_preprocess.translate(
            str.maketrans('', '', punctuation_remove)
        )
        content_preprocess = content_preprocess.translate(
            str.maketrans({k: f' {k} ' for k in punctuation_pad})  # type: ignore
        )
        content_preprocess = re.sub(' +', ' ', content_preprocess)
        content_preprocess = content_preprocess.strip()

        return content_preprocess

    @staticmethod
    def tokenize(content: str) -> Tuple[List[str], Dict[str, int]]:
        """Tokenizes content.

        Tokenizes content string into a list of words and a mapping
        of unique tokens.

        Args:
            content (str): str to be tokenized.

        Returns:
            Tuple[List[str], Dict[str, int]]: A tuple containing the list
                                              of tokens and the mapping
                                              of tokens to indices.
        """
        content_list = content.split(' ')
        content_set = list(set(content_list))
        content_set.sort()
        content_set.append('<| unknown |>')
        content_dict = {v: i for i, v in enumerate(content_set)}

        return content_list, content_dict

    def total_tokens(self) -> int:
        """Returns the total number of tokens in the content."""
        try:
            return len(self._tokens)
        except Exception:
            return 0

    def total_unique_tokens(self) -> int:
        """Returns the total number of unique tokens in the content."""
        try:
            unique_tokens = list(set(self._tokens))
            return len(unique_tokens)
        except Exception:
            return 0

    def info(self) -> None:
        """Prints information about the tokenized content."""
        print(
            f'Total Size: {getsizeof(self.raw)}b\nTotal Tokens: '
            f'{self.total_tokens()}\nTotal Distinct Tokens: '
            f'{self.total_unique_tokens()}'
        )


class NLPTextStateSpace(StateSpaceInterface[NLPTextTokens]):
    """A class representing the state space for NLP text analysis.

    It is designed to work with NLPTextTokens objects to create
    and analyze state spaces based on n-grams. This class extends the
    StateSpaceInterface and specializes in handling text data through
    tokenization and n-gram modeling.

    Attributes:
        n (int): The size of n-grams to be used in the state space.
        content (NLPTextTokens): The tokenized text data encapsulated in
                                 NLPTextTokens object.
        n_grams (List[str]): List of generated n-grams from the tokenized
                             text.
        state_space (Dict[str, int]): A dictionary representing the state
                                      space, mapping n-grams to their indices.
        transition_matrix (coo_matrix): A sparse matrix representing the
                                        transition probabilities between
                                        states (n-grams).
        transition_matrix_prob (csr_matrix): A sparse matrix representing
                                             normalized transition
                                             probabilities.
    """

    def __init__(self, content: NLPTextTokens, n: int = 2) -> None:
        """Initializes an instance of NLPTextStateSpace.

        Args:
            content (NLPTextTokens): An NLPTextTokens object containing
                                     the tokenized text data.
            n (int): The size of n-grams to be used. Must be between 2 and
                     5, inclusive.

        Raises:
            TypeError: If the content is not an instance of NLPTextTokens.
            ValueError: If 'n' is not in the range [2, 5].
        """
        if not isinstance(content, NLPTextTokens):
            raise TypeError('content is not and object of class NLPTextTokens.')
        if not (2 <= n <= 5):
            raise ValueError('n must be between 2 and 5, inclusive')

        self.n = n
        self._content = content
        self._ngrams: List[str] = self.generate_ngrams()
        self._state_space: Dict[str, int] = self.generate_state_space()
        self._transition_matrix: coo_matrix = self.generate_transition_matrix()
        self._transition_matrix_prob: csr_matrix = (
            self.generate_transition_matrix_prob()
        )

    @property
    def content(self) -> NLPTextTokens:
        """Returns the NLPTextTokens object containing the tokenized text data."""
        return self._content

    @property
    def state_space(self) -> Dict[str, int]:
        """Returns the list of states in the state space.

        Each is represented as a string n-gram.
        """
        return self._state_space

    @property
    def transition_matrix(self) -> coo_matrix:
        """Returns the sparse transition matrix.

        It represents the transition probabilities between states.
        """
        return self._transition_matrix

    @property
    def transition_probability_matrix(self) -> csr_matrix:
        """Returns the normalized transition matrix with probabilities.

        The probabilities represent the transitions between states.
        """
        return self._transition_matrix_prob

    @property
    def ngrams(self) -> List[str]:
        """Returns the list of n-grams generated from the tokenized text."""
        return self._ngrams

    def generate_ngrams(self) -> List[str]:
        """Generates and returns n-grams from the tokenized text.

        Returns:
            List[str]: A list of string n-grams.
        """
        sequences = [self._content.tokens[i:] for i in range(self.n)]

        return [' '.join(ngram) for ngram in list(zip(*sequences))]

    def generate_state_space(self) -> Dict[str, int]:
        """Generates and returns a state space from the n-grams.

        The state space is a dictionary mapping each unique n-gram
        to a unique integer.

        Returns:
            Dict[str, int]: The state space dictionary.
        """
        if not self._ngrams:
            self._ngrams = self.generate_ngrams()

        n_grams_distinct = list(set(self._ngrams))
        n_grams_distinct.append('<| unknwon |>')

        return {v: i for i, v in enumerate(n_grams_distinct)}

    def generate_transition_matrix(self) -> coo_matrix:
        """Generates a sparse matrix representing the transitions between n-gram states.

        This method creates a matrix where each entry (i, j) represents the
        transition from state i to state j.

        Returns:
            coo_matrix: The sparse transition matrix.
        """
        # create n-gram map if not already done so
        if not self._state_space:
            self._state_space = self.generate_state_space()

        # create coo matrix args
        row_ind, col_ind, values = ([] for i in range(3))
        for i in range(len(self._content.tokens[: -self.n])):
            ngram = ' '.join(self._content.tokens[i : i + self.n])
            ngram_ind = self._state_space[ngram]
            next_word_ind = self._content.mapping[self._content.tokens[i + self.n]]

            row_ind.extend([ngram_ind])
            col_ind.extend([next_word_ind])
            values.extend([1])

        # create and return coo matrix
        S = coo_matrix(
            (values, (row_ind, col_ind)),
            shape=(len(self._state_space), len(self._content.mapping)),
        )

        return S

    def generate_transition_matrix_prob(self) -> csr_matrix:
        """Generates and returns a normalized transition matrix.

        This matrix is normalized such that each row sums to 1, representing
        transition probabilities.

        Returns:
            csr_matrix: The normalized transition probability matrix.
        """
        transition_matrix = self.generate_transition_matrix()

        return normalize(transition_matrix, norm='l1', axis=1)

    @staticmethod
    def create_from_text(text: str, n: int = 2) -> 'NLPTextStateSpace':
        """Creates an NLPTextStateSpace object from a given text.

        This method tokenizes the input text and initializes the state space
        based on the specified n-gram size.

        Args:
            text (str): The raw text to be tokenized and analyzed.
            n (int): The n-gram size to be used. Default is 2.

        Returns:
            NLPTextStateSpace: An instance of NLPTextStateSpace with the
                               given text and n-gram size.

        Raises:
            ValueError: If an error occurs during the creation of
                        NLPTextTokens.
        """
        try:
            text_tokens = NLPTextTokens(text)
            return NLPTextStateSpace(text_tokens, n)
        except Exception:
            raise ValueError('Exception returned while creating NLP Text Tokenizer')


class NLPTextMarkovChain(MarkovChain[NLPTextStateSpace]):
    """A class representing a Markov Chain.

    Specifically designed for NLP text processing.

    This class extends a generic MarkovChain class and is tailored to work with
    NLPTextStateSpace instances. It provides methods for generating text
    sequences based on the Markov Chain model.

    Attributes:
        _state_space (NLPTextStateSpace): The state space of the Markov Chain,
                                          which contains the n-grams and
                                          transition probabilities.
        _reverse_word_mapping (Dict[int, str]): A mapping from indices to
                                                words, reversed from the
                                                original mapping in the state
                                                space.
    """

    def __init__(self, state_space: NLPTextStateSpace):
        """Initializes the NLPTextMarkovChain with a given state space.

        Args:
            state_space (NLPTextStateSpace): The state space to be used in
                                             the Markov Chain.
        """
        self._state_space = state_space
        self._reverse_word_mapping = {
            i: v for v, i in self._state_space.content.mapping.items()
        }

    @property
    def state_space(self) -> NLPTextStateSpace:
        """Returns the state space of the Markov Chain."""
        return self._state_space

    def random_ngram(self) -> str:
        """Chooses and returns a random n-gram from the state space.

        Returns:
            str: A randomly selected n-gram.
        """
        choice: str = np.random.choice(self.state_space.ngrams)
        return choice

    def check_prefix(self, prefix: str) -> str:
        """Validates and adjusts the given prefix.

        Adjusts to fit the n-gram size of the state space.

        Args:
            prefix (str): The prefix string to be validated.

        Returns:
            str: A valid prefix. If the original prefix is invalid, a
                 warning is issued and a random n-gram is returned.
        """
        prefix_list = prefix.split(' ')[-self._state_space.n :]
        if len(prefix_list) < self._state_space.n:
            warnings.warn(
                'Prefix is too short, please provide prefix of length: '
                f'{self._state_space.n}. Random ngram used instead.'
            )
            return self.random_ngram()
        else:
            prefix = ' '.join(prefix_list)
            if prefix in self.state_space.ngrams:
                return prefix
            else:
                warnings.warn(
                    'Prefix is not included in ngrams of the model. '
                    'Provide another prefix. Random ngram used instead.'
                )
                return self.random_ngram()

    def return_next_element(self, prefix: str) -> str:
        """Generates the next element in the sequence based on the given prefix.

        Args:
            prefix (str): The prefix string for which the next element is
                          to be generated.

        Returns:
            str: The next element in the sequence.
        """
        prefix = self.check_prefix(prefix)
        prefix_index = self.state_space.state_space[prefix]
        # TODO: add temperature to change weights here
        weights = self.state_space.transition_probability_matrix[
            prefix_index
        ].toarray()[0]
        token_index = np.random.choice(range(len(weights)), p=weights)

        return self._reverse_word_mapping[token_index]

    def generate_sequence(self, length: int, prefix: str) -> str:
        """Generates a text sequence of a specified length using the Markov Chain model.

        Args:
            length (int): The length of the sequence to be generated.
            prefix (str): The starting prefix of the sequence.

        Returns:
            str: A generated sequence of words.
        """
        prefix = self.check_prefix(prefix)
        print(prefix)
        sequence = prefix.split(' ')
        range_length = length - len(sequence)

        for i in range(range_length):
            next_word = self.return_next_element(prefix)
            sequence.append(next_word)
            prefix = ' '.join(sequence[-self._state_space.n :])

        return ' '.join(sequence)
