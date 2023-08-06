#!python

import argparse

from importlib.metadata import version
from sys import exit, stderr

from Bio.Seq import reverse_complement, translate

from twobitreader import TwoBitFile

FA_SEP = "|"

log_wtr = stderr


def get_bed_from_line(line, log_wtr=log_wtr):
    fields = line.rstrip("\r\n").split("\t")
    if len(fields) < 12:
        raise Exception("BADBED: Not a proper 12 column BED line (%s)." % line)
    (
        chrom,
        chromStart,
        chromEnd,
        name,
        score,
        strand,
        thickStart,
        thickEnd,
        itemRgb,
        blockCount,
        blockSizes,
        blockStarts,
    ) = fields[0:12]
    bed = BedInterval(
        chrom=chrom,
        chromStart=chromStart,
        chromEnd=chromEnd,
        name=name,
        score=score,
        strand=strand,
        thickStart=thickStart,
        thickEnd=thickEnd,
        itemRgb=itemRgb,
        blockCount=blockCount,
        blockSizes=blockSizes,
        blockStarts=blockStarts,
        log_wtr=log_wtr,
    )
    return bed


def make_int_list(obj, sep=","):
    if obj is None:
        return None
    if isinstance(obj, list):
        return [int(x) for x in obj]
    return [int(x) for x in obj.rstrip(sep).split(sep)]


def get_all_canonical_sequences(input_rdr, twobit, log_wtr=log_wtr):
    tell = input_rdr.tell()
    rval = []
    i = 0
    for i, bedline in enumerate(input_rdr, start=1):
        try:
            bed = get_bed_from_line(bedline)
            regions, cds = bed.get_cds(twobit)
            if cds and cds not in rval:
                rval.append(cds)
        except Exception as e:
            print("Cannot determine CDS for exclusion: %s" % str(e), file=log_wtr)
    print(
        "Excluding %i unique canonical coding sequences from %i BED lines."
        % (len(rval), i),
        file=log_wtr,
    )
    input_rdr.seek(tell)
    return rval


