from typing import Any, Dict, List, Tuple, Union

import numpy as np
import pytest
import torch
from torch import nn

from pytorch_optimizer import (
    LARS,
    MADGRAD,
    PNM,
    SAM,
    SGDP,
    AdaBelief,
    AdaBound,
    AdamP,
    AdaPNM,
    DiffGrad,
    DiffRGrad,
    Lamb,
    Lookahead,
    PCGrad,
    RAdam,
    RaLamb,
    Ranger,
    Ranger21,
    SafeFP16Optimizer,
    Shampoo,
)
from tests.utils import (
    MultiHeadLogisticRegression,
    build_environment,
    build_lookahead,
    dummy_closure,
    ids,
    make_dataset,
    tensor_to_numpy,
)

OPTIMIZERS: List[Tuple[Any, Dict[str, Union[float, bool, int]], int]] = [
    (build_lookahead, {'lr': 5e-1, 'weight_decay': 1e-3}, 200),
    (AdaBelief, {'lr': 5e-1, 'weight_decay': 1e-3}, 200),
    (AdaBelief, {'lr': 5e-1, 'weight_decay': 1e-3, 'amsgrad': True}, 200),
    (AdaBelief, {'lr': 5e-1, 'weight_decay': 1e-3, 'weight_decouple': False}, 200),
    (AdaBelief, {'lr': 5e-1, 'weight_decay': 1e-3, 'fixed_decay': True}, 200),
    (AdaBelief, {'lr': 5e-1, 'weight_decay': 1e-3, 'rectify': False}, 200),
    (AdaBound, {'lr': 5e-1, 'gamma': 0.1, 'weight_decay': 1e-3}, 200),
    (AdaBound, {'lr': 5e-1, 'gamma': 0.1, 'weight_decay': 1e-3, 'fixed_decay': True}, 200),
    (AdaBound, {'lr': 5e-1, 'gamma': 0.1, 'weight_decay': 1e-3, 'weight_decouple': False}, 200),
    (AdaBound, {'lr': 5e-1, 'gamma': 0.1, 'weight_decay': 1e-3, 'amsbound': True}, 200),
    (AdamP, {'lr': 5e-1, 'weight_decay': 1e-3}, 200),
    (AdamP, {'lr': 5e-1, 'weight_decay': 1e-3, 'use_gc': True}, 200),
    (AdamP, {'lr': 5e-1, 'weight_decay': 1e-3, 'nesterov': True}, 200),
    (DiffGrad, {'lr': 5e-1, 'weight_decay': 1e-3}, 200),
    (DiffRGrad, {'lr': 5e-1, 'weight_decay': 1e-3}, 200),
    (Lamb, {'lr': 1e-1, 'weight_decay': 1e-3}, 500),
    (Lamb, {'lr': 1e-1, 'weight_decay': 1e-3, 'adam': True, 'eps': 1e-8}, 500),
    (Lamb, {'lr': 1e-1, 'weight_decay': 1e-3, 'pre_norm': True, 'eps': 1e-8}, 500),
    (LARS, {'lr': 1e-1, 'weight_decay': 1e-3}, 500),
    (RaLamb, {'lr': 1e-1, 'weight_decay': 1e-3}, 200),
    (RaLamb, {'lr': 5e-1, 'weight_decay': 1e-3, 'pre_norm': True}, 500),
    # (RaLamb, {'lr': 1e-1, 'weight_decay': 1e-3, 'degenerated_to_sgd': True}, 200),
    (MADGRAD, {'lr': 1e-2, 'weight_decay': 1e-3}, 500),
    (MADGRAD, {'lr': 1e-2, 'weight_decay': 1e-3, 'eps': 0.0}, 500),
    (MADGRAD, {'lr': 1e-2, 'weight_decay': 1e-3, 'momentum': 0.0}, 500),
    (MADGRAD, {'lr': 1e-2, 'weight_decay': 1e-3, 'decouple_decay': True}, 500),
    (RAdam, {'lr': 1e-1, 'weight_decay': 1e-3}, 200),
    (RAdam, {'lr': 1e-1, 'weight_decay': 1e-3, 'degenerated_to_sgd': True}, 200),
    (SGDP, {'lr': 2e-1, 'weight_decay': 1e-3}, 500),
    (SGDP, {'lr': 2e-1, 'weight_decay': 1e-3, 'nesterov': True}, 500),
    (Ranger, {'lr': 5e-1, 'weight_decay': 1e-3}, 200),
    (Ranger21, {'lr': 5e-1, 'weight_decay': 1e-3, 'num_iterations': 500}, 500),
    (Shampoo, {'lr': 3e-1, 'weight_decay': 1e-3, 'momentum': 0.05}, 500),
    (PNM, {'lr': 2e-1}, 200),
    (PNM, {'lr': 2e-1, 'weight_decouple': False}, 200),
    (AdaPNM, {'lr': 3e-1, 'weight_decay': 1e-3}, 500),
    (AdaPNM, {'lr': 3e-1, 'weight_decay': 1e-3, 'weight_decouple': False}, 500),
    (AdaPNM, {'lr': 3e-1, 'weight_decay': 1e-3, 'amsgrad': False}, 500),
]

