import _thread
import sys
import os
import traceback
import keyword
import msvcrt
''''''
highlight_list = {'+':35,'-':35,'%':35,'=':31,'*':35,'\\':35,'/':35,
'(':34,')':34,'[':34,']':34,'{':34,'}':34,'"':32,"'":32,':':32,'>':32,'<':32,
'|':35,'.':35,'~':35,'%':35,'^':35}
os.system('')
wch_list = []
prompt_list = ['']
many_lines = []
del_index = 0
command_list = {}
__version__ = '0.1x'
PureOPENS = 'Pure2022 OPENS[3]'
__by__ = None
__from__ = 'Pure2022 OPENS[3]'
__info__ = ' The Python console  - From Pure2022 OPENS[3].github - Use : msvcrt,_thread - Version0.1x'
key = [' in ',' ont ',' or ',' and ',' as ',' is ']
if_exit = False
get_max = []
my_import = []
string_paint = '''\033[2m	    _____                   ____  _____  ______ _   _  _____ 
	   |  __ \                 / __ \|  __ \|  ____| \ | |/ ____|
	   | |__) |   _ _ __ ___  | |  | | |__) | |__  |  \| | (___  
	   |  ___/ | | | '__/ _ \ | |  | |  ___/|  __| | . ` |\___ \ 
	   | |   | |_| | | |  __/ | |__| | |    | |____| |\  |____) |
	   |_|    \__,_|_|  \___|  \____/|_|    |______|_| \_|_____/ 
														 
\033[0m'''
history = []
''''''
print(__info__,'\n','-',sys.version)
print(string_paint)
Lines = 0
def change_console_title(str):
	os.system(f'title {str}')
change_console_title(sys.version)
def make_argv_file():
	global command_list
	get_argv = {}
	for i in dir(__builtins__):
		with open('help.py','w') as fhelp:
			fhelp.write(f'help({i})')
		with os.popen('help.py','r') as gethelp:
			out = gethelp.readlines()
		try:
			get_argv[i] = f'    ╰\033[32m < __builtins__ :\033[0m\033[2m {out[2][:-1]}\033[0m \033[32m>\033[0m'
		except:
			pass
	with open('argv.txt','w') as fargv:
		fargv.write(str(get_argv))
	command_list = get_argv
if os.path.exists('argv.txt') == False:
	print('making argv.file')
	make_argv_file()
else:
	with open('argv.txt','r') as fargv:
		command_list = eval(fargv.read())
for kw in keyword.kwlist:
	command_list[kw] = f'    ╰\033[32m <keyword :\033[0m\033[2m {str(kw)} \033[0m \033[32m>\033[0m'
if command_list != {}:
	for item in command_list:
		get_max.append(command_list[item])
MAX_Char = len(max(get_max))*2
keyw = []
for i in command_list:
	keyw.append(i)
for i in ['in','and','as','or','not','is']:
	keyw.remove(i)
def find_equal(List,sub):
	for i in List:
		if i != sub:
			return False
	return True
def find_all(string, sub):
	start = 0
	pos = []
	while True:
		start = string.find(sub, start)
		if start == -1:
			return pos
		pos.append(start)
		start += len(sub)
def prompt(wch_list,line):
	get_string = ''.join(wch_list)
	out = ['']
	kw = ''
	get_string = get_string.replace('\033[34m','').replace('\033[0m','').replace('\033[35m','').replace('\033[33m','').replace('\033[32m','').replace('\033[31m','').replace('\n',' ').replace('\t','')
	if get_string.split(' ')[-1] in command_list:
		out = [command_list[get_string.split(' ')[-1]]]
		kw = get_string.split(' ')[-1]
	elif get_string.split(':')[-1] in command_list:
		out = [command_list[get_string.split(':')[-1]]]
		kw = get_string.split(':')[-1]
	outstring = get_string[::-1]
	length = len(outstring) - (outstring.index(kw[::-1])+len(kw))
	gettab = wch_list.count('\t')
	return ['\t'*gettab+' '*length+out[0].replace('\n','')+' '*(MAX_Char-len(out[0])-length-gettab*4)]
