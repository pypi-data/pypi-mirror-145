# RYU Sequential Orchestrator

This is a specification framework that can automatically generate template code and a JSON-over-socket server that allows clients to execute programs defined by a spec.

This framework was initially developed to formalise the backend operations for the [GRC Wallet Bot](https://gitlab.com/delta1512/grc-wallet-bot) when I realised that what I made can be extended from transaction processing to pretty much any process in an atomic and optionally reversible fashion.

The concept is that you have a problem to solve that is made up of a set of steps that can't be looped. This problem might make changes to data or other operations that need to be reversed, and for each step, you may specify how to reverse it if it has run successfully. Each step may depend on other steps and whenever an error occurs, the framework automatically reverses the operations starting one-before the erroneous step and working backwards.

# Python package

You can install this package using pip `pip install ryuso`

**Please note that this package will only include the library at this time and not contain the necessary set of files to utilise the code generation command-line.** This can be solved by copying the `templates` directory to the location of installation or waiting for [this issue](https://gitlab.com/delta1512/ryu-sequential-orchestrator/-/issues/2) to be solved.

# The name

The name is based on the Japanese name for the "Yakuza" game franchise (Ryu Ga Gotoku) which I am completely obsessed with. I chose the name because many of the Yakuza games are highly sequential singleplayer games and I couldn't think of anything else that wasn't already taken.

# Overview

The framework operates over a simple send and then receive socket.

1. The client sends a JSON payload to the RYU server telling it what program to run and what inputs to initialise it with.
2. The server queues these tasks in the socket accept queue and accepts them on a single thread
3. One-by one, the server will read and verify the tasks before running the appropriate hooks according to the spec
5. If a hook fails, then it will iterate back through the hooks (in reverse) and execute their rectification functions (if any are specified) starting from the previous hook.
6. The resulting data pool is placed on an output queue and the program run is flagged as successful or unsuccessful.


## A program

A program is a specific function you can call from the framework. It consists of hooks which will run in a particular sequence. This is not an actually defined function in code, rather it abstractly defines the sequence of functions that accomplish a task.

## A hook

A hook is either a defined function (in code) that can be run and referenced by any program spec, or it is a reference to a program (yet to be implemented). Hooks operate on a data pool (key-value store made accessible to all children of a program) and accomplish a single, defined task. Hooks can optionally contain reversal functions which intend on reversing the actions of the hook.

It is important that hooks achieve a single operation, eg, a data-write because then it is far easier to maintain atomicity and data integrity through rectification.

## A dependency

A type of hook that can be attached to an existing hook which is run before that hook is executed. This introduces recursiveness into the system, making it possible to make very large hooks comprising of many dependencies.

## Request body

The body of a RYU request consists of the following:

```
{
  "program" : "my_program",
  "data_pool" : {
    "a" : "variable A",
    "b" : 2.345
  },
  "metadata" : {}
}
```

Where:
- `program` is the name of the program you wish to run
- `data_pool` is a dictionary structure containing the initial data pool
- `metadata` (currently undocumented and optional)


# Multi-threading and parallelism

This framework is a single-threaded framework. However, there is nothing stopping a user of this framework to launch more than one RYUSO server for a particular spec. So long as you have some method of load balancing and logical mutual exclusion for all data operations, you can safely parallelise all RYUSO operations by redirecting tasks to the appropriate (or idle) server.


# Specification

The following is a spec definition which must be followed in order to create a valid RYUSO spec.

| Spec key | Required | Data Type | Description | Example |
| ------ | ------ | ------ | ------ | ------ |
| version | False | String | Current version or build of the spec | 1.2.3 |
| name | True | String | The name of the spec containing only alphanumeric characters, spaces, underscores and hyphens. The module name will be a lower-case and underscore-spaced version of this. | My transaction processing |
| programs | True | Dictionary | The dictionary of `program` where the key is the name of the program. The contents are defined below in `program.*`  | NA |
| program.hooks | True | List of strings | The list of references to hooks or programs in the spec. These hooks will run in the defined sequence. | ["hooks.check_balance", "programs.make_deposit"] |
| program.args | True | Dictionary | The dictionary of `arg` where the key is the name of the argument. This defines the initial data pool. | NA |
| arg.type | True | String | One of {string, int, float, list, dict, bool} | "bool" |
| arg.description | False | String | A description of the variable and what it is for. | "Tells the TX clearer to run" |
| arg.required | True | Boolean | Tells the spec whether this argument must be in the initial data pool. For outputs, it determines whether or not it has to be in the output data pool. | true |
| program.outputs | True | Dictionary | The dictionary of `arg` where the key is the name of the argument. This defines the output data pool and returns only these args if they exist in the pool. | NA |
| program.description | False | String | A description of what the program achieves and how it works | "Will commit a transaction and optionally generates currency when the generate flag is set" |
| hooks | True | Dictionary | The dictionary of `hook` where the key is the name of the hook. | NA |
| hook.reference | True | String | The reference to the function from the root of the built package. | "my_orchestrator.util.math.is_prime" |
| hook.args | True | Dictionary | The dictionary of `arg` where the key is the name of the argument. This defines the requirements for the contents inside of the initial data pool for the hook. This is checked before the referenced function is run and after the dependencies are executed. | NA |
| hook.dependencies | False | List of strings | The list of references to hooks or programs in the spec. These hooks will run in the defined sequence. They will run before the referenced function is executed. | ["hooks.has_balance", "hooks.prep_working_dir"] |
| hook.rectifiers | False | List of strings | The list of references to hooks or programs in the spec. These hooks will be run in-order when the framework asks this hook to reverse its actions. | ["hooks.undo_commit_balance", "hooks.unwrap_tx_data"] |
| hook.description | False | String | The string describing what the hook is suppoosed to accomplish | "Checks whether the user's balance is > 5 and fails otherwise" |
