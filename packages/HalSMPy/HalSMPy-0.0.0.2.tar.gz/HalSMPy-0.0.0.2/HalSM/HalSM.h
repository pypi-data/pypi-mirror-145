#ifndef HALSM_H
#define HALSM_H
#include <Error.h>
#include <Null.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>

typedef struct HalSMInteger {
    unsigned char* value;
    unsigned long long size;
} HalSMInteger;

typedef enum HalSMVariableType {
    HalSMVariableType_int,
    HalSMVariableType_float,
    HalSMVariableType_char,
    HalSMVariableType_void,
    HalSMVariableType_HalSMArray,
    HalSMVariableType_str,
    HalSMVariableType_int_array,
    HalSMVariableType_HalSMFunctionC,
    HalSMVariableType_HalSMClassC,
    HalSMVariableType_HalSMRunClassC,
    HalSMVariableType_HalSMSetArg,
    HalSMVariableType_HalSMError,
    HalSMVariableType_HalSMNull,
    HalSMVariableType_HalSMRunFunc,
    HalSMVariableType_HalSMLocalFunction,
    HalSMVariableType_HalSMCModule,
    HalSMVariableType_HalSMModule,
    HalSMVariableType_HalSMCompiler,
    HalSMVariableType_HalSMCompiler_source,
    HalSMVariableType_HalSMRunClassC_source,
    HalSMVariableType_HalSMRunClass_source,
    HalSMVariableType_HalSMRunClass,
    HalSMVariableType_HalSMFloatGet,
    HalSMVariableType_HalSMClass,
    HalSMVariableType_HalSMVar,
    HalSMVariableType_HalSMMult,
    HalSMVariableType_HalSMDivide,
    HalSMVariableType_HalSMPlus,
    HalSMVariableType_HalSMMinus,
    HalSMVariableType_HalSMEqual,
    HalSMVariableType_HalSMNotEqual,
    HalSMVariableType_HalSMMore,
    HalSMVariableType_HalSMLess,
    HalSMVariableType_HalSMBool,
    HalSMVariableType_HalSMCLElement,
    HalSMVariableType_HalSMDict,
    HalSMVariableType_HalSMSetVar,
    HalSMVariableType_HalSMReturn,
    HalSMVariableType_HalSMFunctionCTypeDef,
    HalSMVariableType_HalSMFunctionArray
} HalSMVariableType;

typedef struct HalSMVariable {
    void* value;
    HalSMVariableType type;
} HalSMVariable;

typedef struct HalSMArray {
    HalSMVariable* arr;
    int size;
} HalSMArray;

typedef enum HalSMFunctionArrayType {
    HalSMFunctionArrayType_function,
    HalSMFunctionArrayType_array
} HalSMFunctionArrayType;

typedef struct HalSMFunctionArray {
    HalSMArray args;
    HalSMFunctionArrayType type;
} HalSMFunctionArray;

typedef struct DictElement {
    HalSMVariable key;
    HalSMVariable value;
} DictElement;

typedef struct DictElementForEach {
    HalSMVariable key;
    HalSMVariable value;
    int index;
} DictElementForEach;

typedef struct Dict {
    int size;
    DictElement *elements;
} Dict;

typedef struct HalSMCalculateVars {
    char *version;
    char*(*addStr)(HalSMVariable,HalSMVariable);
    int(*addInt)(HalSMVariable,HalSMVariable);
    float(*addFloat)(HalSMVariable,HalSMVariable);
    char*(*subStr)(HalSMVariable,HalSMVariable);
    int(*subInt)(HalSMVariable,HalSMVariable);
    float(*subFloat)(HalSMVariable,HalSMVariable);
    char*(*mulStr)(HalSMVariable,HalSMVariable);
    int(*mulInt)(HalSMVariable,HalSMVariable);
    float(*mulFloat)(HalSMVariable,HalSMVariable);
    char*(*divStr)(HalSMVariable,HalSMVariable);
    int(*divInt)(HalSMVariable,HalSMVariable);
    float(*divFloat)(HalSMVariable,HalSMVariable);
} HalSMCalculateVars;

