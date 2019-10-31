//
//  jfs9, 10/24/15  v2, add variable for altering frequency
//



#include <stdio.h>
#include <wiringPi.h>
int main (int argc, char** argv)
{
  int period = 500;  // set initial period for delay
  
  if (argc>=2 && atoi(argv[1])>0 ) {  // if we have a positive input value
     period = atoi(argv[1]);
     printf ("Set period to %d\n",period);
  }
     
  
  wiringPiSetup () ;
  pinMode (23, OUTPUT) ; // wiringPi pin 23 = GPIO pin 13
  for (;;)
  {
    digitalWrite (23, HIGH) ; delay (period);
    digitalWrite (23,  LOW) ; delay (period) ;
  }
  return 0 ;
}
