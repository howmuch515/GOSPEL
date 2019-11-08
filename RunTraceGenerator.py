import sys
import Evtx.Evtx as evtx
import re
import json
import pandas as pd

OUTPUT_FILE_NAME = "result.json"
OPCODE_PATTERN = re.compile(r"CommandInvocation\((\S+)\)")


# abstract run_trace
def abstractRunTrace(event_log_file_name):
    run_trace_list = []
    with evtx.Evtx(event_log_file_name) as log:
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
                run_trace_list.append([{"key": "command_let", "value": opcode}])
        print(f"[+] record_length = {record_length}")
    return run_trace_list


# make opcode graph from run_trace
def makeOpcode(run_trace):
    # make opcode graph DataFrame.
    opcode_graph = {}
    with open("cmdlet.json", "r") as j:
        cmdlet_list = json.load(j)
        ## make opcode_graph with pandas and numpy.
        opcode_graph = pd.DataFrame(0, index=cmdlet_list, columns=cmdlet_list)

    opcode = ""
    for h, i in enumerate(run_trace):
        for j in i:
            if j["key"] == "command_let":
                old_opcode = opcode
                opcode = j["value"]
                if h == 0:
                    # skiip the first opcode
                    continue
                else:
                    print(f"[+] {old_opcode} ==> {opcode}")
                    opcode_graph[old_opcode][opcode] += 1
    return opcode_graph


def main():
    event_log_file_name = sys.argv[1]
    print(f"[+] INPUT_FILE_NAME = {event_log_file_name}")

    # abstract run_trace from event log
    run_trace_list = abstractRunTrace(event_log_file_name)

    # make opcode graph from run_trace
    opcode_graph = makeOpcode(run_trace_list)

    # output result to file
    with open(OUTPUT_FILE_NAME, 'w') as j:
        print(f"[+] OUTPUT_FILE_NAME = {OUTPUT_FILE_NAME}")
        j.write(opcode_graph.to_json())


if __name__ == '__main__':
    main()
