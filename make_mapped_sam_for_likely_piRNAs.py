# This script takes a _mapped.sam file (SAM file containing all mapped small RNA reads
# from a certain library's reads to a certain reference genome),
# and keeps only the subset of reads that are 24-29 bp and with A in the 10th position
# (for sense reads) or T in the 1st position (for antisense reads).

# Used to extract reads for the 3rd track from the top on shown coverage plots.

from sys import argv

if len(argv) != 3:
	print("Run with 2 arguments: input_mapped.sam output_mapped.sam")
	exit(0)
else:
	pass

script, input_filename, output_filename = argv

current_file = open(input_filename)
write_page = open(output_filename, 'w')

# Go through each line in the SAM file (not counting the header).
# Write out the line if the read is the correct length.
for line in current_file:
	if line[0] == "@":
		write_page.write(line)
		continue
	
	current_line = line.split('\t')
	flag = int(current_line[1])
	read_sequence = current_line[9]
	read_length = len(read_sequence)
	
	correct_nucleotide = False
	
	if flag == 0:
		# 10th nucleotide needs to be A for forward reads.
		key_nucleotide = read_sequence[9]
		if key_nucleotide == "A":
			correct_nucleotide = True
			
	elif flag == 16:
		# Reverse read needs to start with T. A on genome.
		key_nucleotide = read_sequence[-1]
		if key_nucleotide == "A":
			correct_nucleotide = True
			
	else:
		print("ERROR")
		exit(1)
			
	if read_length > 23 and read_length < 30 and correct_nucleotide:
		write_page.write(line)
		
	
write_page.close()