def ConsolePrint(color,*argv):
	put_string = ''
	for i in argv:
		put_string += str(i)+' '
	print(f'\033[{color}m{put_string}\033[0m')
def pgetwch():
	tabwrite = 0
	global wch_list,del_index,prompt_list,MAX_Char,Lines,if_exit,many_lines,Lines,keyw
	while True:
		wch = msvcrt.getwch()
		if wch == '\x08':
			'''Del 16'''
			if del_index < len(wch_list):
				del_index += 1
				for i in range(del_index):
					wch_list[-(i+1)] = ' '
				sys.stdout.write(f"\033[1A\033[2m[{Lines+1}]\033[0m {''.join(wch_list)}\n{''.join(prompt_list)}\r")
				sys.stdout.flush()
		elif wch == '\x0d':
			###
			if ''.join(wch_list).replace('\033[34m','').replace('\033[0m','').replace('\033[35m','').replace('\033[33m','').replace('\033[32m','').replace('\033[31m','').split(' ')[0] in ['for','while','if','else:','elif','def','class','with'] or many_lines != []:
				Lines = Lines + 1
				sys.stdout.write(f"\033[1A\033[2m[{Lines}]\033[0m {''.join(wch_list)}\n{' '*len(prompt_list[-1])}\r")
				sys.stdout.flush()
				prompt_list = ['']
				for i in wch_list:
					many_lines.append(i)
				many_lines.append('\n')
				if find_equal(wch_list,'\t') == True:
					tabwrite = tabwrite + 1
				if wch_list == [] or tabwrite == 1:
					print()
					command_run = ''.join(many_lines).replace('\033[34m','').replace('\033[0m','').replace('\033[35m','').replace('\033[33m','').replace('\033[32m','').replace('\033[31m','').replace('print(','ConsolePrint("36",')
					try:
						if command_run in globals():
							ConsolePrint("36",globals()[command_run])
						exec(command_run)
						print()
					except:
						trace = traceback.format_exc()
						print(f"\033[31m{trace}\033[0m",end='')
					many_lines = []
				get_command = ''.join(wch_list).replace('\033[34m','').replace('\033[0m','').replace('\033[35m','').replace('\033[33m','').replace('\033[32m','').replace('\033[31m','').replace('print(','ConsolePrint("36",')
				if 'import' in get_command:
					get_import = get_command.replace('import','').strip()
					get_import_list = get_import.split(',')
					for i in get_import_list:
						if i != '' and i not in my_import:
							__import__(i)
							exec(get_import)
							my_import.append(i)
							for item in eval(f'dir({i})'):
								keyw.append(item)
				wch_list_s = wch_list
				wch_list = []
				tab = wch_list_s.count('\t')
				if tabwrite != 1:
					if ''.join(wch_list_s).replace('\033[34m','').replace('\033[0m','').replace('\033[35m','').replace('\033[33m','').replace('\033[32m','').replace('\033[31m','').replace('\t','').split(' ')[0] in ['for','while','if','else:','elif','def','class','with']:
						wch_list = wch_list + [i for i in '\t'*tab]
						wch_list = wch_list + ['\t']
					else:
						wch_list = wch_list + [i for i in '\t'*tab]
				if tabwrite == 1:
					tabwrite = 0
				history.append(wch_list)
				print()
			else:
				'''Enter 16'''
				Lines = Lines + 1
				sys.stdout.write(f"\033[1A\033[2m[{Lines}]\033[0m {''.join(wch_list)}\n{' '*len(prompt_list[-1])}\r")
				sys.stdout.flush()
				prompt_list = ['']
				command_run = ''.join(wch_list).replace('\033[34m','').replace('\033[0m','').replace('\033[35m','').replace('\033[33m','').replace('\033[32m','').replace('\033[31m','').replace('print(','ConsolePrint("36",')
				change_console_title(f'{sys.version} - Run : '+''.join(wch_list).replace('\033[34m','').replace('\033[0m','').replace('\033[35m','').replace('\033[33m','').replace('\033[32m','').replace('\033[31m',''))
				if 'import' in command_run:
					get_import = command_run.replace('import','').strip()
					get_import_list = get_import.split(',')
					for i in get_import_list:
						if i != '' and i not in my_import:
							__import__(i)
							exec(get_import)
							my_import.append(i)
							for item in eval(f'dir({i})'):
								keyw.append(item)
				if command_run != 'reload':
					try:
						if command_run in globals():
							ConsolePrint("36",globals()[command_run])
						exec(command_run)
					except:
						if command_run == 'exit()':
							if_exit = True
							exit()
						trace = traceback.format_exc()
						print(f"\033[31m{trace}\033[0m",end='')
				else:
					print('?[reload file <argv.txt>]')
				print('\n')
				history.append(wch_list)
				wch_list = []
		elif wch == '\x09':
			'''Tab 16'''
			wch_list.append('\t')
		elif wch == '\x26':
			wch_list.append('↑')
			exit()
		else:
			try:
				if del_index != 0:
					del_index -= 1
					if wch not in highlight_list:
						wch_list[-(del_index+1)] = wch
					else:
						wch_list[-(del_index+1)] = f'\033[{str(highlight_list[wch])}m{wch}\033[0m'
				else:
					if wch not in highlight_list:
						wch_list.append(wch)
					else:
						wch_list.append(f'\033[{str(highlight_list[wch])}m{wch}\033[0m')
			except:
				pass
			sys.stdout.write(f"\033[1A\033[2m[{Lines+1}]\033[0m {''.join(wch_list)}\n{''.join(prompt_list)}{' '* (MAX_Char - len(''.join(prompt_list)))}\r")
			sys.stdout.flush()
