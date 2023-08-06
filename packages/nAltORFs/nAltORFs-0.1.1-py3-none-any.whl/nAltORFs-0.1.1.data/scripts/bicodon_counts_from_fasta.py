#!python

import argparse

from importlib.metadata import version
from sys import exit

from Bio import SeqIO

NUCS = list("atgc")

BICODON_HEADERS = [
    "Division",
    "Assembly",
    "Taxid",
    "Species",
    "Organelle",
    "Translation Table",
    "# CDS",
    "# Codon Pairs",
]
CODON_HEADERS = [
    "Division",
    "Assembly",
    "Taxid",
    "Species",
    "Organelle",
    "Translation Table",
    "# CDS",
    "# Codons",
]
HEADER_COUNT = 8


def __main__():
    parser = argparse.ArgumentParser(
        description="Get Codon and Bicodon frequency from FASTA files"
    )
    parser.add_argument("--seq", default="in.fasta", help="FASTA nucleotide sequences")
    parser.add_argument("--taxid", default="9606", help="tax id")
    parser.add_argument("--organelle", default="genomic", help="organelle")
    parser.add_argument("--codon_out", default=None, help="Path to codon usage output")
    parser.add_argument(
        "--bicodon_out", default=None, help="Path to bicodon usage output"
    )
    parser.add_argument("--division", default="custom", help="division")
    parser.add_argument("--assembly", default="hg38", help="assembly")
    parser.add_argument("--species", default="Homo sapiens", help="species")
    parser.add_argument("--translation_table", default="0", help="translation_table")
    parser.add_argument(
        "--version", action="store_true", help="Report version and exit"
    )
    args = parser.parse_args()

    if args.version:
        print("nAltORFs {}".format(version("naltorfs")))
        exit()

    codons = {}
    for i in NUCS:
        for j in NUCS:
            for k in NUCS:
                codons[i + j + k] = 0

    bicodons = {}
    for i in codons.keys():
        for j in codons.keys():
            bicodons[i + j] = 0

    for seq_count, seq_record in enumerate(SeqIO.parse(args.seq, "fasta"), 1):
        seq = str(seq_record.seq).lower()
        n = 3
        for i in range(0, len(seq), n):
            codon = seq[i : i + n]
            codons[codon] = codons[codon] + 1
        for i in range(0, len(seq) - n, n):
            bicodon = seq[i : i + 2 * n]
            bicodons[bicodon] = bicodons[bicodon] + 1

    def write_counts(count_dict, headers, filename):
        with open(filename, "w") as fh:
            keys = list(count_dict.keys())
            keys.sort()
            header = headers + keys
            fh.write("%s\n" % "\t".join(header))
            fh.write(
                "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"
                % (
                    args.division,
                    args.assembly,
                    args.taxid,
                    args.species,
                    args.organelle,
                    args.translation_table,
                    seq_count,
                    sum(count_dict.values()),
                )
            )
            for key in keys:
                fh.write("\t%i" % count_dict[key])
            fh.write("\n")

    write_counts(codons, CODON_HEADERS, args.codon_out)
    write_counts(bicodons, BICODON_HEADERS, args.bicodon_out)


if __name__ == "__main__":
    __main__()
