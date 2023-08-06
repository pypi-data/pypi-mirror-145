import numpy as np
import torch
import time
from statistics import mean
from collections import namedtuple
from torch.utils.data import TensorDataset, DataLoader, random_split

from diffql.networks import AbstractParametrisedConvexApproximator


Datum = namedtuple("Datum", [
    "s",  # state
    "a",  # action
    "r",  # reward
    "s_next",  # next_state
    "t",  # time
    "d",  # done
])


class DataBuffer():
    def __init__(self):
        self.data = []

    def __repr__(self):
        return f"length = {len(self.data)}\ndata = {self.data}"

    def __add__(self, other):
        data_buffer = DataBuffer()
        data_buffer.extend(self)
        data_buffer.extend(other)
        return data_buffer

    def __len__(self):
        return len(self.data)

    def append(self, s, a, r, s_next, t=torch.Tensor([torch.nan]), d=torch.Tensor([torch.nan])):
        if type(s) is np.ndarray:
            s = torch.Tensor(s)
        else:
            assert type(s) is torch.Tensor
        if type(a) is np.ndarray:
            a = torch.Tensor(a)
        else:
            assert type(a) is torch.Tensor
        if isinstance(r, float):  # considering inheritance; e.g., type(r) could be numpy.float64
            r = torch.Tensor([r])
        else:
            assert type(r) is torch.Tensor
        if type(s_next) is np.ndarray:
            s_next = torch.Tensor(s_next)
        else:
            assert type(s_next) is torch.Tensor
        if type(t) is float:
            t = torch.Tensor([t])
        else:
            assert type(t) is torch.Tensor
        if type(d) is bool:
            d = torch.BoolTensor([d])

        datum = Datum(s, a, r, s_next, t, d)
        self.data.append(datum)

    def extend(self, data_buffer):
        assert type(data_buffer) is DataBuffer
        self.data.extend(data_buffer.data)

    @property
    def s(self):
        # return torch.stack([datum[0] for datum in self.data])
        return torch.stack([datum.s for datum in self.data])

    @property
    def a(self):
        # return torch.stack([datum[1] for datum in self.data])
        return torch.stack([datum.a for datum in self.data])

    @property
    def r(self):
        # return torch.stack([datum[2] for datum in self.data])
        return torch.stack([datum.r for datum in self.data])

    @property
    def c(self):
        """
        cost = -reward
        """
        return -self.r

    @property
    def s_next(self):
        # return torch.stack([datum[3] for datum in self.data])
        return torch.stack([datum.s_next for datum in self.data])

    @property
    def t(self):
        # return torch.stack([datum[4] for datum in self.data])
        return torch.stack([datum.t for datum in self.data])

    @property
    def d(self):
        # return torch.stack([datum[4] for datum in self.data])
        return torch.stack([datum.d for datum in self.data])

    @property
    def sacs(self):
        return self.s, self.a, self.c, self.s_next

    @property
    def sars(self):
        return self.s, self.a, self.r, self.s_next


def split_data(dataset, ratio=0.8):
    """
    ratio:1-ratio = train:test
    """
    assert ratio >= 0.0 and ratio <= 1.0
    size_train = int(len(dataset) * ratio)
    size_test = len(dataset) - size_train
    dataset_train, dataset_test = random_split(dataset, [size_train, size_test])
    return dataset_train, dataset_test


def supervised_learning(model, xs, us, fs, loss_fn, optimiser,
                        epochs=100,
                        batch_size_train=16, batch_size_test=16):
    """
    model: approximator
    """
    # data setting
    dataset = TensorDataset(xs, us, fs)
    dataset_train, dataset_test = split_data(dataset)
    loader_train = DataLoader(dataset_train, batch_size=batch_size_train, shuffle=True)
    loader_test = DataLoader(dataset_test, batch_size=batch_size_test)
    # training
    losses_test = []
    for epoch in range(epochs):
        if epoch % 5 == 0:
            print(f"epoch: {epoch}/{epochs}")
        model.train()
        for x_train, u_train, f_train in loader_train:
            optimiser.zero_grad()
            f_pred_train = model(x_train, u_train)
            loss = loss_fn(f_pred_train, f_train)
            loss = loss / len(loader_train.dataset)
            loss.backward()
            optimiser.step()
        model.eval()
        with torch.no_grad():
            batch_loss_test = 0.0
            for x_test, u_test, f_test in loader_test:
                f_pred_test = model(x_test, u_test)
                loss_test = loss_fn(f_pred_test, f_test)
                batch_loss_test += loss_test.item()
            losses_test.append(batch_loss_test / len(loader_test.dataset))  # mean value; total sum / number of data
    return losses_test


