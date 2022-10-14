#include <cstdlib>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>    //taille<2^20


__global__ void vecsumKernel(unsigned int *dVec, unsigned int *dSum, int size){
	int taille=1023/2;

	int bid = blockIdx.x;
	int id = blockIdx.x*blockDim.x+threadIdx.x;
	int tid = threadIdx.x;
		if(id<size){
	while(taille>=1&& tid <= taille){
		dVec[tid]+=dVec[taille+tid];
    taille/=2;
    __syncthreads();
    }
    if(tid==0){
        dSum[bid]=dVec[blockIdx.x*blockDim.x];
    }
		
	while(taille>=1 && id <= taille){
		dVec[id] += dVec[taille+id];
		taille = taille / 2;
		__syncthreads();
	}
    }
}

void vecsum (unsigned int *vec, unsigned int *sum, int size){
     int bsize = 1024;
     int gsize = (size+bsize-1)/bsize;
     int bytes = size * sizeof(unsigned int);
     unsigned int *dVec, *dSum;
     printf("gsize: %i\n", gsize);
     cudaMalloc((void **) &dVec, bytes);
     cudaMalloc((void **) &dSum, gsize*sizeof(unsigned int));
     cudaMemcpy(dVec, vec, bytes, cudaMemcpyHostToDevice);
     vecsumKernel <<< 1, size >>> (dVec, dSum, size);
     cudaMemcpy(sum, dSum, sizeof(unsigned int), cudaMemcpyDeviceToHost);
     cudaFree(dVec); cudaFree(dSum);
}




int main(int argc, char **argv){
  if (argc < 2){
    printf("Usage: <filename>\n");
    exit(-1);
  }
  int size;
  unsigned int *vec;
  FILE *f = fopen(argv[1],"r");
  fscanf(f,"%d\n",&size);
  size = 1 << size;
  if (size >= (1 << 20)){
    printf("Size (%u) is too large: size is limited to 2^20\n",size);
    exit(-1);
  }
   vec = (unsigned int *) malloc(size * sizeof(unsigned int)); assert(vec);
  for (int i=0; i<size; i++){
    fscanf(f, "%u\n",&(vec[i])); 
}
 
  unsigned int sum=0;
  vecsum(vec, &sum, size);
  printf("sum = %u\n", sum);
  fclose(f);
}

