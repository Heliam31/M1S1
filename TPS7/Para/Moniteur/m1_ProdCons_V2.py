import time
import random
import sys
from multiprocessing import Process, Lock, Condition, Value, Array



### Monitor start
class Buffer:
    def __init__(self, nb_cases):
        self.lock = Lock() 
        self.nb_wait_p = Array('i',[0,0])
        self.nb_wait_c = Value('i',0)
        self.nb_cases = nb_cases
        self.nb_libres = Value('i',nb_cases)
        self.last_type = Value('i',-1)
        self.storage_val = Array('i',[-1] * nb_cases)
        self.storage_type = Array('i', [-1] * nb_cases)
        self.prod = [Condition(self.lock),Condition(self.lock)]
        self.cons = Condition(self.lock)
        self.ptr_prod = Value('i',0)
        self.ptr_cons = Value('i',0)
        
        

    def produce(self, msg_val, msg_type, msg_source, nb_times_prod):
        with self.lock:
            if self.nb_libres.value == 0 or self.last_type.value == msg_type:
                self.nb_wait_p[msg_type] += 1
                self.prod[msg_type].wait()
            self.nb_wait_p[msg_type] -= 1
            position = self.ptr_prod.value
            self.storage_val[position] = msg_val
            self.storage_type[position] = msg_type
            self.ptr_prod.value = (position + 1) % self.nb_cases
            print('%3d produced %3d (type:%d) in place %3d and the buffer is\t\t %s' %
                (msg_source, msg_val, msg_type, position, self.storage_val[:]))
            self.nb_libres.value -= 1
            self.last_type.value = msg_type
            if self.nb_libres.value>0 and (self.nb_wait_p[1-msg_type]>0):
                self.prod[1-msg_type].notify()
            else:
                self.cons.notify()
        


    def consume(self, id_cons, nb_times_cons):
        with self.lock:
            if self.nb_libres.value == nb_cases:
                self.nb_wait_c.value += 1
                self.cons.wait()
            self.nb_wait_c.value -= 1
            position = self.ptr_cons.value
            result = self.storage_val[position]
            result_type = self.storage_type[position]
            self.storage_val[position] = -1
            self.storage_type[position] = -1
            self.ptr_cons.value = (position + 1) % self.nb_cases
            print('\t%3d consumed %3d (type:%d) in place %3d and the buffer is\t %s' %
                (id_cons, result, result_type, position, self.storage_val[:]))
            self.nb_libres.value +=1
            if self.nb_wait_p[1-self.last_type.value]>0:
                self.prod[1-self.last_type.value].notify()
            elif self.nb_libres.value < nb_cases:
                self.cons.notify()
            return result

#### Monitor end

def producer(msg_val, msg_type, msg_source, nb_times, buffer):
    for _ in range(nb_times):
        time.sleep(.1 + random.random())
        buffer.produce(msg_val, msg_type, msg_source,nb_times)
        msg_val += 1


def consumer(id_cons, nb_times, buffer):
    for _ in range(nb_times):
        time.sleep(.5 + random.random())
        buffer.consume(id_cons,nb_times)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: %s <Nb Prod <= 20> <Nb Conso <= 20> <Nb Cases <= 20>" % sys.argv[0])
        sys.exit(1)

    nb_prod = int(sys.argv[1])
    nb_cons = int(sys.argv[2])
    nb_cases = int(sys.argv[3])

    nb_times_prod = 2
    nb_times_cons = 2

    buffer = Buffer(nb_cases)
    
    producers, consumers = [], []
    
    for id_prod in range(nb_prod):
        msg_val_start, msg_type, msg_source = id_prod * nb_times_prod, id_prod % 2, id_prod
        prod = Process(target=producer, args=(msg_val_start, msg_type, msg_source, nb_times_prod, buffer))
        prod.start()
        producers.append(prod)

    for id_cons in range(nb_cons):
        cons=Process(target=consumer, args=(id_cons, nb_times_cons, buffer))
        cons.start()
        consumers.append(cons)

    for prod in producers:
        prod.join()

    for cons in consumers:
        cons.join()
