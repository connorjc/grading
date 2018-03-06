#include <stdio.h>
FILE * file = NULL;
int rand(){
    int r;
    if(file == NULL)
        file = fopen("../../rand1.txt", "r");
    fscanf(file, "%d", &r);
    return r;
}
