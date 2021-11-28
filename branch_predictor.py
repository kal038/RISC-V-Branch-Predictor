"""
Kartikeya Sharma and Khoi Lam
CSCI 320: Computer Architecture
Professor Alan Marchiori

Final Project: Branch Predictor
"""

import re
import sys

instr_filepath = sys.argv[1]

# Adapted from
instr_file = open(instr_filepath)
lines = instr_file.readlines()
for line in lines:
	regex = '([a-fa-f0-9]{8})'
	hex_vals = re.findall(regex, line)
	if hex_vals == None: continue
	if len(hex_vals) < 2: continue
	pc = hex_vals[0]
	ir = hex_vals[1]
	
	regex = '^(.+?):'
	entity_pre_colon_list = re.findall(regex, line)
	if entity_pre_colon_list  == None: continue
	if len(entity_pre_colon_list) < 1: continue
	instr_num = entity_pre_colon_list[0]

	regex = '.*?, .*?, (.+)'
	instr_str_list = re.findall(regex, line)
	if instr_str_list == None: continue
	if len(instr_str_list) < 1: continue
	instr_str = instr_str_list[0]

	instr_dict = {"num": instr_num,
		"pc": pc,
		"ir": ir,
		"str": instr_str
	}

	print(instr_dict)
