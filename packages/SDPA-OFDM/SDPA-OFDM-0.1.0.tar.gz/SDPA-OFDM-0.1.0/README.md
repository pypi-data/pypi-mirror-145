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