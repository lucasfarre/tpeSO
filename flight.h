//
//  flight.h
//  SO
//
//  Created by Franco Román Meola on 11/03/14.
//  Copyright (c) 2014 Franco Román Meola. All rights reserved.
//

#ifndef SO_flight_h
#define SO_flight_h
#define MAX_STRING 20

typedef int flightStatus;
typedef int seatStatus;

typedef struct {
    char id[MAX_STRING]; // Pasaporte
    char name[MAX_STRING];
    char dateOfBirth[MAX_STRING];
} passenger;

typedef struct {
    int row; // 65
    char col; // A
    seatStatus status;
    passenger passenger;
} seat;

typedef struct {
    char id[MAX_STRING];
    char airline[MAX_STRING];
    seat seatList[MAX_STRING];
} airplane;

typedef struct {
    char id[MAX_STRING];
    char startDate[MAX_STRING];
    char endDate[MAX_STRING];
    airplane airplane;
    flightStatus status;
} flight;

#endif
