import pytest
from scipy.sparse import coo_matrix, csr_matrix

from ..common.models import NLPTextMarkovChain, NLPTextStateSpace, NLPTextTokens


@pytest.fixture
def sample_tokenizer():
    return NLPTextTokens('Sample text for testing.')


@pytest.fixture
def sample_state_space():
    text_tokens = NLPTextTokens('This is a test. This test is for NLP.')
    return NLPTextStateSpace(text_tokens, n=2)


@pytest.fixture
def sample_markov_chain(sample_state_space):
    return NLPTextMarkovChain(sample_state_space)


def test_NLPTextTokens_init_with_string():
    text = 'Hello, world!'
    tokenizer = NLPTextTokens(text)
    assert tokenizer.raw == text


def test_NLPTextTokens_init_with_non_string():
    with pytest.raises(TypeError):
        NLPTextTokens(1234)


def test_NLPTextTokens_preprocess():
    text = 'Hello, world! This is a test.'
    tokenizer = NLPTextTokens(text)
    # Assuming specific preprocessing rules
    assert tokenizer.content == 'Hello , world ! This is a test .'


def test_NLPTextTokens_tokenize():
    text = 'hello hello world'
    tokenizer = NLPTextTokens(text)
    assert len(tokenizer.tokens) == 3
    assert tokenizer.tokens == ['hello', 'hello', 'world']
    assert tokenizer.mapping == {'hello': 0, 'world': 1, '<| unknown |>': 2}


def test_NLPTextTokens_total_tokens():
    text = 'hello world'
    tokenizer = NLPTextTokens(text)
    assert tokenizer.total_tokens() == 2  # 'hello', 'world'


def test_NLPTextTokens_total_unique_tokens():
    text = 'hello hello world'
    tokenizer = NLPTextTokens(text)
    assert tokenizer.total_unique_tokens() == 2  # 'hello', 'world'
    assert tokenizer.total_tokens() == 3  # 'hello' and 'world'


def test_NLPTextTokens_info_output(capsys):
    text = 'hello hello world'
    tokenizer = NLPTextTokens(text)
    tokenizer.info()
    captured = capsys.readouterr()
    assert 'Total Tokens: 3' in captured.out
    assert 'Total Distinct Tokens: 2' in captured.out


def test_NLPStateSpace_init(sample_tokenizer):
    # Valid initialization
    state_space = NLPTextStateSpace(sample_tokenizer, 2)
    assert isinstance(state_space, NLPTextStateSpace)

    # Invalid content type
    with pytest.raises(TypeError):
        NLPTextStateSpace('not a tokenizer', 2)

    # Invalid 'n' value
    with pytest.raises(ValueError):
        NLPTextStateSpace(sample_tokenizer, 6)


def test_NLPStateSpace_properties(sample_tokenizer):
    state_space = NLPTextStateSpace(sample_tokenizer, 2)
    assert isinstance(state_space.content, NLPTextTokens)
    assert isinstance(state_space.state_space, dict)
    assert isinstance(state_space.transition_matrix, coo_matrix)
    assert isinstance(state_space.transition_probability_matrix, csr_matrix)
    assert isinstance(state_space.ngrams, list)


def test_NLPStateSpace_generate_ngrams(sample_tokenizer):
    state_space = NLPTextStateSpace(sample_tokenizer, 2)
    ngrams = state_space.generate_ngrams()
    assert isinstance(ngrams, list)
    # Additional checks can be added based on expected behavior


def test_NLPStateSpace_generate_state_space(sample_tokenizer):
    state_space = NLPTextStateSpace(sample_tokenizer, 2)
    state_space_dict = state_space.generate_state_space()
    assert isinstance(state_space_dict, dict)
    # Additional checks can be added based on expected behavior


def test_NLPStateSpace_generate_transition_matrix(sample_tokenizer):
    state_space = NLPTextStateSpace(sample_tokenizer, 2)
    matrix = state_space.generate_transition_matrix()
    assert isinstance(matrix, coo_matrix)
    # Additional checks can be added based on expected behavior


def test_NLPStateSpace_generate_transition_matrix_prob(sample_tokenizer):
    state_space = NLPTextStateSpace(sample_tokenizer, 2)
    matrix_prob = state_space.generate_transition_matrix_prob()
    assert isinstance(matrix_prob, csr_matrix)
    # Additional checks can be added based on expected behavior


def test_NLPStateSpace_create_from_text():
    state_space = NLPTextStateSpace.create_from_text('Sample text', 2)
    assert isinstance(state_space, NLPTextStateSpace)
    # Check for ValueError
    with pytest.raises(ValueError):
        NLPTextStateSpace.create_from_text(1234, 2)  # Invalid text type


def test_NLPTextMarkovChain_init(sample_state_space):
    chain = NLPTextMarkovChain(sample_state_space)
    assert isinstance(chain, NLPTextMarkovChain)


def test_NLPTextMarkovChain_state_space(sample_markov_chain):
    assert isinstance(sample_markov_chain.state_space, NLPTextStateSpace)


def test_NLPTextMarkovChain_random_ngram(sample_markov_chain):
    ngram = sample_markov_chain.random_ngram()
    assert ngram in sample_markov_chain.state_space.ngrams


def test_NLPTextMarkovChain_check_prefix(sample_markov_chain):
    # Valid prefix
    valid_prefix = 'This is'
    assert sample_markov_chain.check_prefix(valid_prefix) == valid_prefix

    # Too short prefix
    with pytest.warns(UserWarning):
        assert sample_markov_chain.check_prefix('This') != 'This'

    # Invalid prefix
    with pytest.warns(UserWarning):
        assert (
            sample_markov_chain.check_prefix('Nonexistent prefix')
            != 'Nonexistent prefix'
        )


def test_NLPTextMarkovChain_return_next_element(sample_markov_chain):
    next_element = sample_markov_chain.return_next_element('This is')
    assert isinstance(next_element, str)
    # Further checks can depend on the behavior of your method


def test_NLPTextMarkovChain_generate_sequence(sample_markov_chain):
    generated_sequence = sample_markov_chain.generate_sequence(5, 'This is')
    assert isinstance(generated_sequence, str)
    assert len(generated_sequence.split(' ')) == 5
