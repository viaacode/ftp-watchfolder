# ftp-watchfolder
This python daemon watches one or more directories on a server for incoming files or groups of files. Files are grouped based on their filename. The daemon watches for certain (configurable) files, based on extension.

# Usage

After placing the needed .watcher.conf file in the directory you want to monitor you can start/stop/restart a daemon with the following command:

```
python3 watcher.py start|stop|restart [directory_path]
```

Example: python3 watcher.py start /home/viaa/watchfolder

# Configuration

## Dependencies

If you havn't done so already, install pip3 to use the pip package manager of python:

```
    sudo apt-get install python3-pip
```

The daemon relies on 2 non-standard python3 libraries

### Pika

This is used to establish the connection to RabbitMQ. Install this with pip or your package manager

```
    pip3 install pika
```

```
    sudo apt-get install python-pika
```

The used library is also included in the branch, your can manually install this with:
```
    pip3 install pika.whl
```

### PyInotify

This is used to hook into inotify. Install this with pip or your package manager

```
    pip3 install pyinotify
```
```
    sudo apt-get install python-pyinotify
```

The used library is also included in the branchm you can manually install this with:


```
    python3 setup.py install
```

## Starting the daemon

To start the daemon you will need to create a .watcher.conf file in the directory. The conf file must have the follwoing structure:

```
[DEFAULT]
CP = VRT                                            # CP Name
FLOW_ID = VRT.VIDEO.1                               # System unique flow id
ESSENCE_FILE_TYPE = mxf|txt                         # Extensions defining the Essence file, seperated by '|' if more
SIDECAR_FILE_TYPE = xml                             # Extensions defining the sidecar, same as essence
COLLATERAL_FILE_TYPE = srt                          # Extensions defining the collateral file, same as essence. Leave this empty if no extensions apply (daemon will not check on collaterals)
RABBIT_MQ_HOST = do-tst-rab-01.do.viaa.be           # RabbitMQ hostname/address
RABBIT_MQ_PORT = 5672                               # RabbitMQ host server port
RABBIT_MQ_SUCCESS_EXCHANGE = daemon.success         # Exchange name for the completed package
RABBIT_MQ_SUCCESS_QUEUE = vrt.video.1               # The queue name to bind to for completed package exchange
RABBIT_MQ_ERROR_EXCHANGE = daemon.errors            # Exchange name for failed packages
RABBIT_MQ_ERROR_QUEUE = incomplete_packages         # Queue name to bind to the failed packag exchange
RABBIT_MQ_TOPIC_TYPE = direct                       # Topic type set on the Exchanges on creations if they do not exist
RABBIT_MQ_USER = admin                              # Username for RabbitMQ access
RABBIT_MQ_PASSWORD = test123                        # Password for RabbitMQ user specified above
CHECK_PACKAGE_INTERVAL = 1                          # Interval the daemon has to wait between package completion checks
PROCESSING_FOLDER_NAME = processing                 # Folder name to move completed packages to, this folder has to exist in the folder you want to watch
INCOMPLETE_FOLDER_NAME = incomplete                 # Folder name to move failed packages to, same as above.

```

When you start the daemon there will be 2 additional hidden files created by the process:

1. .watcher.pid
    * This file contains the process nummer of the running process for this specific folder. This is used to stop the daemon process for this directory.
2. .watcher.log
    * This file contains all logs written by the process. You can watch this file to monitor the running process for this specific directory.