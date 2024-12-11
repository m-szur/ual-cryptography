import sys
import os

__SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(__SCRIPT_DIR))

from functools import reduce

#########################################################################################################
class CoderDecoder:
    def __init__(self, name: str):
        self.name = name

    def encode(self, message: list[int]) -> list[int]:
        raise NotImplementedError("Method not implemented")

    def decode(self, message: list[int]) -> list[int] | int:
        raise NotImplementedError("Method not implemented")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
#########################################################################################################

class HammingCoderDecoder(CoderDecoder):
    def __init__(self, total_bits: int = 7, data_bits: int = 4) -> None:
        super().__init__(name=f"hamming{total_bits}_{data_bits}")
        self.total_bits: int = total_bits
        self.data_bits: int = data_bits
        self.parity_bits: int = self.total_bits - self.data_bits
        self.parity_bits_positions: list[int] = self.calculate_parity_bits_positions()

    def calculate_parity_bits_positions(self) -> list[int]:
        positions =  [2**i for i in range(self.parity_bits) if 2**i <= self.total_bits]
        return positions

    def find_error_position(self, chunk: list[int]) -> int:
        return (
            reduce(lambda a, b: a ^ b, [i for i, bit in enumerate(chunk) if bit])
            if sum(chunk) != 0
            else 0
        )

    def encode_chunk(self, chunk: list[int]) -> list[int]:
        if len(chunk) != self.data_bits:
            raise ValueError(
                f"Size of the chunk must be equal to a number of the data bits ({self.data_bits})"
            )

        encoded_chunk = [0] * (self.total_bits + 1)
        j = 0
        for i in range(1, self.total_bits + 1):
            if i in self.parity_bits_positions:
                continue
            encoded_chunk[i] = chunk[j]
            j += 1

        error_position = self.find_error_position(encoded_chunk)
        if error_position in [0] + self.parity_bits_positions:
            encoded_chunk[error_position] = int(not encoded_chunk[error_position])
        else:
            for parity_bit_position in self.parity_bits_positions:
                if parity_bit_position ^ error_position < error_position:
                    encoded_chunk[parity_bit_position] = int(
                        not encoded_chunk[parity_bit_position]
                    )
        return encoded_chunk

    def decode_chunk(self, chunk: list[int]) -> list[int]:
        if len(chunk) != self.total_bits + 1:
            raise ValueError(
                f"Size of the chunk must be equal a number of total bits + 1 ({self.total_bits + 1}) - {len(chunk)}"
            )
        chunk_copy = chunk.copy()
        error_position = self.find_error_position(chunk_copy)
        chunk_copy[error_position] = int(not chunk_copy[error_position])
        return [
            bit
            for i, bit in enumerate(chunk_copy)
            if i not in [0] + self.parity_bits_positions
        ]

    def encode(self, message: list[int]) -> list[int]:
        if len(message) % self.data_bits != 0:
            raise ValueError(
                f"Size of a message({len(message)}) must be dividable by a number of the data bits ({self.data_bits})\n calling from: {self.name}"
            )
        encoded_message = []
        for i in range(0, len(message), self.data_bits):
            chunk = self.encode_chunk(message[i : i + self.data_bits])
            encoded_message.extend(chunk)
        return encoded_message

    def decode(self, message: list[int]) -> tuple[list[int], int]:
        if len(message) % (self.total_bits + 1) != 0:
            raise ValueError(
                f"Size of a message must be divisible by a number of total bits + 1 ({self.total_bits + 1})"
            )
        decoded_message = []
        errors_found = 0
        for i in range(0, len(message), self.total_bits + 1):
            pre_decoded_chunk = message[i : i + self.total_bits + 1]
            if self.find_error_position(pre_decoded_chunk) != 0:
                errors_found += 1
            chunk = self.decode_chunk(pre_decoded_chunk)
            decoded_message.extend(chunk)
        return decoded_message, errors_found


if __name__ == "__main__":

    def __str__(self) -> str:
        return f"HammingCoderDecoder(total_bits={self.total_bits}, data_bits={self.data_bits})"

    def __repr__(self) -> str:
        return f"HammingCoderDecoder(total_bits={self.total_bits}, data_bits={self.data_bits})"
