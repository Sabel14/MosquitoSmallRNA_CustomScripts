# This script takes a _mapped.sam file (SAM file containing all mapped small RNA reads
# from a certain library's reads to a certain reference genome),
# and keeps only the subset of reads that are the given length, making a mapped.sam
# file from these.

from sys import argv

if len(argv) != 4:
	print("Run with 3 arguments: input_mapped.sam output_mapped.sam target_length")
	exit(0)
else:
	pass

script, input_filename, output_filename, target_length = argv

target_length = int(target_length)
current_file = open(input_filename)
write_page = open(output_filename, 'w')

# Go through each line in the SAM file (not counting the header).
# Write out the line if the read is the correct length.
for line in current_file:
	if line[0] == "@":
		write_page.write(line)
		continue
	
	current_line = line.split('\t')
	read_sequence = current_line[9]
	read_length = len(read_sequence)
	
	if read_length == target_length:
		write_page.write(line)
		
	
write_page.close()