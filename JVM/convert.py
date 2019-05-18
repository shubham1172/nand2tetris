"""
Convert JVM instructions into Hack

@author: shubham1172
"""
segment_symbol = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
    "static": 16,
    "temp": 5,
    "internal": 13    # used by VM internally
}

operation_symbol = {
    "add": "+",
    "sub": "-",
    "and": "&",
    "or": "|",
    "neg": "-",
    "not": "!",
    "eq": "JNE",
    "gt": "JLE",
    "lt": "JGE"
}


def _get_base_address(segment, index="0"):
    """
    return base address for a (segment, index) combination
    :param segment: local, static, this, etc.
    :param index: non negative number
    :return: base address of segment
    """
    if segment == 'constant':
        return index
    elif segment == 'pointer':
        return 'this' if index == "0" else 'that'
    elif segment in ['static', 'temp', 'internal']:
        return str(int(segment_symbol[segment]) + int(index))
    else:
        return segment_symbol[segment]


def push(segment, index):
    """
    push segment index
    :param segment: segment of memory
    :param index: index in the segment
    generic algorithm: addr = base_address + index, *SP = *addr, SP++
    assembly:
    @SG     // seg_ptr
    D=M
    @i
    A=D+A   // addr = *(seg_ptr + index)
    D=M
    @SP
    M=M+1   // SP++
    A=M-1
    M=D     // *(SP-1) = *addr
    """
    if segment == 'constant':
        set_data = ["D=A"]
    elif segment in ['pointer', 'temp', 'static', 'internal']:
        set_data = ["D=M"]
    else:
        set_data = [
            "D=M",
            "@%s" % index,
            "A=D+A",
            "D=M"
        ]
    return [
        "@%s" % _get_base_address(segment, index),
        *set_data,
        "@SP",
        "M=M+1",
        "A=M-1",
        "M=D"
    ]


def pop(segment, index):
    """
    pop segment index
    :param segment: segment of memory
    :param index: index in the segment
    algorithm: addr = base_address + index, SP--, *addr = *SP
    @i      // D=i
    D=A
    @SG     // addr=*SG+i
    A=M
    D=A+D
    @15
    M=D     // store addr
    @SP     // SP--
    MD=M-1
    @15     // *addr = *SP
    A=M
    M=D
    """
    if segment == 'constant':
        raise Exception('Invalid pop into constant.')
    elif segment in ['pointer', 'temp', 'static', 'internal']:
        return [
            "@SP",
            "AM=M-1",
            "D=M",
            "@%s" % _get_base_address(segment, index),
            "M=D"
        ]
    else:
        return [
            "@%s" % _get_base_address(segment),
            "D=M",
            "@%s" % index,
            "D=D+A"
            "@15",
            "M=D",
            "@SP",
            "AM=M-1",
            "D=M",
            "@15",
            "A=M",
            "M=D"
        ]


def arithmetic(operation, counter):
    """
    perform and arithmetic operation
    :param operation: one of the nine operations
    :param counter: unique value to distinguish labels
    algorithm:
    unary - pop R13, R15=op(R13), push R15
    binary - pop R13, pop R14, R15=op(R13,R14), push R15
    """
    out = pop('internal', 0)        # pop R13
    # unary operation
    if operation in ['neg', 'not']:
        out += [
            "@13",
            "D=%sM" % operation_symbol[operation],
            "@15",
            "M=D"
        ]
    # binary operation
    else:
        out += pop('internal', 1)  # pop R14
        if operation in ['add', 'sub', 'and', 'or']:
            out += [
                "@13",
                "D=M",
                "@14",
                "D=M%sD" % operation_symbol[operation],
                "@15",
                "M=D"
            ]
        else:
            # lt, gt, eq
            out += [
                "@13",
                "D=M",
                "@14",
                "D=M-D",
                "@false%d" % counter,
                "D;%s" % operation_symbol[operation],
                "D=-1",
                "@set%d" % counter,
                "0;JMP",
                "(false%d)" % counter,
                "D=0",
                "(set%d)" % counter,
                "@15",
                "M=D"
            ]
    out += push('internal', 2)     # push R15
    return out
