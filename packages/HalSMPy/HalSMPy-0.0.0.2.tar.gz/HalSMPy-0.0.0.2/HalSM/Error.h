#ifndef HALSMERROR_H
#define HALSMERROR_H
#include <string.h>
#include <stdlib.h>

typedef struct HalSMError {
    int line;
    char *error;
} HalSMError;

HalSMError HalSMError_init(int line,char error[]);
#endif