import pysam
import argparse

parser = argparse.ArgumentParser(description='Add missing query qualities to bam file')
parser.add_argument('-i', '--in_bam', help='input bam file')
parser.add_argument('-o', '--out_bam', help='output bam file')
parser.add_argument('-f', '--fastq', help='fastq file used for mapping')
args = parser.parse_args()

# Build a dictionary that maps read names to quality scores
qual_dict = {}
with open(args.fastq, 'r') as f:
    lines = f.readlines()
    for i in range(0, len(lines), 4):
        read_name = lines[i].rstrip()[1:]
        quality = lines[i+3].rstrip()
        qual_dict[read_name] = quality

aln_file = pysam.AlignmentFile(args.in_bam, "rb")
outfile = pysam.AlignmentFile(args.out_bam, "wb", template= aln_file)

for aln in aln_file.fetch():
    if aln.query_qualities == None:
        cigar = aln.cigar
        left, right = cigar[0], cigar[-1]
        H1, H2 = 0,0
        if left[0] == 5:
            H1 = left[1]
        if right[0] == 5:
            H2 = right[1]
        if aln.query_name in qual_dict:
            quality = qual_dict[aln.query_name]
            if H2 == 0:
                aln.query_qualities = pysam.qualitystring_to_array(quality[H1:])
            else:
                aln.query_qualities = pysam.qualitystring_to_array(quality[H1:-H2])
    outfile.write(aln)
