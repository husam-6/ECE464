from random import randint

def generateID(Table):
    tid = randint(1, 2**32)
    tmp = Table.query.filter_by(id=tid).first()
    while tmp:
        tid = randint(1, 2**32)
        tmp = Table.query.filter_by(id=tid).first()
            
    return tid