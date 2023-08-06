# alma-hilse

ALMA Hardware-In-the-Loop Simulation Environment setup, monitoring and verification package.

The `alma-hilse` package provides an application and libraries aiming to help in the setup, monitoring and verfication of the ALMA HILSE infrastructure.
Most online requests are based on the AmbManager object to minimize dependencies.

## Installation

    pip install alma-hilse

If installed for user only, it may be necessary to modify PATH accordingly by running:

    export PATH=$PATH:$HOME/.local/bin/

## Installation for development

    git clone ssh://git@bitbucket.sco.alma.cl:7999/esg/alma-hilse.git
    make venv
    source venv/bin/activate
    alma-hilse --help

## Usage

Following is a non-exhaustive list of available commands, for illustrative purposes only. Use the following command for all available options:

    alma-hilse --help

### Timing-related commands

    alma-hilse timing --help
    alma-hilse timing status # LORR/LFTRR status for HILSE
    alma-hilse timing resync # LORR/LFTRR resync to CLO reference

![lftrr status example](https://raw.githubusercontent.com/bandaangosta/alma-hilse/master/img/lftrr_status.png)

### Correlator-related commands
    alma-hilse corr --help
    alma-hilse corr status # power, parity and delay status of DRXs
    alma-hilse corr set-metaframe-delays # NOT IMPLEMENTED YET
    alma-hilse corr mute-edfa # NOT IMPLEMENTED YET
    alma-hilse corr eeprom-read # NOT IMPLEMENTED YET
    alma-hilse corr eeprom-write # NOT IMPLEMENTED YET

![lftrr status example](https://raw.githubusercontent.com/bandaangosta/alma-hilse/master/img/drx_status.png)

### General environment setup and troubleshooting commands
    alma-hilse utils --help
    alma-hilse utils get-devices # list devices connected to ABM
    alma-hilse utils turn-on-ambmanager
    alma-hilse utils array-info # NOT IMPLEMENTED YET (to be based on existing BE scripts)

###  Antenna integration-related commands
Generation of reports aiming to help in the integration of new antennas to HILSE enviroment. E.g., by collecting relevant information to be used during AOS patch panel fiber movements and following verifications.

    alma-hilse integration --help  # NOT IMPLEMENTED YET
    alma-hilse integration general-status  # NOT IMPLEMENTED YET (to be based on existing BE scripts)
    alma-hilse integration lo-resources  # NOT IMPLEMENTED YET (to be based on existing BE scripts)
    alma-hilse integration dts-resources # NOT IMPLEMENTED YET (to be based on existing BE scripts)
    alma-hilse integration pad-resources # NOT IMPLEMENTED YET
