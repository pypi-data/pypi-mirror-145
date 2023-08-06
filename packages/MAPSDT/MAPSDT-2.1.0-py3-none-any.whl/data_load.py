from tqdm import tqdm
from colorama import Style, Fore
from time import sleep
import numpy as np
import time


class Data(object):
    def __init__(self, keys, values):
        for (key, value) in zip(keys, values):
            self.__dict__[key] = value
        self.id = 0
        self.winner = ''
        self.usedCategorical = []
        self.predict = None


class Attribute:
    def __init__(self):
        self.name = None
        self.type = None
        self.new = False
        self.use = False


class Leaf:
    def __init__(self):
        self.rule = ''
        self.dataset = []
        self.terminateBuilding = False
        self.branch = 0
        self.parent = None
        self.id = None
        self.branchAttribute = None
        self.classes = None
        self.decision = []
        self.predict = None


class Chromosome:
    def __init__(self):
        self.string = []
        self.expression = ''

    def combine(self):
        if ' ' not in self.string:
            self.expression = '((obj.' + self.string[0].name + self.string[2] + 'obj.' + self.string[1].name + ')' + \
                              self.string[-1] + '(obj.' + self.string[3].name + self.string[5] + 'obj.' + self.string[
                                  4].name + '))'
        elif (self.string[2] != ' ') and (self.string[5] == ' '):
            self.expression = '(obj.' + self.string[0].name + self.string[2] + 'obj.' + self.string[1].name + ')' + self.string[-1] + 'obj.' + self.string[4].name
        elif (self.string[2] == ' ') and (self.string[5] != ' '):
            self.expression = 'obj.' + self.string[1].name + self.string[-1] + '(obj.' + self.string[3].name + self.string[5] + 'obj.' + self.string[4].name + ')'
        else:
            self.expression = 'obj.' + self.string[1].name + self.string[-1] + 'obj.' + self.string[4].name





class Population:
    def __init__(self):
        self.population = []


class DT:
    def __init__(self):
        self.leaf = list
        self.root = None
        self.test_data = None
        self.rule_decision = list
        self.accuracy = 0
        self.chromosome = None

    def fit(self):
        self.root.dataset = self.test_data
        decisions = sorted(list(set(map(lambda x: x.Decision, self.test_data))))
        num_of_decisions = []
        for i in decisions:
            num_of_decisions.append(list(map(lambda x: x.Decision, self.root.dataset)).count(i))
        self.root.decision = num_of_decisions
        # for _leaf in tqdm(self.leaf, desc=Fore.GREEN + Style.BRIGHT + "Fitting : ", mininterval=0.1, ncols=150):
        for _leaf in self.leaf:
            _leaf.dataset = []
            # for i in list(filter(lambda obj:eval(_leaf.rule), _leaf.parent.dataset)):
            #
            #     i.predict = _leaf.predict
            #     _leaf.dataset.append(i)

            for obj in _leaf.parent.dataset:
                if eval(_leaf.rule):
                    obj.predict = _leaf.predict
                    _leaf.dataset.append(obj)

            num_of_decisions = []
            for i in decisions:
                num_of_decisions.append(list(map(lambda x: x.Decision, _leaf.dataset)).count(i))
            _leaf.decision = num_of_decisions
            sleep(0.1)


def attribute_set(attribute, data):
    # attribute 의 데이터 타입(범주형 or 연속형)을 판단
    if len(set(map(lambda x: x.__getattribute__(attribute.name), data))) <= 8:
        attribute.type = 'Categorical'
        for _data in data:
            setattr(_data, attribute.name, str(_data.__getattribute__(attribute.name)))
    else:
        attribute.type = 'Continuous'


