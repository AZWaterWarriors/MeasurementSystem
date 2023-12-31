/*
 *
 * Water Warriors Moisture Harvester Meteorological Measurement System
 *
 */

/* Sensor manual: https://cdn-shop.adafruit.com/datasheets/Digital%20humidity%20and%20temperature%20sensor%20AM2302.pdf */

#include <stdio.h>
#include <unistd.h>
#include <stdint.h>
#include <time.h>

#include "measure.h"
#include "rpigpio/gpio.h"

int initsensor(void);
reading_t *getreading(void);

int main(int argc, char *argv[]){

	FILE * file = fopen("/var/waterwarriors/data", "a");

	if(initsensor() != 0){ return -1; };

	for(;;){
		reading_t *reading = { 0 };
		reading = getreading();
		
		if(reading == NULL){
			fprintf(file, "ERROR, ERROR, ERROR\n");
		}
		else{
			float humid = ((float)reading->humid)/10;
			float temp = ((float)reading->temp)/10;
			time_t rtime;
			struct tm * timeinfo;
			time(&rtime);
			timeinfo = localtime(&rtime);
			fprintf(file, "%s, %.1f, %.1f\n", asctime(timeinfo), humid, temp);
		};

		usleep(WAIT_TIME);
 	};

};

int initsensor(void){

	writepin(SENSOR_VCC, 1);

	/* Init sequence */
	writepin(SENSOR_DATA, 0);
	usleep(10000); /* Wait 10 ms */
	writepin(SENSOR_DATA, 1);
	usleep(40); /* Wait 40 us */
	getpin(SENSOR_DATA); /* Set to input mode */
	usleep(40); /* Wait approx. half of 80 us */
	if(getpin(SENSOR_DATA)){ return -1; }; /* Should not be high */
	usleep(80); /* Wait until about half way through second part */
	if(!getpin(SENSOR_DATA)){ return -1; }; /* Should be high. */
	usleep(40); /* Wait until data transmission starts. */

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
	reading->temp = (((uint16_t)buffer[2])<<8) | buffer[3];
	reading->check = buffer[4];

	uint16_t test = reading->humid + reading->temp;
	if((uint8_t)(test & 0xFF) != reading->check){ return NULL; };

	return reading;

};
