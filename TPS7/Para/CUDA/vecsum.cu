#include <cstdlib>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>    //taille<2^20


__global__ void vecsumKernel(unsigned int *dVec, int size){
  printf("kerneled\n");
	int taille=blockDim.x/2;
	int id = blockIdx.x*blockDim.x+threadIdx.x;

	while(taille>=1 && id<=taille){
		dVec[id] += dVec[taille+id];
		taille = taille / 2;
		__syncthreads();
	}
  
}

void vecsum (unsigned int *vec, unsigned int *sum, int size){
     int bytes = size * sizeof(unsigned int);
     unsigned int *dVec;
     printf("size: %i\n", size);
     cudaMalloc((void **) &dVec, bytes);
     cudaMemcpy(dVec, vec, bytes, cudaMemcpyHostToDevice);
     vecsumKernel <<< 1, size >>> (dVec, size);
     cudaMemcpy(sum, dVec, sizeof(unsigned int), cudaMemcpyDeviceToHost);
     cudaFree(dVec);
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

