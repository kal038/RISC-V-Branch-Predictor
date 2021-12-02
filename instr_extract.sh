#!/bin/bash

# adapted from: https://unix.stackexchange.com/questions/31414/how-can-i-pass-a-command-line-argument-into-a-shell-script

helpFunction()
{
   echo ""
   echo "Usage: $0 -e parameterE -o parameterO"
   echo -e "\t-e File path of executable containing assembly instructions to run the onestage elf ALU on and extract from. For example: bpa-pyriscv/riscv_isa/programs/return"
   echo -e "\t-o file to output extracted instructions to. For example: output.txt"
   exit 1 # Exit script after printing help
}

while getopts "e:o:" opt
do
   case "$opt" in
      e ) parameterE="$OPTARG" ;;
      o ) parameterO="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$parameterE" ] || [ -z "$parameterO" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

python3 bpa_pyriscv/onestage_elf_instr_print.py $parameterE > $parameterO