typedef struct HalSMCompiler {
    Dict functions;
    Dict sys_modules;
    HalSMCalculateVars calcVars;
    HalSMArray numbers;
    int line;
    Dict variables;
    Dict modules;
    Dict localFunctions;
    Dict classes;
    char* code;
    char* path;
    char* pathModules;
    void(*print)(char*);
    void(*printErrorf)(char*);
    char*(*inputf)(char*);
    char*(*readFilef)(char*);
    HalSMArray externModules;
} HalSMCompiler;

typedef HalSMVariable(*HalSMFunctionCTypeDef)(HalSMCompiler,HalSMArray);

typedef struct HalSMFunctionC {
    HalSMFunctionCTypeDef func;
} HalSMFunctionC;

typedef struct HalSMRunClassC {
    char* name;
    Dict vrs;
    Dict funcs;
} HalSMRunClassC;

typedef struct HalSMClassC {
    Dict vrs;
    Dict funcs;
    char*(*getName)();
    void(*init_runclass)(HalSMRunClassC*);
} HalSMClassC;

typedef struct HalSMCModule {
    Dict lfuncs;
    Dict vrs;
    Dict classes;
    char*(*getName)();
} HalSMCModule;

typedef struct HalSMModule {
    char* name;
    Dict vrs;
    Dict lfuncs;
    Dict classes;
} HalSMModule;

typedef struct HalSMLocalFunction {
    char* name;
    HalSMArray args;
    HalSMArray func;
    Dict vars;
} HalSMLocalFunction;

typedef struct HalSMVar {
    char* name;
} HalSMVar;

typedef struct HalSMPlus {unsigned char n;} HalSMPlus;
typedef struct HalSMMinus {unsigned char n;} HalSMMinus;
typedef struct HalSMMult {unsigned char n;} HalSMMult;
typedef struct HalSMDivide {unsigned char n;} HalSMDivide;

typedef struct HalSMEqual {unsigned char n;} HalSMEqual;
typedef struct HalSMNotEqual {unsigned char n;} HalSMNotEqual;
typedef struct HalSMMore {unsigned char n;} HalSMMore;
typedef struct HalSMLess {unsigned char n;} HalSMLess;

typedef struct HalSMSetArg {
    char *name;
    HalSMVariable value;
} HalSMSetArg;

typedef struct HalSMRunFunc {
    HalSMFunctionC func;
    HalSMArray args;
} HalSMRunFunc;

typedef struct HalSMRunClass {
    char* name;
    Dict funcs;
    Dict vars;
} HalSMRunClass;

typedef struct HalSMClass {
    char* name;
    Dict funcs;
    Dict vars;
} HalSMClass;

typedef struct HalSMFloatGet {
    char* st;
} HalSMFloatGet;

typedef struct HalSM {
    char version[30];
    HalSMArray externModules;
    char* pathModules;
    void(*print)(char*);
    void(*printErrorf)(char*);
    char*(*inputf)(char*);
    char*(*readFilef)(char*);
} HalSM;

typedef struct HalSMSetVar {
    char* name;
    char* value;
} HalSMSetVar;

typedef struct HalSMReturn {
    HalSMArray value;
} HalSMReturn;

typedef enum HalSMCLElementType {
    HalSMCLElementType_while,
    HalSMCLElementType_elif,
    HalSMCLElementType_if,
    HalSMCLElementType_else,
    HalSMCLElementType_for
} HalSMCLElementType;

typedef struct HalSMCLElement {
    HalSMArray func;
    void(*addFunc)(void*,HalSMVariable);
    HalSMVariable(*start)(void*,HalSMCompiler*);
    HalSMCLElementType type;
    void* element;
} HalSMCLElement;

