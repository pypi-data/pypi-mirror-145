#include "Error.h"

HalSMError HalSMError_init(int line,char *error)
{
    HalSMError err;
    err.line=line;
    err.error=error;
    return err;
}