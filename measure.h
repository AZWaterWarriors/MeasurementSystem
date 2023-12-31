/*
 *
 * Water Warriors Moisture Harvester Meteorological Measurement System
 *
 */

#ifndef _MEASURE_H
#define _MEASURE_H

#define SENSOR_VCC 35
#define SENSOR_DATA 37
#define WAIT_TIME 1000000*60

typedef struct reading_s{
	uint16_t humid;
	uint16_t temp;
	uint8_t check;
} reading_t;

int initsensor(void);
reading_t *getreading(void);

#endif
