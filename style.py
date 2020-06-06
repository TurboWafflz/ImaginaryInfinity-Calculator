import colorama
import json
class darkStyle:
	normal=colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.NORMAL
	error=colorama.Fore.RED + colorama.Back.RESET + colorama.Style.BRIGHT
	important=colorama.Fore.MAGENTA + colorama.Back.RESET + colorama.Style.BRIGHT
	startupmessage=colorama.Fore.YELLOW + colorama.Back.RESET + colorama.Style.NORMAL
	prompt=colorama.Fore.GREEN + colorama.Back.RESET + colorama.Style.BRIGHT
	link=colorama.Fore.BLUE + colorama.Back.RESET + colorama.Style.NORMAL
	answer=colorama.Fore.GREEN + colorama.Back.RESET + colorama.Style.NORMAL
	input=colorama.Fore.CYAN + colorama.Back.RESET + colorama.Style.NORMAL
	output=colorama.Fore.WHITE + colorama.Back.RESET + colorama.Style.NORMAL

class lightStyle:
	normal=colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.NORMAL
	error=colorama.Fore.RED + colorama.Back.RESET + colorama.Style.BRIGHT
	important=colorama.Fore.MAGENTA + colorama.Back.RESET + colorama.Style.BRIGHT
	startupmessage=colorama.Fore.YELLOW + colorama.Back.RESET + colorama.Style.NORMAL
	prompt=colorama.Fore.BLACK + colorama.Back.RESET + colorama.Style.BRIGHT
	link=colorama.Fore.BLUE + colorama.Back.RESET + colorama.Style.NORMAL
	answer=colorama.Fore.GREEN + colorama.Back.RESET + colorama.Style.NORMAL
	input=colorama.Fore.CYAN + colorama.Back.RESET + colorama.Style.NORMAL
	output=colorama.Fore.WHITE + colorama.Back.RESET + colorama.Style.NORMAL
style=darkStyle