import pysam
import subprocess
import argparse
parser = argparse.ArgumentParser(description='Add missing query qualities to bam file')
parser.add_argument('-i', '--in_bam', help='input bam file')
parser.add_argument('-o', '--out_sam', help='output sam file')
parser.add_argument('-f', '--fastq', help='fastq file used for mapping')
args = parser.parse_args()
aln_file = pysam.AlignmentFile(args.in_bam, "rb")
outfile = pysam.AlignmentFile(args.out_sam, "w", template= aln_file)
qual_dict = {} #saves quality scores of primary alignments
for aln in aln_file.fetch():
    if aln.query_qualities == None:            
        cigar = aln.cigar
        left, right = cigar[0], cigar[-1] 
        H1, H2 = 0,0 #H1, H2 stand for the number of hardclipped bases at the left and right end
        if left[0] == 5:
            H1 = left[1]
        if right[0] == 5:
            H2 = right[1]
        if aln.query_name in qual_dict: #seraching for existing quality scores for non-primary alignments to avoid repeatedly call grep
            if H2 == 0:
                aln.query_qualities = pysam.qualitystring_to_array(qual_dict[aln.query_name][H1:])
            else:
                aln.query_qualities = pysam.qualitystring_to_array(qual_dict[aln.query_name][H1:-H2])
        else:
            child = subprocess.run(["grep", "-A3", aln.query_name, args.fastq], stdout=subprocess.PIPE, encoding="utf-8")
            quality = child.stdout.split()[9] 
            if H2 == 0:
                aln.query_qualities = pysam.qualitystring_to_array(quality[H1:])
            else:
                aln.query_qualities = pysam.qualitystring_to_array(quality[H1:-H2])
            if H1 == H2 == 0: #if no hardclipped bases, this quality scores will be complete and should be saved for later use
                qual_dict[aln.query_name] = quality
    outfile.write(aln)    
