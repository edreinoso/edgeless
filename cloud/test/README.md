# Executing test in the cloud

## General concept

There are three different kind of execution environments.

- Fargate Container
- Lambda Sequential
- Lambda Concurrent

## Signal Processing

To run the signal processing test you need to use the following command

`python load_test.py --threads --requests --repetitions`

### Parameters

- **Request:** the number of jobs that will be assigned to the system. This varies in three different ranges, 1-10-100. These jobs are audio files that the system should be able to handle.
- **Sortby:** the condition for which to sort the data, for better visualization
- **Concurrency:** the number of parallel executions that will be invoked for the second lambda function. A constraint to keep in mind is that this should only be in *even numbers*

## Ouput Data

This is the structure of the output data from the performance (throughput) experiment.

```
{
    "env_time":,
    "process_time":,
    "total_execution_time":,
    "env_throughput":,
    "process_throughput":,
    "total_execution_throughput":
    "latency":,
}
```