typedef struct HalSMFor {
    HalSMVariable var;
    HalSMArray arr;
} HalSMFor;

typedef struct HalSMIf {
    HalSMArray arr;
} HalSMIf;

typedef struct HalSMElse {
    unsigned char n;
} HalSMElse;

typedef struct HalSMWhile {
    HalSMArray arr;
} HalSMWhile;

HalSMArray HalSMArray_init();
HalSMArray HalSMArray_init_with_elements(HalSMVariable* arr,unsigned int size);
HalSMArray HalSMArray_split_str(char* str,char* spl);
void HalSMArray_add(HalSMArray *harr,HalSMVariable value);
void HalSMArray_set(HalSMArray *harr,HalSMVariable value,unsigned int index);
void HalSMArray_remove(HalSMArray *harr,unsigned int index);
void HalSMArray_appendArray(HalSMArray* harr,HalSMArray t);
HalSMVariable HalSMArray_get(HalSMArray harr,unsigned int index);
HalSMArray HalSMArray_reverse(HalSMArray harr);
char* HalSMArray_join_str(HalSMArray harr,char* join);
char* HalSMArray_to_print(HalSMArray harr);
char* HalSMArray_chars_to_str(HalSMArray harr);
HalSMArray HalSMArray_slice(HalSMArray harr,unsigned int s,unsigned int e);
unsigned char HalSMArray_compare(HalSMArray harr,HalSMArray barr);
HalSMArray HalSMArray_from_str(char* str,unsigned int size);
HalSMArray HalSMArray_make_args(unsigned int size,...);
HalSMArray HalSMArray_copy(HalSMArray harr);

HalSM HalSM_init(HalSMArray externModules,void(*printf)(char*),void(*printErrorf)(char*),char*(*inputf)(char*),char*(*readFilef)(char*),char* pathModules);
void HalSM_compile(HalSM hsm,char* code,char* path);
void HalSM_compile_without_path(HalSM hsm,char* code);

HalSMCalculateVars HalSMCalculateVars_init();
char* HalSMCalculateVars_addStr(HalSMVariable v0,HalSMVariable v1);
char* HalSMCalculateVars_subStr(HalSMVariable v0,HalSMVariable v1);
char* HalSMCalculateVars_mulStr(HalSMVariable v0,HalSMVariable v1);
char* HalSMCalculateVars_divStr(HalSMVariable v0,HalSMVariable v1);
int HalSMCalculateVars_addInt(HalSMVariable v0,HalSMVariable v1);
int HalSMCalculateVars_subInt(HalSMVariable v0,HalSMVariable v1);
int HalSMCalculateVars_mulInt(HalSMVariable v0,HalSMVariable v1);
int HalSMCalculateVars_divInt(HalSMVariable v0,HalSMVariable v1);
float HalSMCalculateVars_addFloat(HalSMVariable v0,HalSMVariable v1);
float HalSMCalculateVars_subFloat(HalSMVariable v0,HalSMVariable v1);
float HalSMCalculateVars_mulFloat(HalSMVariable v0,HalSMVariable v1);
float HalSMCalculateVars_divFloat(HalSMVariable v0,HalSMVariable v1);

HalSMVariable HalSMCompiler_readFile(HalSMCompiler hsmc,HalSMArray args);
HalSMVariable HalSMCompiler_input(HalSMCompiler hsmc,HalSMArray args);
HalSMVariable HalSMCompiler_reversed(HalSMCompiler hsmc,HalSMArray args);
HalSMVariable HalSMCompiler_range(HalSMCompiler hsmc,HalSMArray args);
HalSMVariable HalSMCompiler_print(HalSMCompiler hsmc,HalSMArray args);
HalSMCompiler HalSMCompiler_init(char* code,char* path,HalSMArray externModules,void(*printf)(char*),void(*printErrorf)(char*),char*(*inputf)(char*),char*(*readFilef)(char*),char* pathModules);
HalSMArray HalSMCompiler_getLines(char* text);
void HalSMCompiler_ThrowError(HalSMCompiler hsmc,int line,char* error);
HalSMVariable HalSMCompiler_getNameFunction(HalSMCompiler hsmc,char* l);
HalSMVariable HalSMCompiler_isSetVar(char* l);
HalSMArray HalSMCompiler_getTabs(char* l);
unsigned char HalSMCompiler_isNull(char* text);
HalSMArray HalSMCompiler_compile(HalSMCompiler hsmc,char* text);
HalSMModule HalSMCompiler_loadHalSMModule(HalSMCompiler hsmc,char* name,char* file);

