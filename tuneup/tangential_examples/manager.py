import asyncio
import random
import uuid
from pprint import pprint
from copy import deepcopy

# https://vimeo.com/463913870


async def objective_function(suggestion):
    """  Mocks an objective function """
    print("Evaluating "+str(suggestion))
    await asyncio.sleep(10*random.random())
    return random.choice([-3.14157,42,17])


async def suggestor(suggestion_queue):
    """ Puts a list of suggestions on the queue """
    for _ in range(10):
        x = random.choice([2,4.5,13.4])
        suggestion = {'id':str(uuid.uuid4()),'x':x}
        print('Making suggestion')
        pprint(suggestion)
        await suggestion_queue.put(suggestion)
        await asyncio.sleep(2)
    print('Done making suggestions')


async def evaluator(suggestion_queue, location, result_queue):
    """
         Takes suggestions off the queue, calls the objective function, and
         pops the results on the results queue
    """
    finished = False
    my_results = list()
    while not finished:
        try:
            suggestion = await asyncio.wait_for(suggestion_queue.get(), timeout=5.)
        except asyncio.TimeoutError:
            finished = True
        if not finished:
            print('Begun working on '+str(suggestion['id'])+' at location '+str(location))
            value = await objective_function(suggestion=suggestion)
            result = deepcopy(suggestion)
            result['value'] = value
            result_queue.put_nowait(result)
            my_results.append(result)
            suggestion_queue.task_done()
    print('Evaluator at location '+str(location)+' is quitting as queue has been empty for a few seconds.')
    return my_results


async def main():
    suggestion_queue = asyncio.Queue()
    result_queue = asyncio.Queue()

    x_suggestor = asyncio.create_task(suggestor(suggestion_queue))
    y_evaluators = [asyncio.create_task(evaluator(suggestion_queue, location, result_queue))
                 for location in range(3)]

    await asyncio.gather(x_suggestor)
    return await asyncio.gather(*y_evaluators)


if __name__=='__main__':
    results = asyncio.run(main())
    print("Here's who did what ...")
    pprint(results)