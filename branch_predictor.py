"""
Kartikeya Sharma and Khoi Lam
CSCI 320: Computer Architecture
Professor Alan Marchiori

Final Project: Branch Predictor
"""

import re
import sys

class BranchPredictor:

    instr_filepath = None
    instr_file = None
    instr_dict_list = None

    def init():
        BranchPredictor.instr_filepath = sys.argv[1]
        BranchPredictor.instr_file = open(BranchPredictor.instr_filepath)
        BranchPredictor.instr_dict_list = []
        BranchPredictor._import_instrs()

    def _import_instrs():
        lines = BranchPredictor.instr_file.readlines()
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
            instr_num = int(entity_pre_colon_list[0])

            regex = '.*?, .*?, (.+)'
            instr_str_list = re.findall(regex, line)
            if instr_str_list == None: continue
            if len(instr_str_list) < 1: continue
            instr_str = instr_str_list[0]

            instr_dict = {"pc": pc,
                        "ir": ir,
                        "str": instr_str
            }

            BranchPredictor._grow_instr_dict_list(instr_num)
            BranchPredictor.instr_dict_list[instr_num] = instr_dict

    def _grow_instr_dict_list(instr_num: int):
        if len(BranchPredictor.instr_dict_list) < 1:
            BranchPredictor.instr_dict_list.append(None)
        curr_instr_dict_len = len(BranchPredictor.instr_dict_list)
        for i in range(instr_num - curr_instr_dict_len + 2):
            BranchPredictor.instr_dict_list.append(None)

    def get_str():
        output = "[\n"
        for i in range(len(BranchPredictor.instr_dict_list)):
            output += f"{i}: {BranchPredictor.instr_dict_list[i]}"
            if i != len(BranchPredictor.instr_dict_list)-1:
                output += ",\n"
        output += "\n]"
        return output
