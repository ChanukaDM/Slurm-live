from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def render_header(job_id, info):
    table = Table(show_header=False)

    table.add_row("Job ID", str(job_id))
    table.add_row("State", info.get("job_state", "Unknown"))
    table.add_row("Runtime", info.get("run_time", "Unknown"))
    table.add_row("Node", info.get("node_list", "Unknown"))

    panel = Panel(table, title="slurm-live", expand=False)

    console.print(panel)


def print_log(line):
    console.print(line, end="")