Bodo Tokenizer
==============
### About:
Bodo is one of the scheduled languages of India and belongs to the Tibeto-Burman branch of the Sino-Tibetan language family. It uses a Devanagari script like other Indian languages such as Hindi, Konkani, Maithili, Marathi, Nepali, Sanskrit, Sindhi, and Dogri. However there are some differences, this python library tokenizes Bodo sentences into its tokens that is useful for NLP tasks.

### Prerequisite:
Python 3.6+

### Installation:
```bash
git clone https://github.com/bodonlp/bodo-tokenizer.git
cd bodo-tokenizer
python setup.py install
```
### Available functions:
```python
    # Tokenize single sentence
    from bodotokenizer import tokenize
    tokenize(sentence)
```
```python
    # Tokenize sentences from a file
    # Suitable for tokenize sentences in parallel corpus
    from bodotokenizer import tokenize_file
    tokenize_file(input_file, out_file)
```
### Usage:
```python
    from bodotokenizer import tokenize
    sentence = "नोंसिनि फरायसालियाव य'गा फोरोंगुरु दङ नामा?"
    tokenized_sentence = tokenize(sentence)
    # Output: Tokenized Sentence
    # "नोंसिनि फरायसालियाव य'गा फोरोंगुरु दङ नामा ?"
```