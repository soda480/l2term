import time
import random
import names
from essential_generators import DocumentGenerator
from l2term import Lines

def main():
    print('Generating random sentences...')
    size = 15
    indices = [names.get_full_name() for _ in range(size)]
    docgen = DocumentGenerator()
    with Lines(size=size, indices=indices) as lines:
        for _ in range(200):
            index = random.randint(0, len(lines) - 1)
            lines.write(f'{indices[index]}->{docgen.sentence()}')
            time.sleep(.05)

if __name__ == '__main__':
    main()