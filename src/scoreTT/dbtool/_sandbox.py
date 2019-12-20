import csv
def csv_loader(fname):
    csv_open=open('.\db\\'+str(fname)+'.csv', 'r', encoding='utf-8-sig', newline='')
    csv_reader=csv.DictReader(csv_open)
    for r in csv_reader:
        print(r.keys())
        for key in ['idSUBJ', 'idINST']: r[key]=int(r[key])
        for key in ['ds', 'ms']: r[key]=tuple(int(i) for i in r[key].split(','))
        # print(type(r['idSUBJ']))
        print(r)
        print(r['ms'][0])
        # print(dict(r))
    # return {int(r['idSUBJ']): r for r in csv_reader} # list of dictionaries which key is an id
csv_loader('TEST')