//
//  jfs9, 10/24/15  v2, add variable for altering frequency
//         3/17/17 v3,  v3 add internal timer
//         10/14/17 - verify timing...
//



#include <stdio.h>
#include <wiringPi.h>
int main (int argc, char** argv)
{
  int period = 500;  // set initial period for delay
  unsigned int current_sec, start_sec;
  
  if (argc>=2 && atoi(argv[1])>0 ) {  // if we have a positive input value
     period = atoi(argv[1]);
     printf ("Set period to %d\n",period);
  }
     
  
  wiringPiSetup () ;
  start_sec = millis();
  pinMode (23, OUTPUT) ; // wiringPi pin 23 = GPIO pin 13
  for (current_sec = 0; (current_sec / 1000) < 5; current_sec = millis() - start_sec)
  {
    digitalWrite (23, HIGH) ; delay (period);
    digitalWrite (23,  LOW) ; delay (period) ;
  }
  printf ("stopped at %d seconds\n", current_sec/1000);
  return 0 ;
}
