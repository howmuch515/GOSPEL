#!/bin/env python3
from cmdletgraph.CompareMatrix import compare_graph
import pandas as pd
import os
import glob

GRAPH_DIRS = ("./sample/competitor/*.json", "./sample_ps1_evtx/*.json", "./sample_ps2_log/*.json")
OUTPUT_FILE = "./test1_result.csv"

def search_files(dir_tuple):
    result_list = []
    for i in dir_tuple:
        result_list += glob.glob(i)
    return result_list

def main():
    graph_files = search_files(GRAPH_DIRS)
    file_num = len(graph_files)
    print(graph_files)
    print(f"[+] file num: {file_num}")

    result_list = []
    for i, v1 in enumerate(graph_files[:]):
        tmp_list = []
        for j, v2 in enumerate(graph_files[:]):
            if i < j:
                tmp_list.append(compare_graph(v1, v2))
            else:
                print(f"[!] ========== SKIP ==========")
                tmp_list.append(None)
        result_list.append(tmp_list)
        print(result_list)

    csv_label = list(map(os.path.basename, graph_files))
    df = pd.DataFrame(result_list, index=csv_label, columns=csv_label)
    df.to_csv(OUTPUT_FILE)
    print(f"[*] output result: {OUTPUT_FILE}")
    print(df)

if __name__ == '__main__':
    main()