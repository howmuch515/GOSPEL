import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sys import argv

def main():
    if len(argv) > 2:
        COMPARE_SCORE_FILE = argv[1]
        OBFUSCATED_SCORE_FILE = argv[2]
    else:
        COMPARE_SCORE_FILE = "../test1_result.csv"
        OBFUSCATED_SCORE_FILE = "../test02_output.csv"

    fig, ax = plt.subplots()
    ax.set_ylabel("RMS_SCORE")

    df = pd.read_csv(COMPARE_SCORE_FILE)
    diff_y = []
    for y, v in enumerate(df.values.tolist()[:]):
        for x, vv in enumerate(v):
            if type(vv) == float:
                diff_y.append(vv)
                print(vv)


    diff_x = np.random.normal(0, 0.06, size=len(diff_y))
    diff_dot = ax.plot(diff_x, diff_y, "o", color="C1", label="Different scripts")

    df = pd.read_csv(OBFUSCATED_SCORE_FILE)
    obfuscated_y = []
    for i, v in enumerate(df.values.tolist()[:]):
        for j, vv in enumerate(v):
            if j == 0:
                continue

            if isinstance(vv, float):
                obfuscated_y.append(vv*0.0001)
    obfuscated_y_size = len(obfuscated_y)
    print(f"[+] obfuscated_y_size: {obfuscated_y_size}")

    obfuscated_x = np.random.normal(0, 0.06, size=len(obfuscated_y))
    obfuscated_dot = ax.plot(obfuscated_x, obfuscated_y, "o", color="C2", label="Obfuscated scripts")

    ax.legend()
    ax.set_xlim(-1, 1)
    plt.tick_params(labelbottom=False)
    plt.show()

    # save figure
    # plt.savefig("score_plot.png")

if __name__ == '__main__':
    main()
