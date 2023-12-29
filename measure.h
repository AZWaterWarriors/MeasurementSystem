/*
 *
 * Water Warriors Moisture Harvester Meteorological Measurement System
 *
 */

#ifndef _MEASURE_H
#define _MEASURE_H

#define SENSOR_VCC
#define SENSOR_DATA
#define WAIT_TIME

int initsensor(void);
float gettemp(void);
float gethumid(void);

#endif
