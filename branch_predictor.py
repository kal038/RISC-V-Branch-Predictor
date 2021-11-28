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
    
    grouped_branch_seqs = None

    def init():
        BranchPredictor.instr_filepath = sys.argv[1]
        BranchPredictor.instr_file = open(BranchPredictor.instr_filepath)
        BranchPredictor.instr_dict_list = []
        BranchPredictor._import_instrs()

        BranchPredictor.grouped_branch_seqs = []
        BranchPredictor._group_branch_seqs()

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

    def _group_branch_seqs():
        for i in range(len(BranchPredictor.instr_dict_list)):
            if BranchPredictor.instr_dict_list[i] == None: continue
            instr_str = BranchPredictor.instr_dict_list[i]["str"]
            if instr_str.split()[0][0] == "b":
                regex = '([a-fa-f0-9]{8})'
                hex_vals = re.findall(regex, instr_str)
                if hex_vals == None: continue
                if len(hex_vals) < 1: continue
                predicted_pc = hex_vals[-1]           
                actual_pc = BranchPredictor.instr_dict_list[i+1]["pc"]
                is_taken = predicted_pc == actual_pc
                branch_seq_dict = {"instr": BranchPredictor.instr_dict_list[i],
                                   "predicted_pc": predicted_pc,
                                   "actual_pc": actual_pc,
                                   "is_taken": is_taken
                                   }
                BranchPredictor.grouped_branch_seqs.append(branch_seq_dict)

    def _get_dict_list_str(dict_list: list):
        output = "[\n"
        for i in range(len(dict_list)):
            output += f"{i}: {dict_list[i]}"
            if i != len(BranchPredictor.instr_dict_list)-1:
                output += ",\n"
        output += "\n]"
        return output
        

    def get_str():
        output = "Instructions:\n"
        output += BranchPredictor._get_dict_list_str(
            BranchPredictor.instr_dict_list
        )
        output += "\n\nGrouped Branch Sequences\n"
        output += BranchPredictor._get_dict_list_str(
            BranchPredictor.grouped_branch_seqs
        )
        return output
    
    def _grow_instr_dict_list(instr_num: int):
        if len(BranchPredictor.instr_dict_list) < 1:
            BranchPredictor.instr_dict_list.append(None)
        curr_instr_dict_len = len(BranchPredictor.instr_dict_list)
        for i in range(instr_num - curr_instr_dict_len + 2):
            BranchPredictor.instr_dict_list.append(None)
