

from .. import torch as pt
from ...ml import devices as cp_device
from .model_tools import ModelMethods as cc_ModelMethods
from ...maths import prod as cp_prod
import numpy as np
import math
import typing


class BasicPassiveSequenceClassifiers(pt.nn.Module, cc_ModelMethods):

    def __init__(
            self, n_features_inputs_classifiers: int,
            n_features_outs_classifiers: typing.Union[int, list, tuple, np.ndarray, pt.Tensor],
            biases_classifiers: typing.Union[bool, int, list, tuple, np.ndarray, pt.Tensor] = True,
            loss_weights_classifiers: typing.Union[int, float, list, tuple, np.ndarray, pt.Tensor, None] = None,
            batch_first: bool = False,
            device: typing.Union[pt.device, str, None] = None) -> None:

        super(BasicPassiveSequenceClassifiers, self).__init__()

        self.batch_first_inputs = self.batch_first_outs = batch_first

        self.n_axes_inputs = 3
        self.axes_inputs = np.arange(0, self.n_axes_inputs, 1, dtype='i')
        if self.batch_first_inputs:
            self.axis_batch_inputs = 0
            self.axis_time_inputs = 1
        else:
            self.axis_batch_inputs = 1
            self.axis_time_inputs = 0
        self.axis_features_inputs = 2

        self.n_axes_outs = 3
        self.axes_outs = np.arange(0, self.n_axes_outs, 1, dtype='i')
        self.axis_time_outs = self.axis_time_inputs
        self.axis_batch_outs = self.axis_batch_inputs
        self.axis_features_outs = self.axis_features_inputs
        self.axes_non_features_outs = np.asarray(
            [a for a in self.axes_outs if a != self.axis_features_outs], dtype='i')

        self.n_axes_losses = 3
        self.axes_losses = np.arange(0, self.n_axes_losses, 1, dtype='i')

        self.axis_models_losses = 0
        if self.axis_models_losses < 0:
            self.axis_models_losses += 1

        self.axis_time_losses = self.axis_time_outs
        if self.axis_time_outs > self.axis_features_outs:
            self.axis_time_losses -= 1
        if self.axis_time_losses >= self.axis_models_losses:
            self.axis_time_losses += 1

        self.axis_batch_losses = self.axis_batch_outs
        if self.axis_batch_outs > self.axis_features_outs:
            self.axis_batch_losses -= 1
        if self.axis_batch_losses >= self.axis_models_losses:
            self.axis_batch_losses += 1
        self.axes_non_models_losses = np.asarray(
            [a for a in self.axes_losses if a != self.axis_models_losses], dtype='i')

        self.axis_batch_losses_trials = 0
        self.axis_models_losses_trials = 1
        self.axis_time_losses_trials = 2
        self.n_axes_losses_trials = self.n_axes_losses
        self.axes_losses_trials = np.arange(0, self.n_axes_losses_trials, 1, dtype='i')
        self.axes_losses_trials_in_losses = [self.axis_batch_losses, self.axis_models_losses, self.axis_time_losses]
        self.destination_axes_losses_trials = [
            a for a in range(0, self.n_axes_losses_trials, 1) if a != self.axes_losses_trials_in_losses[a]]
        self.source_axes_losses_trials = [
            self.axes_losses_trials_in_losses[a] for a in self.destination_axes_losses_trials]
        self.n_moves_axes_losses_trials = len(self.source_axes_losses_trials)
        self.move_axes_losses_trials = self.n_moves_axes_losses_trials > 0

        self.axis_batch_outs_trials = 0
        self.axis_features_outs_trials = 1
        self.axis_time_outs_trials = 2
        self.n_axes_outs_trials = self.n_axes_outs
        self.axes_outs_trials = np.arange(0, self.n_axes_outs_trials, 1, dtype='i')
        self.axes_outs_trials_in_outs = [self.axis_batch_outs, self.axis_features_outs, self.axis_time_outs]
        self.destination_axes_outs_trials = [
            a for a in range(0, self.n_axes_outs_trials, 1) if a != self.axes_outs_trials_in_outs[a]]
        self.source_axes_outs_trials = [
            self.axes_outs_trials_in_outs[a] for a in self.destination_axes_outs_trials]
        self.n_moves_axes_outs_trials = len(self.source_axes_outs_trials)
        self.move_axes_outs_trials = self.n_moves_axes_outs_trials > 0

        self.n_features_inputs_classifiers = n_features_inputs_classifiers

        if isinstance(n_features_outs_classifiers, int):
            self.n_features_outs_classifiers = [n_features_outs_classifiers]
        elif isinstance(n_features_outs_classifiers, list):
            self.n_features_outs_classifiers = n_features_outs_classifiers
        elif isinstance(n_features_outs_classifiers, tuple):
            self.n_features_outs_classifiers = list(n_features_outs_classifiers)
        elif isinstance(n_features_outs_classifiers, (np.ndarray, pt.Tensor)):
            self.n_features_outs_classifiers = n_features_outs_classifiers.tolist()
        else:
            raise TypeError('n_features_outs_classifiers')

        self.n_outputs = self.O = self.n_dimensions_classes = self.C = len(self.n_features_outs_classifiers)

        if isinstance(biases_classifiers, bool):
            self.biases_classifiers = [biases_classifiers]
        elif isinstance(biases_classifiers, int):
            self.biases_classifiers = [bool(biases_classifiers)]
        elif isinstance(biases_classifiers, list):
            self.biases_classifiers = biases_classifiers
        elif isinstance(biases_classifiers, tuple):
            self.biases_classifiers = list(biases_classifiers)
        elif isinstance(biases_classifiers, (np.ndarray, pt.Tensor)):
            self.biases_classifiers = biases_classifiers.tolist()
        else:
            raise TypeError('biases_classifiers')

        if len(self.biases_classifiers) != self.C:
            if len(self.biases_classifiers) == 1:
                self.biases_classifiers = [self.biases_classifiers[0] for c in range(self.C)]
            else:
                raise ValueError('biases_classifiers = ' + str(biases_classifiers))

        if loss_weights_classifiers is None:
            loss_weight_classifier_c = 1.0 / self.C
            self.loss_weights_classifiers = [loss_weight_classifier_c for c in range(self.C)]
        elif isinstance(loss_weights_classifiers, int):
            self.loss_weights_classifiers = [float(loss_weights_classifiers)]
        elif isinstance(loss_weights_classifiers, float):
            self.loss_weights_classifiers = [loss_weights_classifiers]
        elif isinstance(loss_weights_classifiers, list):
            self.loss_weights_classifiers = loss_weights_classifiers
        elif isinstance(loss_weights_classifiers, tuple):
            self.loss_weights_classifiers = list(loss_weights_classifiers)
        elif isinstance(loss_weights_classifiers, (np.ndarray, pt.Tensor)):
            self.loss_weights_classifiers = loss_weights_classifiers.tolist()
        else:
            raise TypeError('loss_weights_classifiers')

        if len(self.loss_weights_classifiers) != self.C:
            if len(self.loss_weights_classifiers) == 1:
                self.loss_weights_classifiers = [self.loss_weights_classifiers[0] for c in range(self.C)]
            else:
                raise ValueError('loss_weights_classifiers = ' + str(loss_weights_classifiers))

        sum_loss_weights_classifiers = sum(self.loss_weights_classifiers)
        self.loss_weights_classifiers = [
            (self.loss_weights_classifiers[c] / sum_loss_weights_classifiers) for c in range(self.C)]
        self.sum_loss_weights_classifiers = sum(self.loss_weights_classifiers)

        self.device = cp_device.define_device(device)

        self.classifiers = pt.nn.ModuleList([pt.nn.Linear(
            self.n_features_inputs_classifiers, self.n_features_outs_classifiers[c],
            bias=self.biases_classifiers[c], device=self.device) for c in range(0, self.C, 1)])
        # self.classifiers = pt.nn.ModuleList([pt.nn.Linear(
        #     self.n_features_inputs_classifiers[c], self.n_features_outs_classifiers[c],
        #     bias=self.biases_classifiers[c]) for c in range(0, self.C, 1)])
        # self.classifiers.to(self.device)

        self.criterion_predictions_classes = pt.nn.CrossEntropyLoss(reduction='none')
        self.criterion_predictions_classes_reduction = pt.nn.CrossEntropyLoss(reduction='mean')

        self.shape_losses = np.asarray(
            [self.C if a == self.axis_models_losses else -1 for a in range(0, self.n_axes_losses, 1)],
            dtype='i')

        self.softmax = pt.nn.Softmax(dim=self.axis_features_outs)

        self.to(self.device)

    def forward(self, x):

        predictions_classes = [self.classifiers[c](x) for c in range(0, self.C, 1)]

        return predictions_classes

    def compute_probabilities(self, predictions_classes):

        probabilities = [self.softmax(predictions_classes[c]) for c in range(0, self.C, 1)]

        return probabilities

    def reduce_losses(
            self, losses: typing.Union[pt.Tensor, np.ndarray],
            weigh: bool = True, type_models: typing.Optional[int] = None,
            axes_not_included: typing.Union[int, list, tuple, np.ndarray, pt.Tensor] = None):

        if axes_not_included is None:
            axes_not = []
        elif isinstance(axes_not_included, int):
            axes_not = [axes_not_included + self.n_axes_losses if axes_not_included < 0 else axes_not_included]
        elif isinstance(axes_not_included, (list, tuple)):
            axes_not = [a + self.n_axes_losses if a < 0 else a for a in axes_not_included]
        elif isinstance(axes_not_included, (np.ndarray, pt.Tensor)):
            axes_not = [a + self.n_axes_losses if a < 0 else a for a in axes_not_included.tolist()]
        else:
            raise TypeError('axes_not_included')

        n_axes_not = len(axes_not)

        if weigh:
            if type_models == 0:
                loss_weights_models = self.loss_weights_classifiers
                M = self.C
            else:
                raise ValueError('type_models')

            if n_axes_not == 0:
                axes_included = [
                    a for a in range(0, losses.ndim, 1) if a != self.axis_models_losses]

                reduced_class_prediction_losses = pt.mean(losses, dim=axes_included, keepdim=False)
                for m in range(0, M, 1):
                    reduced_class_prediction_losses[m] *= loss_weights_models[m]
                reduced_class_prediction_losses = pt.sum(reduced_class_prediction_losses)

            elif self.axis_models_losses not in axes_not:
                axes_included = [
                    a for a in range(0, losses.ndim, 1)
                    if (a not in axes_not) and (a != self.axis_models_losses)]
                reduced_class_prediction_losses = pt.mean(losses, dim=axes_included, keepdim=False)

                new_axis_models_losses = self.axis_models_losses
                for a in axes_included:
                    if a < self.axis_models_losses:
                        new_axis_models_losses -= 1
                indexes_losses = [
                    slice(0, reduced_class_prediction_losses.shape[a], 1)
                    for a in range(0, reduced_class_prediction_losses.ndim, 1)]
                for m in range(0, M, 1):
                    indexes_losses[new_axis_models_losses] = m
                    reduced_class_prediction_losses[tuple(indexes_losses)] *= loss_weights_models[m]
                reduced_class_prediction_losses = pt.sum(
                    reduced_class_prediction_losses, dim=new_axis_models_losses, keepdim=False)
            else:
                # axes_included = [a for a in range(0, class_prediction_losses.ndim, 1) if a not in axes_not]
                # reduced_class_prediction_losses = pt.mean(class_prediction_losses, dim=axes_included, keepdim=False)
                raise ValueError('axes_not_included')
        else:
            if n_axes_not == 0:
                reduced_class_prediction_losses = pt.mean(losses)
            else:
                axes_included = [a for a in range(0, losses.ndim, 1) if a not in axes_not]
                reduced_class_prediction_losses = pt.mean(losses, dim=axes_included, keepdim=False)

        return reduced_class_prediction_losses

    def compute_class_prediction_losses(self, predictions_classes, labels):

        self.shape_losses[self.axes_non_models_losses] = [
            predictions_classes[0].shape[a] for a in self.axes_non_features_outs]

        class_prediction_losses = pt.empty(
            self.shape_losses.tolist(), dtype=pt.float32, device=self.device, requires_grad=False)

        indexes_losses = [
            slice(0, class_prediction_losses.shape[a], 1) for a in range(0, class_prediction_losses.ndim, 1)]

        for c in range(0, self.C, 1):
            indexes_losses[self.axis_models_losses] = c
            tuple_indexes_losses = tuple(indexes_losses)

            if self.axis_features_outs == 1:
                class_prediction_losses[tuple_indexes_losses] = self.criterion_predictions_classes(
                    predictions_classes[c], labels[tuple_indexes_losses])
            else:
                class_prediction_losses[tuple_indexes_losses] = self.criterion_predictions_classes(
                    pt.movedim(predictions_classes[c], self.axis_features_outs, 1), labels[tuple_indexes_losses])

        return class_prediction_losses

    def compute_classifications(self, predictions_classes, axis_classes=None):

        if axis_classes is None:
            axis_classes = self.axis_features_outs

        self.shape_losses[self.axis_models_losses] = self.C
        self.shape_losses[self.axes_non_models_losses] = [
            predictions_classes[0].shape[a] for a in self.axes_non_features_outs]

        classifications = pt.empty(self.shape_losses.tolist(), dtype=pt.int64, device=self.device, requires_grad=False)
        indexes_classifications = [slice(0, classifications.shape[a], 1) for a in range(0, classifications.ndim, 1)]

        for c in range(0, self.C, 1):

            indexes_classifications[self.axis_models_losses] = c

            classifications[tuple(indexes_classifications)] = pt.max(
                predictions_classes[c], dim=axis_classes, keepdim=False)[1]

        return classifications

    def compute_correct_classifications(
            self, classifications: typing.Union[pt.Tensor, np.ndarray],
            labels: typing.Union[pt.Tensor, np.ndarray]):

        correct_classifications = (classifications == labels).long()

        return correct_classifications

    def compute_n_corrects(
            self, correct_classifications: typing.Union[pt.Tensor, np.ndarray],
            axes_not_included: typing.Union[int, list, tuple, np.ndarray, pt.Tensor] = None, keepdim: bool = False):

        if axes_not_included is None:
            axes_not = []
        elif isinstance(axes_not_included, int):
            axes_not = [axes_not_included + self.n_axes_losses if axes_not_included < 0 else axes_not_included]
        elif isinstance(axes_not_included, (list, tuple)):
            axes_not = [a + self.n_axes_losses if a < 0 else a for a in axes_not_included]
        elif isinstance(axes_not_included, (np.ndarray, pt.Tensor)):
            axes_not = [a + self.n_axes_losses if a < 0 else a for a in axes_not_included.tolist()]
        else:
            raise TypeError('axes_not_included')

        n_axes_not = len(axes_not)

        if n_axes_not == 0:
            n_corrects = pt.sum(correct_classifications).item()
        else:
            axes_included = [a for a in range(0, correct_classifications.ndim, 1) if a not in axes_not]
            n_corrects = pt.sum(correct_classifications, dim=axes_included, keepdim=keepdim)

        return n_corrects

    def compute_n_classifications(
            self, classifications, axes_not_included: typing.Union[int, list, tuple, np.ndarray, pt.Tensor] = None):

        if axes_not_included is None:
            axes_not = []
        elif isinstance(axes_not_included, int):
            axes_not = [axes_not_included + self.n_axes_losses if axes_not_included < 0 else axes_not_included]
        elif isinstance(axes_not_included, (list, tuple)):
            axes_not = [a + self.n_axes_losses if a < 0 else a for a in axes_not_included]
        elif isinstance(axes_not_included, (np.ndarray, pt.Tensor)):
            axes_not = [a + self.n_axes_losses if a < 0 else a for a in axes_not_included.tolist()]
        else:
            raise TypeError('axes_not_included')

        n_axes_not = len(axes_not)

        if n_axes_not == 0:
            n_classifications = cp_prod(classifications.shape)
        else:
            axes_included = [a for a in range(0, classifications.ndim, 1) if a not in axes_not]
            n_classifications = cp_prod(np.asarray(classifications.shape, dtype='i')[axes_included])

        return n_classifications

    def compute_losses_trials(self, losses):

        if self.move_axes_losses_trials:

            if isinstance(losses, pt.Tensor):
                losses_trials = pt.moveaxis(
                    input=losses,
                    source=self.source_axes_losses_trials,
                    destination=self.destination_axes_losses_trials).tolist()
            else:
                losses_trials = np.moveaxis(
                    a=losses,
                    source=self.source_axes_losses_trials,
                    destination=self.destination_axes_losses_trials)
        else:
            losses_trials = losses.tolist()

        return losses_trials

    def compute_outs_trials(self, outs):

        M = len(outs)

        if isinstance(outs[0], pt.Tensor):
            if self.move_axes_outs_trials:
                outs_trials = pt.cat([
                    pt.moveaxis(
                        input=outs[m],
                        source=self.source_axes_outs_trials,
                        destination=self.destination_axes_outs_trials) for m in range(0, M, 1)],
                    dim=self.axis_features_outs_trials).tolist()
            else:
                outs_trials = pt.cat(
                    outs, dim=self.axis_features_outs_trials).tolist()
        else:
            if self.move_axes_outs_trials:

                outs_trials = np.concatenate([
                    np.moveaxis(
                        a=outs[m],
                        source=self.source_axes_outs_trials,
                        destination=self.destination_axes_outs_trials) for m in range(0, M, 1)],
                    axis=self.axis_features_outs_trials).tolist()
            else:
                outs_trials = np.concatenate(
                    outs, axis=self.axis_features_outs_trials).tolist()

        return outs_trials


