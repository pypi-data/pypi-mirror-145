from pathlib import Path

def is_ext(ext):
	if not ext.startswith('.'):
		return False
	return True

def is_ext_mapper(exts:list):
	for ext in exts:
		if not is_ext(ext):
			return ext
	return True

def search_all_files(directory:Path):   
    file_list = []

    for x in directory.iterdir():
        if x.is_file():

           file_list.append(x)
        else:

           file_list.append(search_all_files(directory/x))

    return file_list

def count_file_lines(file):
	file_sum = 0
	with file.open('r', errors='ignore') as FILE:
		for line in FILE.readlines():
			file_sum += 1

	return file_sum
	
def handle_nested_files(files:list):
	sum_of_every_file = 0
	
	for file in files:
		if isinstance(file, list):
			sum_of_every_file += handle_nested_files(file)
		else:
			sum_of_every_file += count_file_lines(file)

	return sum_of_every_file