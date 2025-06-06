from rich.console import Console
from rich.table import Table


def format_responses(journeys):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("From")
    table.add_column("To")
    table.add_column("Scheduled dept.")
    table.add_column("Estimated dept.")
    table.add_column("Arrival time")
    table.add_column("Platform")

    for journey in journeys:
        table.add_row(
            f"[bold]{journey['departure_station_name']}[/bold]",
            journey["destination_location_name"],
            journey["scheduled_departure"],
            journey["estimated_departure"],
            journey["arrival"],
            journey["platform"],
        )
        table.add_section()

    console.print(table)