class AbstractTrainer:
    def __init__(self):
        pass

    def train_cycle(self, *args, **kwargs):
        raise NotImplementedError("Define method `train_cycle")

    def test_cycle(self, *args, **kwargs):
        raise NotImplementedError("Define method `test_cycle")


class FakeTrainer(AbstractTrainer):
    def __init__(self):
        pass

    def train_cycle(self, *args, **kwargs):
        return {}

    def test_cycle(self, *args, **kwargs):
        return {}  # empty dictionary

    def make_loaders(self, *args, **kwargs):
        return None, None  # dummy


class PCQL(AbstractTrainer):
    def __init__(
        self,
        # epochs=1,
        batch_size_train=16, batch_size_test=16,
        weight_origin=None, weight_nonneg=None, gamma=1.0,
        grad_max_norm=None, lr_scheduler_max_epoch=40,
    ):
        # self.epochs = epochs
        self.batch_size_train = batch_size_train
        self.batch_size_test = batch_size_test
        self.weight_origin = weight_origin
        self.loss_fn_origin = torch.nn.L1Loss(reduction="sum")
        self.weight_nonneg = weight_nonneg
        self.grad_max_norm = grad_max_norm
        self.lr_scheduler_max_epoch = lr_scheduler_max_epoch
        if self.weight_origin is not None:
            assert self.weight_origin >= 0.0
        if self.weight_nonneg is not None:
            assert self.weight_nonneg >= 0.0
        self.gamma = gamma

    def make_loaders(self, data_buffer):
        dataset = TensorDataset(*data_buffer.sacs)  # sacs: state, action, cost, next_state
        dataset_train, dataset_test = split_data(dataset)
        loader_train = DataLoader(dataset_train, batch_size=self.batch_size_train, shuffle=True)
        loader_test = DataLoader(dataset_test, batch_size=self.batch_size_test)
        return loader_train, loader_test

    def train_cycle(self, model, loader_train, loss_fn, optimiser, scheduler, epoch):
        model.train()
        total_norms = []
        for s_train, a_train, c_train, s_next_train in loader_train:
            optimiser.zero_grad()
            Q_train = model(s_train, a_train)
            u_next_train = model.minimise_tch(s_next_train)
            Q_next_optimal_train = model(s_next_train, u_next_train)
            td_target_train = c_train + self.gamma * Q_next_optimal_train
            loss = loss_fn(td_target_train, Q_train)
            if self.weight_origin is not None:
                # penalty 1: min_{u} Q(0, u) = 0
                s_origin = torch.zeros(1, model.n)
                # a_at_origin = model.minimise_tch(s_origin)  # TODO: check this
                a_at_origin = torch.zeros(1, model.m)
                Q_min_at_origin = model(s_origin, a_at_origin)
                penalty_origin = self.loss_fn_origin(Q_min_at_origin, torch.zeros_like(Q_min_at_origin))
                loss += self.weight_origin * penalty_origin
            if self.weight_nonneg is not None:
                # penalty 2: Q(x, u) >= 0
                penalty_nonneg = torch.sum(
                    torch.maximum(-Q_train, torch.zeros_like(Q_train))
                )
                loss += self.weight_nonneg * penalty_nonneg
            loss = loss / len(loader_train.dataset)
            loss.backward()
            total_norm = 0.0
            for p in model.parameters():
                param_norm = p.grad.data.norm(2)
                total_norm += param_norm.item() ** 2
            total_norm = total_norm ** 0.5
            total_norms.append(total_norm)
            # gradient clipping
            if self.grad_max_norm is not None:
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=self.grad_max_norm)
            optimiser.step()
        if scheduler is not None:
            if epoch <= self.lr_scheduler_max_epoch:
                scheduler.step()
        train_cycle_info = {
            "grad_norm": mean(total_norms),
        }
        return train_cycle_info

    # def test_cycle(self, model, loader_test, loss_fn,
    #                losses_td_test, losses_origin_test, losses_nonneg_test, losses_test):
    def test_cycle(self, model, loader_test, loss_fn):
        model.eval()
        with torch.no_grad():
            batch_loss_td_test = 0.0
            batch_penalty_origin_test = 0.0
            batch_penalty_nonneg_test = 0.0
            for s_test, a_test, c_test, s_next_test in loader_test:
                Q_test = model(s_test, a_test)
                u_next_test = model.minimise_tch(s_next_test)
                Q_next_optimal_test = model(s_next_test, u_next_test)
                td_target_test = c_test + self.gamma * Q_next_optimal_test
                # TD error
                loss_td_test = loss_fn(td_target_test, Q_test)
                batch_loss_td_test += loss_td_test.item()
                # origin penalty
                s_origin = torch.zeros(1, model.n)
                # a_at_origin = model.minimise_tch(s_origin)  # TODO: check this
                a_at_origin = torch.zeros(1, model.m)
                Q_min_at_origin = model(s_origin, a_at_origin)
                penalty_origin_test = loss_fn(Q_min_at_origin, torch.zeros_like(Q_min_at_origin))
                batch_penalty_origin_test += penalty_origin_test.item()
                # nonneg penalty
                penalty_nonneg_test = torch.sum(
                    torch.maximum(-Q_test, torch.zeros_like(Q_test))
                )
                batch_penalty_nonneg_test += penalty_nonneg_test.item()
                # total
            batch_loss_test = batch_loss_td_test
            if self.weight_origin is not None:
                batch_loss_test += self.weight_origin * batch_penalty_origin_test
            if self.weight_nonneg is not None:
                batch_loss_test += self.weight_nonneg * batch_penalty_nonneg_test
            # losses_td_test.append(batch_loss_td_test / len(loader_test.dataset))  # mean value; total sum / number of data
            # losses_origin_test.append(batch_penalty_origin_test / len(loader_test.dataset))  # mean value; total sum / number of data
            # losses_nonneg_test.append(batch_penalty_nonneg_test / len(loader_test.dataset))  # mean value; total sum / number of data
            # losses_test.append(batch_loss_test / len(loader_test.dataset))  # mean value; total sum / number of data
            test_cycle_info = {
                "loss_td_test": batch_loss_td_test / len(loader_test.dataset),
                "loss_origin_test": batch_penalty_origin_test / len(loader_test.dataset),
                "loss_nonneg_test": batch_penalty_nonneg_test / len(loader_test.dataset),
                "loss_test": batch_loss_test / len(loader_test.dataset),
            }
            return test_cycle_info

