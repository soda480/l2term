import time
import random
from essential_generators import DocumentGenerator
from l2term import Lines

def main():
    print('Generating random sentences...')
    docgen = DocumentGenerator()
    with Lines([''] * 15) as lines:
        for _ in range(200):
            index = random.randint(0, len(lines.data) - 1)
            lines[index] = docgen.sentence()
            time.sleep(.05)

if __name__ == '__main__':
    main()