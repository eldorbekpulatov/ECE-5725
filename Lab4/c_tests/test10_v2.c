//
//  jfs9, 3/15/19   Sample C 
//
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

#define MY_VALUE 10

int main() {

   int index;

   index = 0;

   if (index <= 0) {
      printf ("index is less than 1\n");
     } else {
      printf ("index is greater than or equal to 1\n");
   }
   printf ("\n");
//   while ( index < 10 ) {
   while ( index < MY_VALUE ) {
      printf ("index = %d\n", index);
      ++index;
   }
   printf ("\n");
   for ( index=0 ; index<10 ; ++index ) {
      printf ("index = %d\n", index);
   }

} /* end of main */
      