class BedInterval(object):
    def __init__(
        self,
        chrom=None,
        chromStart=None,
        chromEnd=None,
        name=None,
        score=None,
        strand=None,
        thickStart=None,
        thickEnd=None,
        itemRgb=None,
        blockCount=None,
        blockSizes=None,
        blockStarts=None,
        log_wtr=log_wtr,
    ):
        self.chrom = chrom
        self.chromStart = int(chromStart)
        self.chromEnd = int(chromEnd)
        self.name = name
        self.score = int(score) if score is not None else 0
        self.strand = "-" if str(strand).startswith("-") else "+"
        self.thickStart = int(thickStart) if thickStart else self.chromStart
        self.thickEnd = int(thickEnd) if thickEnd else self.chromEnd
        self.itemRgb = str(itemRgb) if itemRgb is not None else r"100,100,100"
        self.blockCount = int(blockCount)
        self.blockSizes = make_int_list(blockSizes)
        self.blockStarts = make_int_list(blockStarts)
        self.log_wtr = log_wtr

    def __str__(self):
        return "%s\t%d\t%d\t%s\t%d\t%s\t%d\t%d\t%s\t%d\t%s\t%s" % (
            self.chrom,
            self.chromStart,
            self.chromEnd,
            self.name,
            self.score,
            self.strand,
            self.thickStart,
            self.thickEnd,
            str(self.itemRgb),
            self.blockCount,
            ",".join([str(x) for x in self.blockSizes]),
            ",".join([str(x) for x in self.blockStarts]),
        )

    def get_cds_bed(self):
        trimmed = self.trim_by_region(self.thickStart, self.thickEnd)
        return trimmed

    def trim_by_region(self, region_start, region_end):
        starts = []
        ends = []
        exon_starts = [x + self.chromStart for x in self.blockStarts]
        exon_ends = [x + y for x, y in zip(exon_starts, self.blockSizes)]

        for start, end in zip(exon_starts, exon_ends):
            start = max(start, region_start)
            end = min(end, region_end)
            if start < end:
                starts.append(start)
                ends.append(end)

        thick_start = max(region_start, self.thickStart)
        thick_end = min(region_end, self.thickEnd)

        block_starts = [x - region_start for x in starts]
        block_sizes = [x - y for x, y in zip(ends, starts)]

        return BedInterval(
            chrom=self.chrom,
            chromStart=region_start,
            chromEnd=region_end,
            name=self.name,
            score=self.score,
            strand=self.strand,
            thickStart=thick_start,
            thickEnd=thick_end,
            itemRgb=self.itemRgb,
            blockCount=len(block_sizes),
            blockSizes=block_sizes,
            blockStarts=block_starts,
            log_wtr=self.log_wtr,
        )

    def trim_by_cds_offsets(self, start_offset, end_offset):
        cds_bed = self.get_cds_bed()
        if cds_bed.strand != "+":
            t = start_offset
            start_offset = end_offset
            end_offset = t
        starts = []
        sizes = []
        for start, size in zip(cds_bed.blockStarts, cds_bed.blockSizes):
            if start_offset:
                size = size - start_offset
                if size <= 0:
                    start_offset = abs(size)
                    continue
                start = start + start_offset
                start_offset = 0
            starts.append(start)
            sizes.append(size)
        starts2 = []
        sizes2 = []
        starts.reverse()
        sizes.reverse()
        for start, size in zip(starts, sizes):
            if end_offset:
                size = size - end_offset
                if size <= 0:
                    end_offset = abs(size)
                    continue
                end_offset = 0
            starts2.append(start)
            sizes2.append(size)
        starts2.reverse()
        sizes2.reverse()
        cds_bed.blockSizes = sizes2
        cds_bed.blockStarts = starts2
        cds_bed.blockCount = len(sizes2)

        start = cds_bed.blockStarts[0] + cds_bed.chromStart
        end = cds_bed.blockStarts[-1] + cds_bed.chromStart + cds_bed.blockSizes[-1]
        return cds_bed.trim_by_region(start, end)

    def get_cdna_exon_regions(self):
        return [
            (self.chromStart + x, self.chromStart + x + y)
            for x, y in zip(self.blockStarts, self.blockSizes)
        ]

    def get_coding_exon_regions(self):
        starts = []
        ends = []
        exon_starts = [x + self.chromStart for x in self.blockStarts]
        exon_ends = [x + y for x, y in zip(exon_starts, self.blockSizes)]
        for start, end in zip(exon_starts, exon_ends):
            start = max(start, self.thickStart)
            end = min(end, self.thickEnd)
            if start < end:
                starts.append(start)
                ends.append(end)
        return [(x, y) for x, y in zip(starts, ends)]

    def get_sequence_for_region(self, chrom, start, end, twobit, strand="+"):
        seq = None
        if chrom in twobit and 0 <= start < end < len(twobit[chrom]):
            seq = twobit[chrom][start:end]
        contig = chrom[3:] if chrom.startswith("chr") else "chr%s" % chrom
        if contig in twobit and 0 <= start < end < len(twobit[contig]):
            seq = twobit[contig][start:end]
        if not seq:
            print(
                "Seq is None (%s): %s. %s %s %s %s"
                % (seq, str(self), chrom, start, end, strand),
                file=self.log_wtr,
            )
        elif strand != "+":
            seq = reverse_complement(seq)
        return seq

    def get_sequence_for_regions(self, chrom, regions, twobit, strand="+"):
        seq = [
            self.get_sequence_for_region(chrom, start, end, twobit, strand=strand)
            for start, end in regions
        ]
        if None in seq:
            return None  # most likely the chromosome does not exist in twobit
        if strand != "+":
            seq.reverse()
        return "".join(seq)

    def get_sequence(self, twobit):
        return self.get_sequence_for_region(
            self.chrom, self.chromStart, self.chromEnd, twobit, strand=self.strand
        )

    def get_cdna(self, twobit):
        regions = self.get_cdna_exon_regions()
        return (
            regions,
            self.get_sequence_for_regions(
                self.chrom, regions, twobit, strand=self.strand
            ),
        )

    def get_cds(self, twobit):
        regions = self.get_coding_exon_regions()
        return (
            regions,
            self.get_sequence_for_regions(
                self.chrom, regions, twobit, strand=self.strand
            ),
        )


