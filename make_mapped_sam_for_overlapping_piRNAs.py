# This script takes a _mapped.sam file (SAM file containing all mapped small RNA reads
# from a certain library's reads to a certain reference genome),
# and keeps only the subset of reads that are 24-29 bp, have A in the 10th position
# (for sense reads) or T in the 1st position (for antisense reads), AND have a 10-nt
# overlap with an antisense read (for sense reads) or sense read (for antisense reads).

# Used to extract reads for the 4th track on supplemental figure coverage plots.

from sys import argv

if len(argv) != 3:
	print("Run with 2 arguments: input_mapped.sam output_mapped.sam")
	exit(0)
else:
	pass

script, input_filename, output_filename = argv

current_file = open(input_filename)
write_page = open(output_filename, 'w')	

forward_piRNA_sizerange_info_lists = list()
reverse_piRNA_sizerange_info_lists = list()

trans = str.maketrans('TACG', 'ATGC')

# First, go through file, storing lines for 24-29 bp reads.
# Also write out the header here.
for line in current_file:
	if line[0] == "@":
		write_page.write(line)
		continue
	
	current_line = line.split('\t')
	flag = int(current_line[1])
	read_sequence = current_line[9]
	read_length = len(read_sequence)
	
	# Store lines for forward and reverse reads in separate lists.
	if read_length > 23 and read_length < 30 and flag == 0:
		forward_piRNA_sizerange_info_lists.append(current_line)
	elif read_length > 23 and read_length < 30 and flag == 16:
		reverse_piRNA_sizerange_info_lists.append(current_line)
	elif read_length > 23 and read_length < 30 and flag != 16 and flag != 0:
		print("WARNING: piRNA size range read with flag that is not 0 or 16.")
	else:
		pass

list_of_written_read_names = list()		
# Go through each reverse-read line in the stored lists.
# Write out the line if the read is the correct length, starts with T,
# and has a 10-nt overlap with some forward read. In this case, write out
# the forward read as well.
for info in reverse_piRNA_sizerange_info_lists:
	read_sequence = info[9]
	read_name = info[0]
	
	# Reverse complement the reverse read because the sequence in the SAM 
	# file is in the orientation of the genome (forward strand).
	rev = read_sequence[::-1]
	rev_comp = rev.translate(trans)
	rev_prefix = rev_comp[0:10]
	key_nucleotide = rev_prefix[0]
	
	# Reverse read needs to start with T. A on genome.	
	if key_nucleotide == "T":
		for f_info in forward_piRNA_sizerange_info_lists:
			f_read_sequence = f_info[9]
			f_read_name = f_info[0]
			f_prefix = f_read_sequence[0:10]
			
			if f_prefix[9] != "A":
				continue
		
			# As done previously, reverse complement the forward prefix
			# because we need to check if the forward prefix is complementary
			# to the reverse prefix. Could also reverse complement the reverse
			# prefix.
			f_rev_prefix = f_prefix[::-1]
			f_revcomp_prefix = f_rev_prefix.translate(trans)
			
			# If they are complementary, write out the lines into the output
			# SAM file.
			if rev_prefix == f_revcomp_prefix:
				if read_name not in list_of_written_read_names:
					for element in info:
						write_page.write(element)
						if '\n' not in element:
							write_page.write('\t')
				
				if f_read_name not in list_of_written_read_names:
					for f_element in f_info:
						write_page.write(f_element)			
						if '\n' not in f_element:
							write_page.write('\t')
					
				# Store written read names, to not write out the same read more than once.	
				list_of_written_read_names.append(read_name)
				list_of_written_read_names.append(f_read_name)
								
	
write_page.close()