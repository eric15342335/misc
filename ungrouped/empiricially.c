#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>


/* Returns an integer in the range [0, n).
 *
 * Uses rand(), and so is affected-by/affects the same seed.
 */
int randint(int n) {
  if ((n - 1) == RAND_MAX) {
    return rand();
  } else {
    // Supporting larger values for n would requires an even more
    // elaborate implementation that combines multiple calls to rand()
    assert (n <= RAND_MAX);

    // Chop off all of the values that would cause skew...
    int end = RAND_MAX / n; // truncate skew
    assert (end > 0);
    end *= n;

    // ... and ignore results from rand() that fall above that limit.
    // (Worst case the loop condition should succeed 50% of the time,
    // so we can expect to bail out of this loop pretty quickly.)
    int r;
    while ((r = rand()) >= end);

    return r % n;
  }
}

int main(){
  int a,b,c=0;
  srand((unsigned int) time(NULL));
  for (int d = 0; d<1000000; d++)
  {
    if (a==4) {b++;}
    else
    {
      if (b==3) {a++;}
      else {
        if (randint(2)==1) {a++;}
        else {b++;}
      }
    }
    if ((a==4) && (b==2))
    {
      c++;
      a=0;
      b=0;
    }
    if ((a==4) && (b==3))
    {
      a=0;
      b=0;
    }
  }
  printf("%d", 1000000 / c);
  return 0;
}