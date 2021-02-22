"""A collection of utility functions used throughout the calculator"""
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import os
import sys
from typing import Iterable
import urllib.request

from rich.progress import (
	BarColumn,
	DownloadColumn,
	TextColumn,
	TransferSpeedColumn,
	TimeRemainingColumn,
	Progress,
	TaskID,
)

# progress =
def copy_url(task_id: TaskID, url: str, path: str, progress) -> None:
	req = urllib.request.Request(url, data=None, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'})
	"""Copy data from a url to a local file."""
	try:
		response = urllib.request.urlopen(req)
	except Exception:
		return False
	# This will break if the response doesn't contain content length
	progress.update(task_id, total=len(response.read()))
	response = urllib.request.urlopen(req)
	with open(path, "wb") as dest_file:
		progress.start_task(task_id)
		for data in iter(partial(response.read, 32768), b""):
			dest_file.write(data)
			progress.update(task_id, advance=len(data))
	return True

def progress_download(urls: Iterable[str], dest: str, isFile=False):
	"""Download multuple files to the given directory. Shows progress bar"""
	returns = []
	progress = Progress(TextColumn("[bold blue]{task.fields[filename]}", justify="right"), BarColumn(bar_width=None), "[progress.percentage]{task.percentage:>3.1f}%", "•", DownloadColumn(), "•", TransferSpeedColumn(), "•", TimeRemainingColumn())
	with progress:
		with ThreadPoolExecutor(max_workers=4) as pool:
			for url in urls:
				filename = url.split("/")[-1]
				task_id = progress.add_task("download", filename=filename, start=False)
				if isFile == True:
					returns.append(pool.submit(copy_url, task_id, url, dest, progress).result())
				else:
					returns.append(pool.submit(copy_url, task_id, url, os.path.join(dest, filename), progress).result())
	if False in returns:
		return returns.index(False)
	else:
		return True

def flatten(iterable):
	if isinstance(iterable, (list, tuple, set, range)):
		for sub in iterable:
			yield from flatten(sub)
	else:
		yield iterable

def removeDuplicates(iterable):
	res = []
	[res.append(item) for item in iterable if item not in res]
	return type(iterable)(res)
	
def loadConfig(config):
	items = []
	for each_section in config.sections():
		for (each_key, each_val) in config.items(each_section):
			items.append((each_section, each_key, each_val))
	return items