[![PyPI version](https://badge.fury.io/py/torch-emb2vec.svg)](https://badge.fury.io/py/torch-emb2vec)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/ulf1/torch-emb2vec.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ulf1/torch-emb2vec/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ulf1/torch-emb2vec.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ulf1/torch-emb2vec/context:python)


# torch-emb2vec
Convert W2V embeddings of a sequence (2D) to one vector (1D)


## Usage

Create toy data

```py
num_emb, emb_dim = 1000, 256
emb = torch.nn.Embedding(num_emb, emb_dim)

batch_sz, seq_len = 5, 128
inputs = torch.randint(num_emb, (batch_sz, seq_len))

z = emb(inputs)
```

Averaging the embedding vectors over the sequence is the most common technique to convert the 2D representation to a 1D representation.

```py
avg = AverageToVec()
vec = avg(z)
vec.shape
# torch.Size([5, 128])
```

Concatenating the W2V values, i.e., flattening, might seem like an attractive option but will result in huge vectors that is usually not practiable for downstream tasks.

```py
con = ConcatToVec()
vec = con(z)
vec.shape
# torch.Size([5, 32768])
```

Another way are random projections. ConvToVec applies a 1D-Convolution over the sequence wheras the embedding elements are treated as Conv1D input channels.

```py
conv1 = ConvToVec(seq_len=z.shape[1], emb_dim=z.shape[2], num_output=768)
vec = conv1(z)
vec.shape
# torch.Size([5, 768])
```

It is also possible to apply the heaviside function to generate binary 1D vector embeddings.

```py
conv1 = ConvToVec(seq_len=z.shape[1], emb_dim=z.shape[2], num_output=2048, hashed=True)
vec = conv1(z)
vec.shape, vec.min(), vec.max()
# torch.Size([5, 2048]), 0.0, 1.0
```

## Appendix

### Installation
The `torch-emb2vec` [git repo](http://github.com/ulf1/torch-emb2vec) is available as [PyPi package](https://pypi.org/project/torch-emb2vec)

```sh
pip install torch-emb2vec
pip install git+ssh://git@github.com/ulf1/torch-emb2vec.git
```

### Install a virtual environment

```sh
python3.6 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Python commands

* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `PYTHONPATH=. pytest`

Publish

```sh
pandoc README.md --from markdown --to rst -s -o README.rst
python setup.py sdist 
twine upload -r pypi dist/*
```

### Clean up 

```sh
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


### Support
Please [open an issue](https://github.com/ulf1/torch-emb2vec/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/torch-emb2vec/compare/).
