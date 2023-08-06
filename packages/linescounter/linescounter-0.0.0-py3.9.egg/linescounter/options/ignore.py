def ignore(file, file_types:list=[]):
    file_types = tuple(file_types)
    if file.name.endswith(file_types):
        return (0, 0, 0)

    file_lines = 0
    file_words = 0
    file_chars = 0

    with file.open('r', errors='ignore') as FILE:
        for line in FILE.readlines():
            file_lines += 1
    
    with file.open('r', errors='ignore') as FILE:
        words = FILE.read().split()
        file_words += len(words)

    with file.open('r', errors='ignore') as FILE:
        for char in FILE.read():
            file_chars += 1

    return (file_lines, file_words, file_chars) 

def handle_ignore(files:list, file_types:list=[]):
    file_lines = 0
    file_words = 0
    file_chars = 0
    t_file_types = tuple(file_types)

    for file in files:
        if (not isinstance(file, list)) and file.name.endswith(t_file_types):
            continue
        elif isinstance(file, list):
            files_full_data = handle_ignore(file, t_file_types)
            file_lines += files_full_data[0]
            file_words += files_full_data[1]
            file_chars += files_full_data[2]
        else:
            file_full_data = ignore(file)
            file_lines += file_full_data[0]
            file_words += file_full_data[1]
            file_chars += file_full_data[2]
            
    return (file_lines, file_words, file_chars) 