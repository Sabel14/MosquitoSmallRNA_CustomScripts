# This script takes a _piRNA_sizerange_reads.txt file and generates
# a position-frequency matrix using the reads, for use in ggseqlogo
# to show nucleotide bias in each position of the reads.

from sys import argv
import numpy as np

if len(argv) != 3:
	print("Run with 2 arguments: input_piRNA_sizerange_reads.txt output_pfm.txt")
	exit(0)
else:
	pass

script, input_filename, output_filename = argv

current_file = open(input_filename)
write_page = open(output_filename, 'w')

# A 2-D array will hold the final PFM.
final_pfm = np.zeros((4,29))

# A list will hold the counts of each nucleotide at each position.
position_counts = list()

# Each position will contain a dictionary mapping nucleotide to counts.
for i in range(0, 29):
	nucleotide_counts = dict()
	nucleotide_counts["A"] = 0; nucleotide_counts["G"] = 0; 
	nucleotide_counts["C"] = 0; nucleotide_counts["T"] = 0; 
	position_counts.append(nucleotide_counts)
		
# Go through each line (read) in the input file.
# For every nucleotide, increment the count for that position.
for line in current_file:
	line = line.rstrip()
	read_length = len(line)
	
	for i in range(0, read_length):
		if line[i] == "A":
			position_counts[i]["A"] += 1
		elif line[i] == "C":
			position_counts[i]["C"] += 1
		elif line[i] == "G":
			position_counts[i]["G"] += 1
		elif line[i] == "T":
			position_counts[i]["T"] += 1
		else:
			print("Non-ACGT nucleotide.")
	
# For each position, store the counts in the final PFM 
# (no need to convert to decimals).
for i in range(0, len(position_counts)):
	final_pfm[0,i] = position_counts[i]["A"]
	final_pfm[1,i] = position_counts[i]["C"] 
	final_pfm[2,i] = position_counts[i]["G"]
	final_pfm[3,i] = position_counts[i]["T"] 

# Output the final PWM to the output .txt file.
for i in range(0,4):
	for j in range(0, 29):
		write_page.write(f"{final_pfm[i,j]}\t")
	write_page.write('\n')
	
