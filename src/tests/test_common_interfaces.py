from ..common.interfaces import SequenceTokenizerInterface


# Mock implementation of the SequenceTokenizerInterface
class MockTokenizer(SequenceTokenizerInterface):
    def __init__(self, content):
        self._raw = content
        self._content = self.preprocess()
        self._tokens, self._mapping = self.tokenize()

    @property
    def raw(self):
        return self._raw

    @property
    def content(self):
        return self._content

    @property
    def tokens(self):
        return self._tokens

    @property
    def mapping(self):
        return self._mapping

    def preprocess(self):
        # Mock preprocess implementation
        return self._raw.lower()

    def tokenize(self):
        # Mock tokenize implementation
        tokens = sorted(self._content.split())
        print(set(tokens))
        for i, t in enumerate(set(tokens)):
            print(i, t)
        mapping = {token: index for index, token in enumerate(set(tokens))}
        return tokens, mapping

    def total_tokens(self):
        return len(self._tokens)

    def total_unique_tokens(self):
        return len(self._mapping)


# Test Cases
def test_raw_content():
    tokenizer = MockTokenizer('Hello World')
    assert tokenizer.raw == 'Hello World'


def test_preprocessed_content():
    tokenizer = MockTokenizer('Hello World')
    assert tokenizer.content == 'hello world'


def test_tokens():
    tokenizer = MockTokenizer('Hello Hello World')
    assert tokenizer.tokens == ['hello', 'hello', 'world']


def test_mapping():
    tokenizer = MockTokenizer('Hello Hello World')
    map_keys = list(tokenizer.mapping.keys())
    map_values = list(tokenizer.mapping.values())
    assert all([key in map_keys for key in ['hello', 'world']])
    assert all([value in map_values for value in [0, 1]])
    assert tokenizer.mapping['hello'] == 0 or tokenizer.mapping['hello'] == 1
    assert tokenizer.mapping['world'] == 0 or tokenizer.mapping['world'] == 1


def test_total_tokens():
    tokenizer = MockTokenizer('Hello World')
    assert tokenizer.total_tokens() == 2


def test_total_unique_tokens():
    tokenizer = MockTokenizer('Hello Hello World')
    assert tokenizer.total_unique_tokens() == 2


# Test the subclasshook
def test_subclasshook():
    assert issubclass(MockTokenizer, SequenceTokenizerInterface)
