#include <wiringPi.h>
int main (void)
{
  wiringPiSetup () ;
  pinMode (23, OUTPUT) ; // wiringPi pin 23 = GPIO pin 13
//  pinMode (0, OUTPUT) ; // wiringPi pin 0 = GPIO pin 17 
  for (;;)
  {
    digitalWrite (23, HIGH) ; delay (500) ;
    digitalWrite (23,  LOW) ; delay (500) ;
  }
  return 0 ;
}
