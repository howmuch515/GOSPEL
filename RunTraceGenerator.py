import sys
import Evtx.Evtx as evtx
import re
import json

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
    result_matrix = {}
    old_opcode = ""
    opcode = ""
    for h, i in enumerate(run_trace):
        for j in i:
            if j["key"] == "command_let":
                old_opcode = opcode
                opcode = j["value"]
                if h == 0:
                    continue
                else:
                    print(f"[+] {old_opcode} ==> {opcode}")
                    if result_matrix.get(old_opcode) is None:
                        result_matrix[old_opcode] = {}
                        result_matrix[old_opcode][opcode] = 1
                    else:
                        if result_matrix[old_opcode].get(opcode) is None:
                            result_matrix[old_opcode][opcode] = 1
                        else:
                            result_matrix[old_opcode][opcode] += 1
    return result_matrix


a = makeOpcode(result_list)
print(a)
