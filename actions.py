import csv
import random

def pocketcard(exemption):
    prefix = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
    suffix = ["H", "D", "S", "C"]
    while True:
        name = str(random.choice(prefix))
        name = name + str(random.choice(suffix))
        if name != exemption:
            break
    return name


def read(filename):
    file = open(filename, 'r')
    try:
        csv_reader = csv.DictReader(file)
        combos = {}
        for row in csv_reader:
            combos[row.get("pocket")] = row.get("seat")
        return combos
    finally:
        file.close()
