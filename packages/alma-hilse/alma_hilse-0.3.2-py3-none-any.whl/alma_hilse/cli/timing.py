import typer
from typing import Optional
from alma_hilse.lib.lo_timing.lftrr import Lftrr

timing_app = typer.Typer(short_help="LFTRR/LORR related commands")


@timing_app.callback()
def timing_app_callback():
    """
    Obtain basic status of HILSE LFTRR device and issue resync command.

    Referring to the status, a stripped down version of the LORR status is presented,
    focusing only on variables relevant to HILSE.

    Usage:

    \b
    alma-hilse timing status # Display LFTRR status
    alma-hilse timing resync # Resync TE to central reference
    alma-hilse timing clear  # Clear TE and PLL error flags

    """


@timing_app.command("status", short_help="LFTRR healthcheck")
def status_lftrr(
    abm: Optional[str] = typer.Option(None, help="ABM name for AmbManager"),
    node: Optional[int] = typer.Option(None, help="Node id for LFTRR/LORR"),
    channel: Optional[int] = typer.Option(None, help="Channel number for LFTRR/LORR"),
):
    try:
        lftrr = Lftrr(abm, node, channel)
        lftrr.status()
    except Exception as e:
        print(f"Error: {str(e)}")


@timing_app.command("resync", short_help="Resync TE to central reference")
def resync_te(
    abm: Optional[str] = typer.Option(None, help="ABM name for AmbManager"),
    node: Optional[int] = typer.Option(None, help="Node id for LFTRR/LORR"),
    channel: Optional[int] = typer.Option(None, help="Channel number for LFTRR/LORR"),
):
    try:
        lftrr = Lftrr(abm, node, channel)
        lftrr.resync_te()
    except Exception as e:
        print(f"Error: {str(e)}")


@timing_app.command("clear", short_help="Clear TE and PLL error flags")
def clear_flags(
    abm: Optional[str] = typer.Option(None, help="ABM name for AmbManager"),
    node: Optional[int] = typer.Option(None, help="Node id for LFTRR/LORR"),
    channel: Optional[int] = typer.Option(None, help="Channel number for LFTRR/LORR"),
):
    try:
        lftrr = Lftrr(abm, node, channel)
        lftrr.clear_flags()
    except Exception as e:
        print(f"Error: {str(e)}")
