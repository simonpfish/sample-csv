# `sample-csv`

A minimal CLI tool for sampling data from large CSV files.

**Usage**:

```console
$ sample-csv [OPTIONS] INPUT_PATH [PERCENTAGE]
```

**Arguments**:

- `INPUT_PATH`: Path to the input CSV file. [required]
- `[PERCENTAGE]`: Percentage of data to sample. The value should be between 0.0 and 1.0. [default: 0.1]

**Options**:

- `--help`: Show this message and exit.
