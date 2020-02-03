from cmdletgraph.CompareMatrix import compare_graph
import pandas as pd
import glob
import os

TARGET_DIR = "./obfuscated_scripts/"
OUTPUT_FILE = "test02_output.csv"
SUFFIX_TUPLE = ("ori", "token", "ast", "string", "ascii", "aes", "compress")

def search_scripts(scripts_name):
    base_path = TARGET_DIR + scripts_name + "/"
    result_dict = {}
    file_list = glob.glob(base_path + "/*")
    print(f"[+] file_list: {file_list}")

    for obfus_type in SUFFIX_TUPLE:
        tmp_file_name = base_path + obfus_type + "_" + scripts_name + ".json"
        print(f"[+] tmp_file_name: {tmp_file_name}")
        if tmp_file_name not in file_list:
            result_dict[obfus_type] = None
        else:
            result_dict[obfus_type] = tmp_file_name

    return result_dict


def main():
    script_list = glob.glob(TARGET_DIR + "**")
    result_list = []
    for i in script_list:
        i = os.path.basename(i)
        scripts_dict = search_scripts(i)
        print(scripts_dict)

        result_dict = {}
        for key, value in scripts_dict.items():
            if (key == "ori") or (value is None):
                # result_dict[key] = None
                continue
            else:
                rms = compare_graph(scripts_dict["ori"], value)
                result_dict[key] = round(rms * 10000, 2)
                print(f"{key}: {rms}")
        result_list.append(result_dict)

    graph_label = list(map(os.path.basename, script_list))
    df = pd.DataFrame(result_list, index=graph_label)
    print(df)
    df.to_csv(OUTPUT_FILE)


if __name__ == '__main__':
    main()
