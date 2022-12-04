#!/usr/bin/python3
import subprocess
import sys

day = sys.argv[1]

day_with_two_digits = '0' + day if int(day) < 10 else day
cmd = 'mkdir day{}'.format(day_with_two_digits)
subprocess.check_output(cmd, shell=True)
cmd = 'touch day{}/day{}.py'.format(day_with_two_digits, day_with_two_digits)
subprocess.check_output(cmd, shell=True)
cmd = './get_input.py --day {} > day{}/input.txt'.format(day, day_with_two_digits)
output = subprocess.check_output(cmd, shell=True)
output = output.decode('utf-8')
print(output, end='')
print('\n'.join(output.split('\n')[:10]), file=sys.stderr)
