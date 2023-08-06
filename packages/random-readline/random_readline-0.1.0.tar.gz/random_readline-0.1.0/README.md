# random-readline

Randomized fast readline for large text files.

## Install

```sh
pip install random_readline
```

## Usage

```python
from random_readline import readline

# lines are shuffled by default.
n_lines, read = readline("text.txt")

for line in read():
    print(line)
```

### Sequencial read

```python
from random_readline import readline

# lines are not shuffled as it is.
n_lines, read = readline("text.txt", shuffle=False)

for line in read():
    print(line)
```

### Gzipped file

```python
import gzip
from random_readline import readline

n_lines, read = readline("text.txt.gz", opener=gzip.open)

for line in read():
    print(line)
```

### Control the frequency of seeking

Since random seeking can be very slow with gzipped files, the readline function has an option `chunk_size` to control the frequency of seeking.

This value is set to `1` by default, which means that a seeking is performed every single line to read the entire file completely at random.

Increasing the value of `chunk_size` will reduce the frequency with which seekings are performed, thus improving performance in exchange for randomness.

```python
import gzip
from random_readline import readline

# lines will be randomized by every 100 lines
n_lines, read = readline("text.txt.gz", opener=gzip.open, chunk_size=100)

for line in read():
    print(line)
```
