"""Classes which represent features in the genome.

Classes which represent features in the genome

  Typical usage example:

  exon = Exon(length=1000)
  intron = Intron()
  transcript = Transcript()
  gene = Gene()
  intergenic = Intergenic()
"""

from insilicodna import core


class Exon:
    """Class representation of an exon.

    A simplified represention of the molecular object, exon.
    Sequences are represented in upper case.

    Attributes:
        synid (str): A unique, synthetic ID.
        length (int): Number of base pairs in the sequence.
        sequence (list of str): A list of base pairs.

    """
    def __init__(self, synid=None, length=60):
        length = max(length, 60)
        if synid is None:
            synid = f"SYNEXON-{core.generate_uuid4()}"
        self.synid = synid
        self.length = length
        self.sequence = core.generate_sequence(self.length)

class Intron:
    """Class representation of an intron.

    A simplified represention of the molecular object, intron.
    Sequences are represented in lower case.

    Attributes:
        synid (str): A unique, synthetic ID.
        length (int): Number of base pairs in the sequence.
        sequence (list of str): A list of base pairs.

    """
    def __init__(self, synid=None, length=100):
        length = max(length, 60)
        if synid is None:
            synid = f"SYNINTRON-{core.generate_uuid4()}"
        self.synid = synid
        self.length = length
        self.sequence = core.generate_sequence(self.length, upper=False)

class Transcript:
    """Class representation of a transcript.

    A simplified represention of the molecular object, transcript.

    Attributes:
        synid (str): A unique, synthetic ID.
        exons (list of obj): A list of Exon objects.
        sequence (list of str): A composite of Exon sequences,
            in order of exons in list.

    """
    def __init__(self, exons, synid=None):
        if synid is None:
            synid = f"SYNTRANSCRIPT-{core.generate_uuid4()}"
        self.synid = synid
        self.exons = exons
        self.sequence = []
        for exon in self.exons:
            self.sequence.extend(exon.sequence)

class Gene:
    """Class representation of a gene.

    A simplified represention of the molecular object, gene.

    Attributes:
        synid (str): A unique, synthetic ID.
        exons (list of obj): A list of Exon objects.
        introns (list of obj): A list of Intron objects.
        transcripts (list of obj): A list of Transcript objects.
        gene_structure (list of obj): A list of Exon and
            Intron objects.
        sequence (list of str): A list of base pairs.
        length (int): Number of base pairs in the sequence.

    """
    def __init__(self, synid=None, exons=None, introns=None, transcripts=None):
        if synid is None:
            synid = f"SYNGENE-{core.generate_uuid4()}"
        self.synid = synid
        if exons is None:
            exons = []
        self.exons = exons
        if introns is None:
            introns = []
        self.introns = introns
        if transcripts is None:
            transcripts = []
        self.transcripts = transcripts
        self.gene_structure = None
        self.sequence = None
        self.length = None

    def add_exon(self, exon):
        """Adds an Exon object to the list of exons.

        Appends an Exon object to the list of exons.

        Args:
            exon:
              A single Exon object.

        """
        self.exons.append(exon)

    def add_intron(self, intron):
        """Adds an Intron object to the list of introns.

        Appends an Intron object to the list of introns.

        Args:
            intron:
              A single Intron object.

        """
        self.exons.append(intron)

    def add_transcript(self, transcript):
        """Adds an Transcript object to the list of transcripts.

        Appends an Transcript object to the list of transcripts.

        Args:
            transcript:
              A single Transcript object.

        """
        self.transcripts.append(transcript)

    def generate_sequence(self):
        """Generates a gene sequence.

        Generates a an attribute, `gene_structure` which
        maintains a list of objects to represent a gene.

        """
        exons = self.exons
        introns = self.introns
        gene_structure = [None]*(len(exons)+len(introns))
        gene_structure[::2] = exons
        gene_structure[1::2] = introns
        sequence = []
        for item in gene_structure:
            sequence.extend(item.sequence)
        self.gene_structure = gene_structure
        self.sequence = sequence
        self.length = len(sequence)

    def generate_fasta_gene(self, filename=None):
        """Generates FASTA formated gene sequence.

        Generates FASTA formated gene sequence.

        Args:
            filename:
                Name of output FASTA file

        Returns:
            If `filename` is supplied, a file is returned,
            otherwise the FASTA sequence is printed as stdout.

        """
        exons = self.exons
        introns = self.introns
        exons_introns = [None]*(len(exons)+len(introns))
        exons_introns[::2] = exons
        exons_introns[1::2] = introns
        sequence = []
        for item in exons_introns:
            sequence.extend(item.sequence)
        fasta = [{self.synid: sequence}]
        if filename is None:
            core.print_fasta(fasta)
        else:
            core.generate_fasta_file(filename, fasta)

    def generate_fasta_transcripts(self, filename=None):
        """Generates FASTA formated transcript sequence.

        Generates FASTA formated transcript sequence.

        Args:
            filename:
                Name of output FASTA file

        Returns:
            If `filename` is supplied, a file is returned,
            otherwise the FASTA sequence is printed as stdout.

        """
        fasta = []
        for transcript in self.transcripts:
            transcript_dict = {transcript.synid: transcript.sequence}
            fasta.append(transcript_dict)
        if filename is None:
            core.print_fasta(fasta)
        else:
            core.generate_fasta_file(filename, fasta)

    def generate_fasta_exons(self, filename=None):
        """Generates FASTA formated exon sequence.

        Generates FASTA formated exon sequence.

        Args:
            filename:
                Name of output FASTA file

        Returns:
            If `filename` is supplied, a file is returned,
            otherwise the FASTA sequence is printed as stdout.

        """
        fasta = []
        for exon in self.exons:
            exon_dict = {exon.synid: exon.sequence}
            fasta.append(exon_dict)
        if filename is None:
            core.print_fasta(fasta)
        else:
            core.generate_fasta_file(filename, fasta)

class Intergenic:
    """Class representation of intergenic dna.

    A simplified represention of intergenic dna.

    Attributes:
        synid (str): A unique, synthetic ID.
        length (int): Number of base pairs in the sequence.
        sequence (list of str): A list of base pairs.

    """
    def __init__(self, synid=None, length=100):
        length = max(length, 60)
        if synid is None:
            synid = f"SYNINTERGENIC-{core.generate_uuid4()}"
        self.synid = synid
        self.length = length
        self.sequence = core.generate_sequence(self.length, upper=False)
