import random
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


random.seed(rank)
nb=100001
inside = 0

start_time = time.time()
for _ in range(nb):
    x = random.random()
    y = random.random()
    if x*x + y*y <= 1:
        inside += 1



print("inside rank ", rank, ": ", inside )
data=comm.reduce( inside, op = MPI.SUM,root = 0)
end_time = time.time()

if rank == 0:
    print("Pi =", 4*data/(nb*size), "en temps: ", end_time - start_time)
