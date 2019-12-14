from sys import argv
import pandas as pd
import numpy as np

GRAPH_A = argv[1]
GRAPH_B = argv[2]

# load opcode graph
df_a = pd.read_json(GRAPH_A)
df_b = pd.read_json(GRAPH_B)

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
print(f"[*] rms = {rms}")
