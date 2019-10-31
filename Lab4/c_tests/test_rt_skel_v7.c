//
// jfs9 10/24/15
// v2 Add wiringPi to toggle output
// v5 10/22/18 - add frequency display
// v6 10/22/18 - loop not nanosleep
// v7 3/20/19 - test and cleanup loop code
//

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <sched.h>
#include <sys/mman.h>
#include <string.h>
#include <wiringPi.h>

#define MY_PRIORITY (49) /* we use 49 as the PRREMPT_RT use 50
                            as the priority of kernel tasklets
                            and interrupt handler by default */

#define MAX_SAFE_STACK (8*1024) /* The maximum stack size which is
                                   guaranteed safe to access without
                                   faulting */

#define NSEC_PER_SEC    (1000000000) /* The number of nsecs per sec. */

void stack_prefault(void) {

        unsigned char dummy[MAX_SAFE_STACK];

        memset(dummy, 0, MAX_SAFE_STACK);
        return;
}

int main(int argc, char* argv[])
{
        struct timespec t;
        struct sched_param param;
        int interval = 20000; /* about 3.7 kHz frequency,  268 micorseconds period */
        int PinValue = 0;  // used to toggle output pin
        float freq;
        int i;

        int current_sec, start_sec;

       if ( argc>=2 && atoi(argv[1] ) >0 ) { // if positive argument
          interval = atoi(argv[1]);
       }
       printf ( "Interval = %d \n", interval);
       //printf ( "Temp = %0.10f \n",(double) 1 / (2 * (interval) )  );
//       freq = NSEC_PER_SEC * ( ( 1/(float) (2*interval) ) );
//       printf ( "Frequency = %f Hz\n", freq );

        wiringPiSetup();   // initialize WiringPi
        pinMode (23, OUTPUT);  // Setup wPi pin 23 = GPIO 13 = OUTPUT

        /* Declare ourself as a real time task */
/****/
        param.sched_priority = MY_PRIORITY;
        if(sched_setscheduler(0, SCHED_FIFO, &param) == -1) {
                perror("sched_setscheduler failed");
                exit(-1);
        }
/****/
        /* Lock memory */

        if(mlockall(MCL_CURRENT|MCL_FUTURE) == -1) {
                perror("mlockall failed");
                exit(-2);
        }

        /* Pre-fault our stack */
        stack_prefault();

         while(1) { // run forever ...
//        while( current_sec < 5 ) {   // run the loop for 5 sec

               for ( i=0 ; i<interval ; ++i ) {  /// use delay loop to control frequency
               }

               //  code to control GPIO goes here....

   }
}

