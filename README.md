# test-db

## Overview

test-db is a command-line tool designed to automatically generate and execute database queries for SQLite testing purposes. The tool automatically produces a specified number of test queries, outputs any bugs found and saves the resulting analysis plots in a designated directory.

## Installation

```
sudo docker build -t <docker-name> .
sudo docker run -it <docker-name> /bin/bash
```

## Usage

The basic syntax for using the Test-DB tool is:

```
sudo /bin/test-db <number_of_queries>
```

Where `<number_of_queries>` is an integer representing the number of database queries you want the tool to generate and execute.
It will default to 200 if not provided.

## Output

After execution, all results and analysis plots will be saved in the `/workspace/plots` directory. These include:

- Expression depth histogram
- Clause frequency histogram
- Code coverage over number of queries executed


## Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| number_of_queries | Integer value specifying how many queries to generate | No |
