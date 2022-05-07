# Envilog

## Usage
```
usage: envilog.py [-h] [-p PERIOD] [-q QUANT] [-v] path

Log values from Enviro+ HAT.

positional arguments:
  path                  Path to directory where logs are saved.

optional arguments:
  -h, --help            show this help message and exit
  -p PERIOD, --period PERIOD
                        Time in seconds between measurements, default: 1.
  -q QUANT, --quantities QUANT
                        Comma separated list of quantities that shold be logged, default: all.
  -v, --verbose         Print debug informations.

Allowed quantities: ['temperature', 'humidity', 'pressure', 'altitude', 'lux', 'proximity', 'gas_oxidising', 'gas_reducing', 'gas_nh3', 'noise_profile', 'all']	
```
