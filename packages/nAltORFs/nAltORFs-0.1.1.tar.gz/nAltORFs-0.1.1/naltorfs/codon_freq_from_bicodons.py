#!/usr/bin/env python3

import argparse

from importlib.metadata import version
from sys import exit

from Bio.Seq import translate

# headers = "Division Assembly    Taxid   Species Organelle   Translation Table   # CDS   # Codon Pairs"
HEADER_COUNT = 8


def __main__():
    parser = argparse.ArgumentParser(
        description="Get Codon frequency from bicodon frames"
    )
    parser.add_argument(
        "--bicodons", default="o586358-Refseq_Bicod.tsv", help="Bicondon rates input"
    )
    parser.add_argument("--taxid", default="9606", help="tax id")
    parser.add_argument("--organelle", default="genomic", help="tax id")
    parser.add_argument("--out", default=None, help="Path to output")
    parser.add_argument("--aa_out", default=None, help="Path to AA output")
    parser.add_argument(
        "--version", action="store_true", help="Report version and exit"
    )
    args = parser.parse_args()

    if args.version:
        print("nAltORFs {}".format(version("naltorfs")))
        exit()

    codons1 = {}
    codons2 = {}
    aa1 = {}
    aa2 = {}
    with open(args.bicodons, "r") as fh:
        header = fh.readline().strip().split("\t")
        taxid_index = header.index("Taxid")
        organelle_index = header.index("Organelle")
        # codon_pairs_index = header.index('# Codon Pairs')
        bicodons = header[HEADER_COUNT:]
        print("Using %i codon pairs" % (len(bicodons)))
        # TODO: should we confirm all codon pairs are actually listed in header?
        for line in fh:
            line = line.strip().split("\t")
            if (
                line[taxid_index] == args.taxid
                and line[organelle_index] == args.organelle
            ):
                bicodon_counts = line[HEADER_COUNT:]
                assert len(bicodons) == len(
                    bicodon_counts
                ), "Bicodons and bicodons counts are not same length"
                for bicodon, count in zip(bicodons, bicodon_counts):
                    codon = bicodon[1:4]
                    count = int(count)
                    if codon not in codons1:
                        codons1[codon] = []
                    codons1[codon].append(count)
                    aa = translate(codon)
                    if aa not in aa1:
                        aa1[aa] = 0
                    aa1[aa] = aa1[aa] + count
                    codon = bicodon[2:5]
                    if codon not in codons2:
                        codons2[codon] = []
                    codons2[codon].append(count)
                    aa = translate(codon)
                    if aa not in aa2:
                        aa2[aa] = 0
                    aa2[aa] = aa2[aa] + count
                break

    c1_keys = list(codons1.keys())
    c2_keys = list(codons2.keys())
    c_keys = list(set(c1_keys + c2_keys))
    c_keys.sort()
    print("Reporting %i codons" % len(c_keys))
    assert (
        len(c1_keys) == len(c2_keys) == len(c_keys)
    ), "Mismatching key lengths of codons"
    with open(args.out, "w") as fh:
        fh.write("#frame\tcodon_count\t%s\n" % ("\t".join(c_keys)))
        codons = {}
        for key, value in codons1.items():
            codons[key] = sum(value)
        codon_count = sum(codons.values())
        fh.write("2-counts\t%i" % codon_count)
        for key in c_keys:
            fh.write("\t%i" % (codons[key]))
        fh.write("\n")
        percent = 0
        fh.write("2-percent\t%i" % codon_count)
        for key in c_keys:
            p = codons[key] / codon_count * 100
            fh.write("\t%.28f" % (p))
            percent += p
        fh.write("\n")
        print("Found a total of %f percent for 2." % percent)

        codons = {}
        for key, value in codons2.items():
            codons[key] = sum(value)
        codon_count = sum(codons.values())
        fh.write("3-counts\t%i" % codon_count)
        for key in c_keys:
            fh.write("\t%i" % (codons[key]))
        fh.write("\n")
        percent = 0
        fh.write("3-percent\t%i" % codon_count)
        for key in c_keys:
            p = codons[key] / codon_count * 100
            fh.write("\t%.28f" % (p))
            percent += p
        fh.write("\n")
        print("Found a total of %f percent for 3." % percent)

    aa1_keys = list(aa1.keys())
    aa2_keys = list(aa2.keys())
    aa_keys = list(set(aa1_keys + aa2_keys))
    aa_keys.sort()
    print("Reporting %i amino acids" % len(aa_keys))
    assert (
        len(aa1_keys) == len(aa2_keys) == len(aa_keys)
    ), "Mismatching key lengths of amino acids"
    with open(args.aa_out, "w") as fh:
        fh.write("#frame\taa_count\t%s\n" % ("\t".join(aa_keys)))
        aas = aa1
        aa_count = sum(aas.values())
        fh.write("2-counts\t%i" % aa_count)
        for key in aa_keys:
            fh.write("\t%i" % (aas[key]))
        fh.write("\n")
        percent = 0
        fh.write("2-percent\t%i" % aa_count)
        for key in aa_keys:
            p = aas[key] / aa_count * 100
            fh.write("\t%.28f" % (p))
            percent += p
        fh.write("\n")
        print("Found a total of %f percent for 2-aa." % percent)

        aas = aa2
        aa_count = sum(aas.values())
        fh.write("3-counts\t%i" % aa_count)
        for key in aa_keys:
            fh.write("\t%i" % (aas[key]))
        fh.write("\n")
        percent = 0
        fh.write("3-percent\t%i" % aa_count)
        for key in aa_keys:
            p = aas[key] / aa_count * 100
            fh.write("\t%.28f" % (p))
            percent += p
        fh.write("\n")
        print("Found a total of %f percent for 3-aa." % percent)


if __name__ == "__main__":
    __main__()
