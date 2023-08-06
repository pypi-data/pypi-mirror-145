"""Command line interface.

Command line accessible functions.

  Typical usage example:

  $insilicodna test
"""
import random
import click
import insilicodna.application as app


@click.command()
@click.option('--version', is_flag=True, help="Will print version.")
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--gene-count', is_flag=False, default=1, help="Number of genes.")
@click.option('--output-prefix', is_flag=False, help="Assign file output prefix.")
@click.option('--fasta', is_flag=True, help="Will create the file, <prefix>.fasta.")
@click.option('--gff3', is_flag=True, help="Will create the file, <prefix>.gff3.")
def cli(
    version,
    verbose,
    gene_count,
    output_prefix,
    fasta,
    gff3):

    # Sepcify variables
    header = f"In Silico DNA v0.0.2"
    if not output_prefix:
        output_prefix = "synthetic"

    # Print version
    if version:
        click.echo(f"{header}")
        return

    # List options
    if not fasta and not gff3:
        click.echo(f"{header}")
        click.echo("")
        click.echo("Please specify at least one of the following options:")
        click.echo("  --fasta")
        click.echo("  --gff3")
        click.echo("")
        click.echo("To list all options:")
        click.echo("  insilicodna --help")
        click.echo("")
        click.echo("Common Usage:")
        click.echo("  insilicodna --fasta --output-prefix Example")
        click.echo("    Create a synthetic file called, Example.fasta")
        click.echo("  insilicodna --gff3")
        click.echo("    Create a synthetic .gff3 file.")
        click.echo("  insilicodna --fasta --gff3")
        click.echo("    Create both a synthetic .fasta and .gff3 file.")
        click.echo("  insilicodna --fasta --gene-count 50")
        click.echo("    Create both a synthetic .fasta with 50 genes")
        return

    # Print all actions
    if verbose:
        click.echo(f"{header}")
        click.echo("")
        click.echo(f"Setting number of genes: {gene_count}")
        click.echo(f"Setting output file prefix: {output_prefix}")
        if fasta:
            click.echo(f"Creating file {output_prefix}.fasta...")
        if gff3:
            click.echo(f"Creating file {output_prefix}.gff3...")

    # Create contig
    app.generate_contig(
        seqid="synthetic-chromosome",
        n_genes=gene_count,
        fasta_file=fasta,
        gff3_file=gff3,
        output_prefix=output_prefix)

    return
