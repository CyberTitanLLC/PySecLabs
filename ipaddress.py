import os

# Run ifconfig and redirect output to a file
os.system("ifconfig > /home/student/workspace/ifconfig.txt")

# Read the file and look for a line containing 'broadcast'
with open("/home/student/workspace/ifconfig.txt", 'r') as if_file:
    for line in if_file:
        if 'broadcast' in line:
            split_line = line.split()
            print(f"Your IP is: {split_line[1]}")
            break  # Exit the loop after finding the IP
