import time, random
from l2term import Lines
from essential_generators import DocumentGenerator

def main():
    print('Generating random sentences...')
    docgen = DocumentGenerator()
    with Lines([''] * 10) as lines:
        for _ in range(100):
            index = random.randint(0, len(lines.data) - 1)
            lines[index] = docgen.sentence()
        for _ in range(100):
            update = ['update'] * 18
            append = ['append'] * 18
            pop = ['pop'] * 14
            clear = ['clear']
            choice = random.choice(append + pop + clear + update)
            if choice == 'pop':
                if len(lines.data):
                    index = random.randint(0, len(lines.data) - 1)
                    lines.pop(index)
            elif choice == 'append':
                lines.append(docgen.sentence())
            elif choice == 'update':
                if len(lines.data):
                    index = random.randint(0, len(lines.data) - 1)
                    lines[index] = docgen.sentence()
            else:
                if len(lines.data):
                    lines.pop()
                if len(lines.data):
                    lines.pop()
            time.sleep(.1)

if __name__ == '__main__':
    main()