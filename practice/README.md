# Practice Round

Problem statement can be found [here](https://github.com/hermanzdosilovic/hashcode-2017/blob/master/practice/pizza.pdf).

## How To Run

Our solution [greedy.py](https://github.com/hermanzdosilovic/hashcode-2017/blob/master/practice/greedy.py) script takes two arguments:

1. **output file**, *string* - file where best solution will be written
2. **number of iterations**, *integer* - how many times you want to run algorithm

For example:
```
$ python greedy.py best/example.txt 100
```

Will run algorithm 100 times and will write best solution into `best/example.txt` file.

Combine this with input redirect:
```
$ python greedy.py best/big.txt 100 < data/big.in
```

## Score
![score](https://github.com/hermanzdosilovic/hashcode-2017/blob/master/practice/score.png)
