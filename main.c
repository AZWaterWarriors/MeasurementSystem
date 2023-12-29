/*
 *
 * Water Warriors Moisture Harvester Meteorological Measurement System
 *
 */

#include <stdio.h>
#include <unistd.h>
#include <stdint.h>

#include "measure.h"
#include "rpigpio/electronics.h"

int initsensor(void);
float gettemp(void);
float gethumid(void);

typedef struct reading_s{
	uint16_t humid;
	uint16_t temp;
	uint8_t check;
} reading_t;

int main(int argc, char *argv[]){

  setupio();

  if(initsensor() != 0){ return -1; };

	for(;;){
    float temp = gettemp();
    float humid = gethumid();
  };

};

int initsensor(void){

	writepin(SENSOR_VCC, 1);

	

};

reading_t *getreading(void){

	reading_t *reading;
	uint8_t buffer[5] = { 0 }; /* 40 bits */

	for(int i = 0; i < 40; i++){
		usleep(100); /* Skip through intial 50us and past the max. 28us for 0, accounting for +- 10us error */
		if(getpin(SENSOR_DATA)){ buffer[(int)(i/8)] |= (1<<(i % 8)); };
		while(getpin(SENSOR_DATA)){
			usleep(10);
		};
	};

	reading->humid = (((uint16_t)buffer[0])<<8) | buffer[1];
	reading->temp = (((uint_16_t)buffer[2])<<8) | buffer[3];
	reading->check = buffer[4];

	uint16_t test = reading->humid + reading->temp;
	if((uint8_t)(test & 0xFF) != reading->check){ return NULL; };

	return reading;

};
