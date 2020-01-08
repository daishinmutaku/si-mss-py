import csv


def csv_write(p):
    print("selective-p:", p[0])
    with open('/Users/oomoriyumehiro/lab/Seminar/mss-python/CSV/selective-p.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(p)
