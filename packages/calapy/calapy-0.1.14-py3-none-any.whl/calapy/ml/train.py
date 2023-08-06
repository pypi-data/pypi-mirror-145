# websites:
# https://pytorch.org/docs/stable/torchvision/transforms.html
# https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#sphx-glr-beginner-blitz-cifar10-tutorial-py
# https://pytorch.org/hub/pytorch_vision_resnet/
# https://discuss.pytorch.org/t/normalize-each-input-image-in-a-batch-independently-and-inverse-normalize-the-output/23739
# https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html

from . import torch as pt
import numpy as np
import typing
import math
import os
import copy
from .. import txt as cp_txt
from .. import clock as cp_clock
from .. import strings as cp_strings


def passive_feature_sequence_classifiers(
        model, loader, optimizer, scheduler, I=10, E=None, directory_outputs=None):
    cp_timer = cp_clock.Timer()

    if model.training:
        model.eval()
    model.freeze()
    pt.set_grad_enabled(False)

    for key_loader_k in loader.keys():
        if key_loader_k == 'training' or key_loader_k == 'validation':
            pass
        else:
            raise ValueError('Unknown keys in loader')

    headers = [
        'Epoch', 'Unsuccessful_Epochs',

        'Training_Unweighted_Class_Prediction_Loss',
        'Training_Weighted_Class_Prediction_Loss',
        'Training_Accuracy',

        'Training_Unweighted_Class_Prediction_Loss_In_Last_Time_Point',
        'Training_Weighted_Class_Prediction_Loss_In_Last_Time_Point',
        'Training_Accuracy_In_Last_Time_Point',

        'Training_Unweighted_Class_Prediction_Losses_In_Each_Time_Point',
        'Training_Weighted_Class_Prediction_Losses_In_Each_Time_Point',
        'Training_Accuracy_In_Each_Time_Point',

        'Validation_Unweighted_Class_Prediction_Loss',
        'Lowest_Validation_Unweighted_Class_Prediction_Loss',
        'Is_Lower_Validation_Unweighted_Class_Prediction_Loss',

        'Validation_Weighted_Class_Prediction_Loss',
        'Lowest_Validation_Weighted_Class_Prediction_Loss',
        'Is_Lower_Validation_Weighted_Class_Prediction_Loss',

        'Validation_Accuracy',
        'Highest_Validation_Accuracy',
        'Is_Higher_Accuracy',

        'Validation_Unweighted_Class_Prediction_Loss_In_Last_Time_Point',
        'Validation_Weighted_Class_Prediction_Loss_In_Last_Time_Point',
        'Validation_Accuracy_In_Last_Time_Point',

        'Validation_Unweighted_Class_Prediction_Losses_In_Each_Time_Point',
        'Validation_Weighted_Class_Prediction_Losses_In_Each_Time_Point',
        'Validation_Accuracy_In_Each_Time_Point']

    n_columns = len(headers)
    new_line_stats = [None for i in range(0, n_columns, 1)]  # type: list

    stats = {
        'headers': {headers[k]: k for k in range(n_columns)},
        'n_columns': n_columns,
        'lines': []}

    if directory_outputs is None:
        directory_outputs = 'outputs'
    os.makedirs(directory_outputs, exist_ok=True)

    directory_model_at_last_epoch = os.path.join(directory_outputs, 'model_at_last_epoch.pth')

    directory_model_with_lowest_unweighted_class_prediction_loss = os.path.join(
        directory_outputs, 'model_with_lowest_unweighted_class_prediction_loss.pth')

    directory_model_with_lowest_weighted_class_prediction_loss = os.path.join(
        directory_outputs, 'model_with_lowest_weighted_class_prediction_loss.pth')

    directory_model_with_highest_accuracy = os.path.join(directory_outputs, 'model_with_highest_accuracy.pth')

    directory_stats = os.path.join(directory_outputs, 'stats.csv')

    separators_times = '  '

    n_decimals_for_printing = 6
    n_dashes = 150
    dashes = '-' * n_dashes
    print(dashes)

    lowest_unweighted_class_prediction_loss = math.inf
    lowest_unweighted_class_prediction_loss_str = str(lowest_unweighted_class_prediction_loss)

    lowest_weighted_class_prediction_loss = math.inf
    lowest_weighted_class_prediction_loss_str = str(lowest_weighted_class_prediction_loss)

    highest_accuracy = -math.inf
    highest_accuracy_str = str(highest_accuracy)

    if E is None:
        E = math.inf

    if I is None:
        I = math.inf

    i = 0
    e = 0

    while (e < E) and (i < I):

        print('Epoch {e} ...'.format(e=e))

        stats['lines'].append(new_line_stats.copy())
        stats['lines'][e][stats['headers']['Epoch']] = e

        # Each epoch has a training and a validation phase
        # training phase

        running_n_corrects_e = 0
        running_n_classifications_e = 0
        running_unweighted_class_prediction_loss_e = 0.0
        running_weighted_class_prediction_loss_e = 0.0

        running_n_corrects_T_e = 0  # type: typing.Union[int, float, list, tuple, np.ndarray, torch.Tensor]
        running_n_classifications_T_e = 0  # type: typing.Union[int, float, list, tuple, np.ndarray, torch.Tensor]
        running_unweighted_class_prediction_losses_T_e = 0.0  # type: typing.Union[int, float, list, tuple, np.ndarray, torch.Tensor]
        running_weighted_class_prediction_losses_T_e = 0.0  # type: typing.Union[int, float, list, tuple, np.ndarray, torch.Tensor]

        b = 0
        # Iterate over data.
        for batch_eb, labels_eb in loader['training']:
            # zero the parameter gradients
            optimizer.zero_grad()

            # forward
            # track history
            pt.set_grad_enabled(True)
            model.unfreeze()
            model.train()

            predictions_classes_eb = model(batch_eb)

            # compute class prediction loss
            class_prediction_losses_eb = model.compute_class_prediction_losses(
                predictions_classes=predictions_classes_eb, labels=labels_eb)

            weighted_class_prediction_loss_eb = model.reduce_losses(
                losses=class_prediction_losses_eb, weigh=True, type_models=0, axes_not_included=None)

            # backward + optimize
            weighted_class_prediction_loss_eb.backward()
            optimizer.step()

            model.eval()
            model.freeze()
            pt.set_grad_enabled(False)

            unweighted_class_prediction_loss_eb = model.reduce_losses(
                losses=class_prediction_losses_eb, weigh=False, type_models=0, axes_not_included=None)

            # compute accuracy
            classifications_eb = model.compute_classifications(
                predictions_classes=predictions_classes_eb, axis_classes=None)
            correct_classifications_eb = model.compute_correct_classifications(
                classifications=classifications_eb, labels=labels_eb)
            n_corrects_eb = model.compute_n_corrects(
                correct_classifications=correct_classifications_eb, axes_not_included=None, keepdim=False)
            n_classifications_eb = model.compute_n_classifications(
                classifications=classifications_eb, axes_not_included=None)

            running_n_corrects_e += n_corrects_eb
            running_n_classifications_e += n_classifications_eb
            running_unweighted_class_prediction_loss_e += unweighted_class_prediction_loss_eb.item() * n_classifications_eb
            running_weighted_class_prediction_loss_e += weighted_class_prediction_loss_eb.item() * n_classifications_eb

            # compute accuracy for each time point
            n_corrects_T_eb = model.compute_n_corrects(
                correct_classifications=correct_classifications_eb,
                axes_not_included=model.axis_time_losses, keepdim=False)
            n_classifications_T_eb = model.compute_n_classifications(
                classifications=classifications_eb, axes_not_included=model.axis_time_losses)

            # compute class prediction loss for each time point
            unweighted_class_prediction_losses_T_eb = model.reduce_losses(
                losses=class_prediction_losses_eb, weigh=False, type_models=0,
                axes_not_included=model.axis_time_losses)
            weighted_class_prediction_losses_T_eb = model.reduce_losses(
                losses=class_prediction_losses_eb, weigh=True, type_models=0,
                axes_not_included=model.axis_time_losses)

            running_n_corrects_T_e += n_corrects_T_eb
            running_n_classifications_T_e += n_classifications_T_eb
            running_unweighted_class_prediction_losses_T_e += unweighted_class_prediction_losses_T_eb * n_classifications_T_eb
            running_weighted_class_prediction_losses_T_e += weighted_class_prediction_losses_T_eb * n_classifications_T_eb

            b += 1

        # scheduler.step()

        unweighted_class_prediction_loss_e = running_unweighted_class_prediction_loss_e / running_n_classifications_e
        weighted_class_prediction_loss_e = running_weighted_class_prediction_loss_e / running_n_classifications_e
        accuracy_e = running_n_corrects_e / running_n_classifications_e

        unweighted_class_prediction_losses_T_e = (
                running_unweighted_class_prediction_losses_T_e / running_n_classifications_T_e)
        weighted_class_prediction_losses_T_e = (
                running_weighted_class_prediction_losses_T_e / running_n_classifications_T_e)
        accuracy_T_e = running_n_corrects_T_e / running_n_classifications_T_e

        last_unweighted_class_prediction_loss_e = unweighted_class_prediction_losses_T_e[-1].item()
        last_weighted_class_prediction_loss_e = weighted_class_prediction_losses_T_e[-1].item()
        last_accuracy_e = accuracy_T_e[-1].item()

        stats['lines'][e][stats['headers']['Training_Unweighted_Class_Prediction_Loss']] = (
            unweighted_class_prediction_loss_e)
        stats['lines'][e][stats['headers']['Training_Weighted_Class_Prediction_Loss']] = (
            weighted_class_prediction_loss_e)
        stats['lines'][e][stats['headers']['Training_Accuracy']] = accuracy_e

        stats['lines'][e][stats['headers']['Training_Unweighted_Class_Prediction_Loss_In_Last_Time_Point']] = (
            last_unweighted_class_prediction_loss_e)
        stats['lines'][e][stats['headers']['Training_Weighted_Class_Prediction_Loss_In_Last_Time_Point']] = (
            last_weighted_class_prediction_loss_e)
        stats['lines'][e][stats['headers']['Training_Accuracy_In_Last_Time_Point']] = last_accuracy_e

        stats['lines'][e][stats['headers']['Training_Unweighted_Class_Prediction_Losses_In_Each_Time_Point']] = (
            separators_times.join([str(t) for t in unweighted_class_prediction_losses_T_e.tolist()]))
        stats['lines'][e][stats['headers']['Training_Weighted_Class_Prediction_Losses_In_Each_Time_Point']] = (
            separators_times.join([str(t) for t in weighted_class_prediction_losses_T_e.tolist()]))

        stats['lines'][e][stats['headers']['Training_Accuracy_In_Each_Time_Point']] = separators_times.join(
            [str(t) for t in accuracy_T_e.tolist()])

        unweighted_class_prediction_loss_str_e = cp_strings.format_float_to_str(
            unweighted_class_prediction_loss_e, n_decimals=n_decimals_for_printing)
        weighted_class_prediction_loss_str_e = cp_strings.format_float_to_str(
            weighted_class_prediction_loss_e, n_decimals=n_decimals_for_printing)
        accuracy_str_e = cp_strings.format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

        print(
            'Epoch: {e:d}. Training. Unweighted Classification Loss: {class_prediction_loss:s}. Accuracy: {accuracy:s}.'.format(
                e=e, class_prediction_loss=unweighted_class_prediction_loss_str_e, accuracy=accuracy_str_e))

        # validation phase

        running_n_corrects_e = 0
        running_n_classifications_e = 0
        running_unweighted_class_prediction_loss_e = 0.0
        running_weighted_class_prediction_loss_e = 0.0

        running_n_corrects_T_e = 0
        running_n_classifications_T_e = 0
        running_unweighted_class_prediction_losses_T_e = 0.0
        running_weighted_class_prediction_losses_T_e = 0.0

        b = 0
        # Iterate over data.
        for batch_eb, labels_eb in loader['validation']:
            predictions_classes_eb = model(batch_eb)

            # compute accuracy
            classifications_eb = model.compute_classifications(
                predictions_classes=predictions_classes_eb, axis_classes=None)
            correct_classifications_eb = model.compute_correct_classifications(
                classifications=classifications_eb, labels=labels_eb)
            n_corrects_eb = model.compute_n_corrects(
                correct_classifications=correct_classifications_eb, axes_not_included=None, keepdim=False)
            n_classifications_eb = model.compute_n_classifications(
                classifications=classifications_eb, axes_not_included=None)

            # compute class prediction loss
            class_prediction_losses_eb = model.compute_class_prediction_losses(
                predictions_classes=predictions_classes_eb, labels=labels_eb)

            unweighted_class_prediction_loss_eb = model.reduce_losses(
                losses=class_prediction_losses_eb, weigh=False, type_models=0, axes_not_included=None)
            weighted_class_prediction_loss_eb = model.reduce_losses(
                losses=class_prediction_losses_eb, weigh=True, type_models=0, axes_not_included=None)

            running_n_corrects_e += n_corrects_eb
            running_n_classifications_e += n_classifications_eb
            running_unweighted_class_prediction_loss_e += unweighted_class_prediction_loss_eb.item() * n_classifications_eb
            running_weighted_class_prediction_loss_e += weighted_class_prediction_loss_eb.item() * n_classifications_eb

            # compute accuracy for each time point
            n_corrects_T_eb = model.compute_n_corrects(
                correct_classifications=correct_classifications_eb,
                axes_not_included=model.axis_time_losses, keepdim=False)
            n_classifications_T_eb = model.compute_n_classifications(
                classifications=classifications_eb, axes_not_included=model.axis_time_losses)

            # compute class prediction loss for each time point
            unweighted_class_prediction_losses_T_eb = model.reduce_losses(
                losses=class_prediction_losses_eb, weigh=False, type_models=0,
                axes_not_included=model.axis_time_losses)
            weighted_class_prediction_losses_T_eb = model.reduce_losses(
                losses=class_prediction_losses_eb, weigh=True, type_models=0,
                axes_not_included=model.axis_time_losses)

            running_n_corrects_T_e += n_corrects_T_eb
            running_n_classifications_T_e += n_classifications_T_eb
            running_unweighted_class_prediction_losses_T_e += unweighted_class_prediction_losses_T_eb * n_classifications_T_eb
            running_weighted_class_prediction_losses_T_e += weighted_class_prediction_losses_T_eb * n_classifications_T_eb

            b += 1

        unweighted_class_prediction_loss_e = running_unweighted_class_prediction_loss_e / running_n_classifications_e
        weighted_class_prediction_loss_e = running_weighted_class_prediction_loss_e / running_n_classifications_e
        accuracy_e = running_n_corrects_e / running_n_classifications_e

        unweighted_class_prediction_losses_T_e = (
                running_unweighted_class_prediction_losses_T_e / running_n_classifications_T_e)
        weighted_class_prediction_losses_T_e = (
                running_weighted_class_prediction_losses_T_e / running_n_classifications_T_e)
        accuracy_T_e = running_n_corrects_T_e / running_n_classifications_T_e

        last_unweighted_class_prediction_loss_e = unweighted_class_prediction_losses_T_e[-1].item()
        last_weighted_class_prediction_loss_e = weighted_class_prediction_losses_T_e[-1].item()
        last_accuracy_e = accuracy_T_e[-1].item()

        stats['lines'][e][stats['headers']['Validation_Unweighted_Class_Prediction_Loss']] = (
            unweighted_class_prediction_loss_e)
        stats['lines'][e][stats['headers']['Validation_Weighted_Class_Prediction_Loss']] = (
            weighted_class_prediction_loss_e)
        stats['lines'][e][stats['headers']['Validation_Accuracy']] = accuracy_e

        stats['lines'][e][stats['headers']['Validation_Unweighted_Class_Prediction_Loss_In_Last_Time_Point']] = (
            last_unweighted_class_prediction_loss_e)
        stats['lines'][e][stats['headers']['Validation_Weighted_Class_Prediction_Loss_In_Last_Time_Point']] = (
            last_weighted_class_prediction_loss_e)
        stats['lines'][e][stats['headers']['Validation_Accuracy_In_Last_Time_Point']] = last_accuracy_e

        stats['lines'][e][stats['headers']['Validation_Unweighted_Class_Prediction_Losses_In_Each_Time_Point']] = (
            separators_times.join([str(t) for t in unweighted_class_prediction_losses_T_e.tolist()]))
        stats['lines'][e][stats['headers']['Validation_Weighted_Class_Prediction_Losses_In_Each_Time_Point']] = (
            separators_times.join([str(t) for t in weighted_class_prediction_losses_T_e.tolist()]))

        stats['lines'][e][stats['headers']['Validation_Accuracy_In_Each_Time_Point']] = (
            separators_times.join([str(t) for t in accuracy_T_e.tolist()]))

        model_dict = copy.deepcopy(model.state_dict())
        if os.path.isfile(directory_model_at_last_epoch):
            os.remove(directory_model_at_last_epoch)
        pt.save(model_dict, directory_model_at_last_epoch)

        is_successful_epoch = False

        if unweighted_class_prediction_loss_e < lowest_unweighted_class_prediction_loss:

            lowest_unweighted_class_prediction_loss = unweighted_class_prediction_loss_e
            lowest_unweighted_class_prediction_loss_str = cp_strings.format_float_to_str(
                lowest_unweighted_class_prediction_loss, n_decimals=n_decimals_for_printing)

            stats['lines'][e][stats['headers']['Is_Lower_Validation_Unweighted_Class_Prediction_Loss']] = 1
            is_successful_epoch = True

            if os.path.isfile(directory_model_with_lowest_unweighted_class_prediction_loss):
                os.remove(directory_model_with_lowest_unweighted_class_prediction_loss)
            pt.save(model_dict, directory_model_with_lowest_unweighted_class_prediction_loss)
        else:
            stats['lines'][e][stats['headers']['Is_Lower_Validation_Unweighted_Class_Prediction_Loss']] = 0

        stats['lines'][e][stats['headers']['Lowest_Validation_Unweighted_Class_Prediction_Loss']] = (
            lowest_unweighted_class_prediction_loss)

        if weighted_class_prediction_loss_e < lowest_weighted_class_prediction_loss:

            lowest_weighted_class_prediction_loss = weighted_class_prediction_loss_e
            lowest_weighted_class_prediction_loss_str = cp_strings.format_float_to_str(
                lowest_weighted_class_prediction_loss, n_decimals=n_decimals_for_printing)

            stats['lines'][e][stats['headers']['Is_Lower_Validation_Weighted_Class_Prediction_Loss']] = 1
            is_successful_epoch = True

            if os.path.isfile(directory_model_with_lowest_weighted_class_prediction_loss):
                os.remove(directory_model_with_lowest_weighted_class_prediction_loss)
            pt.save(model_dict, directory_model_with_lowest_weighted_class_prediction_loss)
        else:
            stats['lines'][e][stats['headers']['Is_Lower_Validation_Weighted_Class_Prediction_Loss']] = 0

        stats['lines'][e][stats['headers']['Lowest_Validation_Weighted_Class_Prediction_Loss']] = (
            lowest_weighted_class_prediction_loss)

        if accuracy_e > highest_accuracy:
            highest_accuracy = accuracy_e
            highest_accuracy_str = cp_strings.format_float_to_str(
                highest_accuracy, n_decimals=n_decimals_for_printing)

            stats['lines'][e][stats['headers']['Is_Higher_Accuracy']] = 1
            is_successful_epoch = True

            if os.path.isfile(directory_model_with_highest_accuracy):
                os.remove(directory_model_with_highest_accuracy)
            pt.save(model_dict, directory_model_with_highest_accuracy)
        else:
            stats['lines'][e][stats['headers']['Is_Higher_Accuracy']] = 0

        stats['lines'][e][stats['headers']['Highest_Validation_Accuracy']] = highest_accuracy

        if is_successful_epoch:
            i = 0
        else:
            i += 1
        stats['lines'][e][stats['headers']['Unsuccessful_Epochs']] = i

        if os.path.isfile(directory_stats):
            os.remove(directory_stats)

        cp_txt.lines_to_csv_file(stats['lines'], directory_stats, stats['headers'])

        unweighted_class_prediction_loss_str_e = cp_strings.format_float_to_str(
            unweighted_class_prediction_loss_e, n_decimals=n_decimals_for_printing)
        weighted_class_prediction_loss_str_e = cp_strings.format_float_to_str(
            weighted_class_prediction_loss_e, n_decimals=n_decimals_for_printing)
        accuracy_str_e = cp_strings.format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

        print(
            'Epoch: {e:d}. Validation. Unweighted Classification Loss: {class_prediction_loss:s}. Accuracy: {accuracy:s}.'.format(
                e=e, class_prediction_loss=unweighted_class_prediction_loss_str_e, accuracy=accuracy_str_e))

        print('Epoch {e:d} - Unsuccessful Epochs {i:d}.'.format(e=e, i=i))

        print(dashes)

        e += 1

    print()

    E = e

    time_training = cp_timer.get_delta_time()

    print('Training completed in {d} days {h} hours {m} minutes {s} seconds'.format(
        d=time_training.days, h=time_training.hours,
        m=time_training.minutes, s=time_training.seconds))
    print('Number of Epochs: {E:d}'.format(E=E))
    print('Lowest Unweighted Classification Loss: {:s}'.format(lowest_unweighted_class_prediction_loss_str))
    print('Lowest Weighted Classification Loss: {:s}'.format(lowest_weighted_class_prediction_loss_str))
    print('Highest Accuracy: {:s}'.format(highest_accuracy_str))

    return None
