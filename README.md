# AddQuality
Add Missing Quality Score to Bam FIle. Some mappers, e.g. LRA will generate bam file with some alignments's quality scores missed. Here I wrote a python scipt to restore those quality scores from the original fastq file. The quality scores are important information for SNPs and SV calling.

usage: python addQuality.py [-h] [-i IN_BAM] [-o OUT_SAM] [-f FASTQ]

Add missing query qualities to bam file

optional arguments:
  -h, --help            show this help message and exit
  -i IN_BAM, --in_bam IN_BAM
                        input bam file
  -o OUT_SAM, --out_sam OUT_SAM
                        output sam file
  -f FASTQ, --fastq FASTQ
                        fastq file used for mapping

Not recommended for large fastq files
