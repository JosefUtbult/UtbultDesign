import os
import time  
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler  
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape
from jinja2.exceptions import TemplateSyntaxError
from pathlib import Path

def main():

	print("Init Jinjaparser")

	patterns = "*"
	ignore_patterns = ""
	ignore_directories = False
	case_sensitive = True
	my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
	my_event_handler.on_modified = build
	my_event_handler.on_created = build
	my_event_handler.on_modified = build
	my_event_handler.on_moved = build

	path = "./templates"
	go_recursively = True
	my_observer = Observer()
	my_observer.schedule(my_event_handler, path, recursive=go_recursively)

	my_observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		my_observer.stop()
		my_observer.join()


def build(args):
	print('.')

	working_dir = os.path.dirname(os.path.realpath(__file__))

	env = Environment(
	    loader=FileSystemLoader('templates'),
	    autoescape=select_autoescape(['html'])
	)
	for filepath in env.list_templates():
	 	try:
 			template = env.get_template(filepath)

 			try:
		 		Path(f'build/{"/".join(filepath.split("/")[:-1])}').mkdir(parents=True, exist_ok=True)
		 	except:
		 		pass
		 	
	 		template.stream(name='foo').dump(f'build/{filepath}')

	 	except TemplateSyntaxError as e:
	 		print(f'Could not build {filepath}:\n{e}')

	 	except UnicodeDecodeError:
	 		try:
		 		Path(f'build/{"/".join(filepath.split("/")[:-1])}').mkdir(parents=True, exist_ok=True)
		 	except:
		 		pass

	 		os.system(f'cp {working_dir}/templates/{filepath} {working_dir}/build/{filepath}')


if __name__ == '__main__':
	main()