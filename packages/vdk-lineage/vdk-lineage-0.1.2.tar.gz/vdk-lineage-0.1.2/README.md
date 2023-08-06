# VDK Lineage

VDK Lineage plugin provides lineage data (input data -> job -> output data) information and send it to pre-configured
destination. 

At POC level currently. It collect lineage information for each job run and for each executed query. 
Query execution is currently before it's executed (so not query status is logged).


## Usage

```
pip install vdk-lineage
```

And it will start collecting lineage from job and sql queries. 

To send data using openlineage specify VDK_OPENLINEAGE_URL. For example: 
```
export VDK_OPENLINEAGE_URL=http://localhost:5002
```

## Build and testing

In order to build and test a plugin go to the plugin directory and use `../build-plugin.sh` script to build it
