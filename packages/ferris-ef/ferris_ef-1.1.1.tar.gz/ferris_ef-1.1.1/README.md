# FERRIS Eexecutor Helper

 This package can be used for fetching package's configuration, parameters, secrets and state through it's context.
 
```python
from ferris_ef import context
```

### Accessing package configuration

```python
from ferris_ef import context

context.config.get('some_configuration_key')
```

### Accessing execution parameters

```python
from ferris_ef import context

context.params.get('param_name')
```

### Accessing package secrets

```python
from ferris_ef import context

context.secrets.get('secret_name')
```

### Accessing package id and name

```python
from ferris_ef import context

context.package.name
context.package.id
```

### Accessing and updating package state

```python
from ferris_ef import context

context.state.get()
context.state.put("some_key", "some_value")
```


## Using `ferris_ef` for local development

To use `ferris_ef` for local development and testing without need to run scripts through Executor `EF_ENV=local` env variable must be set. When it is set `ferris_ef.context` will be read from local file `ef_env.json` that must be created within same directory as the script that is accessing `ferris_ef.context`.  
`ef_env.json` must have following structure:

```json
{
  "params": {
    "package_name": "some_package_name",
    "package_id": "some_package_id",
    "optional_param_1": "param_1_value",
    "optional_param_2": "param_2_value"
  },
  "secrets": {
    "secret_param_1": "secret_1_value",
    "secret_param_2": "secret_2_value"
  },
  "config": {
    "config_param_1": "config_1_value",
    "config_param_2": "config_2_value"
  }
}
```

NOTE: `params`, `package_name` and `package_id` are mandatory.

When `EF_ENV=local` is set, package state is also stored and fetched from the local file `ef_package_state.json` within the same directory. If file does not exist it will be created on the fly. 
