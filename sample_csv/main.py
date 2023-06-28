import os
from typing import Annotated
import pandas as pd
import random
import typer
from rich.console import Console
from rich.table import Table
from rich.filesize import decimal as filesize_decimal
from rich.progress import Progress, SpinnerColumn, TextColumn, open


app = typer.Typer(add_completion=False)
console = Console()


from rich.status import Status


@app.command()
def sample_csv(
    input_path: Annotated[str, typer.Argument(help="Path to the input CSV file.")],
    percentage: Annotated[
        float,
        typer.Argument(
            help="Percentage of data to sample. The value should be between 0.0 and 1.0.",
        ),
    ] = 0.1,
):
    """
    A minimal CLI tool for sampling data from large CSV files.
    """
    console = Console()

    # Check if the input file exists
    if not os.path.exists(input_path):
        console.print(f"[red]Error:[/red] The file {input_path} does not exist.")
        return

    # Autogenerate output path
    file_name = os.path.basename(input_path)
    name, ext = os.path.splitext(file_name)
    percentage_str = f"{percentage*100:.2g}"
    sampled_file_name = f"{name}_sampled_{percentage_str}{ext}"

    output_path = os.path.join(os.path.dirname(input_path), sampled_file_name)

    console.print(
        f"Sampling [yellow]{percentage_str}%[/yellow] of rows into [magenta]{output_path}[/magenta]"
    )

    with open(
        input_path,
        "rb",
        description="Reading file...",
    ) as f:
        num_lines = sum(1 for _ in f)

    with Status("Sampling...", console=console):
        skip = int(num_lines * (1 - percentage))
        skip_ids = sorted(random.sample(range(1, num_lines + 1), skip))  # 0-indexed
        df = pd.read_csv(input_path, skiprows=skip_ids)

    # Check if the output file already exists
    if os.path.exists(output_path):
        typer.confirm(
            f"The file {output_path} already exists. Do you want to overwrite it?",
            abort=True,
            default=True,
        )

    with Status("Writing to new file...", console=console):
        # Save the DataFrame to a new CSV file
        df.to_csv(output_path, index=False)

    # Create a table for the output
    table = Table(title="")

    table.add_column("Input")
    table.add_column("Output")

    table.add_row(input_path, output_path, style="magenta")
    table.add_row(
        filesize_decimal(os.path.getsize(input_path)),
        filesize_decimal(os.path.getsize(output_path)),
        style="green",
    )
    table.add_row(
        f"{num_lines} rows",
        f"{df.shape[0]} rows",
        style="yellow",
    )

    console.print(table)
