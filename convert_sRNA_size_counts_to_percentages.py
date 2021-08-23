# This script converts size profiles with counts to size profiles
# with percentages.
# The input size_profile.txt files need to be in the same folder as
# the script.

from sys import argv

if len(argv) != 3:
	print("Run with 2 arguments: input_size_profile.txt output_size_percentages.txt")
	exit(0)
else:
	pass

script, input_filename, output_filename = argv

write_page = open(output_filename, 'w')

# Two dictionaries will hold the read sizes and corresponding percentages.
# Populate them with the possible read lengths.
# Also, two dictionaries to hold the counts for the first pass through the
# file, because cannot go through file a second time.
forward_sizes_and_counts = dict()
reverse_sizes_and_counts = dict()
forward_sizes_and_percents = dict()
reverse_sizes_and_percents = dict()

for i in range(18, 77):
	forward_sizes_and_counts[i] = 0
	reverse_sizes_and_counts[i] = 0
	forward_sizes_and_percents[i] = 0
	reverse_sizes_and_percents[i] = 0
	
forward_total = 0
reverse_total = 0	
read_strand = "F"	

with open(input_filename) as input:
	# Make pass through size_profile.txt.
	# Add up all counts for forward and reverse, to
	# use for calculating percentages.
	for line in input:
		# If the blank line between forward and reverse counts is
		# reached, change strand.
		if len(line.strip()) == 0:
			read_strand = "R"
			continue

		current_line = line.split('\t')
		read_length = int(current_line[0])
		read_count = int(current_line[1])
	
		if read_strand == "F":
			forward_total = forward_total + read_count
			forward_sizes_and_counts[read_length] = read_count
		elif read_strand == "R":
			reverse_total = reverse_total + read_count
			reverse_sizes_and_counts[read_length] = read_count			
		else:
			print("ERROR: Should never reach here.")
			exit(1)		
	
# Make second pass, but through the stored dictionaries with counts.
# Convert each count to a percentage using the calculated total.
# Store in the dictionaries with percentages.			
for read_length in forward_sizes_and_counts.keys():
	read_count = forward_sizes_and_counts[read_length]

	read_percent = read_count / forward_total
	forward_sizes_and_percents[read_length] = round(read_percent, 3)
	
for read_length in reverse_sizes_and_counts.keys():
	read_count = reverse_sizes_and_counts[read_length]

	read_percent = read_count / reverse_total
	reverse_sizes_and_percents[read_length] = round(read_percent, 3)

# Output the contents of the dicts to the output .txt file.
#write_page.write("READS ALIGNED TO FORWARD STRAND\n\n")

for possible_length in forward_sizes_and_percents.keys():
	percent = str(forward_sizes_and_percents[possible_length])
	write_page.write(str(possible_length) + '\t' + percent + '\n')
	
write_page.write('\n')	
#write_page.write("READS ALIGNED TO REVERSE STRAND\n\n")

for possible_length in reverse_sizes_and_percents.keys():
	percent = str(reverse_sizes_and_percents[possible_length])
	write_page.write(str(possible_length) + '\t' + percent + '\n')
	
write_page.close()