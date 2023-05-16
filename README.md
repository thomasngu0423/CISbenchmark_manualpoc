# CISbenchmark_manualpoc

## Introduction

CISbenchmark_manualpoc is a Python script designed to facilitate SSH access to target machines and retrieve manual proof of concept (POC) data that may not be covered by CISCat. It enhances vulnerability assessments by providing the ability to identify missed vulnerabilities and gather critical information.

## Prerequisites

- Python 3.x
- Paramiko library

## Usage

python main.py 
python main.py -i IP_ADDRESS -u USERNAME -p PASSWORD


**Note:** 
1. Please ensure that you do not delete the `data` folder, as it contains essential files for the script to function properly.
2. If running with sudo throws the error "sudo: sorry, you must have a tty to run sudo," please run the script without sudo.
3. If the error persists, manually SSH into the target server and retrieve the manual POC data.
4. The results will be output to the `manual` folder.

## Disclaimer

This script is provided as-is without any warranty. Use it at your own risk.
