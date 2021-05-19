f = open('long-logs.log','r')
data = []
date=[]
fulltime=0
length = 0
for line in f:
        
            try:
                t = line.strip().split('\t')

                
                time = int(t[2].strip().split(' ')[0])
                qber = float(t[3].strip().split(' ')[0])/100
                rrate = int(t[4].strip().split(' ')[0])
                srate = int(t[4].strip().split(' ')[-2])

                if rrate<80 and rrate>50 and qber<8.5:
                    data.append([t[0],time,qber,rrate,srate,srate])
                    date.append(t[0])
                    fulltime=fulltime + time
                    length=length + srate*time/1000
            except:
                pass

            
from math import log2, exp
from random import random
def getH(x):
    result = -x*log2(x)-(1-x)*log2(1-x)
    return result

def getratio(qber, u):
    result = 1-getH(qber)-getH((1-exp(-2*u))/2)
    return result

from copy import deepcopy
moddata = deepcopy(data)

u=0.2

for item in data:
    k = getratio(item[2], u)
    if k>0:
        item[5]= item[3]*getratio(item[2], u)
    else:
        item[5]=0
    #item[1]= item[1]*(1+(random()-0.5)/0.5)
    #item[2]= item[2]*(1+(random()-0.5)/10)
    
f = open('output.txt','w')
f.writelines('date\tkeytime\tqber\tsifted_br\tsecret_br\tc_secret_br\n')
for line in data:
    f.writelines(str(line[0])+'\t'+str(line[1])+'\t'+str(round(line[2],4))+'\t'+str(line[3])+'\t'+str(line[4])+'\t'+str(round(line[5],4))+'\n')
f.close()
    
qber = list(zip(*data))[2]
rrate = list(zip(*data))[3]
srate = list(zip(*data))[5]



from numpy import mean, median

print(mean(srate))
print(median(srate))

bins1=22

bins2=22



import matplotlib.pyplot as plt

#rat=[]
#for qber in range(5, 65, 5):
#    rat.append(getratio(qber/1000, 0.2))



plt.figure(1)
plt.subplot(221)
plt.title('QBER')
plt.plot(qber, linewidth=0.3)

plt.subplot(222)
plt.title('QBER \nhist')
plt.hist(qber, bins=bins1)

plt.subplot(223)
plt.title('qrate, бит/сек')
plt.plot(srate, linewidth=0.3)

plt.subplot(224)
plt.title('qrate, бит/сек')
plt.hist(srate, bins=bins2)


plt.show()
