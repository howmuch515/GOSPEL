import sys
import Evtx.Evtx as evtx
import re
import json
import pandas as pd
import numpy as np

INPUT_FILE_NAME = sys.argv[1]
OUTPUT_FILE_NAME = "result.json"
OPCODE_PATTERN = re.compile(r"CommandInvocation\((\S+)\)")

print(f"[+] INPUT_FILE_NAME = {INPUT_FILE_NAME}")


result_list = []
with evtx.Evtx(INPUT_FILE_NAME) as log:
    record_length = 0
    for record in log.records():
        record_length += 1
        xml = record.xml()
        m = re.search(OPCODE_PATTERN, xml)
        if m is None:
            print(f"[!] Not match!: {xml}")
        else:
            opcode = m.group(1)
            print(f"[*] opcode: {opcode}")
            result_list.append([{"key": "command_let", "value": opcode}])
    print(f"[+] record_length = {record_length}")

with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as f:
    print(f"[+] OUTPUT_FILE_NAME = {OUTPUT_FILE_NAME}")
    f.write(json.dumps(result_list))


def makeOpcode(run_trace):
    # load cmdlet.json
    cmdlet_list = []
    with open("cmdlet.json", "r") as j:
        cmdlet_list = json.load(j)

    ## make opcode_graph with pandas and numpy.
    cmdlet_num = len(cmdlet_list)
    opcode_graph = pd.DataFrame(0, index=cmdlet_list, columns=cmdlet_list)

    result_matrix = {}
    old_opcode = ""
    opcode = ""
    counter = 0
    for h, i in enumerate(run_trace):
        for j in i:
            if j["key"] == "command_let":
                old_opcode = opcode
                opcode = j["value"]
                if h == 0:
                    continue
                else:
                    print(f"[+] {old_opcode} ==> {opcode}")
                    counter +=1
                    opcode_graph[old_opcode][opcode] += 1
    print(counter)
    return opcode_graph


a = makeOpcode(result_list)
b = a.to_numpy()
print(b)
print(np.sum(b[b>0]))


with open('result.json', 'w') as j:
    j.write(a.to_json())