HalSMVariable HalSMCompiler_isGet(HalSMCompiler hsmc,char* l,unsigned char ret);
HalSMArray HalSMCompiler_getArgs(HalSMCompiler hsmc,char* l,unsigned char tabs);
HalSMVariable HalSMCompiler_getArgsSetVar(HalSMCompiler hsmc,char* value);
HalSMVariable HalSMCompiler_isRunFunction(HalSMCompiler hsmc,unsigned char tabs,char* l);

HalSMVariable HalSMCompiler_additionVariables(HalSMCompiler hsmc,HalSMVariable v0,HalSMVariable v1);
HalSMVariable HalSMCompiler_subtractionVariables(HalSMCompiler hsmc,HalSMVariable v0,HalSMVariable v1);
HalSMVariable HalSMCompiler_multiplyVariables(HalSMCompiler hsmc,HalSMVariable v0,HalSMVariable v1);
HalSMVariable HalSMCompiler_divideVariables(HalSMCompiler hsmc,HalSMVariable v0,HalSMVariable v1);

HalSMLocalFunction HalSMLocalFunction_init(char* name,char* args,Dict vrs);
HalSMVariable HalSMLocalFunction_run(HalSMLocalFunction lf,HalSMCompiler hsmc,HalSMArray args);

unsigned char HalSMCompiler_isMore(HalSMVariable a,HalSMVariable b);
unsigned char HalSMCompiler_isLess(HalSMVariable a,HalSMVariable b);

unsigned char HalSMIsInt(char *c);
unsigned char HalSMIsFloat(char *c);

HalSMFloatGet HalSMFloatGet_init(char* st);

HalSMCModule HalSMCModule_init(char*(*getName)());

HalSMModule HalSMModule_init(char* name, Dict vrs, Dict lfuncs, Dict classes);

HalSMRunFunc HalSMRunFunc_init(HalSMFunctionC func,HalSMArray args);

HalSMClassC HalSMClassC_init(void(*init_runclass)(HalSMRunClassC*),char*(*getName)());
HalSMRunClassC HalSMClassC_run(HalSMCompiler hsmc,HalSMClassC classc,HalSMArray args);

HalSMClass HalSMClass_init(char* name,Dict vrs);
HalSMRunClass HalSMClass_run(HalSMClass class,HalSMCompiler hsmc,HalSMArray args);

HalSMRunClass HalSMRunClass_init(char* name,Dict vrs,Dict funcs);
HalSMRunClass HalSMRunClass__init__(HalSMRunClass runclass,HalSMCompiler hsmc,HalSMArray args);

HalSMFunctionC HalSMFunctionC_init(HalSMFunctionCTypeDef func);
HalSMVariable HalSMFunctionC_run(HalSMCompiler hsmc,HalSMFunctionC hfc,HalSMArray args);
void HalSMFunctionC_GetArg(void* var,HalSMArray args,int index);

HalSMRunClassC HalSMRunClassC_init(void(*init_runclass)(HalSMRunClassC*),char* name,Dict vrs,Dict funcs);
HalSMRunClassC HalSMRunClassC__init__(HalSMCompiler hsmc,HalSMRunClassC runclassc,HalSMArray args);

