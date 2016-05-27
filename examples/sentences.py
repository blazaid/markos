import random

from markos import MarkovChain

if __name__ == '__main__':
    mc = MarkovChain(grade=1)
    with open('frases.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        random.shuffle(lines)
        for line in lines:
            marks = '.', ',', ':', ';', '¡', '!', '?', '¿', '.', '.', '.', '(', ')',
            for mark in marks:
                line = line.replace(mark, ' {} '.format(mark))
            result = line.lower().strip().split()
            mc.train(result)
    for e in mc.generate():
        print(e, ' ', end='')
    print('')
