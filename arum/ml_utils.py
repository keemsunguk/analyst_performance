from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score


def prf_analysis(y_true: list, y_pred: list) -> None:
    """
    Compute and display P/R/F1 score
    :param y_true: Label
    :param y_pred: Prediction results
    :return: None
    """
    print('Precision: {:,.2f}'.format(precision_score(y_true, y_pred)))
    print('Recall   : {:,.2f}'.format(recall_score(y_true, y_pred)))
    print('F1       : {:,.2f}'.format(f1_score(y_true, y_pred)))
    print('Accuracy : {:,.2f}'.format(accuracy_score(y_true, y_pred)))
    return None
