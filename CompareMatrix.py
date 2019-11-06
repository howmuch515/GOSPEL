matrixA = {}
matrixB = {}
N = 620


class OpcodeList:
    def __init__(self, pre_opcode, next_opcode_list):
        self.pre_opcode = pre_opcode
        self.next_opcode_list = next_opcode_list

    def pop(self, new_opcode):
        try:
            self.next_opcode_list.remove(new_opcode)
            return len(self.next_opcode_list)

        except Exception as e:
            print(f"[!] {new_opcode} don't exist in {self.pre_opcode} list")
            print(self.new_opcode_list)

            print(e)


class OpcodeGraph:
    def __init__(self, opcode_dict):
        self.opcode_dict = opcode_dict
        self.opcode_list = self.listupOpcode()

    def listupOpcode(self):
        result_list = []
        for k1, v1 in self.opcode_dict.items():
            opcode_list = []
            for opcode, _ in v1.items():
                opcode_list.append(opcode)
            result_list.append(OpcodeList(k1, opcode_list))

    def getElement(self, x, y):
        if self.opcode_dict.get(x) is None:
            return 0
        else:
            if self.opcode_dict.get(y) is None:
                return 0
            else:
                return self.opcode_dict[x][y]

    def popElement(self, x, y):
        for i in self.opcode_list[:]:
            if i.pre_opcode == x:
                list_length = i.pop(y)
                if list_length == 0:
                    self.opcode_list.remove(i)
                return y
        raise Exception(f"[!] {y} don't exist in {x} !!")


def getRate(d, oldopcode, opcode):
    pass


def evaluate(A, B):
    """
     score = pow(AB_sum + A_sum + B_sum + 0, 2)/ pow(N, 2)
    """

    total = 0
    for i in A.opcode_list:
        pre_opcode = i.pre_opcode
        for next_opcode in i.next_opcode_list[:]:
            a_score = A.getElement(pre_opcode, next_opcode)
            b_score = B.getElement(pre_opcode, next_opcode)
            if b_score == 0:
                # A ==> B
                total += a_score
            elif b_score > 0:
                # A <==> B
                total += abs(a_score - b_score)
                B.popElement(pre_opcode, next_opcode)
            else:
                raise Exception(f"[!] B score is negative! {b_score}")

    # A <== B
    for i in B.opcode_list:
        pre_opcode = i.pre_opcode
        for j in i.next_opcode_list[:]:
            next_opcode = j
            b_score = B.getElement(pre_opcode, next_opcode)
            if b_score <= 0:
                raise Exception(f"[!] B score is negative! {b_score}")
            else:
                total += b_score
                B.popElement(pre_opcode, next_opcode)

    return pow(total, 2) / pow(N, 2)


def main():
    A = {}
    B = {}
    A = OpcodeGraph(A)
    B = OpcodeGraph(B)

    score = evaluate(A, B)
    print(f"[*] score = {score}")


if __name__ == "__main__":
    main()
