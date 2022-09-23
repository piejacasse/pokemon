from datetime import datetime

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, MofNCompleteColumn, TaskProgressColumn
from rich.syntax import Syntax
from rich.table import Table

console = Console()


class MyProgress(Progress):
    def get_renderables(self):
        yield Panel(self.make_tasks_table(self.tasks))

layout = Layout(name="root")

layout.split(
    Layout(name="main"),
    Layout(name="footer"),
)
layout["main"].split_column(
    Layout(name="side_up"),
    Layout(name="side_down"),
)
layout["side_up"].split_row(
    Layout(name="hp_bar"),
    Layout(name="side_right", ratio=2),
)

layout["side_down"].split_row(
    Layout(name="side_right", ratio=2),
    Layout(name="hp_bar"),
)

console.print(layout)

job_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    MofNCompleteColumn(separator='/', table_column=None),
    # TimeRemainingColumn(),
)
job_progress.add_task("[magenta]HP", total=200)

progress_table = Table.grid(expand=True,)
progress_table.add_row(
    Panel(job_progress, title="[b]HP", border_style="cyan", padding=(1, 2), height=8),
)

layout["hp_bar"].update(progress_table)
layout["side_down"]["hp_bar"].update(job_progress)

console.print(layout)