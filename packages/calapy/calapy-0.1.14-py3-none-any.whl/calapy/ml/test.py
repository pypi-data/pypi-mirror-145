# websites:
# https://pytorch.org/docs/stable/torchvision/transforms.html
# https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#sphx-glr-beginner-blitz-cifar10-tutorial-py
# https://pytorch.org/hub/pytorch_vision_resnet/
# https://discuss.pytorch.org/t/normalize-each-input-image-in-a-batch-independently-and-inverse-normalize-the-output/23739
# https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html

from . import torch
import typing
import os
import numpy as np
from .. import txt as cp_txt
from .. import maths as cp_maths
from .. import clock as cp_clock
from .. import strings as cp_strings


def feature_classifier(model, loader, criterion):

    cp_timer = cp_clock.Timer()

    headers_stats = ['N_samples', *['C_' + str(g) for g in range(loader.G)], 'Loss', 'Accuracy']

    n_columns_stats = len(headers_stats)
    line_stats = [loader.n_samples, *loader.n_conditions_directories_inter, None, None]  # type: list

    stats = {
        'headers': {headers_stats[i]: i for i in range(n_columns_stats)},
        'lines': [line_stats]}

    headers_trials = [
        'ID_Trial',
        *['Condition_' + str(g) for g in range(loader.G)],
        'Label',
        *['Probability_' + str(k) for k in range(loader.K[0])],
        'Classification',
        'Correct_Classification'
    ]

    n_columns_trials = len(headers_trials)

    trials = {
        'headers': {headers_trials[i]: i for i in range(n_columns_trials)},
        'lines': None}

    n_decimals_for_printing = 6

    if model.training:
        model.eval()  # Set model to evaluate mode

    if criterion.training:
        criterion.eval()

    softmax = torch.nn.Softmax(dim=1)
    if softmax.training:
        softmax.eval()

    # Now set requires_grad to false
    for param_model in model.parameters():
        param_model.requires_grad = False

    for param_criterion in criterion.parameters():
        param_criterion.requires_grad = False

    for param_softmax in softmax.parameters():
        param_softmax.requires_grad = False

    torch.set_grad_enabled(False)

    running_loss_e = 0.0
    running_corrects_e = 0

    n_samples_e = 0

    start_index_samples = 0
    stop_index_samples = 0

    index_combinations_e = np.empty(2, dtype='O')
    index_combinations_e[1] = slice(0, loader.G, 1)
    combinations_e = np.empty([loader.n_samples_e, loader.G], dtype='O')

    index_probabilities_e = np.empty(2, dtype='O')
    index_probabilities_e[1] = slice(0, loader.K[0], 1)
    probabilities_e = np.empty([loader.n_samples_e, loader.K[0]], dtype='O')

    index_labels_e = np.empty(2, dtype='O')
    index_labels_e[1] = 0
    labels_e = np.empty([loader.n_samples_e, 1], dtype='O')

    classifications_e = labels_e.copy()

    correct_classifications_e = labels_e.copy()

    id_trials = np.arange(loader.n_samples_e, dtype='O')[:, None]

    # b = 0
    # Iterate over data.
    for data_eb in loader:
        samples_eb, labels_eb, combinations_eb = data_eb

        # forward
        outputs_eb = model(samples_eb)
        probabilities_eb = softmax(outputs_eb)
        _, classifications_eb = torch.max(outputs_eb, 1)
        correct_classifications_eb = (classifications_eb == labels_eb).long()
        loss_eb = criterion(outputs_eb, labels_eb)

        n_samples_eb = samples_eb.shape[loader.batch_axis_inputs]
        n_samples_e += n_samples_eb

        # stop_index_samples += n_samples_eb
        stop_index_samples = n_samples_e
        index_samples = slice(start_index_samples, stop_index_samples, 1)

        index_combinations_e[0] = index_samples
        combinations_e[tuple(index_combinations_e)] = combinations_eb.tolist()

        index_probabilities_e[0] = index_samples
        probabilities_e[tuple(index_probabilities_e)] = probabilities_eb.tolist()

        index_labels_e[0] = index_samples
        labels_e[tuple(index_labels_e)] = labels_eb.tolist()

        classifications_e[tuple(index_labels_e)] = classifications_eb.tolist()

        correct_classifications_e[tuple(index_labels_e)] = correct_classifications_eb.tolist()

        start_index_samples = stop_index_samples

        running_loss_e += loss_eb.item() * n_samples_eb
        # noinspection PyTypeChecker
        running_corrects_e += torch.sum(correct_classifications_eb).item()

        # b += 1

    loss_e = running_loss_e / n_samples_e
    accuracy_e = running_corrects_e / n_samples_e

    stats['lines'][0][stats['headers']['Loss']] = loss_e
    stats['lines'][0][stats['headers']['Accuracy']] = accuracy_e

    trials['lines'] = np.concatenate(
        (id_trials, combinations_e, labels_e, probabilities_e, classifications_e, correct_classifications_e),
        axis=1)

    loss_str_e = cp_strings.format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
    accuracy_str_e = cp_strings.format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

    print('Test. Loss: {:s}. Accuracy: {:s}.'.format(loss_str_e, accuracy_str_e))
    print()

    time_test = cp_timer.get_delta_time()

    print('Test completed in {d} days {h} hours {m} minutes {s} seconds'.format(
        d=time_test.days, h=time_test.hours,
        m=time_test.minutes, s=time_test.seconds))

    return stats, trials


