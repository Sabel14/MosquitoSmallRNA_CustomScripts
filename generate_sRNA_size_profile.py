# This script takes a _mapped.sam file (SAM file containing all mapped small RNA reads
# from a certain library's reads to a certain set of contigs or reference genome),
# and returns the size profile of the reads, differentiating between forward-strand
# and reverse-strand reads.

from sys import argv

if len(argv) != 3:
	print("Run with 2 arguments: input_mapped.sam output.txt")
	exit(0)
else:
	pass

script, input_filename, output_filename = argv

current_file = open(input_filename)
write_page = open(output_filename, 'w')

# Two dictionaries will hold the read sizes and corresponding counts.
# Populate them with the possible read lengths.
forward_sizes_and_counts = dict()
reverse_sizes_and_counts = dict()

for i in range(18, 77):
	forward_sizes_and_counts[i] = 0
	reverse_sizes_and_counts[i] = 0

# Go through each line in the SAM file (not counting the header).
# Extract the strandedness information and read length.
# Increment the corresponding count.
for line in current_file:
	if line[0] == "@":
		continue
		
	current_line = line.split('\t')
	flag = int(current_line[1])
	if flag == 0:
		read_strand = "F"
	elif flag == 16:
		read_strand = "R"
	else:
		print("ERROR: Encountered a flag that was not 0 or 16!")
		exit(0)
		
	read_sequence = current_line[9]
	read_length = len(read_sequence)
	
	if read_strand == "F":
		if read_length not in forward_sizes_and_counts.keys():
			forward_sizes_and_counts[read_length] = 1
		else:	
			forward_sizes_and_counts[read_length] += 1
	elif read_strand == "R":
		if read_length not in reverse_sizes_and_counts.keys():
			reverse_sizes_and_counts[read_length] = 1
		else:
			reverse_sizes_and_counts[read_length] += 1
	else:
		print("ERROR: Should never reach here.")
		exit(1)
		

# Output the contents of the dicts to the output .txt file.
#write_page.write("READS ALIGNED TO FORWARD STRAND\n\n")

for possible_length in forward_sizes_and_counts.keys():
	count = str(forward_sizes_and_counts[possible_length])
	write_page.write(str(possible_length) + '\t' + count + '\n')
	
write_page.write('\n')	
#write_page.write("READS ALIGNED TO REVERSE STRAND\n\n")

for possible_length in reverse_sizes_and_counts.keys():
	count = str(reverse_sizes_and_counts[possible_length])
	write_page.write(str(possible_length) + '\t' + count + '\n')
	
write_page.close()