#     def train(self,
#               model: AbstractParametrisedConvexApproximator, data_buffer: DataBuffer,
#               loss_fn, optimiser, scheduler=None, callback_eval=None):
#         """
#         Off-the-shelf train method (could be deprecated soon)
#         """
#         assert isinstance(model, AbstractParametrisedConvexApproximator)  # considering inheritance
#         loader_train, loader_test = self.make_loaders(data_buffer)
#         # training
#         losses_td_test = []  # td error
#         losses_origin_test = []  # origin penalty
#         losses_nonneg_test = []  # nonneg penalty
#         losses_test = []  # total loss
#         early_stop = None
#         for epoch in range(1+self.epochs):
#             t0 = time.time()
#             # train
#             if epoch != 0:
#                 self.train_cycle(model, loader_train, loss_fn, optimiser, scheduler, epoch)
#             # test
#             self.test_cycle(model, loader_test, loss_fn,
#                             losses_td_test, losses_origin_test, losses_nonneg_test, losses_test)
#             t1 = time.time()
#             print(f"Elapsed time for this epoch: {t1-t0} s")
#             # prints
#             print(f"epoch: {epoch}/{self.epochs}")
#             print(f"loss_td: {losses_td_test[-1]}")
#             print(f"penalty_origin (not multiplied by penalty weight): {losses_origin_test[-1]}")
#             print(f"penalty_nonneg (not multiplied by penalty weight): {losses_nonneg_test[-1]}")
#             print(f"loss_total: {losses_test[-1]}")
#             if callback_eval is not None:
#                 early_stop = callback_eval(epoch)
#                 if early_stop:
#                     break
#         # retrieve results
#         train_info = {
#             "losses_td_test": losses_td_test,
#             "losses_origin_test": losses_origin_test,
#             "losses_nonneg_test": losses_nonneg_test,
#             "losses_test": losses_test,
#             "early_stop": early_stop,
#         }
#         return train_info
