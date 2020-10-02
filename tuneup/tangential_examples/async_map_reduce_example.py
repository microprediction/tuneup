import asyncio
import random
import numpy as np

# A little example of fanning out computation, should that be necessary
# Replace worker_run with anything that can be a coroutine, which is to say it plays nice with asyncio
#     See https://docs.python.org/3/library/asyncio-task.html


async def worker_run(worker_id:int,data:dict)->float:
    print('Worker '+str(worker_id)+' is chugging along ')
    await asyncio.sleep(random.choice([1,5,13]))
    print('Worker '+str(worker_id)+' has finished evaluating')
    return random.choice([3.14,1.0,-17.5,data['x']])


async def averager():
    """ Not ideal but very simple map/reduce example """
    tasks = [ asyncio.create_task(worker_run(worker_id=worker_id,data={'x':worker_id*worker_id})) for worker_id in range(5) ]
    results = await asyncio.gather(*tasks)
    return np.mean(results)


if __name__=='__main__':
    avg = asyncio.run(averager())
    print('The result is '+str(avg))