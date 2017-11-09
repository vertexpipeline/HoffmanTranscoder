def mod(x,y):
    (d, m) = divmod(x,y)
    return m


def getHemmingTables(n, c):
    degress = [2**x for x in range(0,n)]
    table = []
    for i in degress:
        cur = [0]*c
        step = i-1
        j = 0
        while j<c:
            if step == 0:
                for k in range(0,i):
                    if j+k<c:
                     cur[j+k] = 1
                j+=i-1
                step = i
            else:
                step-=1
            j+=1
        table.append(cur)
    return (degress, table)

import math

def getDegCount(count):
    log = math.log2(count)
    (rem, integer) = math.modf(log)
    if rem != 0:
        integer +=1
    integer = int(integer+1)
    return integer

def excludeChecksum(args):
    (degrees, table) = args
    for cur in table:
        for i in degrees:
            cur[i-1] = 0
    return (degrees, table)

def insertChecksum(degrees, data):
    for n in degrees:
        data.insert(n-1, 0)
    return data

def getCkecksum(degrees, table, data):

    for n in range(0,len(degrees)):
        sum = 0
        for i in range(0,len(data)):
            if (table[n][i] == 1) and(data[i] == 1):
                sum += 1
        data[degrees[n]-1] = 0 if (mod(sum, 2) == 0) else 1
    return data

def getDegCountWithChecksum(count):
    n = 0
    while count>(n+n**n):
        n+=1;
    return n + 1

def check(degrees, table, data):
    errors = []
    lastError = -1
    errorsn = 0
    for n in range(0,len(degrees)):
        sum = 0
        for i in range(0,len(data)):
            if (table[n][i] == 1) and(data[i] == 1):
                sum += 1
        result = 0 if mod(sum, 2) == 0 else 1
        if result != data[degrees[n]-1]:
                errors.append(degrees[n])
                lastError = n
                errorsn+=1

    return (errors,errorsn)

def encode(data):
    degCount = getDegCount(len(data))

    hemTable = getHemmingTables(degCount, degCount + len(data))
    (degrees,table) = excludeChecksum(hemTable)

    normalized = insertChecksum(degrees, data)
    return getCkecksum(degrees, table, normalized)

def decode(data):
    degCount = getDegCountWithChecksum(len(data))

    hemTable = getHemmingTables(degCount, len(data))
    (degrees,table) = excludeChecksum(hemTable)
    (errors, errorsn) = check(degrees, table, data)
    if errorsn == 1:
        print("Ошибка в контрольной сумме")
    result = []

    def makeres():
        for (i, n) in enumerate(data):
            (reminder, _) = math.modf(math.log2(i+1 if i!=0 else 4))
            if reminder != 0:
                result.append(n)

    if(errorsn<2):
        makeres()
        return result
    else:
        mask = [0]*len(data)
        for n,deg in enumerate(degrees):
            if not errors.__contains__(deg):
                for j,i in enumerate(table[n]):
                    if i == 1:
                        mask[j] = 1
        changes = 0
        for i,m in enumerate(mask):
            (reminder, _) = math.modf(math.log2(i + 1 if i != 0 else 4))
            if (reminder != 0) and (mask[i] == 0):
                data[i] = 0 if data[i] == 1 else 1
                changes += 1
        if changes>1:
            print("не возможно восстановить")
        else:
            makeres()
            return result




while True:
    req = input("From or to: ")
    if(req == "to"):
        data = input("Data: ")
        bits = [(1 if c=="1" else 0) for c in (bin(int(data, 16))[2:])]
        print("Result:",encode(bits))
    else:
        data = input("Data: ")
        bits = [(1 if c=="1" else 0) for c in data]
        print("Result:",decode(bits))
