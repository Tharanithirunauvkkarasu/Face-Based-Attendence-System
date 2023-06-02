import subprocess

# Define the command to run in the CMD
cmd_command = 'python attendanceproject.py a b'  # Replace with your desired command

# Run the command and capture the output
result = subprocess.run(cmd_command, shell=True, check=True, stdout=subprocess.PIPE, text=True)

# Get the output of the command
output = result.stdout

# Display the output to the user
print(f"Output: \n{output}")
