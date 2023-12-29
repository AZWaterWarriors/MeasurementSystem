/*
 *
 * Water Warriors Moisture Harvester Meteorological Measurement System
 *
 */

#include <stdio.h>

#include "measure.h"
#include "rpigpio/electronics.h"

int initsensor(void);
float gettemp(void);
float gethumid(void);

int main(int argc, char *argv[]){

  setupio();

  if(initsensor() != 0){ return -1; };

	for(;;){
    float temp = gettemp();
    float humid = gethumid();
  };

};

int initsensor(void){



};

float gettemp(void){



};

float gethumid(void){



};
