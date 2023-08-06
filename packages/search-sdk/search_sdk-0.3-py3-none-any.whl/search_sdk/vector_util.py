from typing import List


def vector_str(vec: List[float]):
    vec_str = []
    for v in vec:
        vec_str.append(str(v))
    return ','.join(vec_str)
