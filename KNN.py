
import math
def get_accuracy_recall_precision(actual_predicted_pairs):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    PT = 0
    AT = 0
    total = 0
    for pair in actual_predicted_pairs:
        total += 1
        if pair[0] == pair[1]:
            if pair[1]:
                TP += 1
                PT += 1
                AT += 1
            else:
                TN += 1
        else:
            if pair[1]:
                FP += 1
                PT += 1
            else:
                FN += 1
                AT += 1

    return (((TP+TN)/total), TP/AT, TP/PT)


class Model:
    def __init__(self):
        self.data = None

    def train(self, test_case_to_actual_category):
        self.data = test_case_to_actual_category
    def predict(self, test_case):
        dist_dict ={}
        tCount=0
        fCount=0
        Count=0
        for key in self.data:
            dist =0
            for i in range(3):
                dist +=(key[i] - test_case[i]) ** 2
            dist= math.sqrt(dist)
            dist_dict[dist]=self.data[key]
        keylist = dist_dict.keys()
        list = sorted(keylist)
        for key in list:
            Count+=1
            if dist_dict[key]:
                tCount+=1
            else:
                fCount+=1
            if Count >=5:
                break
        return tCount>fCount

import random

random.seed(0)


def generate_data(number_of_test_cases):
    data = []
    for _ in range(number_of_test_cases):
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        data.append(random_color)
    return data


def has_red_function(test_case):
    return test_case[0] > 180


actual_function = has_red_function

training_data = generate_data(400)
test_case_to_actual_category = {test_case: actual_function(test_case)
                                for test_case in training_data}

m = Model()
m.train(test_case_to_actual_category)

testing_data = generate_data(400)
actual_predicted_pairs = []
for test_case in testing_data:
    actual = actual_function(test_case)
    predicted = m.predict(test_case)
    actual_predicted_pairs.append((actual, predicted))

accuracy, recall, precision = get_accuracy_recall_precision(actual_predicted_pairs)
print(f"accuracy = {accuracy}")
print(f"recall = {recall}")
print(f"precision = {precision}")

self.assertGreater(accuracy, 0.75)
self.assertGreater(recall, 0.75)
self.assertGreater(precision, 0.75)