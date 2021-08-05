# Profiling disco

`disco` is pretty simple. Repeating same stuff over and over. This makes it a perfect candidate for performance optimization.

## Profiling tools
For the profiling, we are going to use only `cProfile` and `timeit` which are built-in.

### cProfile: which method takes the most time?

To profile `disco`, go to `scripts` and run:

```bash
python -m cProfile -s tottime disco_profiling.py -d /enter/path/to/your/test/data.csv
```

Expected output is something like below, where you focus on `tottime` as the total time spent in the function but excluding the subfunction calls.

```bash
         6003077 function calls (6002287 primitive calls) in 9.358 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    49914    6.530    0.000    8.991    0.000 clean.py:46(basename)
  1314498    0.590    0.000    0.794    0.000 utils.py:12(<genexpr>)
   250262    0.273    0.000    0.273    0.000 {method 'search' of 're.Pattern' objects}
   101761    0.246    0.000    1.040    0.000 {method 'join' of 'str' objects}
   250387    0.245    0.000    0.341    0.000 re.py:289(_compile)
  1274032    0.204    0.000    0.204    0.000 {built-in method unicodedata.category}
   293631    0.179    0.000    0.297    0.000 utils.py:20(strip_punct)
   250261    0.142    0.000    0.749    0.000 re.py:198(search)
   880908    0.118    0.000    0.118    0.000 {method 'replace' of 'str' objects}
    49915    0.094    0.000    0.120    0.000 disco_profiling.py:19(read_names)
   452657    0.087    0.000    0.087    0.000 {built-in method builtins.isinstance}
    99828    0.072    0.000    0.468    0.000 utils.py:29(strip_tail)
        1    0.069    0.069    9.312    9.312 disco_profiling.py:25(main)
    50605    0.067    0.000    1.129    0.000 utils.py:9(remove_accents)
    99828    0.051    0.000    0.094    0.000 clean.py:52(<lambda>)
    99828    0.051    0.000    0.298    0.000 utils.py:37(strip_head)
```

### timeit: so how long does it take to run this at all?

To locally measure the total time of the run, I use `timeit`. In `scripts`, open the `python` terminal and run:

```python
import timeit
from disco_profiling import clean_all_names
filepath = "/enter/path/to/your/test/data.csv"
# this runs the whole cleaning 5 times in a row and repeats it 3 times.
timeit.repeat(lambda: clean_all_names(filepath), repeat=3, number=5)
# each item in the list is the time of running the function `clean_all_names` 5-times (given by `number` parameter)
>>> [40.85451753099997, 42.625093505999985, 43.338992673999996]
```

## Optimization
### Starting point (Aug 4, 2021)
For this optimization, I used a sample of 50k randomly chosen companies from Sayari parquet table in Databricks. _(TODO: add link for download)_

Profiling results at the very beginning: `cProfile` and `timeit`
```bash
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    49914    6.530    0.000    8.991    0.000 clean.py:46(basename)
  1314498    0.590    0.000    0.794    0.000 utils.py:12(<genexpr>)
   250262    0.273    0.000    0.273    0.000 {method 'search' of 're.Pattern' objects}
   101761    0.246    0.000    1.040    0.000 {method 'join' of 'str' objects}
   250387    0.245    0.000    0.341    0.000 re.py:289(_compile)
```
```python
timeit.repeat(lambda: clean_all_names(filepath), repeat=3, number=5)
>>> [40.85451753099997, 42.625093505999985, 43.338992673999996]
```
