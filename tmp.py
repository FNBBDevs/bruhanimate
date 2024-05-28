def scroll_up(buffer):
    # Scroll the buffer up by one value if possible
    first_key = min(buffer.keys())
    last_key = max(buffer.keys())

    if len(buffer) == 0 or first_key == 0:
        return buffer

    for key in range(first_key, last_key):
        buffer[key] = buffer[key + 1]

    # Clear the last row after scrolling
    buffer[last_key] = []

    return buffer

def scroll_down(buffer, new_row):
    # Scroll the buffer down by inserting a new row at the bottom
    if not buffer:
        buffer[0] = new_row
        return buffer

    last_key = max(buffer.keys())
    buffer[last_key + 1] = new_row

    if len(buffer) > 100:
        first_key = min(buffer.keys())
        del buffer[first_key]

    # Re-adjust keys to ensure they start from 0 and are contiguous
    buffer = {i: buffer[key] for i, key in enumerate(sorted(buffer.keys()))}

    return buffer

# Example usage
buffer = {
    0: [1, 2, 3],
    1: [4, 5, 6],
    2: [7, 8, 9],
    3: [10, 11, 12],
    4: [13, 14, 15],
    5: [16, 17, 18],
    6: [19, 20, 21],
}

print("Original buffer:")
for k, v in buffer.items():
    print(f"{k}: {v}")

for _ in range(100):
    scroll_up(buffer)
print("\nBuffer after scrolling up 100 times:")
for k, v in buffer.items():
    print(f"{k}: {v}")

new_row = [22, 23, 24]
scroll_down(buffer, new_row)
print("\nBuffer after scrolling down:")
for k, v in buffer.items():
    print(f"{k}: {v}")

for _ in range(100):
    scroll_up(buffer)
print("\nBuffer after scrolling up 100 times:")
for k, v in buffer.items():
    print(f"{k}: {v}")