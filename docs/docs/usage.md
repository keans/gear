# Usage

`wrench` is the global command line to that can be used to interact with
the `gear` framework.


## config

The `config` command is a subcommand that allows to use further subcommands
to interact with the configuration.

### create

To create an empty configuration file do:

```
wrench config create <config_name>
```


### view

To see the content of an existing configuration file do:

```
wrench config view <config_name>
```


### list

To list all available configurations do:

```
wrench config list
```


## plugin

The `plugin` command is a subcommand that allows to use further subcommands
to interact with plugins.


### pack

To create a plugin package out of a plugin directory do:

```
wrench plugin pack <directory>
```


### install

To install a plugin package do:

```
wrench plugin install <plugin_package>
```


## run

To run an analysis simply use the `run` command:

```
wrench run <config_name>
```

This will trigger a local worker.

If you have the `luigid` daemon running it is also possible to utilize this
and also the number of workers can be adapted:

```
wrench run <config_name> --workers 8 --no-local
```


## reset

To delete the generated output of a configuration use the `reset` command:

```
wrench reset <config_name>
```
