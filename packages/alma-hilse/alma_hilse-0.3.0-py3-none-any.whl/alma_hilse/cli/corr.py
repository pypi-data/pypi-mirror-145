import typer
from typing import Optional
from alma_hilse.lib.corr.drx import Drx

corr_app = typer.Typer(short_help="HILSE correlator related commands")


@corr_app.callback()
def corr_app_callback():
    """
    Obtain basic status of HILSE correlator device.

    Usage:

    \b
    alma-hilse corr --help
    alma-hilse corr status # power, parity and delay status of DRXs

    """


@corr_app.command("status", short_help="DRX power and status check")
def status_drx(
    abm: Optional[str] = typer.Option(None, help="ABM name for AmbManager"),
    nodes: Optional[str] = typer.Option(
        None, help="Comma-separate 4 nodes list for DRXs"
    ),
    channels: Optional[str] = typer.Option(
        None, help="Comma-separate 4 channel list for DRXs"
    ),
):
    try:
        drx = Drx(abm, nodes, channels)
        drx.get_drx_status()
    except Exception as e:
        print(f"Error: {str(e)}")
