from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Tuple, TypeVar

from scipy.sparse import coo_matrix, csr_matrix

T = TypeVar('T')


class SequenceTokenizerInterface(ABC, Generic[T]):
    """Abstract base class defining the interface for a sequence tokenizer.

    This interface requires implementation of methods for tokenizing sequences,
    managing tokens and mappings, and preprocessing content.

    References:
        https://en.wikipedia.org/wiki/Tokenization_(lexical_analysis)

    Attributes:
        content (T): The processed content from the raw input.
        raw (T): The original raw content.
        tokens (List[T]): A list of tokens derived from the content.
        mapping (Dict[T, int]): A mapping of unique tokens to their indices.
    """

    @classmethod
    def __subclasshook__(cls, subclass: Any) -> bool:
        return (
            hasattr(subclass, '__init__')
            and hasattr(subclass, 'raw')
            and hasattr(subclass, 'content')
            and hasattr(subclass, 'tokens')
            and hasattr(subclass, 'mapping')
            and hasattr(subclass, 'tokenize')
            and callable(subclass.tokenize)
            and hasattr(subclass, 'preprocess')
            and callable(subclass.preprocess)
            and hasattr(subclass, 'total_tokens')
            and callable(subclass.total_tokens)
            and hasattr(subclass, 'total_unique_tokens')
            and callable(subclass.total_unique_tokens)
        )

    @abstractmethod
    def __init__(self, content: T) -> None:
        """Initializes the tokenizer with provided content.

        Args:
            content (T): The content to be tokenized.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def raw(self) -> T:
        """Returns the raw content.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def content(self) -> T:
        """Returns the processed content derived from raw.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def tokens(self) -> List[T]:
        """Returns a list of tokens extracted from the content.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def mapping(self) -> Dict[T, int]:
        """Returns a dictionary mapping unique tokens to their indices.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def preprocess(self) -> T:
        """Preprocesses the raw content before tokenization.

        Returns:
            T: The preprocessed content.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def tokenize(self, content: Any) -> Tuple[List[str], Dict[T, int]]:
        """Tokenizes the preprocessed content.

        Returns:
            Tuple[List[str], Dict[T, int]]: A tuple containing a list of tokens
            and a dictionary mapping the tokens to their indices.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def total_tokens(self) -> int:
        """Calculates the total number of tokens.

        Returns:
            int: The total number of tokens generated during tokenization.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def total_unique_tokens(self) -> int:
        """Calculates the total number of unique tokens.

        Returns:
            int: The total number of unique tokens.
                 during tokenization.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError


class StateSpaceInterface(ABC, Generic[T]):
    """Abstract base class defining the interface for a state space model.

    This class outlines the methods necessary for creating a state space
    representation and its associated transition matrices from a given content.

    References:
        https://en.wikipedia.org/wiki/State_space

    Attributes:
        content (T): The original content used to generate the state space.
        state_space (List[Any]): The generated state space items.
        transition_matrix (coo_matrix): The transition matrix in COO format.
        transition_probability_matrix (csr_matrix): The probability-based
            transition matrix in CSR format.
    """

    @classmethod
    def __subclasshook__(cls, subclass: Any) -> bool:
        return (
            hasattr(subclass, 'content')
            and hasattr(subclass, 'state_space')
            and hasattr(subclass, 'transition_matrix')
            and hasattr(subclass, 'transition_probability_matrix')
            and hasattr(subclass, 'generate_state_space')
            and callable(subclass.generate_state_space)
            and hasattr(subclass, 'generate_transition_matrix')
            and callable(subclass.generate_transition_matrix)
            and hasattr(subclass, 'generate_transition_matrix_prob')
            and callable(subclass.generate_transition_matrix_prob)
        )

    @abstractmethod
    def __init__(self, content: T, *args: Any, **kwargs: Any) -> None:
        """Initializes the state space model with provided content.

        Args:
            content (T): The content from which to create the state space model.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def content(self) -> T:
        """Returns the content used to create the state space.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def state_space(self) -> Dict[Any, int]:
        """Returns the items constituting the state space.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def transition_matrix(self) -> coo_matrix:
        """Returns the transition matrix of the state space in COO format.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def transition_probability_matrix(self) -> csr_matrix:
        """Returns the transition probability matrix of the state space in CSR format.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_state_space(self) -> Dict[Any, int]:
        """Generates the state space from the content.

        Returns:
            Dict: A dictionary representing the state space.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_transition_matrix(self) -> coo_matrix:
        """Generates the transition matrix for the state space.

        Returns:
            coo_matrix: The transition matrix in COO format.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_transition_matrix_prob(self) -> csr_matrix:
        """Generates the transition probability matrix for the state space.

        Returns:
            csr_matrix: The transition probability matrix in CSR format.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError


class MarkovChain(ABC, Generic[T]):
    """Abstract base class for a Markov Chain model.

    This class provides the interface for implementing Markov Chains. It
    outlines the necessary methods for checking prefixes, generating the
    next element, and creating sequences based on the state space.

    References:
        https://en.wikipedia.org/wiki/Markov_chain

    Attributes:
        state_space (T): The state space of the Markov Chain.
    """

    @classmethod
    def __subclasshook__(cls, subclass: Any) -> bool:
        return (
            hasattr(subclass, '__init__')
            and hasattr(subclass, 'state_space')
            and callable(subclass.check_prefix)
            and hasattr(subclass, 'check_prefix')
            and callable(subclass.return_next_element)
            and hasattr(subclass, 'return_next_element')
            and callable(subclass.generate_sequence)
            and hasattr(subclass, 'generate_sequence')
        )

    @property
    @abstractmethod
    def state_space(self) -> T:
        """Provides the state space of the Markov Chain.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def __init__(self, state_space: T, *args: Any, **kwargs: Any) -> None:
        """Initializes the Markov Chain with a given state space.

        Args:
            state_space (T): The state space for the Markov Chain.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def check_prefix(self, prefix: Any) -> Any:
        """Checks if the given prefix is valid in the state space.

        Args:
            prefix (Any): The prefix to be checked against the state space.

        Returns:
            bool: True if the prefix is valid, False otherwise.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def return_next_element(self, prefix: Any) -> Any:
        """Returns the next element of the sequence based on the given prefix.

        Args:
            prefix (Any): The prefix used to determine the next element.

        Returns:
            Any: The next element in the sequence.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_sequence(self, length: int, prefix: Any) -> Any:
        """Generates a sequence of a specified length based on the given prefix.

        Args:
            length (int): The length of the sequence to be generated.
            prefix (Any): The initial prefix for the sequence.

        Returns:
            Any: The generated sequence.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError
