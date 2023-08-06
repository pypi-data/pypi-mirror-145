Snowball stemmer for Maori language, implementing PorterStemmer (https://snowballstem.org/projects.html)

Maori snowball syntax written by kshepherd (https://github.com/kshepherd/maoristemmer)

# Install
```bash
pip install py_maori_stemmer 
```

# Usage
To stem one word:
```python
from py_maori_stemmer import MaoriStemmer
stemmer = MaoriStemmer()
stemmer.stemWord('waihangatia')
# waihanga
```

To stem a sentence:
```python
from py_maori_stemmer import MaoriStemmer
stemmer = MaoriStemmer()
stemmer.stemWord('i waihangatia mō ngā akomanga kaupapa')
# ['i', 'waihanga', 'mō', 'ngā', 'akoma', 'kaupap']
```


# Test
```bash
nosetests --nocapture -v
```
