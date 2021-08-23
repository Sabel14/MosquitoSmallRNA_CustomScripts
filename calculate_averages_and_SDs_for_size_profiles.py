# This script takes all size profiles with percentages for a
# particular virus, that are in the current folder.
# It will, for each small RNA length for forward and reverse,
# calculate the average and SD across all samples in the folder,
# and write them out in two output files, for use in plotting.

from sys import argv
import os, fnmatch
from statistics import mean,stdev

if len(argv) != 4:
	print("Run with 3 arguments: VirusName output_averages.txt output_SDs.txt")
	exit(0)
else:
	pass

script, virus_name, output_avg_filename, output_SD_filename = argv

# Two dictionaries will hold the read sizes and corresponding average
# percentages. Populate them with the possible read lengths.
# Same for two dictionaries that will hold the SDs.
forward_sizes_and_averages = dict()
reverse_sizes_and_averages = dict()
forward_sizes_and_SDs = dict()
reverse_sizes_and_SDs = dict()

# More immediately, need two dictionaries to hold all values (percentages)
# for each sample, for each read length. These will, at the end, be used
# to find the average and SD.
forward_sizes_and_values = dict()
reverse_sizes_and_values = dict()

for i in range(18, 77):
	forward_sizes_and_averages[i] = 0
	reverse_sizes_and_averages[i] = 0
	forward_sizes_and_SDs[i] = 0
	reverse_sizes_and_SDs[i] = 0
	forward_sizes_and_values[i] = list()
	reverse_sizes_and_values[i] = list()
	
# Loop through each file in the folder that contains the supplied
# VirusName argument. Each, one-by-one, becomes the current_file
# which is opened and its counts added to the master output file.	
folderInput = "."
file_pattern = "*_size_profile_percents.txt"
for dirpath, dirnames, filenames in os.walk(folderInput):
	for filename in fnmatch.filter(filenames, file_pattern):
		if virus_name in filename:
			print(filename)
			current_file = open(filename)
	
			read_strand = "F"	
			# Go through each line in the size_profile.txt.
			# Extract the counts for each small RNA size and strandedness.
			# Add to the dictionary combining all the counts.
			for line in current_file:
				# If the blank line between forward and reverse counts is
				# reached, change strand.
				if len(line.strip()) == 0:
					read_strand = "R"
					continue

				current_line = line.split('\t')
				read_length = int(current_line[0])
				read_percent = round(float(current_line[1]), 3)
	
				if read_strand == "F":
					# If input file has a length not 18-76, do not add it.
					if read_length not in forward_sizes_and_values.keys():
						continue
					forward_sizes_and_values[read_length].append(read_percent)
				elif read_strand == "R":
					if read_length not in reverse_sizes_and_values.keys():
						continue
					reverse_sizes_and_values[read_length].append(read_percent)
				else:
					print("ERROR: Should never reach here.")
					exit(1)
		
# The two dictionaries are populated with lists of all percent values.
# Use the lists to calculate averages and SDs.
for read_length in forward_sizes_and_values.keys():
	all_percents = forward_sizes_and_values[read_length]
	average_percent = round(mean(all_percents), 3)
	SD_of_percents = round(stdev(all_percents), 3)
	forward_sizes_and_averages[read_length] = average_percent
	forward_sizes_and_SDs[read_length] = SD_of_percents

print(sum(forward_sizes_and_averages.values()))
	
for read_length in reverse_sizes_and_values.keys():
	all_percents = reverse_sizes_and_values[read_length]
	average_percent = round(mean(all_percents), 3)
	SD_of_percents = round(stdev(all_percents), 3)
	reverse_sizes_and_averages[read_length] = average_percent
	reverse_sizes_and_SDs[read_length] = SD_of_percents
	
print(sum(reverse_sizes_and_averages.values()))
	
# Output the contents of the average and SD dicts to the output .txt file.
write_page_avg = open(output_avg_filename, 'w')

for possible_length in forward_sizes_and_averages.keys():
	average = str(forward_sizes_and_averages[possible_length])
	write_page_avg.write(str(possible_length) + '\t' + average + '\n')
	
write_page_avg.write('\n')	

for possible_length in reverse_sizes_and_averages.keys():
	average = str(reverse_sizes_and_averages[possible_length])
	write_page_avg.write(str(possible_length) + '\t' + average + '\n')
	
write_page_avg.close()

write_page_SD = open(output_SD_filename, 'w')

for possible_length in forward_sizes_and_SDs.keys():
	std_dev = str(forward_sizes_and_SDs[possible_length])
	write_page_SD.write(str(possible_length) + '\t' + std_dev + '\n')
	
write_page_SD.write('\n')	

for possible_length in reverse_sizes_and_SDs.keys():
	std_dev = str(reverse_sizes_and_SDs[possible_length])
	write_page_SD.write(str(possible_length) + '\t' + std_dev + '\n')
	
write_page_SD.close()