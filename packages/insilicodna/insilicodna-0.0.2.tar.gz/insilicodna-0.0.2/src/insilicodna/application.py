"""Application level functions.

Functions called at the application level.

  Typical usage example:

  gene = generate_gene()
"""

import sys
import csv
import random
from itertools import combinations
from insilicodna.reference_genome import *
from insilicodna.core import chunks


def generate_gene(exon_lengths=None, n_transcripts=None):
    """Generate an instance of the Gene class.

    Generate an instance of Gene() class. If no exon lengths
    are provided, the number of exons and lengths are randomly
    sampled (uniform distribution) from a range. If number of
    transcripts are not provided, transcript number will be
    randomly sampled (uniform distrubtion) and a unique combination
    of exons will be provided.

    Args:
        exon_lengths:
          A list of ints of desired exon lengths.
        n_transcripts:
          An int of desired transcripts based on provided exons.

    Returns:
        An instance of the Gene() class

    """
    if not exon_lengths:
        n_exons = random.sample(range(1, 10), 1)[0]
        exon_lengths = random.sample(range(100, 1000), n_exons)
    # Build exons
    exons = [Exon(length=x) for x in exon_lengths]
    # Build introns
    n_introns = len(exon_lengths) - 1
    intron_lengths = random.sample(range(60, 300), n_introns)
    introns = [Intron(length=x) for x in intron_lengths]
    gene = Gene(exons=exons, introns=introns)
    gene.generate_sequence()
    # Build transcripts
    exon_combo = []
    for i in range(1, len(exon_lengths) + 1):
        combo_list = [list(x) for x in combinations(exons, i)]
        exon_combo.extend(combo_list)
    # Ensure first exon is included
    exon_combo = [x for x in exon_combo if exons[0] in x]
    if not n_transcripts:
        n_transcripts = random.sample(range(1, len(exon_lengths) + 1), 1)[0]
    transcript_combos = random.sample(exon_combo, n_transcripts)
    for exon_set in transcript_combos:
        transcript = Transcript(exon_set)
        gene.add_transcript(transcript)
    return gene

def generate_contig(
    seqid="synthetic-chromosome",
    n_genes=10,
    fasta_file=False,
    gff3_file=False,
    output_prefix="insilicodna-synthetic-data"):
    """Generate a modeled chromsome.

    Generate a modeled chromsome

    Args:
        seqid:
          A unique ID (str) to represent the contig ID.
        n_genes:
          An int of desired number of genes.

    Returns:
        An instance of the Gene() class

    """
    sequence = []
    gff3 = []
    chr_pos = 0
    for i in range(n_genes):
        intergenic = Intergenic()
        sequence.extend(intergenic.sequence)
        chr_pos += intergenic.length
        start = chr_pos + 1
        gene = generate_gene()
        sequence.extend(gene.sequence)
        chr_pos += gene.length
        attributes = f"ID={gene.synid};Name={gene.synid}"
        gff3_dict = {
            "seqid": seqid,
            "source": 'synthetic-molecular-data',
            "type": 'gene',
            "start": start,
            "end": chr_pos,
            "score": '.',
            "strand": '+',
            "phase": '.',
            "attributes": attributes
        }
        gff3.append(gff3_dict)
        # Print exon gff3
        unit_start = start
        for feature in gene.gene_structure:
            if isinstance(feature, Exon):
                featuretype = 'exon'
            elif isinstance(feature, Intron):
                featuretype = 'inton'
            else:
                pass
            unit_end = unit_start + feature.length - 1
            attributes = f"ID={feature.synid};Parent={gene.synid};Name={feature.synid}"
            gff3_dict = {
                "seqid": seqid,
                "source": 'synthetic-molecular-data',
                "type": featuretype,
                "start": unit_start,
                "end": unit_end,
                "score": '.',
                "strand": '+',
                "phase": '.',
                "attributes": attributes
            }
            unit_start = unit_end + 1
            gff3.append(gff3_dict)
        intergenic = Intergenic()
        sequence.extend(intergenic.sequence)
        chr_pos += intergenic.length

    # Print .fasta file
    if fasta_file:
        filename = f"{output_prefix}.fasta"
        seq_chunks = chunks(sequence_list=sequence, chunk_length=60)
        original_stdout = sys.stdout
        with open(filename, 'w', encoding="utf-8") as fileout:
            sys.stdout = fileout
            header = "SYNCHROMOSOME-"
            print(f">{header}")
            for line in seq_chunks:
                print("".join(line))
            sys.stdout = original_stdout

    # Print .gff3 file
    if gff3_file:
        filename = f"{output_prefix}.gff3"
        with open(filename, 'w', encoding="utf-8", ) as fileout:
            writer = csv.writer(fileout, delimiter='\t')
            writer.writerow(["##gff-version 3"])
        with open(filename, 'a', newline='', encoding="utf-8") as fileout:
            fieldnames = ['seqid', 'source', 'type', 'start',
                'end', 'score', 'strand', 'phase', 'attributes']
            writer = csv.DictWriter(fileout, fieldnames=fieldnames)
            for item in gff3:
                writer.writerow(item)
    return
