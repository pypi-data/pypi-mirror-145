# detokenizer

detokenizer of configuration files. Inject properties in source code before
deployment.

## Usage

This parameters are positional parameters.

|Parameters|Description|
|:---|:---|
|source|source file, all tokens in this file will be replaced with properties|
|target|target file, output after the replacement|
|config|config files, this fils is a yaml file defining the delimiters for the token|
|properties|properties file, this file contains the dictionary of properties which shall be injected into the source file|

the following command run the tool on the test data contained in this repo:

```
python3 -m detokenizer \
  ./test/data/source_folder/config.properties.php \
  ./build/config.php \
  ./test/data/config.yaml \
  ./test/data/default.properties
```

## Example

Source file:

```
<?php

ini_set('memory_limit', '${packaging.memory_limit}');

$ENVIRONMENT_NAME = '${packaging.environment_name}';

#region URL
$site_URL = '${packaging.site_URL}';
#endregion
...
```

Properties file:
```
packaging.memory_limit=1024
packaging.environment_name=default
packaging.site_URL=

packaging.host=193.168.1.12
packaging.port=3000
packaging.db=db_ms_12
...
```

Produced target:

```
<?php

ini_set('memory_limit', '1024');

$ENVIRONMENT_NAME = 'default';

#region URL
$site_URL = '';
#endregion
...
```
