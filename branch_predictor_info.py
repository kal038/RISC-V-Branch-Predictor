"""
Kartikeya Sharma and Khoi Lam
CSCI 320: Computer Architecture
Professor Alan Marchiori

Final Project: Branch Predictor Info
"""

import re
import sys

class BranchPredictorInfo:
	"""
	This is a static class. There is only one "instance" of the class.
	All attributes and methods should be accessed via BranchPredictorInfo.<attribute/method name>.

	This class encapsulates a branch predictor, which can take a file containing a list of RISC-V
	instructions in the following format:

				   0: PC: xxxxxxxx, IR: xxxxxxxx
				   1: PC: 80000000, IR: 00000093, li ra,0x0
				   2: PC: 80000004, IR: 00000113, li sp,0x0
				   3: PC: 80000008, IR: 00000193, li gp,0x0
	
	Then, the class creates branch sequences or branch events out of them. Each branch sequence
	or branch event is the branch instruction itself, the actual pc taken (pc of the instruction following it),
	and the target pc specified in the branch instruction itself. Finally, specific types of branch predictors can
	be run on the imported sequence of instructions and, consequently, the analyses of their performance can be 
	outputted as well.
	"""

	# Class Fields

	## filepath of the output file containing the instructions
	instr_filepath = None
	## file object
	instr_file = None

	## list of dictionaries, where each dictionary
	## encapsulates an instruction
	instr_dict_list = None
	## list of dictionaries, where each dictionary
	## encapsulates a branch sequence or branch event, so to speak	  
	grouped_branch_seqs = None

	def init():
		"""
		Initializes class fields above with the help of
		helper initialization methods
		"""

		BranchPredictorInfo.instr_filepath = sys.argv[1] # filepath is passed in as an argument
		BranchPredictorInfo.instr_file = open(BranchPredictorInfo.instr_filepath)
		

		BranchPredictorInfo.instr_dict_list = []
		BranchPredictorInfo._import_instrs()
		BranchPredictorInfo.grouped_branch_seqs = []
		BranchPredictorInfo._group_branch_seqs()

	def _import_instrs():
		"""
		Sets the BranchPredictorInfo's list of instructions
		from the output file specified in the class fieldsd

		For each line in the file containing the list of
		instructions, identify the 8-digit hex values.
		The first one is the PC, and the second one is the
		instruction value, IR.

		For example: 1: PC: 80000000, IR: 00000093, li ra,0x0
		
		Then, provided we found at least two hex values (PC and IR),
		we can continue interpreting this line as an instruction, rather
		than a miscellaneous header or some other non-instruction line
		that is unexpectedly present in the file.

		Then, the method extracts the line number as the first number
		that comes before a colon, as seen in the instruction example 
		above.

		Now, the program finds the instruction string. In the example shown
		above, that would be li ra,0x0. We isolate all of the text that
		comes after the second comma (#: PC: x, IR: x, instruction string).
		Then, we just store it in the list of instructions, where each instruction
		is encapsulated in a dictionary containing the pc, ir, and string.
		"""
		lines = BranchPredictorInfo.instr_file.readlines()
		for line in lines:
			regex = '([a-fA-F0-9]{8})'
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

			# MINOR: this method grows the list as needed; rationale:
			# instruction number is preserved through the list index;
			# we cannot assign a value to a particular list index without
			# having initialized it
			BranchPredictorInfo._grow_instr_dict_list(instr_num) 

			BranchPredictorInfo.instr_dict_list[instr_num] = instr_dict

	def _group_branch_seqs():
		"""
		Sets the BranchPredictorInfo's list of branch sequences
	
		If the instruction starts with a b, then we know that
		it is a branch instruction per the RISC-V green sheet.
		We use regular expressions and the re (regular expressions)
		library in Python to search for any 8-digit hex values.
		[a-fA-F0-9] is a hex digit and {8} means search for 8 of them
		in a row. 
		
		The last found hex value in the instruction is the hex value of
		the branch-to instruction. For example, bgeu a0,a1,0x800000c4,
		where 0x800000c4 is the target pc. The pc that was actually taken
		is the pc of the next instruction that was executed in the instruction
		series present in the output file (in our example case, that is output.txt).
		If the actual pc and the target pc are equal, then we know that the branch
		was taken, and store that as a boolean in the dictionary representing the
		branch sequence or branch event, so to speak. 
		"""
		for i in range(len(BranchPredictorInfo.instr_dict_list)):
			if BranchPredictorInfo.instr_dict_list[i] == None: continue
			instr_str = BranchPredictorInfo.instr_dict_list[i]["str"]
			if instr_str.split()[0][0] == "b":
				regex = '([a-fA-F0-9]{8})'
				hex_vals = re.findall(regex, instr_str)

				# making sure that an 8-digit hex value was actually found
				# so we don't get some NoneType error; it's fairly trivial
				if hex_vals == None: continue
				if len(hex_vals) < 1: continue

				taken_pc = BranchPredictorInfo.instr_dict_list[i+1]["pc"]
				target_pc = hex_vals[-1]		   
				is_taken = taken_pc == target_pc
				branch_seq_dict = {"instr": BranchPredictorInfo.instr_dict_list[i],
								   "actual_pc": taken_pc,
								   "target_pc": target_pc,
								   "is_taken": is_taken
								   }
				BranchPredictorInfo.grouped_branch_seqs.append(branch_seq_dict)

	def _get_dict_list_str(dict_list: list):
		"""
		Helper function that formats the output
		of a list of dictionaries more readably
		"""
		output = "[\n"
		for i in range(len(dict_list)):
			output += f"{i}: {dict_list[i]}"
			if i != len(BranchPredictorInfo.instr_dict_list)-1:
				output += ",\n"
		output += "\n]"
		return output
		
	def get_str():
		"""
		Outputs a list of instructions in dictionaries and
		a list of grouped branche sequences in dictionaries.
		""" 
		output = "Instructions:\n"
		output += BranchPredictorInfo._get_dict_list_str(
			BranchPredictorInfo.instr_dict_list
		)
		output += "\n\nGrouped Branch Sequences\n"
		output += BranchPredictorInfo._get_dict_list_str(
			BranchPredictorInfo.grouped_branch_seqs
		)
		return output
   
 
	def _grow_instr_dict_list(instr_num: int):
		"""
		This helper method grows the list by appending
		None to the list until the inputted index is in the
		index range of the instruction list.
		"""
		if len(BranchPredictorInfo.instr_dict_list) < 1:
			BranchPredictorInfo.instr_dict_list.append(None)
		curr_instr_dict_len = len(BranchPredictorInfo.instr_dict_list)
		for i in range(instr_num - curr_instr_dict_len + 2):
			BranchPredictorInfo.instr_dict_list.append(None)
