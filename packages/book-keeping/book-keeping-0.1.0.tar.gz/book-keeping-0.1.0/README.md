# book-keeping

A small util library to help with recording digital experiments.
Creates a markdown report for each experiment, which contains:

-   a summary of the experiment
-   the config used for the experiment
-   any plots/images created
-   a link to all other files created by the experiment
-   the code used to run the experiment

# Usage

See [this demo](./tests/test_demo.py), and [corresponding output](./tests/demo/demo.md).

```python
from book_keeping import Experiment

experiment = Experiment()

@experiment.record
def main(**config):
    # blah blah blah
    return summary # a summary of this experiment

main(a=1, b=2)
```