ADAMD_SUPPORTED_OPTIMIZERS: List[Tuple[Any, Dict[str, Union[float, bool, int]], int]] = [
    (build_lookahead, {'lr': 5e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 500),
    (AdaBelief, {'lr': 5e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 200),
    (AdaBound, {'lr': 5e-1, 'gamma': 0.1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 200),
    (AdaBound, {'lr': 1e-2, 'gamma': 0.1, 'weight_decay': 1e-3, 'amsbound': True, 'adamd_debias_term': True}, 200),
    (AdamP, {'lr': 5e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 500),
    (DiffGrad, {'lr': 15 - 1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 500),
    (DiffRGrad, {'lr': 1e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 200),
    (Lamb, {'lr': 1e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 300),
    (RaLamb, {'lr': 1e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 500),
    (RAdam, {'lr': 1e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 200),
    (Ranger, {'lr': 5e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 200),
]


@pytest.mark.parametrize('optimizer_fp32_config', OPTIMIZERS, ids=ids)
def test_f32_optimizers(optimizer_fp32_config):
    (x_data, y_data), model, loss_fn = build_environment()

    optimizer_class, config, iterations = optimizer_fp32_config
    optimizer = optimizer_class(model.parameters(), **config)

    init_loss, loss = np.inf, np.inf
    for _ in range(iterations):
        optimizer.zero_grad()

        y_pred = model(x_data)
        loss = loss_fn(y_pred, y_data)

        if init_loss == np.inf:
            init_loss = loss

        loss.backward()

        optimizer.step()

    assert tensor_to_numpy(init_loss) > 2.0 * tensor_to_numpy(loss)


@pytest.mark.parametrize('pullback_momentum', ['none', 'reset', 'pullback'])
def test_lookahead(pullback_momentum):
    (x_data, y_data), model, loss_fn = build_environment()

    optimizer = Lookahead(AdamP(model.parameters(), lr=5e-1), pullback_momentum=pullback_momentum)

    init_loss, loss = np.inf, np.inf
    for _ in range(200):
        optimizer.zero_grad()

        y_pred = model(x_data)
        loss = loss_fn(y_pred, y_data)

        if init_loss == np.inf:
            init_loss = loss

        loss.backward()

        optimizer.step()

    assert tensor_to_numpy(init_loss) > 2.0 * tensor_to_numpy(loss)


@pytest.mark.parametrize('optimizer_fp16_config', OPTIMIZERS, ids=ids)
def test_safe_f16_optimizers(optimizer_fp16_config):
    (x_data, y_data), model, loss_fn = build_environment()

    optimizer_class, config, iterations = optimizer_fp16_config

    optimizer_name: str = optimizer_class.__name__
    if (
        (optimizer_name == 'MADGRAD')
        or (optimizer_name == 'RaLamb' and 'pre_norm' in config)
        or (optimizer_name == 'PNM')
    ):
        return True

    optimizer = SafeFP16Optimizer(optimizer_class(model.parameters(), **config))

    init_loss, loss = np.inf, np.inf
    for _ in range(iterations):
        optimizer.zero_grad()

        y_pred = model(x_data)
        loss = loss_fn(y_pred, y_data)

        if init_loss == np.inf:
            init_loss = loss

        loss.backward()

        optimizer.step()

    assert tensor_to_numpy(init_loss) > tensor_to_numpy(loss)


@pytest.mark.parametrize('adaptive', (False, True))
@pytest.mark.parametrize('optimizer_sam_config', OPTIMIZERS, ids=ids)
def test_sam_optimizers(adaptive, optimizer_sam_config):
    (x_data, y_data), model, loss_fn = build_environment()

    optimizer_class, config, iterations = optimizer_sam_config
    if optimizer_class.__name__ == 'Shampoo':
        return True

    optimizer = SAM(model.parameters(), optimizer_class, **config, adaptive=adaptive)

    init_loss, loss = np.inf, np.inf
    for _ in range(iterations):
        loss = loss_fn(y_data, model(x_data))
        loss.backward()
        optimizer.first_step(zero_grad=True)

        loss_fn(y_data, model(x_data)).backward()
        optimizer.second_step(zero_grad=True)

        if init_loss == np.inf:
            init_loss = loss

    assert tensor_to_numpy(init_loss) > 2.0 * tensor_to_numpy(loss)


@pytest.mark.parametrize('adaptive', (False, True))
@pytest.mark.parametrize('optimizer_sam_config', OPTIMIZERS, ids=ids)
def test_sam_optimizers_with_closure(adaptive, optimizer_sam_config):
    (x_data, y_data), model, loss_fn = build_environment()

    optimizer_class, config, iterations = optimizer_sam_config
    if optimizer_class.__name__ == 'Shampoo':
        return True

    optimizer = SAM(model.parameters(), optimizer_class, **config, adaptive=adaptive)

    def closure():
        first_loss = loss_fn(y_data, model(x_data))
        first_loss.backward()
        return first_loss

    init_loss, loss = np.inf, np.inf
    for _ in range(iterations):
        loss = loss_fn(y_data, model(x_data))
        loss.backward()

        optimizer.step(closure)
        optimizer.zero_grad()

        if init_loss == np.inf:
            init_loss = loss

    assert tensor_to_numpy(init_loss) > 2.0 * tensor_to_numpy(loss)


@pytest.mark.parametrize('optimizer_adamd_config', ADAMD_SUPPORTED_OPTIMIZERS, ids=ids)
def test_adamd_optimizers(optimizer_adamd_config):
    (x_data, y_data), model, loss_fn = build_environment()

    optimizer_class, config, iterations = optimizer_adamd_config
    optimizer = optimizer_class(model.parameters(), **config)

    init_loss, loss = np.inf, np.inf
    for _ in range(iterations):
        optimizer.zero_grad()

        y_pred = model(x_data)
        loss = loss_fn(y_pred, y_data)

        if init_loss == np.inf:
            init_loss = loss

        loss.backward()

        optimizer.step()

    assert tensor_to_numpy(init_loss) > 2.0 * tensor_to_numpy(loss)


@pytest.mark.parametrize('reduction', ('mean', 'sum'))
@pytest.mark.parametrize('optimizer_pc_grad_config', OPTIMIZERS, ids=ids)
def test_pc_grad_optimizers(reduction, optimizer_pc_grad_config):
    torch.manual_seed(42)

    x_data, y_data = make_dataset()

    model: nn.Module = MultiHeadLogisticRegression()
    loss_fn_1: nn.Module = nn.BCEWithLogitsLoss()
    loss_fn_2: nn.Module = nn.L1Loss()

    optimizer_class, config, iterations = optimizer_pc_grad_config
    optimizer = PCGrad(optimizer_class(model.parameters(), **config), reduction=reduction)

    if optimizer_class.__name__ == 'RaLamb' and 'pre_norm' in config:
        return True

    init_loss, loss = np.inf, np.inf
    for _ in range(iterations):
        optimizer.zero_grad()
        y_pred_1, y_pred_2 = model(x_data)
        loss1, loss2 = loss_fn_1(y_pred_1, y_data), loss_fn_2(y_pred_2, y_data)

        loss = (loss1 + loss2) / 2.0
        if init_loss == np.inf:
            init_loss = loss

        optimizer.pc_backward([loss1, loss2])
        optimizer.step()

    assert tensor_to_numpy(init_loss) > 1.5 * tensor_to_numpy(loss)


@pytest.mark.parametrize('optimizer_config', OPTIMIZERS, ids=ids)
def test_no_gradients(optimizer_config):
    (x_data, y_data), model, loss_fn = build_environment()

    model.fc1.weight.requires_grad = False
    model.fc1.bias.requires_grad = False

    optimizer_class, config, iterations = optimizer_config
    optimizer = optimizer_class(model.parameters(), **config)

    init_loss, loss = np.inf, np.inf
    for _ in range(iterations):
        optimizer.zero_grad()

        y_pred = model(x_data)
        loss = loss_fn(y_pred, y_data)

        if init_loss == np.inf:
            init_loss = loss

        loss.backward()

        optimizer.step()

    assert tensor_to_numpy(init_loss) >= tensor_to_numpy(loss)


@pytest.mark.parametrize('optimizer_config', OPTIMIZERS, ids=ids)
def test_closure(optimizer_config):
    _, model, _ = build_environment()

    optimizer_class, config, _ = optimizer_config
    if optimizer_class.__name__ == 'Ranger21':
        return True

    optimizer = optimizer_class(model.parameters(), **config)

    optimizer.zero_grad()
    optimizer.step(closure=dummy_closure)


@pytest.mark.parametrize('optimizer_config', OPTIMIZERS, ids=ids)
def test_reset(optimizer_config):
    _, model, _ = build_environment()

    optimizer_class, config, _ = optimizer_config
    optimizer = optimizer_class(model.parameters(), **config)

    optimizer.zero_grad()
    optimizer.reset()
