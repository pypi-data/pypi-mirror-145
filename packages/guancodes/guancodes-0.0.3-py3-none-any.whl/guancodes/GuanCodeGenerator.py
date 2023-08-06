__author__ = "Tomasz Rybotycki"

"""
This script contains implementation of a class that generates Guan codes (generalized
Gray codes). I've changed the notation in comparison to 1998 Guans' work, but I've left
the comments indicating which variable is which in the original code. I've also modified
the method slightly so that I can work out some python magic with reverse and also
don't have additional array/list entries for control.
"""

from typing import List, Tuple
from numpy import ones, zeros


class GuanCodeGenerator:

    def __init__(self) -> None:
        pass

    @staticmethod
    def generate_guan_codes(positions_limits: List[int]) -> List[List[int]]:

        current_code = zeros(len(positions_limits), dtype=int)              # g
        code_update_information = ones(len(positions_limits), dtype=int)    # u
        position_limits = list(reversed(positions_limits))                  # n

        codes = []

        while current_code[-1] <= position_limits[-1]:
            codes.append(list(reversed(current_code)))

            update_index = 0  # i
            updated_value_at_index = current_code[0] + code_update_information[0]    # k
            while updated_value_at_index > position_limits[update_index] or \
                    updated_value_at_index < 0:
                code_update_information[update_index] = \
                    -code_update_information[update_index]
                update_index += 1

                if update_index == len(current_code):
                    return codes

                updated_value_at_index = \
                    current_code[update_index] + code_update_information[update_index]

            current_code[update_index] = updated_value_at_index

        return codes

    @staticmethod
    def generate_guan_codes_tuples(positions_limits: List[int]) -> List[Tuple[int]]:
        codes = GuanCodeGenerator.generate_guan_codes(positions_limits)

        codes = [tuple(code) for code in codes]

        return codes
