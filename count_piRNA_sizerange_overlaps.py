# This script takes a _piRNA_sizerange_reads.txt file, extracted from a mapped.sam file,
# and compares the 1st 10 bp of each antisense read against the 1st 10 bp of each sense
# read, counting the number of overlaps both for antisense reads that begin with T, and
# for other antisense reads (these are called false overlaps in the script).

from sys import argv
import string

if len(argv) != 3:
	print("Run with 2 arguments: input_piRNA_sizerange_reads.txt output_overlap_results.txt")
	exit(0)
else:
	pass

script, input_filename, output_filename = argv

current_file = open(input_filename)

reverse_prefixes = list()
forward_prefixes = list()
blank_lines = 0

# Create translation table for reverse complementing DNA strings.
trans = str.maketrans('TACG', 'ATGC')

# Go through each line in the txt file, extracting 10-bp
# prefixes from each read and storing them in lists.
# Reverse complement the forward reads for later comparison.
for line in current_file:
	if len(line.strip()) == 0:
		blank_lines += 1
		continue
	
	current_line = line.split(' ')
	
	# Skip title lines.
	if len(current_line) > 1:
		continue
		
	if blank_lines == 1:
		forward_prefix = current_line[0][0:10]
		rev = forward_prefix[::-1]
		rev_comp = rev.translate(trans)
		forward_prefixes.append(rev_comp)
		
	if blank_lines == 3:
		reverse_prefix = current_line[0][0:10]
		reverse_prefixes.append(reverse_prefix)	

	if blank_lines > 3:
		break
	

overlap_counts_for_reverse_reads = list()
false_overlap_counts = list()
total_count = 0
# Use the stored prefixes for counting overlaps,
# comparing each reverse prefix against all forward
# prefixes. First nucleotide of overlap must be T.
for reverse_prefix in reverse_prefixes:
	total_count += 1
	overlap_count = 0
	false_overlap_count = 0
	
	for forward_prefix in forward_prefixes:
		if reverse_prefix == forward_prefix and reverse_prefix[0] == "T":
			overlap_count += 1
#			print(reverse_prefix)
#			print(forward_prefix)
		if reverse_prefix == forward_prefix and reverse_prefix[0] != "T":
			false_overlap_count += 1
			
	overlap_counts_for_reverse_reads.append(overlap_count)
	false_overlap_counts.append(false_overlap_count)

# Count numbers of overlaps from list, store in dict.	
overlap_numbers = dict()

for count in overlap_counts_for_reverse_reads:
	if count not in overlap_numbers.keys():
		overlap_numbers[count] = 1
	else:
		overlap_numbers[count] += 1

# Count numbers of FALSE overlaps from list.	
false_overlap_numbers = dict()

for count in false_overlap_counts:
	if count not in false_overlap_numbers.keys():
		false_overlap_numbers[count] = 1
	else:
		false_overlap_numbers[count] += 1

# Write out the results.	
write_page = open(output_filename, 'w')
write_page.write(f"Total number of reverse reads: {total_count}\n")
write_page.write("Number of Overlaps\tNumber of Reverse Reads\n")

for count, value in sorted(overlap_numbers.items()):
	write_page.write(f"{count}\t{value}\n")

total_sum = sum(overlap_numbers.values())
write_page.write(f"Sum of above: {total_sum}\n\n")

write_page.write("Number of False Overlaps\tNumber of Reverse Reads\n")
for count, value in sorted(false_overlap_numbers.items()):
	write_page.write(f"{count}\t{value}\n")

total_false_sum = sum(false_overlap_numbers.values())
write_page.write(f"Sum of above: {total_false_sum}\n\n")
	
write_page.close()