class BasicPassiveRecurrentClassifiers(BasicPassiveSequenceClassifiers):

    def __init__(
            self, n_features_inputs_lstm: int, n_features_outs_lstm: int,
            n_features_outs_classifiers: typing.Union[int, list, tuple, np.ndarray, pt.Tensor],
            n_layers_lstm: int = 1, bias_lstm: typing.Union[bool, int] = True,
            dropout_lstm: typing.Union[int, float] = 0, bidirectional_lstm: bool = False,
            biases_classifiers: typing.Union[bool, int, list, tuple, np.ndarray, pt.Tensor] = True,
            loss_weights_classifiers: typing.Union[int, float, list, tuple, np.ndarray, pt.Tensor, None] = None,
            batch_first: bool = False, return_hc=True, device: typing.Union[pt.device, str, None] = None) -> None:

        self.n_features_inputs_lstm = n_features_inputs_lstm
        self.n_features_outs_lstm = n_features_outs_lstm

        self.n_layers_lstm = n_layers_lstm

        if isinstance(bias_lstm, bool):
            self.bias_lstm = bias_lstm
        elif isinstance(bias_lstm, int):
            self.bias_lstm = bool(bias_lstm)
        else:
            raise TypeError('bias_lstm = ' + str(bias_lstm))

        self.batch_first_lstm = batch_first

        self.dropout_lstm = dropout_lstm

        self.bidirectional_lstm = bidirectional_lstm
        if self.bidirectional_lstm:
            self.n_outs_lstm = self.num_directions_lstm = 2
        else:
            self.n_outs_lstm = self.num_directions_lstm = 1

        self.n_features_all_outs_lstm = self.n_features_outs_lstm * self.n_outs_lstm

        self.device = cp_device.define_device(device)

        super(BasicPassiveRecurrentClassifiers, self).__init__(
            n_features_inputs_classifiers=self.n_features_all_outs_lstm,
            n_features_outs_classifiers=n_features_outs_classifiers,
            biases_classifiers=biases_classifiers,
            loss_weights_classifiers=loss_weights_classifiers,
            batch_first=batch_first,
            device=self.device)

        # lstm tutorials at:
        # https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html
        # https://pytorch.org/tutorials/beginner/nlp/sequence_models_tutorial.html

        self.lstm = pt.nn.LSTM(
            self.n_features_inputs_lstm, self.n_features_outs_lstm,
            num_layers=self.n_layers_lstm, bias=self.bias_lstm,
            batch_first=self.batch_first_lstm, dropout=self.dropout_lstm,
            bidirectional=self.bidirectional_lstm, device=self.device)
        # self.lstm.to(self.device)

        self.return_hc = return_hc

        self.to(self.device)

    def forward(self, x, h=None, c=None):

        if h is None:
            batch_size = x.shape[self.axis_batch_inputs]

            if c is None:
                h, c = self.init_hidden_state(batch_size)
            else:
                h = self.init_h(batch_size)

        elif c is None:
            batch_size = x.shape[self.axis_batch_inputs]
            c = self.init_c(batch_size)

        x, (h, c) = self.lstm(x, (h, c))

        predictions_classes = [self.classifiers[c](x) for c in range(0, self.C, 1)]

        if self.return_hc:
            return predictions_classes, (h, c)
        else:
            return predictions_classes

    def init_h(self, batch_size):

        h = pt.zeros(
            [self.num_directions_lstm * self.n_layers_lstm, batch_size, self.n_features_outs_lstm],
            dtype=pt.float32, device=self.device, requires_grad=False)

        return h

    def init_c(self, batch_size):

        c = pt.zeros(
            [self.num_directions_lstm * self.n_layers_lstm, batch_size, self.n_features_outs_lstm],
            dtype=pt.float32, device=self.device, requires_grad=False)

        return c

    def init_hidden_state(self, batch_size):

        h = self.init_h(batch_size)
        c = self.init_c(batch_size)

        return h, c
