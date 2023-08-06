# SDPA-OFDM

OFDM Modulation


## Installation

    pip install SDPA-OFDM

## Usage

```python
from SDPA_OFDM import ofdm_modulator

mod = ofdm_modulator(args)

I, Q = mod.messageToIQ(message)
```

## Current version : 1.0.0

The package has been tested with SDPA-MR-OFDM and provides correct values when compared with 802.15.4g specification
