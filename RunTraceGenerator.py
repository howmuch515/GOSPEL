import sys
import Evtx.Evtx as evtx
import re
import json
import pandas as pd

OPCODE_PATTERN = re.compile(r"CommandInvocation\((\S+)\)")


# abstract run_trace
def abstract_run_trace(event_log_file_name):
    run_trace_list = []
    with evtx.Evtx(event_log_file_name) as log:
        for record in log.records():
            xml = record.xml()
            m = re.search(OPCODE_PATTERN, xml)
            if m is None:
                print(f"[-] Not match!")
            else:
                opcode = m.group(1)
                print(f"[+] opcode: {opcode}")
                run_trace_list.append([{"key": "command_let", "value": opcode}])
    return run_trace_list


# make opcode graph from run_trace
def make_opcode(run_trace):
    opcode_graph = {}
    cmdlet_list = []

    # make opcode_graph with pandas.
    with open("cmdlet_list.json", "r") as f:
        cmdlet_list = json.load(f)
        opcode_graph = pd.DataFrame(0, index=cmdlet_list, columns=cmdlet_list)

    next_opcode = ""
    for i, v1 in enumerate(run_trace):
        for j in v1:
            if j["key"] == "command_let":
                current_opcode = j["value"]

                # skip unknown cmdlet
                if current_opcode not in cmdlet_list:
                    print(f"[-] {current_opcode} is unknown!")
                    continue

                pre_opcode = next_opcode
                next_opcode = current_opcode

                # skip the first opcode
                if i == 0:
                    continue
                else:
                    print(f"[+] {pre_opcode} ==> {next_opcode}")
                    opcode_graph[pre_opcode][next_opcode] += 1

    return opcode_graph


def main():
    event_log_file_name = sys.argv[1]
    output_json_file_name = event_log_file_name.split(".")[0] + ".json"
    print(f"[+] INPUT_FILE_NAME = {event_log_file_name}") # abstract run_trace from event log
    run_trace_list = abstract_run_trace(event_log_file_name)

    # make opcode graph from run_trace
    opcode_graph = make_opcode(run_trace_list)

    # output result to file
    with open(output_json_file_name, 'w') as j:
        print(f"[*] output_json_file_name = {output_json_file_name}")
        j.write(opcode_graph.to_json())


if __name__ == '__main__':
    main()