HalSMVar HalSMVar_init(char* name);

HalSMSetArg HalSMSetArg_init(char* name);

HalSMReturn HalSMReturn_init(HalSMArray val);

Dict DictInit();
Dict DictInitWithElements(DictElement *elements,int size);
DictElement DictElementInit(HalSMVariable key,HalSMVariable value);
DictElement DictElementFindByKey(Dict dict,HalSMVariable key);
DictElement DictElementFindByValue(Dict dict,HalSMVariable value);
DictElement DictElementFindByIndex(Dict dict,int index);
int DictElementIndexByKey(Dict dict,HalSMVariable key);
int DictElementIndexByValue(Dict dict,HalSMVariable value);
void PutDictElementToDict(Dict *dict,DictElement elem);
Dict DictCopy(Dict dict);
unsigned char DictCompare(Dict a,Dict b);

HalSMVariable HalSMVariable_init(void* value,HalSMVariableType type);
void HalSMVariable_AsVar(void* var,HalSMVariable arg);
void* HalSMVariable_Read(HalSMVariable arg);
HalSMVariable HalSMVariable_init_str(char* str);
char* HalSMVariable_to_str(HalSMVariable var);
unsigned char HalSMVariable_Compare(HalSMVariable v0,HalSMVariable v1);

HalSMSetVar HalSMSetVar_init(char* name,char* value);

char* Int2Str(int c);
char* Float2Str(float c);

int ParseInt(char* c);
HalSMVariable ParseHalSMVariableInt(char* c);

float ParseFloat(char* c);
HalSMVariable ParseHalSMVariableFloat(char* c);

int StringIndexOf(char* c,char* f);
int StringLastIndexOf(char* c,char* f);
unsigned char StringCompare(char* c,char* f);
char* SubString(char* c,int start,int end);
char* ConcatenateStrings(char* c,char* f);
char* StringReplace(char* c,char* f,char* r);
unsigned char StringEndsWith(char* c,char* f);
unsigned char StringStartsWith(char* c,char* f);
void AdditionStrings(char** c,char* f,unsigned int sizec,unsigned int sizef);

int IntMathMax(int f,int t);
int IntMathMin(int f,int t);

HalSMInteger HalSMInteger_init(unsigned char* value,unsigned long long size);
HalSMInteger HalSMInteger_FromSignedInteger(signed int value);
HalSMInteger HalSMInteger_Add(HalSMInteger a,HalSMInteger b);
HalSMInteger HalSMInteger_Sub(HalSMInteger a,HalSMInteger b);

HalSMCLElement HalSMCLElement_init(void(*addFunc)(void*,HalSMVariable),HalSMVariable(*start)(void*,HalSMCompiler*),HalSMCLElementType type,void* element);

HalSMCLElement HalSMFor_init(HalSMVariable var,HalSMArray arr);
HalSMVariable HalSMFor_run(HalSMArray func,HalSMCompiler* hsmc);
void HalSMFor_addFunc(void* element,HalSMVariable func);
HalSMVariable HalSMFor_start(void* element,HalSMCompiler* hsmc);

HalSMCLElement HalSMIf_init(HalSMArray arr);
HalSMVariable HalSMIf_run(HalSMArray func,HalSMCompiler* hsmc);
void HalSMIf_addFunc(void* element,HalSMVariable func);
HalSMVariable HalSMIf_start(void* element,HalSMCompiler* hsmc);

HalSMCLElement HalSMElif_init(HalSMArray arr);

HalSMCLElement HalSMElse_init();
HalSMVariable HalSMElse_run(HalSMArray func,HalSMCompiler* hsmc);
void HalSMElse_addFunc(void* element,HalSMVariable func);
HalSMVariable HalSMElse_start(void* element,HalSMCompiler* hsmc);

