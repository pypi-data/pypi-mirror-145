import fire
import os
from pathlib import Path
from time import time
from prettytable import PrettyTable

from . import options
from . import functions

def counter(filepath, ignore:list[str]=[], only:list=[], full:bool=False):
	if ignore and only:
		print("Error: Can't use ignore and only in the same command")
		return

	# IGNORE
	if ignore:
		if filepath == '.':
			this_dir = os.getcwd()
			path_obj = Path(this_dir)
			files = functions.search_all_files(path_obj)

			data_table = PrettyTable()

			time_start = time()

			lines, words, characters = options.handle_ignore(files, ignore)

			time_end = time()
			time_taken = time_end - time_start

			if full == True or full == 'True' or full == 'true':
				data_table.field_names = ['Lines', 'Words', 'Characters', 'Time Elapsed']
				data_table.add_row([lines, words or '', characters or '', time_taken])
				print(data_table)
			else:
				data_table.field_names = ['Lines', 'Time Elapsed']
				data_table.add_row([lines, time_taken])
				print(data_table)

		elif os.path.isfile(filepath):
			abs_file_path = os.path.abspath(filepath)
			path_obj = Path(abs_file_path)
			file_ext = os.path.splitext(abs_file_path)[1]
			ext_validator = functions.is_ext_mapper(ignore)
			
			data_table = PrettyTable()

			if ext_validator != True:
				print('Error: Invalid Extension')
				print(f'({ext_validator}) must start with "."')
				
				return

			if file_ext in ignore:
				if full == True or full == 'True' or full == 'true':
					data_table.field_names = ['Lines', 'Words', 'Characters', 'Time Elapsed']
					data_table.add_row([0, 0, 0, 0.0])
					print(data_table)
				else:
					data_table.field_names = ['Lines', 'Time Elapsed']
					data_table.add_row([0, 0.0])
					print(data_table)

				return

			time_start = time()

			lines = functions.count_file_lines(path_obj)
			words, characters = options.full(path_obj)

			time_end = time()
			time_taken = time_end - time_start

			if full == True or full == 'True' or full == 'true':
				data_table.field_names = ['Lines', 'Words', 'Characters', 'Time Elapsed']
				data_table.add_row([lines, words or '', characters or '', time_taken])
				print(data_table)
			else:
				data_table.field_names = ['Lines', 'Time Elapsed']
				data_table.add_row([lines, time_taken])
				print(data_table)

		elif os.path.exists(filepath):
			this_dir = os.path.abspath(filepath)
			path_obj = Path(this_dir)
			files = functions.search_all_files(path_obj)

			data_table = PrettyTable()

			time_start = time()

			lines, words, characters = options.handle_ignore(files, ignore)

			time_end = time()
			time_taken = time_end - time_start

			if full == True or full == 'True' or full == 'true':
				data_table.field_names = ['Lines', 'Words', 'Characters', 'Time Elapsed']
				data_table.add_row([lines, words or '', characters or '', time_taken])
				print(data_table)
			else:
				data_table.field_names = ['Lines', 'Time Elapsed']
				data_table.add_row([lines, time_taken])
				print(data_table)



	# ONLY
	elif only:
		if filepath == '.':
			this_dir = os.getcwd()
			path_obj = Path(this_dir)
			files = functions.search_all_files(path_obj)

			data_table = PrettyTable()

			time_start = time()

			lines, words, characters = options.handle_only(files, only)

			time_end = time()
			time_taken = time_end - time_start

			if full == True or full == 'True' or full == 'true':
				data_table.field_names = ['Lines', 'Words', 'Characters', 'Time Elapsed']
				data_table.add_row([lines, words or '', characters or '', time_taken])
				print(data_table)
			else:
				data_table.field_names = ['Lines', 'Time Elapsed']
				data_table.add_row([lines, time_taken])
				print(data_table)

		elif os.path.isfile(filepath):
			abs_file_path = os.path.abspath(filepath)
			path_obj = Path(abs_file_path)
			file_ext = os.path.splitext(abs_file_path)[1]
			ext_validator = functions.is_ext_mapper(only)
			
			data_table = PrettyTable()

			if ext_validator != True:
				print('Error: Invalid Extension')
				print(f'({ext_validator}) must start with "."')
				
				return

			if not file_ext in only:
				if full == True or full == 'True' or full == 'true':
					data_table.field_names = ['Lines', 'Words', 'Characters', 'Time Elapsed']
					data_table.add_row([0, 0, 0, 0.0])
					print(data_table)
				else:
					data_table.field_names = ['Lines', 'Time Elapsed']
					data_table.add_row([0, 0.0])
					print(data_table)

				return

			time_start = time()

			lines = functions.count_file_lines(path_obj)
			words, characters = options.full(path_obj)

			time_end = time()
			time_taken = time_end - time_start

			if full == True or full == 'True' or full == 'true':
				data_table.field_names = ['Lines', 'Words', 'Characters', 'Time Elapsed']
				data_table.add_row([lines, words or '', characters or '', time_taken])
				print(data_table)
			else:
				data_table.field_names = ['Lines', 'Time Elapsed']
				data_table.add_row([lines, time_taken])
				print(data_table)

		elif os.path.exists(filepath):
			this_dir = os.path.abspath(filepath)
			path_obj = Path(this_dir)
			files = functions.search_all_files(path_obj)

			data_table = PrettyTable()

			time_start = time()

			lines, words, characters = options.handle_only(files, only)

			time_end = time()
			time_taken = time_end - time_start

			if full == True or full == 'True' or full == 'true':
				data_table.field_names = ['Lines', 'Words', 'Characters', 'Time Elapsed']
				data_table.add_row([lines, words or '', characters or '', time_taken])
				print(data_table)
			else:
				data_table.field_names = ['Lines', 'Time Elapsed']
				data_table.add_row([lines, time_taken])
				print(data_table)



	elif filepath == '.':
		this_dir = os.getcwd()
		path_obj = Path(this_dir)
		files = functions.search_all_files(path_obj)

		data_table = PrettyTable()

		time_start = time()

		lines = functions.handle_nested_files(files)
		words, characters = options.handle_full(files)

		time_end = time()
		time_taken = time_end - time_start

		if full == True or full == 'True' or full == 'true':
			data_table.field_names = ['Lines', 'Words', 'Characters', 'Time Elapsed']
			data_table.add_row([lines, words or '', characters or '', time_taken])
			print(data_table)
		else:
			data_table.field_names = ['Lines', 'Time Elapsed']
			data_table.add_row([lines, time_taken])
			print(data_table)

	elif os.path.isfile(filepath):
		abs_file_path = os.path.abspath(filepath)
		path_obj = Path(abs_file_path)
		
		data_table = PrettyTable()

		time_start = time()

		lines = functions.count_file_lines(path_obj)
		words, characters = options.full(path_obj)

		time_end = time()
		time_taken = time_end - time_start

		if full == True or full == 'True' or full == 'true':
			data_table.field_names = ['Lines', 'Words', 'Characters', 'Time Elapsed']
			data_table.add_row([lines, words or '', characters or '', time_taken])
			print(data_table)
		else:
			data_table.field_names = ['Lines', 'Time Elapsed']
			data_table.add_row([lines, time_taken])
			print(data_table)

	elif os.path.exists(filepath):
		this_dir = os.path.abspath(filepath)
		path_obj = Path(this_dir)
		files = functions.search_all_files(path_obj)

		data_table = PrettyTable()

		time_start = time()

		lines = functions.handle_nested_files(files)
		words, characters = options.handle_full(files)

		time_end = time()
		time_taken = time_end - time_start

		if full == True or full == 'True' or full == 'true':
			data_table.field_names = ['Lines', 'Words', 'Characters', 'Time Elapsed']
			data_table.add_row([lines, words or '', characters or '', time_taken])
			print(data_table)
		else:
			data_table.field_names = ['Lines', 'Time Elapsed']
			data_table.add_row([lines, time_taken])
			print(data_table)
	else:
		print('Error: Invalid path')