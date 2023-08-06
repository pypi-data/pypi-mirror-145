import functools
from typing import Tuple, Sequence, Iterator, Optional, NamedTuple

import torch
import torch.autograd as autograd
from torch import Tensor
from torch.optim import Optimizer


class LossArguments(NamedTuple):
    target_loss: Tensor
    adaptive_loss: Optional[Tensor] = None
    scale_factor: Optional[float] = 1.


def get_parameters(optimizer: Optimizer) -> Iterator[Tensor]:
    yield from (
        parameter
        for parameter_group in optimizer.param_groups
        for _, parameters in parameter_group.items()
        for parameter in (parameters if isinstance(parameters, list) else [parameters])
        if torch.is_tensor(parameter) and parameter.requires_grad
    )


def manual_step(optimizer: Optimizer, loss: Tensor, allow_unused: bool = False) -> None:
    optimizer.zero_grad()

    parameters = list(get_parameters(optimizer))
    gradients = autograd.grad(loss, parameters, retain_graph=True, allow_unused=allow_unused)

    for parameter, gradient in zip(parameters, gradients):
        parameter.grad = gradient

    optimizer.step()


def compute_norms(adaptive_gradients: Sequence[Tensor], target_gradients: Sequence[Tensor]) -> Tuple[Tensor, Tensor]:
    adaptive_norm, target_norm = functools.reduce(
        lambda tuple_first, tuple_second: (tuple_first[0] + tuple_second[0], tuple_first[1] + tuple_second[1]),
        (
            (torch.sum(adaptive_gradient ** 2), torch.sum(target_gradient ** 2))
            for adaptive_gradient, target_gradient in zip(adaptive_gradients, target_gradients)
            if target_gradient is not None and adaptive_gradient is not None
        ),
    )

    adaptive_norm, target_norm = torch.sqrt(adaptive_norm), torch.sqrt(target_norm)

    return adaptive_norm, target_norm


def combine_gradients(
        adaptive_gradients: Sequence[Tensor],
        target_gradients: Sequence[Tensor],
        scaling_factor: Tensor,
) -> Iterator[Optional[Tensor]]:

    for adaptive_gradient, target_gradient in zip(adaptive_gradients, target_gradients):
        if adaptive_gradient is not None and target_gradient is not None:
            yield target_gradient + scaling_factor * adaptive_gradient
        elif adaptive_gradient is not None:
            yield adaptive_gradient
        elif target_gradient is not None:
            yield target_gradient
        else:
            yield None


def calculate_scaled_gradients(
        parameters: Sequence[Tensor],
        adaptive_loss: Tensor,
        target_loss: Tensor,
        scale_factor: float,
) -> Iterator[Optional[Tensor]]:

    adaptive_gradients = autograd.grad(adaptive_loss, parameters, retain_graph=True, allow_unused=True)
    target_gradients = autograd.grad(target_loss, parameters, retain_graph=True, allow_unused=True)

    adaptive_norm, target_norm = compute_norms(adaptive_gradients, target_gradients)
    scaling_factor = torch.minimum(adaptive_norm, target_norm) / adaptive_norm * scale_factor

    yield from combine_gradients(adaptive_gradients, target_gradients, scaling_factor)


def collect_gradients(parameters: Sequence[Tensor], losses: Sequence[LossArguments],) -> Iterator[Tuple[Tensor, ...]]:
    collected_gradients = []

    for loss in losses:
        if loss.adaptive_loss is None:
            gradients: Iterator[Optional[Tensor]] = (
                loss.scale_factor * gradient if gradient is not None else None
                for gradient
                in autograd.grad(loss.target_loss, parameters, retain_graph=True, allow_unused=True)
            )
        else:
            assert loss.scale_factor is not None
            gradients = calculate_scaled_gradients(parameters, loss.adaptive_loss, loss.target_loss, loss.scale_factor)

        collected_gradients.append(gradients)

    yield from (
        tuple(gradient for gradient in gradients if gradient is not None)
        for gradients in zip(*collected_gradients)
    )


def adaptive_clipping(optimizer: Optimizer, losses: Sequence[LossArguments]) -> None:
    optimizer.zero_grad()

    parameters = list(get_parameters(optimizer))
    gradients = collect_gradients(parameters, losses)

    for parameter, gradient in zip(parameters, gradients):
        if len(gradient) > 0:
            parameter.grad = sum(gradient)

    optimizer.step()
