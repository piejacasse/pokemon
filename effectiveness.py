import pandas
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table
import random
import math
import inquirer

from datetime import datetime

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, MofNCompleteColumn
from rich.table import Table

console = Console()

#layout["root"].size = 10

# layout.split(
#     Layout(name="main"),
#     Layout(name="footer"),
# )
# layout["main"].split_column(
#     Layout(name="side_up"),
#     Layout(name="side_down"),
# )
# layout["side_up"].split_row(
#     Layout(name="hp_bar"),
#     Layout(name="side_right", ratio=2),
# )

# layout["side_down"].split_row(
#     Layout(name="side_right", ratio=2),
#     Layout(name="hp_bar"),
# )

hp_progress_foe = Progress(
    "{task.description}",
    SpinnerColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    BarColumn(),
)

hp_progress_player = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    MofNCompleteColumn(separator='/', table_column=None),
)

hp_progress_foe.add_task("[magenta]HP")
hp_progress_player.add_task("[red]HP", total=200)

progress_table_player = Table.grid(expand=True,)
progress_table_player.add_row(
    Panel(hp_progress_player, title="[b]HP", border_style="green", padding=(1, 2), height=5),
)

progress_table_foe = Table.grid(expand=True,)
progress_table_foe.add_row(
    Panel(hp_progress_foe, title="[b]HP", border_style="magenta", padding=(1, 2), height=5),
)

pokemon_name = Table.grid(padding=1, expand=True)
pokemon_name.add_column(style="b magenta")
pokemon_name.add_column(justify="right", style="b cyan")
pokemon_name.add_row(
    "Zubat",
    "Lvl: 1",
)

pokemon_panel_foe = Table.grid(padding=1, expand=True)
pokemon_panel_foe.add_column(style="b magenta", ratio=1)
pokemon_panel_foe.add_column(justify="right", style="b cyan", ratio=2)
pokemon_panel_foe.add_row(
    Panel(pokemon_name, title="your foe", title_align="left", border_style="red", padding=(1, 2), height=5),
    progress_table_foe,
)

pokemon_panel_player = Table.grid(padding=1, expand=True)
pokemon_panel_player.add_column(style="b magenta", ratio=2)
pokemon_panel_player.add_column(justify="right", style="b cyan", ratio=1)
pokemon_panel_player.add_row(
    progress_table_player,
    Panel(pokemon_name, title="your pokemon", title_align="left", border_style="green", padding=(1, 2), height=5),
)

message_panel = Panel("INSTRUCTIONS \n ### \n ### \n ###",
    box=box.ROUNDED,
    padding=(1, 2),
    title="[b orange1]message panel",
    border_style="cyan")

interface = Panel(
        Align.center(
            Group(pokemon_panel_foe,pokemon_panel_player, message_panel),
            vertical="middle",
        ),
        box=box.HEAVY,
        padding=(1, 2),
        title="[b blue]POKEMON GAME",
        title_align='right',
        border_style="dark_blue",
        expand=False,
    )

# console.print(progress_table_player)
# console.print(hp_progress_player)
console.print(interface)