def pout():
	global prompt_list,wch_list,if_exit,MAX_Char,if_exit,Lines,keyw
	while True:
		get_string = ''.join(wch_list).replace('\033','')
		if len(wch_list) == 0:
			prompt_list = [' '*MAX_Char]
		if get_string == '$reload':
			print('<reload start>')
			os.remove('argv.txt')
			make_argv_file()
			print('<reload end>')
		prompt_list = prompt(wch_list,Lines)
		for i in key:
			if i in get_string:
				m30 = get_string.count('[30m')
				m0 = get_string.count('[0m')
				m33 = get_string.count('[33m')
				m34 = get_string.count('[34m')
				m31 = get_string.count('[31m')
				m32 = get_string.count('[32m')
				m35 = get_string.count('[35m')
				get = find_all(get_string,i)[-1]-m30*4-m0*3-m31*4-m32*4-m33*4-m34*4-m35*4
				for ic in range(get,get+len(i)):
					wch_list[ic] = f'\033[35m{wch_list[ic]}\033[0m'
def highlight():
	global prompt_list,wch_list,if_exit,MAX_Char,if_exit,keyw
	while True:
		get_string = ''.join(wch_list).replace('\033','')
		for i in keyw:
			if i in get_string:
				m30 = get_string.count('[30m')
				m0 = get_string.count('[0m')
				m33 = get_string.count('[33m')
				m34 = get_string.count('[34m')
				m31 = get_string.count('[31m')
				m32 = get_string.count('[32m')
				m35 = get_string.count('[35m')
				get = find_all(get_string,i)[-1]-m30*4-m0*3-m31*4-m32*4-m33*4-m34*4-m35*4
				for ic in range(get,get+len(i)):
					wch_list[ic] = f'\033[33m{wch_list[ic]}\033[0m'

_thread.start_new_thread(pgetwch,())
_thread.start_new_thread(pout,())
_thread.start_new_thread(highlight,())
while 1:
	if if_exit == True:
		exit()