def __main__():
    parser = argparse.ArgumentParser(
        description="Find Nested Alternate ORFs (nAlt-ORFs)"
    )
    parser.add_argument("--bed", default=None, help="BED input")
    parser.add_argument(
        "-t", "--twobit", default=None, help="Genome reference sequence in 2bit format"
    )
    parser.add_argument(
        "-f",
        "--peptide_fasta_out",
        default=None,
        help="Path to output peptide_fasta_out.fasta",
    )
    parser.add_argument(
        "-n",
        "--naltorfs_fasta_out",
        default=None,
        help="Path to output naltorfs_fasta_out.fasta",
    )
    parser.add_argument(
        "-o", "--cds_fasta_out", default=None, help="Path to output cds_fasta_out.fasta"
    )
    parser.add_argument(
        "-b", "--bed_out", default=None, help="Path to output probed.bed"
    )
    parser.add_argument("--log", default=None, help="Path to output log")
    parser.add_argument(
        "-m",
        "--min_length",
        type=int,
        default=10,
        help="Minimum length of protein translation to report",
    )
    parser.add_argument("-r", "--reference", default="", help="Genome Reference Name")
    parser.add_argument(
        "--unique_sequences",
        action="store_true",
        default=False,
        help="Only report the first unique occurrence of an alternate sequence",
    )
    parser.add_argument(
        "--no_canonical_cds",
        default=None,
        help="Do not report any alternate sequences that match a provided cannonical CDS in file",
    )
    parser.add_argument(
        "--version", action="store_true", help="Report version and exit"
    )
    args = parser.parse_args()

    if args.version:
        print("nAltORFs {}".format(version("naltorfs")))
        exit()

    input_rdr = open(args.bed, "r")
    peptide_fasta_wtr = open(args.peptide_fasta_out, "w")
    lno_fasta_wtr = open(args.naltorfs_fasta_out, "w")
    cds_fasta_wtr = open(args.cds_fasta_out, "w")

    log_wtr = open(args.log, "w")

    bed_wtr = open(args.bed_out, "w")

    twobit = TwoBitFile(args.twobit)
    print(twobit.sequence_sizes(), file=log_wtr)

    if args.no_canonical_cds:
        with open(args.no_canonical_cds, "r") as fh:
            unique_seqs = get_all_canonical_sequences(fh, twobit, log_wtr)
    else:
        unique_seqs = []

    def non_canonical(seq):
        if seq not in unique_seqs:
            return True
        return False

    def unique_sequence(seq):
        if seq not in unique_seqs:
            unique_seqs.append(seq)
            return True
        return False

    def is_always_true(seq):
        return True

    is_unique = unique_sequence
    if not args.unique_sequences:
        if args.no_canonical_cds:
            is_unique = non_canonical
        else:
            is_unique = is_always_true

    def write_outputs(tbed, accession, peptide, nucseq, cds_bed, cds):
        probed = "%s\t%s\t%s\t%s%s" % (
            accession,
            peptide,
            "unique",
            args.reference,
            "\t." * 9,
        )
        if bed_wtr:
            bed_wtr.write("%s\t%s\n" % (str(tbed), probed))
            bed_wtr.flush()
        location = "chromosome:%s:%s:%s:%s:%s" % (
            args.reference,
            tbed.chrom,
            tbed.thickStart,
            tbed.thickEnd,
            tbed.strand,
        )
        fa_desc = "%s%s" % (FA_SEP, location)
        fa_id = ">%s%s\n" % (tbed.name, fa_desc)
        peptide_fasta_wtr.write(fa_id)
        peptide_fasta_wtr.write(peptide)
        peptide_fasta_wtr.write("\n")
        peptide_fasta_wtr.flush()

        fa_desc = "%s%s" % (FA_SEP, location)
        fa_id = ">%s%s\n" % (tbed.name, fa_desc)
        lno_fasta_wtr.write(fa_id)
        lno_fasta_wtr.write(nucseq)
        lno_fasta_wtr.write("\n")
        lno_fasta_wtr.flush()

        # fa_desc = '%s%s' % (args.fa_sep, location)
        fa_desc = ""
        fa_id = ">%s%s\n" % (cds_bed.name, fa_desc)
        cds_fasta_wtr.write(fa_id)
        cds_fasta_wtr.write(cds)
        cds_fasta_wtr.write("\n")
        cds_fasta_wtr.flush()

    def find_lno_orf(bed):
        translate_count = 0
        transcript_id = bed.name
        cdna_regions, cdna_seq = bed.get_cdna(twobit)
        cds_regions, cds_seq = bed.get_cds(twobit)

        if cdna_seq is None:
            print("cdna not found for BED: %s" % str(bed), file=log_wtr)
            return 0

        if cds_seq is None:
            print("cds not found for BED: %s" % str(bed), file=log_wtr)
            return 0
        cds_len = len(cds_seq)
        if cds_len % 3 != 0:
            cds_seq = cds_seq[: -(cds_len % 3)]
            print(
                "cds length is not divisible by 3!!!: %d. %s" % (cds_len, str(bed)),
                file=log_wtr,
            )  # why does this happen? check several manually, the records may be listed as incomplete

        cds_bed = bed.get_cds_bed()
        alt_cds = cds_seq[1:]  # original frame is now third (2)
        alt_cds_upper = alt_cds.upper()

        cds_offset = 1
        if "ATG" in alt_cds_upper:
            atg_index = alt_cds_upper.find("ATG")
            atg_mod = atg_index % 3
            if atg_mod == 2:
                return 0  # is is original frame
            elif atg_mod == 0:
                frame = 2
            else:
                frame = 3

            cds_offset = cds_offset + atg_index
            alt_cds = alt_cds[atg_index:]
            alt_cds_mod = len(alt_cds) % 3
            alt_cds = alt_cds[:-alt_cds_mod]

            aaseq = translate(alt_cds)
            assert aaseq.startswith("M"), Exception(
                "Translation did not start with methionine: %s --> %s" % alt_cds, aaseq
            )
            aa_end = aaseq.find("*")
            if aa_end < 0:
                aa_end = len(aaseq)
            aaseq = aaseq[:aa_end]
            len_aaseq = len(aaseq)
            if len_aaseq >= args.min_length:
                alt_cds_len = len_aaseq * 3
                alt_cds_end_trim = cds_len - alt_cds_len - cds_offset
                alt_cds = alt_cds[:alt_cds_len]
                tbed = cds_bed.trim_by_cds_offsets(cds_offset, alt_cds_end_trim)
                prot_acc = "%s_f%d_%d_%d" % (
                    transcript_id,
                    frame,
                    cds_offset,
                    alt_cds_end_trim,
                )  # tbed.chromStart, tbed.chromEnd)
                if is_unique(alt_cds):
                    translate_count += 1
                    write_outputs(tbed, prot_acc, aaseq, alt_cds, cds_bed, cds_seq)
                    return 1
        return 0

    if input_rdr:
        lno_count = 0
        transcript_count = 0
        for i, bedline in enumerate(input_rdr):
            try:
                bed = get_bed_from_line(bedline, log_wtr=log_wtr)
                if bed is None:
                    continue
                transcript_count += 1
                lno_count += find_lno_orf(bed)
            except Exception as e:
                print(
                    "BED format Error: line %d: %s\n%s" % (i, bedline, e), file=log_wtr
                )
        print(
            "transcripts: %d\tunique LNO ORFs: %d" % (transcript_count, lno_count),
            file=log_wtr,
        )


if __name__ == "__main__":
    __main__()
