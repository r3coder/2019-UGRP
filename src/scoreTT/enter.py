f=open('2nd.txt', 'r')
x=f.readlines()[0]
xx=x.replace(')), ', ')),\n')
print(xx)
f.close()