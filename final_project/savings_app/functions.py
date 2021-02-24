# import csv
# from .models import Cities
#
# with open('fixtures/cities.csv') as data_file:
#    reader = csv.reader(data_file)
#    for row in reader:
#        obj = Cities.objects.create(
#            name=row[0],
#            country=row[1],
#            region=row[2],
#            key=row[3]
#        )
#        obj.save()
#


