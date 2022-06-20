# l2term
[![build](https://github.com/soda480/l2term/actions/workflows/main.yml/badge.svg)](https://github.com/soda480/l2term/actions/workflows/main.yml)
[![Code Grade](https://api.codiga.io/project/33832/status/svg)](https://app.codiga.io/public/project/33832/mppbar/dashboard)
[![codecov](https://codecov.io/gh/soda480/l2term/branch/main/graph/badge.svg?token=IYQBFG9J8G)](https://codecov.io/gh/soda480/l2term)
[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)
[![python](https://img.shields.io/badge/python-3.9-teal)](https://www.python.org/downloads/)

The `l2term` module provides a convenient way to dynamically display a list to the terminal stderr stream; the terminal will automatically update and reflect changes that are made to the associated list. The `l2term.Lines` class is a subclass of [collections.UserList](https://docs.python.org/3/library/collections.html#collections.UserList) and is tty aware thus it is safe to use in non-tty environments. This class takes a list instance as an argument and once instantiated the list is accessible via the data attribute of the instance object. The list can be any iterable, but its elements need to be printable; they should implement __str__ function. The intent of this class is to display relatively small lists to the terminal and dynamically update the terminal when list elements are upated, added or removed.

### Installation
```bash
pip install l2term
```

#### [example1](https://github.com/soda480/l2term/blob/main/examples/example1.py)

Initially create an empty list then use document generator to add sentences to the list randomly. As sentences are added the list the respective line in the terminal is updated.

<details><summary>Code</summary>

```Python
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
```

</details>

![example1](https://raw.githubusercontent.com/soda480/l2term/main/docs/images/example1.gif)

#### [example2](https://github.com/soda480/l2term/blob/main/examples/example2.py)

Initially create an empty list then use document generator to add sentences to the list randomly. As sentences are added the list the respective line in the terminal is updated. Also show how the terminal behaves when items are added to and removed from the list.

<details><summary>Code</summary>

```Python
import time
import random
from essential_generators import DocumentGenerator
from l2term import Lines

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
                if len(lines.data) > 0:
                    index = random.randint(0, len(lines.data) - 1)
                    lines.pop(index)
            elif choice == 'append':
                lines.append(docgen.sentence())
            elif choice == 'update':
                if len(lines.data) > 0:
                    index = random.randint(0, len(lines.data) - 1)
                    lines[index] = docgen.sentence()
            else:
                if len(lines.data) > 0:
                    lines.pop()
                if len(lines.data) > 0:
                    lines.pop()
            time.sleep(.1)

if __name__ == '__main__':
    main()
```

</details>

![example2](https://raw.githubusercontent.com/soda480/l2term/main/docs/images/example2.gif)

#### Example3

A Conway [Game-Of-Life](https://github.com/soda480/game-of-life) implementation that uses `l2term` to display game to the terminal.


### Development

Clone the repository and ensure the latest version of Docker is installed on your development server.

Build the Docker image:
```sh
docker image build \
-t \
l2term:latest .
```

Run the Docker container:
```sh
docker container run \
--rm \
-it \
-v $PWD:/code \
l2term:latest \
/bin/bash
```

Execute the build:
```sh
pyb -X
```