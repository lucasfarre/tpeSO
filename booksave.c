/* database.c -- saves structure contents in a file */

#include <stdio.h>

#include <stdlib.h>

#include "flight.h"

#define MAXTITL   40

#define MAXAUTL   40

#define MAXBKS   10             /* maximum number of books */



// struct book {                   /* set up book template    */
// 
//     char title[MAXTITL];
// 
//     char author[MAXAUTL];
// 
//     float value;
// 
// };



int main(void)

{

    flight library[MAXBKS]; /* array of structures     */

    int count = 0;

    int index, filecount;

    FILE * pbooks;

    int size = sizeof (flight);



    if ((pbooks = fopen("book.dat", "a+b")) == NULL)

    {

        fputs("Can't open book.dat file\n",stderr);

        exit(1);

    }



    rewind(pbooks);            /* go to start of file     */

    while (count < MAXBKS &&  fread(&library[count], size,

                1, pbooks) == 1)

    {

        if (count == 0)

            puts("Current contents of book.dat:");

//         printf("%s by %s: $%.2f\n",library[count].title,
// 
//             library[count].author, library[count].value);
			printf("\nVuelo: %s\n", library[count].id);
			printf("Salida: %s\n", library[count].startDate);
			printf("Llegada: %s\n", library[count].endDate);
			printf("Avión: %s\n", library[count].airplane.id);
			printf("Aerolínea: %s\n", library[count].airplane.airline);
			int i;
			//int seatsCount = sizeof(seatList)/sizeof(seat);
			for(i = 0; i < 2; i++) {
				int seatStatus = library[count].airplane.seatList[i].status;
				printf("Asiento: %d", library[count].airplane.seatList[i].row);
				printf("%c\n", library[count].airplane.seatList[i].col);
				printf("Estado: %d\n", seatStatus);
				if(seatStatus) {
					printf("Pasajero: %s\t", library[count].airplane.seatList[i].passenger.id);
					printf("%s\t", library[count].airplane.seatList[i].passenger.name);
					printf("%s\n", library[count].airplane.seatList[i].passenger.dateOfBirth);
				}
			}
        count++;

    }

    filecount = count;

    if (count == MAXBKS)

    {

        fputs("The book.dat file is full.", stderr);

        exit(2);

    }



    puts("Ingrese en número de vuelo.");

    puts("Press [enter] at the start of a line to stop.");

    while (count < MAXBKS && gets(library[count].id) != NULL

                          && library[count].id[0] != '\0')

    {

        puts("Ingrese la fecha de salida.");

        gets(library[count].startDate);

        puts("Ingrese la fecha de llegada.");

        gets(library[count].endDate);
        
        puts("Ingrese el modelo de avión.");

        gets(library[count].airplane.id);
        
        puts("Ingrese la aerolínea.");

        gets(library[count].airplane.airline);
                
        library[count].airplane.seatList[0].row = 1;
        library[count].airplane.seatList[0].col = 'A';
        library[count].airplane.seatList[0].status = 0;
        
        library[count].airplane.seatList[1].row = 1;
        library[count].airplane.seatList[1].col = 'A';
        library[count].airplane.seatList[1].status = 0;
        
        count++;

        while (getchar() != '\n')

            continue;                /* clear input line  */

         if (count < MAXBKS)

             puts("Enter the next title.");
        
        

    }



    if (count > 0)

    {

//         puts("Here is the list of your books:");
// 
//         for (index = 0; index < count; index++) {
//         	printf("\nVuelo: %s\n", library[count].id);
// 			printf("Salida: %s\n", library[count].startDate);
// 			printf("Llegada: %s\n", library[count].endDate);
// 			printf("Avión: %s\n", library[count].airplane.id);
// 			printf("Aerolínea: %s\n", library[count].airplane.airline);
// 			int i;
// 			//int seatsCount = sizeof(seatList)/sizeof(seat);
// 			for(i = 0; i < 2; i++) {
// 				int seatStatus = library[count].airplane.seatList[i].status;
// 				printf("Asiento: %d", library[count].airplane.seatList[i].row);
// 				printf("%c\n", library[count].airplane.seatList[i].col);
// 				printf("Estado: %d\n", seatStatus);
// 				if(seatStatus) {
// 					printf("Pasajero: %s\t", library[count].airplane.seatList[i].passenger.id);
// 					printf("%s\t", library[count].airplane.seatList[i].passenger.name);
// 					printf("%s\n", library[count].airplane.seatList[i].passenger.dateOfBirth);
// 				}
// 			}
//         }
        
        fwrite(&library[filecount], size, count - filecount, pbooks);
    }

    else

          puts("No books? Too bad.\n");



    puts("Bye.\n");

    fclose(pbooks);



    return 0;

}