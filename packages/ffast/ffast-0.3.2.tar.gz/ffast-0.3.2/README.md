# ffast
Fast and lightweight NLP pipeline for ML tasks: powerful tokeniser and (model-free) sentence embeddings using Fast Fourier transforms, power means, positional encoding and Wordnet or Poincare Embeddings

![](images/wordnet.png)
![](images/poincare.jpeg)

## Installation
`pip install ffast`

## Example
```python
from ffast import load

tokeniser = load() #wordnet version (sparse vectors)
tokeniser = load("poincare") #poincare version (dense vectors)
```

see `examples/` to see what you can do!

## Changelog
- 0.3.2 bug fix in wordnet tokeniser where raw and preprocessed tokens were swapped
- 0.3.1 bug fix with encoder and special tokens
- 0.3.0 add padding feature to tokenisers
- 0.2.5 embedding size added to tokeniser class. customisable special tokens for tokenisers. 
- 0.2.4 vocab size can be queries by taking length of tokeniser
- 0.2.3 wordnet setence vectors combined using xor as well as and, or
- 0.2.2 wordnet sentence vectors remain sparse vectors. projections removed (since small dense vectors are covered by poincare model)
- 0.2.1 decode poincare vector/semantics into tokens
- 0.1.11 path finally fixed
- 0.1.10 pathlib added to include local path
- 0.1.9 path lookup error - updated path to fix
- 0.1.8 typo fixed. poincare.txt now being packaged
- 0.1.7 include poincare.txt file in package build to avoid user downloading separately
- 0.1.6 adding method to poincare tokens to return individual token vectors
- 0.1.5 taking morphology of the raw token to allow unknown tokens to be encoded
- 0.1.4 relative download path for poincare embeddings shifted
- 0.1.3 relative download path bug for poincare embeddings
- 0.1.2 added download script for poincare text file to fix dependency bug
- 0.1.1 init files added to fix subdirectory lookup bug
- 0.1.0 poincare model introduced alongside wordnet base model to allow for smaller vectors
- 0.0.4 dot similarity implemented to compare batch more efficiently
- 0.0.3 nltk dependencies load bug fixed
- 0.0.2 scipy load bug fixed
- 0.0.1 Initial release