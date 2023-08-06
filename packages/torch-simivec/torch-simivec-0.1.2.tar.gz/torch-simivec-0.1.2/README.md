[![PyPI version](https://badge.fury.io/py/torch-simivec.svg)](https://badge.fury.io/py/torch-simivec)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/ulf1/torch-simivec.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ulf1/torch-simivec/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ulf1/torch-simivec.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ulf1/torch-simivec/context:python)

# torch-simivec : Input Embedding Training as Similarity Learning Problem (SimiVec)
Train an input embedding as a similarity learning problem.


## Usage

Modelling

```py
from torch_simivec import SimiLossW2V
import torch
import numpy as np

# init model
model = SimiLossW2V(
    vocab_size=10,
    embed_size=300,
    context_size=4,
    use_kernel="diag"
)
# create a positive & negative example
X_pos = torch.tensor([[[0, 2, 9], [6, 0, 8], [1, 3, 4], [7, 8, 9]]])
y_pos = torch.tensor([[1, 4, 2]])
np.random.seed(42)
X_neg = torch.tensor(np.random.permutation(X_pos))
y_neg = torch.tensor(np.random.permutation(y_pos))
# compute loss
loss = model(y_pos, X_pos, y_neg, X_neg)
print(loss)
```

Training

```py
optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)
avg_loss = .0
for epoch in range(50):
    optimizer.zero_grad()
    loss = model(y_pos, X_pos, y_neg, X_neg)
    loss.backward()
    optimizer.step()
    avg_loss += loss.item()
    if (epoch % 10) == 9:
        print(f"epoch {epoch + 1} | loss: {avg_loss / 10.}")
        avg_loss = .0
```


## Appendix

### Installation
The `torch-simivec` [git repo](http://github.com/ulf1/torch-simivec) is available as [PyPi package](https://pypi.org/project/torch-simivec)

```sh
pip install torch-simivec
pip install git+ssh://git@github.com/ulf1/torch-simivec.git
```

### Install a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
pip install -r requirements-demo.txt --no-cache-dir
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Python commands

* Jupyter for the examples: `jupyter lab`
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
Please [open an issue](https://github.com/ulf1/torch-simivec/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/torch-simivec/compare/).
