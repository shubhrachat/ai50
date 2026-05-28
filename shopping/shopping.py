import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # nested list storing all the above values in the comments for each user
    evidence = []
    # labels should be a list of all of the labels for each data point.
    labels = []

    # Previously made a list with month names in full form
    # caused None return and no month integer
    # realised the error was looking for 'Oct'
    # shortened month names

    # creating a month dictionary as prescribed to assign numeric values to each month
    month = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5,
             'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}
    # month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # loading the csv file
    # opening filename as file in read only mode
    with open(filename, 'r') as file:

        # reading contents into identifier read
        read = csv.reader(file)

        # to make it skip one item before your loop and ignore the return value.
        next(read, None)

        # making a list which will be stored in evidence nested list
        values = []

        # for every line in the loaded file
        # skipping first line
        for index in read:

            values = [int(index[0]), float(index[1]), int(index[2]), float(index[3]),
                      int(index[4]), float(index[5]), float(index[6]), float(index[7]),
                      float(index[8]), float(index[9]), month[index[10]], int(index[11]),
                      int(index[12]), int(index[13]), int(
                          index[14]), 1 if index[15] == 'Returning_Visitor' else 0,
                      1 if index[16] == 'TRUE' else 0]

            evidence.append(values)

            # labels should be the corresponding list of labels, where each label
            # is 1 if Revenue is true, and 0 otherwise.
            labels.append(1 if index[-1] == 'TRUE' else 0)

    # return a tuple (evidence, labels)
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # k=1
    # fitted model
    neighbor_model = KNeighborsClassifier(n_neighbors=1).fit(evidence, labels)
    return neighbor_model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # actually present values
    actual_positive = 0
    actual_negative = 0

    # identified positives and negatives
    accurate_positive = 0
    accurate_negative = 0

    for i in range(len(labels)):
        if predictions[i] == labels[i]:
            # count of actual negatives present
            actual_negative = labels.count(0)
            # negative identified or predicted
            if predictions[i] == 0:
                accurate_negative += 1

            else:
                # count of actual positives present
                actual_positive = labels.count(1)
                # positive identified or predicted
                accurate_positive += 1

    # ratio between correctly identified negatives
    # VS the actual negatives
    specificity = accurate_negative / actual_negative

    # ratio between correctly identified positives
    # VS the actual positives
    sensitivity = accurate_positive / actual_positive

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
