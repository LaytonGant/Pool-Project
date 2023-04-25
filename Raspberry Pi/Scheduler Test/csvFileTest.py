import csv

# Normal write
with open('test.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['a','b','c'])
    writer.writerow(['d','e','f'])
    writer.writerow(['g','','h'])

# Normal read
with open('test.csv',newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

print("---Dict Read/Write---")

# Dict write
labels = ["first", "second", "third"]
with open('dest.csv','w',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=labels)
    writer.writeheader()
    writer.writerow({'first':'a', 'second':'b', 'third':'c'})
    writer.writerow({'first':'d', 'second':'e', 'third':'f'})
    writer.writerow({'first':'g', 'third':'h'})

# Dict read
with open('dest.csv',newline='') as f:
    reader = csv.DictReader(f)
    print(reader.fieldnames)
    for row in reader:
        print(row)

print('---Append to file---')

# Append to dict csv file
with open('dest.csv','a',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=labels)
    writer.writerow({'first':'i','second':'j','third':'k'})

# Dict read
with open('dest.csv',newline='') as f:
    reader = csv.DictReader(f)
    print(reader.fieldnames)
    for row in reader:
        print(row)

