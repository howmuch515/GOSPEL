from sys import argv
import pandas as pd
import numpy as np

def compare_graph(graph_a, graph_b):
    # load opcode graph
    df_a = pd.read_json(graph_a)
    df_b = pd.read_json(graph_b)

    opgraph_a = df_a.to_numpy()
    opgraph_b = df_b.to_numpy()

    # Debug
    print(f"[+] opgraph_a: {opgraph_a[opgraph_a>0]}")
    print(f"[+] opgraph_b: {opgraph_b[opgraph_b>0]}")

    # divide sum
    opgraph_a = np.nan_to_num(opgraph_a / np.sum(opgraph_a, axis=1).reshape(-1, 1))
    opgraph_b = np.nan_to_num(opgraph_b / np.sum(opgraph_b, axis=1).reshape(-1, 1))

    # calc rsm
    difference = (opgraph_a - opgraph_b)
    rms = np.sqrt(np.square(difference).mean())
    return rms

def main():
    GRAPH_A = argv[1]
    GRAPH_B = argv[2]

    rms = compare_graph(GRAPH_A, GRAPH_B)
    print(f"[*] rms = {rms}")

if __name__ == '__main__':
    main()