HalSMCLElement HalSMWhile_init(HalSMArray arr);
HalSMVariable HalSMWhile_run(HalSMArray func,HalSMCompiler* hsmc);
void HalSMWhile_addFunc(void* element,HalSMVariable func);
HalSMVariable HalSMWhile_start(void* element,HalSMCompiler* hsmc);

#define typevar(x) _Generic((x),char*:HalSMVariableType_char,void*:HalSMVariableType_void,int*:HalSMVariableType_int,int**:HalSMVariableType_int_array,\
float*:HalSMVariableType_float,HalSMArray*:HalSMVariableType_HalSMArray,char**:HalSMVariableType_str,HalSMFunctionC*:HalSMVariableType_HalSMFunctionC,\
HalSMRunClassC*:HalSMVariableType_HalSMRunClassC,HalSMSetArg*:HalSMVariableType_HalSMSetArg,HalSMError*:HalSMVariableType_HalSMError,\
HalSMNull*:HalSMVariableType_HalSMNull,HalSMRunFunc*:HalSMVariableType_HalSMRunFunc,HalSMLocalFunction*:HalSMVariableType_HalSMLocalFunction,\
HalSMCModule*:HalSMVariableType_HalSMCModule,HalSMModule*:HalSMVariableType_HalSMModule,HalSMClassC*:HalSMVariableType_HalSMClassC,\
HalSMCompiler*:HalSMVariableType_HalSMCompiler,HalSMCompiler**:HalSMVariableType_HalSMCompiler_source,\
HalSMRunClassC**:HalSMVariableType_HalSMRunClassC_source,HalSMRunClass**:HalSMVariableType_HalSMRunClass_source,\
HalSMRunClass*:HalSMVariableType_HalSMRunClass,HalSMFloatGet*:HalSMVariableType_HalSMFloatGet,\
HalSMClass*:HalSMVariableType_HalSMClass,HalSMVar*:HalSMVariableType_HalSMVar,HalSMPlus*:HalSMVariableType_HalSMPlus,\
HalSMMinus*:HalSMVariableType_HalSMMinus,HalSMMult*:HalSMVariableType_HalSMMult,HalSMDivide*:HalSMVariableType_HalSMDivide,\
HalSMEqual*:HalSMVariableType_HalSMEqual,HalSMNotEqual*:HalSMVariableType_HalSMNotEqual,HalSMMore*:HalSMVariableType_HalSMMore,\
HalSMLess*:HalSMVariableType_HalSMLess,unsigned char*:HalSMVariableType_HalSMBool,HalSMCLElement*:HalSMVariableType_HalSMCLElement,\
Dict*:HalSMVariableType_HalSMDict,HalSMReturn*:HalSMVariableType_HalSMReturn,HalSMSetVar*:HalSMVariableType_HalSMSetVar,\
HalSMFunctionCTypeDef*:HalSMVariableType_HalSMFunctionCTypeDef,HalSMFunctionArray*:HalSMVariableType_HalSMFunctionArray)
#define HalSMVariable_auto(val) (HalSMVariable_init(val,typevar(val)))
#define HalSMVariable_GetValue(arg) ({\
    void* var;\
    if(arg.type==HalSMVariableType_str){char* var;}\
    else if(arg.type==HalSMVariableType_int){int var;}\
    else if(arg.type==HalSMVariableType_char){char var;}\
    else if(arg.type==HalSMVariableType_float){float var;}\
    else if(arg.type==HalSMVariableType_HalSMArray){HalSMArray var;}\
    else if(arg.type==HalSMVariableType_int_array){int* var;}\
    else if(arg.type==HalSMVariableType_HalSMFunctionC){HalSMFunctionC var;}\
    else if(arg.type==HalSMVariableType_HalSMRunClassC){HalSMRunClassC var;}\
    else if(arg.type==HalSMVariableType_HalSMSetArg){HalSMSetArg var;}\
    else if(arg.type==HalSMVariableType_HalSMError){HalSMError var;}\
    else if(arg.type==HalSMVariableType_HalSMNull){HalSMNull var;}\
    else if(arg.type==HalSMVariableType_HalSMRunFunc){HalSMRunFunc var;}\
    else if(arg.type==HalSMVariableType_HalSMLocalFunction){HalSMLocalFunction var;}\
    else if(arg.type==HalSMVariableType_HalSMCModule){HalSMCModule var;}\
    else if(arg.type==HalSMVariableType_HalSMModule){HalSMModule var;}\
    else if(arg.type==HalSMVariableType_HalSMClassC){HalSMClassC var;}\
    else if(arg.type==HalSMVariableType_HalSMCompiler){HalSMCompiler var;}\
    else if(arg.type==HalSMVariableType_HalSMCompiler_source){HalSMCompiler* var;}\
    else if(arg.type==HalSMVariableType_HalSMRunClassC_source){HalSMRunClassC* var;}\
    else if(arg.type==HalSMVariableType_HalSMRunClass_source){HalSMRunClass* var;}\
    else if(arg.type==HalSMVariableType_HalSMRunClass){HalSMRunClass var;}\
    else if(arg.type==HalSMVariableType_HalSMFloatGet){HalSMFloatGet var;}\
    else if(arg.type==HalSMVariableType_HalSMClass){HalSMClass var;}\
    else if(arg.type==HalSMVariableType_HalSMVar){HalSMVar var;}\
    else if(arg.type==HalSMVariableType_HalSMPlus){HalSMPlus var;}\
    else if(arg.type==HalSMVariableType_HalSMMinus){HalSMMinus var;}\
    else if(arg.type==HalSMVariableType_HalSMMult){HalSMMult var;}\
    else if(arg.type==HalSMVariableType_HalSMDivide){HalSMDivide var;}\
    else if(arg.type==HalSMVariableType_HalSMEqual){HalSMEqual var;}\
    else if(arg.type==HalSMVariableType_HalSMNotEqual){HalSMNotEqual var;}\
    else if(arg.type==HalSMVariableType_HalSMMore){HalSMMore var;}\
    else if(arg.type==HalSMVariableType_HalSMLess){HalSMLess var;}\
    else if(arg.type==HalSMVariableType_HalSMBool){unsigned char var;}\
    else if(arg.type==HalSMVariableType_HalSMCLElement){HalSMCLElement var;}\
    else if(arg.type==HalSMVariableType_HalSMDict){Dict var;}\
    else if(arg.type==HalSMVariableType_HalSMSetVar){HalSMSetVar var;}\
    else if(arg.type==HalSMVariableType_HalSMReturn){HalSMReturn var;}\
    else if(arg.type==HalSMVariableType_HalSMFunctionArray){HalSMFunctionArray var;}\
    __typeof__(var) out=*(__typeof__(var)*)arg.value;\
    out;\
})

#define HalSMVariable_FromValue(arg) ({\
    __typeof__(arg)* var=(__typeof__(arg)*)malloc(sizeof(__typeof__(arg)));\
    *var=arg;\
    HalSMVariable_init(var,typevar(var));\
})

#define DictForEach(keyOutDictForEach,valueOutDictForEach,dict) \
    HalSMVariable keyOutDictForEach=dict.elements[0].key;HalSMVariable valueOutDictForEach=dict.elements[0].value;\
    for (int indexDictForEach=0;indexDictForEach<dict.size;indexDictForEach++,keyOutDictForEach=dict.elements[indexDictForEach].key,valueOutDictForEach=dict.elements[indexDictForEach].value)

#define HalSMArrayForEach(elementHalSMArrayForEach,array) \
    HalSMVariable elementHalSMArrayForEach=array.arr[0];\
    for (int indexHalSMArrayForEach=0;indexHalSMArrayForEach<array.size;indexHalSMArrayForEach++,elementHalSMArrayForEach=array.arr[indexHalSMArrayForEach])

#endif