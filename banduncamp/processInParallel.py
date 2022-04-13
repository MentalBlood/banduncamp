from tqdm.auto import tqdm
from typing import Callable
from multiprocessing.pool import ThreadPool



def processInParallel(array: list, function: Callable[[any], any], description: str, pool: ThreadPool):

	result = []

	if len(array):

		bar = tqdm(desc=description, total=len(array))

		for r in pool.imap_unordered(function, array):
			result.append(r)
			bar.update(1)

	return result