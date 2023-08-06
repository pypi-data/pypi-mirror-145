def full(file):
    file_words = 0
    file_chars = 0

    with file.open('r', errors='ignore') as FILE:
        words = FILE.read().split()
        file_words += len(words)

    with file.open('r', errors='ignore') as FILE:
        for char in FILE.read():
            file_chars += 1

    return (file_words, file_chars)

def handle_full(files:list):
    words_sum = 0
    chars_sum = 0

    for file in files:
        if isinstance(file, list):
            files_full_data = handle_full(file)
            words_sum += files_full_data[0]
            chars_sum += files_full_data[1]
        else:
            file_full_data = full(file)
            words_sum += file_full_data[0]
            chars_sum += file_full_data[1]

    return (words_sum, chars_sum)