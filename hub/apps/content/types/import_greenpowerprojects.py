import csv
from hub.apps.content.models import GreenPowerProject


with open('gpp.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    row = reader[0]
    print row.keys()
