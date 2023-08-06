from torch_simivec import SimiLossW2V
import torch
import numpy as np


def test1():
    # init model
    model = SimiLossW2V(
        vocab_size=10,
        embed_size=300,
        context_size=4,
        use_kernel=None
    )
    # create a positive & negative example
    X_pos = torch.tensor([[[0, 2, 9], [6, 0, 8], [1, 3, 4], [7, 8, 9]]])
    y_pos = torch.tensor([[1, 4, 2]])
    np.random.seed(42)
    X_neg = torch.tensor(np.random.permutation(X_pos))
    y_neg = torch.tensor(np.random.permutation(y_pos))
    # compute loss
    loss = model(y_pos, X_pos, y_neg, X_neg, regul=False)
    assert torch.abs(loss - 0.0) < 1e-5
