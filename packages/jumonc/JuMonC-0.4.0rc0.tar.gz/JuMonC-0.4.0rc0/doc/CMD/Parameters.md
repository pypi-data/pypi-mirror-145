# Arguments and Usage
## Usage
```
usage: app.py [-h] [--DONT_DEFAULT_TO_HUMAN_READABLE_NUMBERS]
              [--LOG_FORMAT LOG_FORMAT]
              [--LOG_LEVEL {'ERROR','WARN','INFO','DEBUG'}] [--LOG_STDOUT]
              [--LOG_PREFIX LOG_PREFIX]
              [--MAX_WORKER_THREADS MAX_WORKER_THREADS]
              [--ONLY_CHOOSEN_REST_API_VERSION]
              [--PENDING_TASKS_SOFT_LIMIT PENDING_TASKS_SOFT_LIMIT]
              [-p [1024-65535]] [--REST_API_VERSION {0,1}]
              [--SHORT_JOB_MAX_TIME SHORT_JOB_MAX_TIME]
              [--USER_DEFINED_TOKEN USER_DEFINED_TOKEN] [-v]
```
## Arguments
### Quick reference table
|Short|Long                                      |Default                                                              |Description                                                                                                                                               |
|-----|------------------------------------------|---------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
|`-h` |`--help`                                  |                                                                     |show this help message and exit                                                                                                                           |
|     |`--DONT_DEFAULT_TO_HUMAN_READABLE_NUMBERS`|                                                                     |Sets wether numbers are converted into smaller numbers by default, can be overwritten for each API call                                                   |
|     |`--LOG_FORMAT`                            |`[%(asctime)s][PID:%(process)d][%(levelname)s][%(name)s] %(message)s`|Set log format, usable values are the values supported by logging                                                                                         |
|     |`--LOG_LEVEL`                             |`INFO`                                                               |Set the log level used by the logger                                                                                                                      |
|     |`--LOG_STDOUT`                            |                                                                     |If used log to stdout, otherwise to stderr                                                                                                                |
|     |`--LOG_PREFIX`                            |``                                                                   |Set a prefix that will be prefaced to every logging output                                                                                                |
|     |`--MAX_WORKER_THREADS`                    |`4`                                                                  |Limits the number of worker threads that work on the actual tasks at once                                                                                 |
|     |`--ONLY_CHOOSEN_REST_API_VERSION`         |                                                                     |If set will only provide one version of the api links                                                                                                     |
|     |`--PENDING_TASKS_SOFT_LIMIT`              |`100`                                                                |Limits tasks being added by the REST-API, to not have more than PENDING_TASKS_SOFT_LIMIT tasks waiting                                                    |
|`-p` |`--REST_API_PORT`                         |`12121`                                                              |Choose a port that the REST-API will be listening on                                                                                                      |
|     |`--REST_API_VERSION`                      |`1`                                                                  |Choose a major version of the rest api. Depending on ONLY_CHOOSEN_REST_API_VERSION, only this version, or all versions up to this version will be avaiable|
|     |`--SHORT_JOB_MAX_TIME`                    |`0.1`                                                                |Short jobs will be executed rigth away and return results directly via REST-API, blocking all other mpi communication in between [s]                      |
|     |`--USER_DEFINED_TOKEN`                    |`None`                                                               |Define one additional token with scope level, separate multiple tokens by ;Example "--USER_DEFINED_TOKEN=12345678:100"                                    |
|`-v` |`--version`                               |                                                                     |Print Version number of JuMonC                                                                                                                            |

### `-h`, `--help`
show this help message and exit

### `--DONT_DEFAULT_TO_HUMAN_READABLE_NUMBERS`
Sets wether numbers are converted into smaller numbers by default, can be
overwritten for each API call

### `--LOG_FORMAT` (Default: [%(asctime)s][PID:%(process)d][%(levelname)s][%(name)s] %(message)s)
Set log format, usable values are the values supported by logging

### `--LOG_LEVEL` (Default: INFO)
Set the log level used by the logger

### `--LOG_STDOUT`
If used log to stdout, otherwise to stderr

### `--LOG_PREFIX` (Default: )
Set a prefix that will be prefaced to every logging output

### `--MAX_WORKER_THREADS` (Default: 4)
Limits the number of worker threads that work on the actual tasks at once

### `--ONLY_CHOOSEN_REST_API_VERSION`
If set will only provide one version of the api links

### `--PENDING_TASKS_SOFT_LIMIT` (Default: 100)
Limits tasks being added by the REST-API, to not have more than
PENDING_TASKS_SOFT_LIMIT tasks waiting

### `-p`, `--REST_API_PORT` (Default: 12121)
Choose a port that the REST-API will be listening on

### `--REST_API_VERSION` (Default: 1)
Choose a major version of the rest api. Depending on
ONLY_CHOOSEN_REST_API_VERSION, only this version, or all versions up to this
version will be avaiable

### `--SHORT_JOB_MAX_TIME` (Default: 0.1)
Short jobs will be executed rigth away and return results directly via REST-
API, blocking all other mpi communication in between [s]

### `--USER_DEFINED_TOKEN` (Default: None)
Define one additional token with scope level, separate multiple tokens by
;Example "--USER_DEFINED_TOKEN=12345678:100"

### `-v`, `--version`
Print Version number of JuMonC


