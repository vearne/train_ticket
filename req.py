import random
def random_request():
    start = random.randint(1, 10 - 1)
    end = random.randint(start + 1, 10)
    return start, end

with open('req.csv', 'w') as fp:
    for i in range(100000):
        user = 'user' + str(i)
        start, end = random_request()
        fp.write(user + ',' + str(start) + ',' + str(end)) 
        fp.write('\n') 