def passive_feature_sequence_classifiers(model, loader, directory_outputs=None):
    cp_timer = cp_clock.Timer()

    if model.training:
        model.eval()
    model.freeze()
    torch.set_grad_enabled(False)

    headers_stats = [
        'N_Trials',
        *['C_' + str(g) for g in range(0, loader.G, 1)],

        'Unweighted_Class_Prediction_Loss',
        'Weighted_Class_Prediction_Loss',
        'Accuracy',

        'Unweighted_Class_Prediction_Loss_In_Last_Time_Point',
        'Weighted_Class_Prediction_Loss_In_Last_Time_Point',
        'Accuracy_In_Last_Time_Point',

        'Unweighted_Class_Prediction_Losses_In_Each_Time_Point',
        'Weighted_Class_Prediction_Losses_In_Each_Time_Point',
        'Accuracy_In_Each_Time_Point']

    n_columns_stats = len(headers_stats)
    line_stats = [None for i in range(0, n_columns_stats, 1)]  # type: list

    stats = {
        'headers': {headers_stats[i]: i for i in range(n_columns_stats)},
        'n_columns': n_columns_stats,
        'lines': [line_stats]}

    stats['lines'][0][stats['headers']['N_Trials']] = loader.n_samples_e

    n_conditions_directories_inter_list = loader.n_conditions_directories_inter.tolist()
    for g in range(0, loader.G, 1):
        stats['lines'][0][stats['headers']['C_' + str(g)]] = n_conditions_directories_inter_list[g]

    headers_trials = [
        'ID_Trial',
        *['Condition_' + str(g) for g in range(loader.G)],
        *['Labels_for_Class_Type_{c:d}'.format(c=c) for c in range(loader.C)],
        *['Probability_of_Class_{k:d}_for_Class_Type_{c:d}'.format(k=k, c=c) for c in range(loader.C) for k in
          range(loader.K[c])],
        *['Classifications_for_Class_Type_{c:d}'.format(c=c) for c in range(loader.C)],
        *['Correct_Classifications_for_Class_Type_{c:d}'.format(c=c) for c in range(loader.C)],
        *['Class_Prediction_Losses_for_Class_Type_{c:d}'.format(c=c) for c in range(loader.C)]]

    n_columns_trials = len(headers_trials)

    trials = {
        'headers': {headers_trials[i]: i for i in range(n_columns_trials)},
        'lines': None}

    if directory_outputs is None:
        directory_outputs = 'outputs'
    os.makedirs(directory_outputs, exist_ok=True)

    directory_stats = os.path.join(directory_outputs, 'stats.csv')
    directory_trials = os.path.join(directory_outputs, 'trials.csv')

    separators_times = '  '
    n_decimals_for_printing = 6

    running_n_corrects = 0
    running_n_classifications = 0
    running_unweighted_class_prediction_loss = 0.0
    running_weighted_class_prediction_loss = 0.0

    running_n_corrects_T = 0  # type: typing.Union[int, float, list, tuple, np.ndarray, torch.Tensor]
    running_n_classifications_T = 0  # type: typing.Union[int, float, list, tuple, np.ndarray, torch.Tensor]
    running_unweighted_class_prediction_losses_T = 0.0  # type: typing.Union[int, float, list, tuple, np.ndarray, torch.Tensor]
    running_weighted_class_prediction_losses_T = 0.0  # type: typing.Union[int, float, list, tuple, np.ndarray, torch.Tensor]

    n_trials = 0

    start_index_trials = 0
    # stop_index_trials = 0

    P = cp_maths.prod(loader.K)

    id_trials = np.empty([loader.n_samples_e, 1], dtype='O')
    id_trials[slice(0, loader.n_samples_e, 1), 0] = np.arange(loader.n_samples_e, dtype='O')

    index_combinations_trials = np.empty(2, dtype='O')
    index_combinations_trials[1] = slice(0, loader.G, 1)
    combinations_trials = np.empty([loader.n_samples_e, loader.G], dtype='O')

    index_labels_trials = np.empty(2, dtype='O')
    index_labels_trials[1] = slice(0, loader.C, 1)
    labels_trials = np.empty([loader.n_samples_e, loader.C], dtype='O')

    index_probabilities_trials = np.empty(2, dtype='O')
    index_probabilities_trials[1] = slice(0, P, 1)
    probabilities_trials = np.empty([loader.n_samples_e, P], dtype='O')

    classifications_trials = np.empty([loader.n_samples_e, loader.C], dtype='O')
    correct_classifications_trials = np.empty([loader.n_samples_e, loader.C], dtype='O')

    class_prediction_losses_trials = np.empty([loader.n_samples_e, loader.C], dtype='O')

    b = 0
    # Iterate over data.
    for data_b in loader:
        samples_b, labels_b, combinations_b = data_b

        n_time_points = T = samples_b.shape[model.axis_time_inputs]
        n_trials_b = B = samples_b.shape[model.axis_batch_inputs]
        n_trials += n_trials_b

        # forward
        predictions_classes_b = model(samples_b)

        probabilities_b = model.compute_probabilities(predictions_classes=predictions_classes_b)

        # compute accuracy
        classifications_b = model.compute_classifications(
            predictions_classes=predictions_classes_b, axis_classes=None)
        correct_classifications_b = model.compute_correct_classifications(
            classifications=classifications_b, labels=labels_b)
        n_corrects_b = model.compute_n_corrects(
            correct_classifications=correct_classifications_b, axes_not_included=None, keepdim=False)
        n_classifications_b = model.compute_n_classifications(
            classifications=classifications_b, axes_not_included=None)

        # compute class prediction loss
        class_prediction_losses_b = model.compute_class_prediction_losses(
            predictions_classes=predictions_classes_b, labels=labels_b)
        unweighted_class_prediction_loss_b = model.reduce_losses(
            losses=class_prediction_losses_b, weigh=False, type_models=0, axes_not_included=None)
        weighted_class_prediction_loss_b = model.reduce_losses(
            losses=class_prediction_losses_b, weigh=True, type_models=0, axes_not_included=None)

        running_n_corrects += n_corrects_b
        running_n_classifications += n_classifications_b
        running_unweighted_class_prediction_loss += unweighted_class_prediction_loss_b.item() * n_classifications_b
        running_weighted_class_prediction_loss += weighted_class_prediction_loss_b.item() * n_classifications_b

        # compute accuracy for each time point
        n_corrects_T_b = model.compute_n_corrects(
            correct_classifications=correct_classifications_b, axes_not_included=model.axis_time_losses, keepdim=False)
        n_classifications_T_b = model.compute_n_classifications(
            classifications=classifications_b, axes_not_included=model.axis_time_losses)

        # compute class prediction loss for each time point
        unweighted_class_prediction_losses_T_b = model.reduce_losses(
            losses=class_prediction_losses_b, weigh=False, type_models=0,
            axes_not_included=model.axis_time_losses)
        weighted_class_prediction_losses_T_b = model.reduce_losses(
            losses=class_prediction_losses_b, weigh=True, type_models=0,
            axes_not_included=model.axis_time_losses)

        running_n_corrects_T += n_corrects_T_b
        running_n_classifications_T += n_classifications_T_b
        running_unweighted_class_prediction_losses_T += unweighted_class_prediction_losses_T_b * n_classifications_T_b
        running_weighted_class_prediction_losses_T += weighted_class_prediction_losses_T_b * n_classifications_T_b

        # stop_index_trials += n_trials_b
        stop_index_trials = n_trials
        index_trials = slice(start_index_trials, stop_index_trials, 1)

        index_combinations_trials[0] = index_trials
        combinations_trials[tuple(index_combinations_trials)] = combinations_b.tolist()

        index_labels_trials[0] = index_trials
        labels_trials[tuple(index_labels_trials)] = model.compute_losses_trials(labels_b)

        classifications_trials[tuple(index_labels_trials)] = model.compute_losses_trials(classifications_b)

        correct_classifications_trials[tuple(index_labels_trials)] = model.compute_losses_trials(
            correct_classifications_b)

        class_prediction_losses_trials[tuple(index_labels_trials)] = model.compute_losses_trials(
            class_prediction_losses_b)

        index_probabilities_trials[0] = index_trials
        probabilities_trials[tuple(index_probabilities_trials)] = model.compute_outs_trials(
            probabilities_b)

        start_index_trials = stop_index_trials

        b += 1

    unweighted_class_prediction_loss = running_unweighted_class_prediction_loss / running_n_classifications
    weighted_class_prediction_loss = running_weighted_class_prediction_loss / running_n_classifications
    accuracy = running_n_corrects / running_n_classifications

    unweighted_class_prediction_losses_T = running_unweighted_class_prediction_losses_T / running_n_classifications_T
    weighted_class_prediction_losses_T = running_weighted_class_prediction_losses_T / running_n_classifications_T
    accuracy_T = running_n_corrects_T / running_n_classifications_T

    last_unweighted_class_prediction_loss = unweighted_class_prediction_losses_T[-1].item()
    last_weighted_class_prediction_loss = weighted_class_prediction_losses_T[-1].item()
    last_accuracy = accuracy_T[-1].item()

    stats['lines'][0][stats['headers']['Unweighted_Class_Prediction_Loss']] = unweighted_class_prediction_loss
    stats['lines'][0][stats['headers']['Weighted_Class_Prediction_Loss']] = weighted_class_prediction_loss
    stats['lines'][0][stats['headers']['Accuracy']] = accuracy

    stats['lines'][0][stats['headers']['Unweighted_Class_Prediction_Loss_In_Last_Time_Point']] = (
        last_unweighted_class_prediction_loss)
    stats['lines'][0][stats['headers']['Weighted_Class_Prediction_Loss_In_Last_Time_Point']] = (
        last_weighted_class_prediction_loss)
    stats['lines'][0][stats['headers']['Accuracy_In_Last_Time_Point']] = last_accuracy

    stats['lines'][0][stats['headers']['Unweighted_Class_Prediction_Losses_In_Each_Time_Point']] = (
        separators_times.join([str(t) for t in unweighted_class_prediction_losses_T.tolist()]))
    stats['lines'][0][stats['headers']['Weighted_Class_Prediction_Losses_In_Each_Time_Point']] = (
        separators_times.join([str(t) for t in weighted_class_prediction_losses_T.tolist()]))
    stats['lines'][0][stats['headers']['Accuracy_In_Each_Time_Point']] = (
        separators_times.join([str(t) for t in accuracy_T.tolist()]))

    v_join = np.vectorize(pyfunc=cp_strings.join, otypes='O')

    # labels_trials = v_join(elements=labels_trials, sep=separators_times, frmt='{:d}', ignore=False, ignore_value=None)
    # probabilities_trials = v_join(
    #     elements=probabilities_trials, sep=separators_times, frmt='{}', ignore=False, ignore_value=None)
    # classifications_trials = v_join(
    #     elements=classifications_trials, sep=separators_times, frmt='{:d}', ignore=False, ignore_value=None)
    # correct_classifications_trials = v_join(
    #     elements=correct_classifications_trials, sep=separators_times, frmt='{:d}', ignore=False, ignore_value=None)
    # class_prediction_losses_trials = v_join(
    #     elements=class_prediction_losses_trials, sep=separators_times, frmt='{}', ignore=False, ignore_value=None)
    # trials['lines'] = np.concatenate(
    #     (id_trials, combinations_trials, labels_trials, probabilities_trials,
    #      classifications_trials, correct_classifications_trials, class_prediction_losses_trials),
    #     axis=1)

    trials['lines'] = v_join(elements=np.concatenate(
        (id_trials, combinations_trials, labels_trials, probabilities_trials,
         classifications_trials, correct_classifications_trials, class_prediction_losses_trials),
        axis=1), sep=separators_times, frmt='{}', ignore=False, ignore_value=None)

    cp_txt.lines_to_csv_file(stats['lines'], directory_stats, stats['headers'])
    cp_txt.lines_to_csv_file(trials['lines'], directory_trials, trials['headers'])

    unweighted_class_prediction_loss_str = cp_strings.format_float_to_str(
        unweighted_class_prediction_loss, n_decimals=n_decimals_for_printing)
    weighted_class_prediction_loss_str = cp_strings.format_float_to_str(
        weighted_class_prediction_loss, n_decimals=n_decimals_for_printing)
    accuracy_str = cp_strings.format_float_to_str(accuracy, n_decimals=n_decimals_for_printing)

    print('Test. Unweighted Classification Loss: {class_prediction_loss:s}. Accuracy: {accuracy:s}.'.format(
        class_prediction_loss=unweighted_class_prediction_loss_str, accuracy=accuracy_str))
    print()

    time_test = cp_timer.get_delta_time()

    print('Test completed in {d} days {h} hours {m} minutes {s} seconds'.format(
        d=time_test.days, h=time_test.hours,
        m=time_test.minutes, s=time_test.seconds))

    return None
