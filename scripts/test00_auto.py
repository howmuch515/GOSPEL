from cmdletgraph.cmdletgraph import abstractRunTrace, makeOpcode
from sys import argv
from glob import glob

def change_extention(file_path):
    a = file_path.split(".")
    a[-1] = "json"
    return ".".join(a)

def main():
    DIR_NAME = argv[1]
    target_file_list = glob(DIR_NAME + "/*.evtx")
    for target_file in target_file_list:
        opgraph = makeOpcode(abstractRunTrace(target_file))

        output_json_file_name = change_extention(target_file)
        with open(output_json_file_name, 'w') as j:
            print(f"[*] output_json_file_name = {output_json_file_name}")
            j.write(opgraph.to_json())

if __name__ == '__main__':
    main()