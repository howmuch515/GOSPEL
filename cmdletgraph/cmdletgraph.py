import sys
import Evtx.Evtx as evtx
import re
import json
import pandas as pd
import numpy as np

CMDLET_LIST_FILE = "cmdlet_list.json"
CMDLET_PATTARN = re.compile(r"CommandInvocation\((\S+)\)")


# abstract run_trace
def abstract_runtrace(event_log_file_name: str) -> list:
    print(f"[+] event log file: {event_log_file_name}")
    runtrace_list = []
    with evtx.Evtx(event_log_file_name) as log:
        for record in log.records():
            xml = record.xml()
            m = re.search(CMDLET_PATTARN, xml)
            if m is None:
                print(f"[-] Not match!")
            else:
                cmdlet = m.group(1)
                print(f"[+] cmdlet: {cmdlet}")
                runtrace_list.append([{"key": "command_let", "value": cmdlet}])
    return runtrace_list


# make cmdlet graph from run_trace
def make_graph(run_trace: list) -> 'pandas.core.frame.DataFrame':
    cmdlet_graph = {}
    cmdlet_list = []

    # make cmdlet_graph with pandas.
    with open(CMDLET_LIST_FILE, "r") as f:
        cmdlet_list = json.load(f)
        cmdlet_graph = pd.DataFrame(0, index=cmdlet_list, columns=cmdlet_list)

    next_cmdlet = ""
    for i, v1 in enumerate(run_trace):
        for j in v1:
            if j["key"] == "command_let":
                current_cmdlet = j["value"]

                # skip unknown cmdlet
                if current_cmdlet not in cmdlet_list:
                    print(f"[-] {current_cmdlet} is unknown!")
                    continue

                pre_cmdlet = next_cmdlet
                next_cmdlet = current_cmdlet

                # skip the first cmdlet
                if i == 0:
                    continue
                else:
                    print(f"[+] {pre_cmdlet} ==> {next_cmdlet}")
                    cmdlet_graph[pre_cmdlet][next_cmdlet] += 1

    # calc average each row.
    cmdlet_graph = cmdlet_graph.div(cmdlet_graph.sum(axis='columns'), axis='index')
    return cmdlet_graph


def save_graph(output_file_name: str, cmdlet_graph: 'pandas.core.frame.DataFrame') -> None:
    # output result to file
    with open(output_file_name, 'w') as j:
        print(f"[*] output_file_name = {output_file_name}")
        j.write(cmdlet_graph.to_json())


def compare_graph(cmdletgraph_a: 'pandas.core.frame.DataFrame', cmdletgraph_b: 'pandas.core.frame.Data') -> float:
    # change Numpy
    cmdletgraph_a = np.nan_to_num(cmdletgraph_a)
    cmdletgraph_b = np.nan_to_num(cmdletgraph_b)

    # Debug
    print(f"[+] cmdletgraph_a: {cmdletgraph_a[cmdletgraph_a>0]}")
    print(f"[+] cmdletgraph_b: {cmdletgraph_b[cmdletgraph_b>0]}")

    # calc rsm
    rms = calc_rms(cmdletgraph_a, cmdletgraph_b)
    return rms


def compare_graph_file(graphA_file_name: str, graphB_file_name: str) -> float:
    # load cmdlet graph
    df_a = pd.read_json(graphA_file_name)
    df_b = pd.read_json(graphB_file_name)

    cmdletgraph_a = df_a.to_numpy()
    cmdletgraph_b = df_b.to_numpy()

    rms = compare_graph(cmdletgraph_a, cmdletgraph_b)
    return rms


def calc_rms(graph_a, graph_b):
    # calc rsm
    difference = graph_a - graph_b
    rms = np.sqrt(np.square(difference).mean())
    return rms


def main():
    event_log_file_name_a = sys.argv[1]
    event_log_file_name_b = sys.argv[2]

    # make cmdletgraph
    cmdletgraph_a = make_graph(abstract_runtrace(event_log_file_name_a))
    cmdletgraph_b = make_graph(abstract_runtrace(event_log_file_name_b))

    # calculate rms
    rms = compare_graph(cmdletgraph_a, cmdletgraph_b)
    print(f"RMS = {rms}")


if __name__ == '__main__':
    main()
