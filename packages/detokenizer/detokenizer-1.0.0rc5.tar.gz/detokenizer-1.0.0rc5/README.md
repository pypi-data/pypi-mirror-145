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
