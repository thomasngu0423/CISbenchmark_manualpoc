import os
import paramiko
import argparse
import getpass

# create an argument parser
parser = argparse.ArgumentParser(description='SSH script')
parser.add_argument('-i', '--ip', type=str, help='IP address')
parser.add_argument('-u', '--username', type=str, help='Username')
parser.add_argument('-p', '--password', type=str, help='Password')

# parse the command-line arguments
args = parser.parse_args()

# check if IP address is provided as a command-line argument
if args.ip:
    # IP address is provided as an argument
    hostname = args.ip
else:
    # IP address is not provided as an argument, prompt the user
    hostname = input("Enter the IP address: ")

# check if username is provided as a command-line argument
if args.username:
    username = args.username
else:
    # username is not provided as an argument, prompt the user
    username = input("Enter the username: ")

# check if password is provided as a command-line argument
if args.password:
    password = args.password
else:
    # password is not provided as an argument, prompt the user securely
    password = getpass.getpass("Enter the password: ")


# get the user's selection
print('Please select the OS:')
print('1. RHEL5'.ljust(15) + '6. Centos6')
print('2. RHEL6'.ljust(15) + '7. Centos7')
print('3. RHEL7'.ljust(15) + '8. Centos8')
print('4. RHEL8'.ljust(15) + '9. Linux (Testing)')
print('5. RHEL9')
selection = input('Enter your selection: ')

# define the SSH credentials
port = 22

# create a new SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# connect to the SSH server
print(f"Connecting to {hostname}...")
ssh.connect(hostname, port, username, password)
print(f"Connected to {username}@{hostname}")

# determine which files to read commands and names from based on the user's selection
if selection == '1':
    commands_file = 'data/Rhel5/RHEL5_com'
    names_file = 'data/Rhel5/RHEL5_name'
elif selection == '2':
    commands_file = 'data/Rhel6/RHEL76_com'
    names_file = 'data/Rhel6/RHEL6_name'
elif selection == '3':
    commands_file = 'data/Rhel7/RHEL7_com'
    names_file = 'data/Rhel7/RHEL7_name'
elif selection == '4':
    commands_file = 'data/Rhel8/RHEL8_com'
    names_file = 'data/Rhel8/RHEL8_name'
elif selection == '5':
    commands_file = 'data/Rhel9/RHEL9_com'
    names_file = 'data/Rhel9/RHEL9_name'
elif selection == '6':
    commands_file = 'data/Centos6/Centos6_com'
    names_file = 'data/Centos6/Centos6_name'
elif selection == '7':
    commands_file = 'data/Centos7/Centos7_com'
    names_file = 'data/Centos7/Centos7_name'
elif selection == '8':
    commands_file = 'data/Centos8/Centos8_com'
    names_file = 'data/Centos8/Centos8_name'
elif selection == '9':
    commands_file = 'data/Linux/Linux_com'
    names_file = 'data/Linux/Linux_name'
else:
    print("Invalid selection. Exiting...")
    ssh.close()
    exit()

# create a directory for the output files
os.makedirs('manual', exist_ok=True)

# open the file containing the list of commands
with open(commands_file, 'r') as f:
    commands = f.readlines()

# open the file containing the list of output file names
with open(names_file, 'r') as f:
    names = f.readlines()

# select sudo or not
selections = input('1. sudo\n2. non-sudo\nEnter your selection: (Default: non-sudo)')

if selections == '1':
    # execute each command and save the output to a separate file
    for i in range(len(commands)):
        command = f"echo {password} | sudo -S {commands[i].strip()}"
        print(f"[{username}@{hostname} ~]$ {command}")
        # execute the command
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)

        # read the output and save it to a file
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        name = names[i].strip()
        filename = os.path.join('manual', name.split('/')[-1] + '.txt')  # extract the file name from the path
        with open(filename, 'w') as f:
            # Remove the password from the command before writing it to the file
            command_without_password = command.replace(password, "<PASSWORD>")
            f.write(f"[{username}@{hostname} ~]$ {command_without_password}\n")
            f.write(f"{output}\n")
            f.write(f"{error}\n")

        # print the output to the terminal
        print(output)
        print()
        print(error)
        print()
        print('-' * 40)

elif selections == '2' or selections == '':
    # execute each command and save the output to a separate file
    for i in range(len(commands)):
        command = commands[i].strip()
        print(f"[{username}@{hostname} ~]$ {command}")
        # execute the command
        stdin, stdout, stderr = ssh.exec_command(command)

        # read the output and save it to a file
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        name = names[i].strip()
        filename = os.path.join('manual', name.split('/')[-1] + '.txt')  # extract the file name from the path
        with open(filename, 'w') as f:
            # Remove the password from the command before writing it to the file
            command_without_password = command.replace(password, "<PASSWORD>")
            f.write(f"[{username}@{hostname} ~]$ {command_without_password}\n")
            f.write(f"{output}\n")
            f.write(f"{error}\n")

        # print the output to the terminal
        print(output)
        print()
        print(error)
        print()
        print('-' * 40)

else:
    print("Invalid selection. Exiting...")
    ssh.close()
    exit()

# close the SSH connection
ssh.close()
print('The result has been output to the manual folder!')

