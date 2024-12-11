
import random
from crypto.hamming.hamming import HammingCoderDecoder

def list_to_string(list_to_convert):
    return ''.join(str(bit) for bit in list_to_convert)


def hamming74(string_message = "10010"):
    print("Hamming(7, 4)")
    hcd = HammingCoderDecoder()
    if all(char in '01' for char in string_message) and len(string_message) > 0:
        # Convert the string to a list of integers
        list_message =  [int(char) for char in string_message]
    else:
        raise ValueError("The string contains characters other than '0' and '1'.")

    chunk_size = hcd.data_bits
    padding = 0
    remainder = len(list_message) % chunk_size

    if remainder != 0:
        # Calculate how many zeros to add
        padding = chunk_size - remainder
        list_message.extend([0] * padding)


    chunks_list = [list_message[i:i + chunk_size] for i in range(0, len(list_message), chunk_size)]
    encoded_chunks = []
    for chunk in chunks_list:
        encoded_chunk = hcd.encode(chunk)
        encoded_chunks.append(encoded_chunk)

    flattened_encoded_chunks = [bit for sublist in encoded_chunks for bit in sublist[1:]] 
    encoded_message_string = list_to_string(flattened_encoded_chunks)

    for encoded_chunk in encoded_chunks:
        random_index = random.randint(1, hcd.total_bits)
        encoded_chunk[random_index] = 1 - encoded_chunk[random_index]

    flattened_encoded_chunks = [bit for sublist in encoded_chunks for bit in sublist[1:]] 
    encoded_with_errors_string = list_to_string(flattened_encoded_chunks)

    decoded_chunks = []
    total_errors = 0
    for chunk in encoded_chunks:
        decoded_chunk, errors_found = hcd.decode(chunk)
        decoded_chunks.append(decoded_chunk)
        total_errors += errors_found

    flattened_decoded_chunks = [bit for sublist in decoded_chunks for bit in sublist] 
    decoded_string = list_to_string(flattened_decoded_chunks[:-padding] if padding > 0 else flattened_decoded_chunks)
    return(encoded_message_string, encoded_with_errors_string, decoded_string, total_errors)


# result = hamming74("1001")
# print(result)