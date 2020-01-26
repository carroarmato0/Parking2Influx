# Parking2Influx

Python script which fetches the realtime parking data of Gent and inputs it into InfluxDB running inside a Docker container.

```bash
➜  Parking2Influx ./parking2influx.py
➜  Parking2Influx docker exec -it influxdb /bin/bash
root@19f74fe5802a:/# influx
Connected to http://localhost:8086 version 1.7.9
InfluxDB shell version: 1.7.9
> use parking
Using database parking
> show measurements
name: measurements
name
----
state
> select * from state
name: state
time       city   current_capacity description         latitude   longitude max_capacity name                    open
----       ----   ---------------- -----------         --------   --------- ------------ ----                    ----
1580042365 'Gent' 113              'Ramen'             '51.05532' '3.71653' 270          'P08 Ramen'             1
1580042365 'Gent' 319              'Vrijdagmarkt'      '51.05652' '3.72595' 647          'P01 Vrijdagmarkt'      1
1580042365 'Gent' 595              'Sint-Pietersplein' '51.04171' '3.72557' 678          'P10 Sint-Pietersplein' 1
1580042365 'Gent' 216              'Sint-Michiels'     '51.05367' '3.7186'  465          'P07 Sint-Michiels'     1
1580042365 'Gent' 443              'Savaanstraat'      '51.04862' '3.72225' 540          'P04 Savaanstraat'      1
1580042365 'Gent' 315              'Reep'              '51.05207' '3.72981' 449          'P02 Reep'              1
```
