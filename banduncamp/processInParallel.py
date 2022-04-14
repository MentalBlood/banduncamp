from typing import Callable
from multiprocessing.pool import ThreadPool



def processInParallel(array: list, function: Callable[[any], any], description: str, pool: ThreadPool):

	result = []

	if len(array):
		for r in pool.imap_unordered(function, array):
			result.append(r)

	return result