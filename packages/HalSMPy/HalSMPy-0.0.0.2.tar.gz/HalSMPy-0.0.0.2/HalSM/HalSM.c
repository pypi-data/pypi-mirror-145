#include <HalSM.h>
#include <HalSMVars.h>

HalSM HalSM_init(HalSMArray externModules,void(*print)(char*),void(*printErrorf)(char*),char*(*inputf)(char*),char*(*readFilef)(char*),char* pathModules) {
    HalSM hsm;
    char* arrIntChar="0123456789";
    arrInt=HalSMArray_init();
    HalSMArray_add(&arrInt,HalSMVariable_FromValue('0'));
    HalSMArray_add(&arrInt,HalSMVariable_FromValue('1'));
    HalSMArray_add(&arrInt,HalSMVariable_FromValue('2'));
    HalSMArray_add(&arrInt,HalSMVariable_FromValue('3'));
    HalSMArray_add(&arrInt,HalSMVariable_FromValue('4'));
    HalSMArray_add(&arrInt,HalSMVariable_FromValue('5'));
    HalSMArray_add(&arrInt,HalSMVariable_FromValue('6'));
    HalSMArray_add(&arrInt,HalSMVariable_FromValue('7'));
    HalSMArray_add(&arrInt,HalSMVariable_FromValue('8'));
    HalSMArray_add(&arrInt,HalSMVariable_FromValue('9'));
    char abvgd=*(char*)(HalSMArray_get(arrInt,5).value);
    strcpy(hsm.version,"0.0.5 (Pre-Alpha)");
    hsm.externModules=externModules;
    hsm.print=print;
    hsm.printErrorf=printErrorf;
    hsm.inputf=inputf;
    hsm.readFilef=readFilef;
    hsm.pathModules=pathModules;
    return hsm;
}

void HalSM_compile(HalSM hsm,char* code,char* path)
{
    HalSMCompiler hsmc=HalSMCompiler_init(code,path,hsm.externModules,hsm.print,hsm.printErrorf,hsm.inputf,hsm.readFilef,hsm.pathModules);
    HalSMCompiler_compile(hsmc,code);
}

void HalSM_compile_without_path(HalSM hsm,char* code)
{
    HalSM_compile(hsm,code,"");
}

HalSMVariable HalSMCompiler_readFile(HalSMCompiler hsmc,HalSMArray args) {
    char* file=*(char**)args.arr[0].value;
    char* resFile=hsmc.readFilef(file);
    return HalSMVariable_init(resFile,HalSMVariableType_str);
}

HalSMVariable HalSMCompiler_input(HalSMCompiler hsmc,HalSMArray args) {
    char* text=*(char**)args.arr[0].value;
    char* resInput=hsmc.inputf(text);
    return HalSMVariable_init(resInput,HalSMVariableType_str);
}

HalSMVariable HalSMCompiler_reversed(HalSMCompiler hsmc,HalSMArray args) {
    HalSMVariable arr=args.arr[0];
    if (arr.type==HalSMVariableType_HalSMArray) {
        HalSMArray out=HalSMArray_reverse(*(HalSMArray*)arr.value);
        return HalSMVariable_init(&out,HalSMVariableType_HalSMArray);
    } else if (arr.type==HalSMVariableType_str) {
        char* arrv=*(char**)arr.value;
        int arrl=strlen(arrv);
        if (arrl==0) {
            return HalSMVariable_init_str("");
        }
        char* out=malloc(arrl+1);
        out[0]=arrv[arrl-1];
        int b=1;
        for (int i=arrl-2;i--;i>-1) {
            out[b]=arrv[i];
            b++;
        }
        out[arrl]='\0';
        return HalSMVariable_init_str(out);
    }
    //Error
    return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
}

HalSMVariable HalSMCompiler_range(HalSMCompiler hsmc,HalSMArray args) {
    int r=*(int*)args.arr[0].value;
    HalSMArray out=HalSMArray_init();
    for(int i=0;i<r;i++){
        HalSMArray_add(&out,HalSMVariable_FromValue(i));
    }
    return HalSMVariable_FromValue(out);
}

HalSMVariable HalSMCompiler_print(HalSMCompiler hsmc,HalSMArray args) {
    HalSMArray out=HalSMArray_init();
    HalSMVariable a;
    char* c;
    for (int i=0;i<args.size;i++) {
        a=args.arr[i];
        if (a.type==HalSMVariableType_int) {
            HalSMArray_add(&out,HalSMVariable_init_str(Int2Str(*(int*)a.value)));
        } else if (a.type==HalSMVariableType_float) {
            HalSMArray_add(&out,HalSMVariable_init_str(Float2Str(*(float*)a.value)));
        } else if (a.type==HalSMVariableType_str) {
            HalSMArray_add(&out,a);
        } else if (a.type==HalSMVariableType_HalSMNull) {
            HalSMArray_add(&out,HalSMVariable_init_str("Null"));
        } else if (a.type==HalSMVariableType_char) {
            c=malloc(2);
            c[0]=*(char*)a.value;
            c[1]='\0';
            HalSMArray_add(&out,HalSMVariable_init(&c,HalSMVariableType_str));
        } else if (a.type==HalSMVariableType_HalSMArray) {
            HalSMArray_add(&out,HalSMVariable_init_str(HalSMArray_to_print(*(HalSMArray*)a.value)));
        } else if (a.type==HalSMVariableType_HalSMRunClassC) {
            c=malloc(21+strlen((*(HalSMRunClassC*)a.value).name));
            strcpy(c,"<Running Class C (");
            strcat(c,(*(HalSMRunClassC*)a.value).name);
            strcat(c,")>");
            c[strlen((*(HalSMRunClassC*)a.value).name)+20]='\0';
            HalSMArray_add(&out,HalSMVariable_init_str(c));
        } else if (a.type==HalSMVariableType_HalSMFunctionC) {
            char* name=malloc(17);
            sprintf(name,"0x%p",(*(HalSMFunctionC*)a.value).func);
            name[100]='\0';
            c=malloc(35);
            strcpy(c,"<Function C at (");
            strcat(c,name);
            strcat(c,")>");
            c[strlen(name)+18]='\0';
            HalSMArray_add(&out,HalSMVariable_init_str(c));
        } else {
            HalSMArray_add(&out,HalSMVariable_init_str(HalSMVariable_to_str(a)));
        }
    }
    hsmc.print(HalSMArray_join_str(out," "));
    void* o;
    return HalSMVariable_init(&o,HalSMVariableType_void);
}



HalSMCompiler HalSMCompiler_init(char* code,char* path,HalSMArray externModules,void(*print)(char*),void(*printErrorf)(char*),char*(*inputf)(char*),char*(*readFilef)(char*),char* pathModules)
{
    HalSMCompiler hsmc;
    hsmc.print=print;
    hsmc.printErrorf=printErrorf;
    hsmc.inputf=inputf;
    hsmc.readFilef=readFilef;
    hsmc.pathModules=pathModules;
    hsmc.path=path;
    hsmc.externModules=externModules;
    hsmc.functions=DictInit();
    hsmc.code=code;

    HalSMFunctionC funcs[5]={
        HalSMFunctionC_init(&HalSMCompiler_readFile),HalSMFunctionC_init(&HalSMCompiler_input),
        HalSMFunctionC_init(&HalSMCompiler_reversed),HalSMFunctionC_init(&HalSMCompiler_range),
        HalSMFunctionC_init(&HalSMCompiler_print)
    };
    char* funcsnames[5]={"readFile","input","reversed","range","print"};
    
    for (int i=0;i<5;i++)
    {
        PutDictElementToDict(&hsmc.functions,DictElementInit(HalSMVariable_init_str(funcsnames[i]),HalSMVariable_FromValue(funcs[i])));
    }

    DictElement sys_modules_arr[1]={DictElementInit(HalSMVariable_init_str("HOTL"),HalSMVariable_init_str("HOTL.hsm"))};
    hsmc.sys_modules=DictInitWithElements(sys_modules_arr,1);
    for (int i=0;i<externModules.size;i++)
    {
        HalSMCModule cm=*(HalSMCModule*)externModules.arr[i].value;
        PutDictElementToDict(&hsmc.sys_modules,DictElementInit(HalSMVariable_init_str(cm.getName()),HalSMVariable_init(&cm,HalSMVariableType_HalSMCModule)));
    }
    hsmc.calcVars=HalSMCalculateVars_init();
    hsmc.line=1;
    hsmc.variables=DictInit();
    hsmc.modules=DictInit();
    return hsmc;
}

HalSMArray HalSMCompiler_getLines(char* text)
{
    HalSMArray out=HalSMArray_init();
    char* o=calloc(0,sizeof(char));
    unsigned int s=0;
    char isS='n';
    char i;
    for (int d=0;d<strlen(text);d++) {
        i=text[d];
        if (isS!='n') {
            if (i==isS) {
                isS='n';
            }
            s++;
            o=realloc(o,s*sizeof(char));
            o[s-1]=i;
        } else if (i=='"' || i=='\'') {
            isS=i;
            s++;
            o=realloc(o,s*sizeof(char));
            o[s-1]=i;
        } else if (i=='\n') {
            s++;
            o=realloc(o,s*sizeof(char));
            o[s-1]='\0';
            HalSMArray_add(&out,HalSMVariable_init_str(o));
            s=0;
            o=calloc(0,sizeof(char));
        } else if (i==';') {
            s++;
            o=realloc(o,s*sizeof(char));
            o[s-1]='\0';
            HalSMArray_add(&out,HalSMVariable_init_str(o));
            s=0;
            o=calloc(0,sizeof(char));
        } else {
            s++;
            o=realloc(o,s*sizeof(char));
            o[s-1]=i;
        }
    }
    if (s!=0) {
        s++;
        o=realloc(o,s*sizeof(char));
        o[s-1]='\0';
        HalSMArray_add(&out,HalSMVariable_init_str(o));
    }
    free(o);
    return out;
}

void HalSMCompiler_ThrowError(HalSMCompiler hsmc,int line,char* error)
{
    char* sl=Int2Str(line);
    char* out=malloc(17+strlen(sl)+strlen(error));
    strcpy(out,"Error at line ");
    strcat(out,sl);
    strcat(out,": ");
    strcat(out,error);
    out[16+strlen(sl)+strlen(error)]='\0';
    hsmc.printErrorf(out);
}

HalSMVariable HalSMCompiler_isGet(HalSMCompiler hsmc,char* l,unsigned char ret)
{
    if (!(StringIndexOf(l,".")!=-1||(StringIndexOf(l,"[")!=-1&&StringIndexOf(l,"]")))) return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    HalSMVariable out=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    int isInd=0;
    HalSMArray o=HalSMArray_init();
    HalSMVariable module=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    int indF=0;
    char isCovichki='n';
    int index=0;
    int lindex=strlen(l)-1;
    char i;
    HalSMVariable obuff;
    char* obuffs;
    HalSMArray argsbuff;

    for (int ii=0;ii<strlen(l);ii++) {
        i=l[ii];
        if (i=='"'||i=='\'') {
            if (i==isCovichki) {
                isCovichki='n';
            } else if (isCovichki='n') {
                isCovichki=i;
            }
            HalSMArray_add(&o,HalSMVariable_FromValue(i));
        } else if (isCovichki!='n') {
            HalSMArray_add(&o,HalSMVariable_FromValue(i));
        } else if (isInd==1&&indF==0) {
            HalSMArray_add(&o,HalSMVariable_FromValue(i));
            if (i==']') {
                isInd=0;
                obuffs=HalSMArray_chars_to_str(o);
                int indexa=ParseInt(SubString(obuffs,0,strlen(obuffs)-1));
                if (out.type==HalSMVariableType_HalSMArray) {
                    HalSMArray rcls=*(HalSMArray*)out.value;
                    if (indexa>=rcls.size) {
                        //Error
                    } else {
                        out=rcls.arr[indexa];
                    }
                } else if (out.type==HalSMVariableType_HalSMRunClassC) {
                    HalSMRunClassC rcls=*(HalSMRunClassC*)out.value;
                    if (DictElementIndexByKey(rcls.funcs,HalSMVariable_init_str("__getitem__"))==-1) {
                        //Error
                    }
                    argsbuff=HalSMArray_init();
                    HalSMArray_add(&argsbuff,HalSMVariable_init(&rcls,HalSMVariableType_HalSMRunClassC));
                    HalSMArray_add(&argsbuff,HalSMVariable_init(&indexa,HalSMVariableType_int));
                    (*(HalSMFunctionCTypeDef*)DictElementFindByKey(rcls.funcs,HalSMVariable_init_str("__getitem__")).value.value)(hsmc,argsbuff);
                    if (out.type==HalSMVariableType_HalSMError){
                        //Error
                    }
                    o=HalSMArray_init();
                } else {
                    //Error
                }
            }
        } else if (i=='['&&indF==0) {
            isInd=1;
            if (o.size!=0) {
                obuff=HalSMVariable_init_str(HalSMArray_chars_to_str(o));
                if (DictElementIndexByKey(hsmc.variables,obuff)!=-1) {
                    out=DictElementFindByKey(hsmc.variables,obuff).value;
                    o=HalSMArray_init();
                } else {
                    //Error
                }
            }
        } else if (i=='(') {
            if(indF==0) {
                obuff=HalSMVariable_init_str(HalSMArray_chars_to_str(o));
                if(DictElementIndexByKey(hsmc.functions,obuff)!=-1) {
                    out=DictElementFindByKey(hsmc.functions,obuff).value;
                } else if (out.type==HalSMVariableType_HalSMModule) {
                    if (DictElementIndexByKey((*(HalSMModule*)out.value).lfuncs,obuff)!=-1) {
                        module=out;
                        out=DictElementFindByKey((*(HalSMModule*)out.value).lfuncs,obuff).value;
                    }
                } else if (out.type==HalSMVariableType_HalSMCModule) {
                    if (DictElementIndexByKey((*(HalSMCModule*)out.value).lfuncs,obuff)!=-1) {
                        module=out;
                        out=DictElementFindByKey((*(HalSMCModule*)out.value).lfuncs,obuff).value;
                    } else if (DictElementIndexByKey((*(HalSMCModule*)out.value).vrs,obuff)!=-1&&DictElementFindByKey((*(HalSMCModule*)out.value).vrs,obuff).value.type==HalSMVariableType_HalSMFunctionC) {
                        module=out;
                        out=DictElementFindByKey((*(HalSMCModule*)out.value).vrs,obuff).value;
                    } else if (DictElementIndexByKey((*(HalSMCModule*)out.value).classes,obuff)!=-1) {
                        module=DictElementFindByKey((*(HalSMCModule*)out.value).classes,obuff).value;
                        argsbuff=HalSMArray_init();
                        out=HalSMVariable_FromValue(HalSMClassC_run(hsmc,*(HalSMClassC*)(DictElementFindByKey((*(HalSMCModule*)out.value).classes,obuff).value.value),argsbuff));
                    }
                } else if (out.type==HalSMVariableType_HalSMRunClass) {
                    if (DictElementIndexByKey((*(HalSMRunClass*)out.value).funcs,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMRunClass*)out.value).funcs,obuff).value;
                    } else if (DictElementIndexByKey((*(HalSMRunClass*)out.value).vars,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMRunClass*)out.value).vars,obuff).value;
                    }
                } else if (out.type==HalSMVariableType_HalSMRunClassC) {
                    if (DictElementIndexByKey((*(HalSMRunClassC*)out.value).funcs,obuff)!=-1) {
                        module=out;
                        out=DictElementFindByKey((*(HalSMRunClassC*)out.value).funcs,obuff).value;
                    } else if (DictElementIndexByKey((*(HalSMRunClassC*)out.value).vrs,obuff)!=-1&&DictElementFindByKey((*(HalSMRunClassC*)out.value).vrs,obuff).value.type==HalSMVariableType_HalSMFunctionC) {
                        module=out;
                        out=DictElementFindByKey((*(HalSMRunClassC*)out.value).vrs,obuff).value;
                    }
                } else if (out.type==HalSMVariableType_HalSMClassC) {
                    if (DictElementIndexByKey((*(HalSMClassC*)out.value).funcs,obuff)!=-1) {
                        HalSMRunClassC hrcc;
                        module=HalSMVariable_init(&hrcc,HalSMVariableType_HalSMRunClassC);
                        out=DictElementFindByKey((*(HalSMClassC*)out.value).funcs,obuff).value;
                    } else if (DictElementIndexByKey((*(HalSMClassC*)out.value).vrs,obuff)!=-1&&DictElementFindByKey((*(HalSMClassC*)out.value).vrs,obuff).value.type==HalSMVariableType_HalSMFunctionC) {
                        HalSMRunClassC hrcc;
                        module=HalSMVariable_init(&hrcc,HalSMVariableType_HalSMRunClassC);
                        out=DictElementFindByKey((*(HalSMClassC*)out.value).vrs,obuff).value;
                    }
                }
                o=HalSMArray_init();
            } else {
                HalSMArray_add(&o,HalSMVariable_FromValue('('));
            }
            indF+=1;
        } else if (i==')') {
            if (out.type==HalSMVariableType_HalSMFunctionC&&indF==1) {
                HalSMArray args=HalSMCompiler_getArgs(hsmc,HalSMArray_chars_to_str(o),ret);

                if (index==lindex&&ret) {
                    HalSMArray ob=HalSMArray_init();
                    HalSMArray_add(&ob,out);
                    HalSMArray_add(&ob,HalSMVariable_init(&args,HalSMVariableType_HalSMArray));
                    HalSMArray_add(&ob,HalSMVariable_init(&null,HalSMVariableType_HalSMNull));
                    HalSMArray_add(&ob,module);
                    return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                } else {
                    out=HalSMFunctionC_run(hsmc,*(HalSMFunctionC*)out.value,args);
                }
            } else if (out.type==HalSMVariableType_HalSMLocalFunction&&indF==1) {
                if (ret) {
                    HalSMArray args=HalSMCompiler_getArgs(hsmc,HalSMArray_chars_to_str(o),ret);
                    HalSMLocalFunction_run(*(HalSMLocalFunction*)out.value,hsmc,args);
                }
                o=HalSMArray_init();
            } else {
                HalSMArray_add(&o,HalSMVariable_FromValue(')'));
            }
            indF-=1;
        } else if (i=='.'&&indF==0) {
            obuff=HalSMVariable_init_str(HalSMArray_chars_to_str(o));
            if (out.type==HalSMVariableType_HalSMNull) {
                if (DictElementIndexByKey(hsmc.variables,obuff)!=-1) {
                    out=DictElementFindByKey(hsmc.variables,obuff).value;
                } else if (DictElementIndexByKey(hsmc.modules,obuff)!=-1) {
                    out=DictElementFindByKey(hsmc.modules,obuff).value;
                } else if (HalSMIsInt(*(char**)obuff.value)) {
                    out=HalSMVariable_FromValue(HalSMFloatGet_init(*(char**)obuff.value));
                } else {
                    //Error
                }
            } else if (out.type==HalSMVariableType_HalSMModule) {
                if (StringIndexOf(*(char**)obuff.value,"(")!=-1&&StringIndexOf(*(char**)obuff.value,")")!=-1) {
                    HalSMVariable cobuff=HalSMArray_get(HalSMArray_split_str(*(char**)cobuff.value,"("),0);
                    if (DictElementIndexByKey((*(HalSMModule*)out.value).lfuncs,cobuff)!=-1) {
                        out=HalSMLocalFunction_run(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMModule*)out.value).lfuncs,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                    } else if (DictElementIndexByKey((*(HalSMModule*)out.value).classes,cobuff)!=-1) {
                        out=HalSMVariable_FromValue(HalSMClass_run(*(HalSMClass*)(DictElementFindByKey((*(HalSMModule*)out.value).classes,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0))); 
                    } else if (DictElementIndexByKey((*(HalSMCModule*)out.value).vrs,cobuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMCModule*)out.value).vrs,cobuff).value; 
                        if (out.type==HalSMVariableType_HalSMLocalFunction) {
                            out=HalSMLocalFunction_run(*(HalSMLocalFunction*)out.value,hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                        } else if (out.type==HalSMVariableType_HalSMClassC) {
                            //In future
                        } else {
                            //Error
                        }
                    } else {
                        //Error
                    }
                } else {
                    if (DictElementIndexByKey((*(HalSMModule*)out.value).vrs,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMModule*)out.value).vrs,obuff).value;
                    } else if (DictElementIndexByKey((*(HalSMModule*)out.value).lfuncs,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMModule*)out.value).lfuncs,obuff).value;
                    } else if (DictElementIndexByKey((*(HalSMCModule*)out.value).classes,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMModule*)out.value).classes,obuff).value;
                    } else {
                        //Error
                    }
                }
            } else if (out.type==HalSMVariableType_HalSMCModule) {
                if (StringIndexOf(*(char**)obuff.value,"(")!=-1&&StringIndexOf(*(char**)obuff.value,")")!=-1) {
                    HalSMVariable cobuff=HalSMArray_get(HalSMArray_split_str(*(char**)cobuff.value,"("),0);
                    if (DictElementIndexByKey((*(HalSMCModule*)out.value).lfuncs,cobuff)!=-1) {
                        out=HalSMLocalFunction_run(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMCModule*)out.value).lfuncs,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                    } else if (DictElementIndexByKey((*(HalSMCModule*)out.value).classes,cobuff)!=-1) {
                        out=HalSMVariable_FromValue(HalSMClass_run(*(HalSMClass*)(DictElementFindByKey((*(HalSMCModule*)out.value).classes,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0))); 
                    } else if (DictElementIndexByKey((*(HalSMCModule*)out.value).vrs,cobuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMCModule*)out.value).vrs,cobuff).value;
                        if (out.type==HalSMVariableType_HalSMFunctionC) {
                            out=HalSMFunctionC_run(hsmc,*(HalSMFunctionC*)out.value,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                        } else {
                            //Error
                        }
                    } else {
                        //Error
                    }
                } else {
                    if (DictElementIndexByKey((*(HalSMCModule*)out.value).vrs,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMCModule*)out.value).vrs,obuff).value;
                    } else if (DictElementIndexByKey((*(HalSMCModule*)out.value).lfuncs,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMCModule*)out.value).lfuncs,obuff).value;
                    } else if (DictElementIndexByKey((*(HalSMCModule*)out.value).classes,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMCModule*)out.value).classes,obuff).value;
                    } else {
                        //Error
                    }
                }
            } else if (out.type==HalSMVariableType_HalSMClassC) {
                if (StringIndexOf(*(char**)obuff.value,"(")!=-1&&StringIndexOf(*(char**)obuff.value,")")!=-1) {
                    HalSMVariable cobuff=HalSMArray_get(HalSMArray_split_str(*(char**)cobuff.value,"("),0);
                    if (DictElementIndexByKey((*(HalSMClassC*)out.value).funcs,cobuff)!=-1) {
                        out=HalSMLocalFunction_run(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMClassC*)out.value).funcs,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                    } else if (DictElementIndexByKey((*(HalSMClassC*)out.value).vrs,cobuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMClassC*)out.value).vrs,cobuff).value;
                        if (out.type==HalSMVariableType_HalSMLocalFunction) {
                            out=HalSMLocalFunction_run(*(HalSMLocalFunction*)out.value,hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                        } else {
                            //Error
                        }
                    }
                } else {
                    if (DictElementIndexByKey((*(HalSMClassC*)out.value).vrs,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMClassC*)out.value).vrs,obuff).value;
                    } else if (DictElementIndexByKey((*(HalSMClassC*)out.value).funcs,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMClassC*)out.value).funcs,obuff).value;
                    } else {
                        //Error
                    }
                }
            } else if (out.type==HalSMVariableType_HalSMRunClassC) {
                if (StringIndexOf(*(char**)obuff.value,"(")!=-1&&StringIndexOf(*(char**)obuff.value,")")!=-1) {
                    HalSMVariable cobuff=HalSMArray_get(HalSMArray_split_str(*(char**)cobuff.value,"("),0);
                    if (DictElementIndexByKey((*(HalSMRunClassC*)out.value).funcs,cobuff)!=-1) {
                        out=HalSMLocalFunction_run(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMRunClassC*)out.value).funcs,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                    } else if (DictElementIndexByKey((*(HalSMRunClassC*)out.value).vrs,cobuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMRunClassC*)out.value).vrs,cobuff).value;
                        if (out.type==HalSMVariableType_HalSMLocalFunction) {
                            out=HalSMLocalFunction_run(*(HalSMLocalFunction*)out.value,hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                        } else {
                            //Error
                        }
                    }
                } else {
                    if (DictElementIndexByKey((*(HalSMRunClassC*)out.value).vrs,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMRunClassC*)out.value).vrs,obuff).value;
                    } else if (DictElementIndexByKey((*(HalSMRunClassC*)out.value).funcs,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMRunClassC*)out.value).funcs,obuff).value;
                    } else {
                        //Error
                    }
                }
            } else if (out.type==HalSMVariableType_HalSMRunClass) {
                if (StringIndexOf(*(char**)obuff.value,"(")!=-1&&StringIndexOf(*(char**)obuff.value,")")!=-1) {
                    HalSMVariable cobuff=HalSMArray_get(HalSMArray_split_str(*(char**)cobuff.value,"("),0);
                    if (DictElementIndexByKey((*(HalSMRunClass*)out.value).funcs,cobuff)!=-1) {
                        out=HalSMLocalFunction_run(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMRunClassC*)out.value).funcs,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                    } else if (DictElementIndexByKey((*(HalSMRunClass*)out.value).vars,cobuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMRunClass*)out.value).vars,cobuff).value;
                        if (out.type==HalSMVariableType_HalSMLocalFunction) {
                            out=HalSMLocalFunction_run(*(HalSMLocalFunction*)out.value,hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                        } else {
                            //Error
                        }
                    }
                } else {
                    if (DictElementIndexByKey((*(HalSMRunClassC*)out.value).vrs,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMRunClassC*)out.value).vrs,obuff).value;
                    } else if (DictElementIndexByKey((*(HalSMRunClassC*)out.value).funcs,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMRunClassC*)out.value).funcs,obuff).value;
                    } else {
                        //Error
                    }
                }
            } else if (out.type==HalSMVariableType_HalSMClass) {
                if (StringIndexOf(*(char**)obuff.value,"(")!=-1&&StringIndexOf(*(char**)obuff.value,")")!=-1) {
                    HalSMVariable cobuff=HalSMArray_get(HalSMArray_split_str(*(char**)cobuff.value,"("),0);
                    if (DictElementIndexByKey((*(HalSMClass*)out.value).funcs,cobuff)!=-1) {
                        out=HalSMLocalFunction_run(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMClass*)out.value).funcs,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                    } else if (DictElementIndexByKey((*(HalSMClass*)out.value).vars,cobuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMClass*)out.value).vars,cobuff).value;
                        if (out.type==HalSMVariableType_HalSMLocalFunction) {
                            out=HalSMLocalFunction_run(*(HalSMLocalFunction*)out.value,hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                        } else {
                            //Error
                        }
                    }
                } else {
                    if (DictElementIndexByKey((*(HalSMClass*)out.value).vars,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMClass*)out.value).vars,obuff).value;
                    } else if (DictElementIndexByKey((*(HalSMClass*)out.value).funcs,obuff)!=-1) {
                        out=DictElementFindByKey((*(HalSMClass*)out.value).funcs,obuff).value;
                    } else {
                        //Error
                    }
                }
            }
            o=HalSMArray_init();
        } else {
            HalSMArray_add(&o,HalSMVariable_FromValue(i));
        }
        index++;
    }

    if (o.size!=0) {
        if (out.type==HalSMVariableType_HalSMModule) {
            if (StringIndexOf(*(char**)obuff.value,"(")!=-1&&StringIndexOf(*(char**)obuff.value,")")!=-1) {
                HalSMVariable cobuff=HalSMArray_get(HalSMArray_split_str(*(char**)cobuff.value,"("),0);
                if (DictElementIndexByKey((*(HalSMModule*)out.value).lfuncs,cobuff)!=-1) {
                    if (ret) {
                        HalSMArray ob=HalSMArray_init();
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMModule*)out.value).lfuncs,cobuff).value.value)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMModule*)out.value));
                        return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                    }
                    return HalSMLocalFunction_run(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMModule*)out.value).lfuncs,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                } else if (DictElementIndexByKey((*(HalSMModule*)out.value).classes,cobuff)!=-1) {
                    if (ret) {
                        HalSMArray ob=HalSMArray_init();
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMClass*)(DictElementFindByKey((*(HalSMModule*)out.value).classes,cobuff).value.value)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMModule*)out.value));
                        return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                    }
                    return HalSMVariable_FromValue(HalSMClass_run(*(HalSMClass*)(DictElementFindByKey((*(HalSMModule*)out.value).classes,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0))); 
                } else if (DictElementIndexByKey((*(HalSMCModule*)out.value).vrs,cobuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMCModule*)out.value).vrs,cobuff).value; 
                    if (out.type==HalSMVariableType_HalSMLocalFunction) {
                        if (ret) {
                            HalSMArray ob=HalSMArray_init();
                            HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMLocalFunction*)out.value));
                            HalSMArray_add(&ob,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0)));
                            HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMModule*)out.value));
                            return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                        }
                        return HalSMLocalFunction_run(*(HalSMLocalFunction*)out.value,hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                    } else if (out.type==HalSMVariableType_HalSMClassC) {
                        //In future
                    } else {
                        //Error
                    }
                } else {
                    //Error
                }
            } else {
                if (DictElementIndexByKey((*(HalSMModule*)out.value).vrs,obuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMModule*)out.value).vrs,obuff).value;
                } else if (DictElementIndexByKey((*(HalSMModule*)out.value).lfuncs,obuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMModule*)out.value).lfuncs,obuff).value;
                } else if (DictElementIndexByKey((*(HalSMCModule*)out.value).classes,obuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMModule*)out.value).classes,obuff).value;
                } else {
                    //Error
                }
            }
        } else if (out.type==HalSMVariableType_HalSMCModule) {
            if (StringIndexOf(*(char**)obuff.value,"(")!=-1&&StringIndexOf(*(char**)obuff.value,")")!=-1) {
                HalSMVariable cobuff=HalSMArray_get(HalSMArray_split_str(*(char**)cobuff.value,"("),0);
                if (DictElementIndexByKey((*(HalSMCModule*)out.value).lfuncs,cobuff)!=-1) {
                    if (ret) {
                        HalSMArray ob=HalSMArray_init();
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMCModule*)out.value).lfuncs,cobuff).value.value)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMCModule*)out.value));
                        return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                    }
                    return HalSMLocalFunction_run(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMCModule*)out.value).lfuncs,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                } else if (DictElementIndexByKey((*(HalSMCModule*)out.value).classes,cobuff)!=-1) {
                    if (ret) {
                        HalSMArray ob=HalSMArray_init();
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMClass*)(DictElementFindByKey((*(HalSMCModule*)out.value).classes,cobuff).value.value)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMCModule*)out.value));
                        return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                    }
                    return HalSMVariable_FromValue(HalSMClass_run(*(HalSMClass*)(DictElementFindByKey((*(HalSMCModule*)out.value).classes,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0))); 
                } else if (DictElementIndexByKey((*(HalSMCModule*)out.value).vrs,cobuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMCModule*)out.value).vrs,cobuff).value;
                    if (out.type==HalSMVariableType_HalSMFunctionC) {
                        if (ret) {
                            HalSMArray ob=HalSMArray_init();
                            HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMLocalFunction*)out.value));
                            HalSMArray_add(&ob,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0)));
                            HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMCModule*)out.value));
                            return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                        }
                        return HalSMFunctionC_run(hsmc,*(HalSMFunctionC*)out.value,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                    } else {
                        //Error
                    }
                } else {
                    //Error
                }
            } else {
                if (DictElementIndexByKey((*(HalSMCModule*)out.value).vrs,obuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMCModule*)out.value).vrs,obuff).value;
                } else if (DictElementIndexByKey((*(HalSMCModule*)out.value).lfuncs,obuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMCModule*)out.value).lfuncs,obuff).value;
                } else if (DictElementIndexByKey((*(HalSMCModule*)out.value).classes,obuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMCModule*)out.value).classes,obuff).value;
                } else {
                    //Error
                }
            }
        } else if (out.type==HalSMVariableType_HalSMRunClass) {
            if (StringIndexOf(*(char**)obuff.value,"(")!=-1&&StringIndexOf(*(char**)obuff.value,")")!=-1) {
                HalSMVariable cobuff=HalSMArray_get(HalSMArray_split_str(*(char**)cobuff.value,"("),0);
                if (DictElementIndexByKey((*(HalSMRunClass*)out.value).funcs,cobuff)!=-1) {
                    if (ret) {
                        HalSMArray ob=HalSMArray_init();
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMRunClass*)out.value).funcs,cobuff).value.value)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMRunClass*)out.value));
                        return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                    }
                    return HalSMLocalFunction_run(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMRunClassC*)out.value).funcs,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                } else if (DictElementIndexByKey((*(HalSMRunClass*)out.value).vars,cobuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMRunClass*)out.value).vars,cobuff).value;
                    if (out.type==HalSMVariableType_HalSMLocalFunction) {
                        if (ret) {
                            HalSMArray ob=HalSMArray_init();
                            HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMLocalFunction*)out.value));
                            HalSMArray_add(&ob,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0)));
                            HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMRunClass*)out.value));
                            return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                        }
                        return HalSMLocalFunction_run(*(HalSMLocalFunction*)out.value,hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                    } else {
                        //Error
                    }
                }
            } else {
                if (DictElementIndexByKey((*(HalSMRunClassC*)out.value).vrs,obuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMRunClassC*)out.value).vrs,obuff).value;
                } else if (DictElementIndexByKey((*(HalSMRunClassC*)out.value).funcs,obuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMRunClassC*)out.value).funcs,obuff).value;
                } else {
                    //Error
                }
            }
        } else if (out.type==HalSMVariableType_HalSMClass) {
            if (StringIndexOf(*(char**)obuff.value,"(")!=-1&&StringIndexOf(*(char**)obuff.value,")")!=-1) {
                HalSMVariable cobuff=HalSMArray_get(HalSMArray_split_str(*(char**)cobuff.value,"("),0);
                if (DictElementIndexByKey((*(HalSMClass*)out.value).funcs,cobuff)!=-1) {
                    if (ret) {
                        HalSMArray ob=HalSMArray_init();
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMClass*)out.value).funcs,cobuff).value.value)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMClass*)out.value));
                        return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                    }
                    return HalSMLocalFunction_run(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMClass*)out.value).funcs,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                } else if (DictElementIndexByKey((*(HalSMClass*)out.value).vars,cobuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMClass*)out.value).vars,cobuff).value;
                    if (out.type==HalSMVariableType_HalSMLocalFunction) {
                        if (ret) {
                            HalSMArray ob=HalSMArray_init();
                            HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMLocalFunction*)out.value));
                            HalSMArray_add(&ob,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0)));
                            HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMClass*)out.value));
                            return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                        }
                        return HalSMLocalFunction_run(*(HalSMLocalFunction*)out.value,hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                    } else {
                        //Error
                    }
                }
            } else {
                if (DictElementIndexByKey((*(HalSMClass*)out.value).vars,obuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMClass*)out.value).vars,obuff).value;
                } else if (DictElementIndexByKey((*(HalSMClass*)out.value).funcs,obuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMClass*)out.value).funcs,obuff).value;
                } else {
                    //Error
                }
            }
        } else if (out.type==HalSMVariableType_HalSMClassC) {
            if (StringIndexOf(*(char**)obuff.value,"(")!=-1&&StringIndexOf(*(char**)obuff.value,")")!=-1) {
                HalSMVariable cobuff=HalSMArray_get(HalSMArray_split_str(*(char**)cobuff.value,"("),0);
                if (DictElementIndexByKey((*(HalSMClassC*)out.value).funcs,cobuff)!=-1) {
                    if (ret) {
                        HalSMArray ob=HalSMArray_init();
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMClassC*)out.value).funcs,cobuff).value.value)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMClassC*)out.value));
                        return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                    }
                    return HalSMLocalFunction_run(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMClassC*)out.value).funcs,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                } else if (DictElementIndexByKey((*(HalSMClassC*)out.value).vrs,cobuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMClassC*)out.value).vrs,cobuff).value;
                    if (out.type==HalSMVariableType_HalSMLocalFunction) {
                        if (ret) {
                            HalSMArray ob=HalSMArray_init();
                            HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMLocalFunction*)out.value));
                            HalSMArray_add(&ob,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0)));
                            HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMClassC*)out.value));
                            return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                        }
                        return HalSMLocalFunction_run(*(HalSMLocalFunction*)out.value,hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                    } else {
                        //Error
                    }
                }
            } else {
                if (DictElementIndexByKey((*(HalSMClassC*)out.value).vrs,obuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMClassC*)out.value).vrs,obuff).value;
                } else if (DictElementIndexByKey((*(HalSMClassC*)out.value).funcs,obuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMClassC*)out.value).funcs,obuff).value;
                } else {
                    //Error
                }
            }
        } else if (out.type==HalSMVariableType_HalSMRunClassC) {
            if (StringIndexOf(*(char**)obuff.value,"(")!=-1&&StringIndexOf(*(char**)obuff.value,")")!=-1) {
                HalSMVariable cobuff=HalSMArray_get(HalSMArray_split_str(*(char**)cobuff.value,"("),0);
                if (DictElementIndexByKey((*(HalSMRunClassC*)out.value).funcs,cobuff)!=-1) {
                    if (ret) {
                        HalSMArray ob=HalSMArray_init();
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMRunClassC*)out.value).funcs,cobuff).value.value)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0)));
                        HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMRunClassC*)out.value));
                        return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                    }
                    return HalSMLocalFunction_run(*(HalSMLocalFunction*)(DictElementFindByKey((*(HalSMRunClassC*)out.value).funcs,cobuff).value.value),hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                } else if (DictElementIndexByKey((*(HalSMRunClassC*)out.value).vrs,cobuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMRunClassC*)out.value).vrs,cobuff).value;
                    if (out.type==HalSMVariableType_HalSMLocalFunction) {
                        if (ret) {
                            HalSMArray ob=HalSMArray_init();
                            HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMLocalFunction*)out.value));
                            HalSMArray_add(&ob,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0)));
                            HalSMArray_add(&ob,HalSMVariable_FromValue(*(HalSMRunClassC*)out.value));
                            return HalSMVariable_init(&ob,HalSMVariableType_HalSMArray);
                        }
                        return HalSMLocalFunction_run(*(HalSMLocalFunction*)out.value,hsmc,HalSMCompiler_getArgs(hsmc,SubString(*(char**)obuff.value,StringIndexOf(*(char**)cobuff.value,"(")+1,strlen(*(char**)obuff.value)-1),0));
                    } else {
                        //Error
                    }
                }
            } else {
                if (DictElementIndexByKey((*(HalSMRunClassC*)out.value).vrs,obuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMRunClassC*)out.value).vrs,obuff).value;
                } else if (DictElementIndexByKey((*(HalSMRunClassC*)out.value).funcs,obuff)!=-1) {
                    out=DictElementFindByKey((*(HalSMRunClassC*)out.value).funcs,obuff).value;
                } else {
                    //Error
                }
            }
        } else if (out.type==HalSMVariableType_HalSMFloatGet) {
            if (HalSMIsInt(*(char**)obuff.value)) {
                char* outfs=malloc(strlen((*(HalSMFloatGet*)out.value).st)+2+strlen(*(char**)obuff.value));
                strcpy(outfs,(*(HalSMFloatGet*)out.value).st);
                strcat(outfs,".");
                strcat(outfs,*(char**)obuff.value);
                outfs[strlen((*(HalSMFloatGet*)out.value).st)+1+strlen(*(char**)obuff.value)]='\0';
                out=HalSMVariable_FromValue(ParseFloat(outfs));
            } else {
                //Error It's not float
            }
        } else {
            //Error
        }
    }

    return out;
}

HalSMVariable HalSMCompiler_additionVariables(HalSMCompiler hsmc,HalSMVariable v0,HalSMVariable v1)
{
    if (v0.type==HalSMVariableType_str||v1.type==HalSMVariableType_str) {
        return HalSMVariable_init_str(hsmc.calcVars.addStr(v0,v1));
    } else if (v0.type==HalSMVariableType_float||v1.type==HalSMVariableType_float) {
        return HalSMVariable_FromValue(hsmc.calcVars.addFloat(v0,v1));
    } else if (v0.type==HalSMVariableType_int||v1.type==HalSMVariableType_int) {
        return HalSMVariable_FromValue(hsmc.calcVars.addInt(v0,v1));
    }
    return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
}

HalSMVariable HalSMCompiler_subtractionVariables(HalSMCompiler hsmc,HalSMVariable v0,HalSMVariable v1)
{
    if (v0.type==HalSMVariableType_float||v1.type==HalSMVariableType_float&&v0.type!=HalSMVariableType_str&&v1.type!=HalSMVariableType_str) {
        return HalSMVariable_FromValue(hsmc.calcVars.subFloat(v0,v1));
    } else if (v0.type==HalSMVariableType_int) {
        if (v1.type==HalSMVariableType_str) {
            v1=HalSMVariable_FromValue(ParseInt(*(char**)v1.value));
        }
        return HalSMVariable_FromValue(hsmc.calcVars.subInt(v0,v1));
    } else if (v1.type==HalSMVariableType_int) {
        if (v0.type==HalSMVariableType_str) {
            v0=HalSMVariable_FromValue(ParseInt(*(char**)v0.value));
        }
        return HalSMVariable_FromValue(hsmc.calcVars.subInt(v0,v1));
    }
    return HalSMVariable_init_str(hsmc.calcVars.subStr(v0,v1));
}

HalSMVariable HalSMCompiler_multiplyVariables(HalSMCompiler hsmc,HalSMVariable v0,HalSMVariable v1)
{
    if (v0.type==HalSMVariableType_str&&v1.type==HalSMVariableType_str) {
        //Error it is not possible to multiply a string by a string
    } else if (v0.type==HalSMVariableType_str||v1.type==HalSMVariableType_str) {
        return HalSMVariable_init_str(hsmc.calcVars.mulStr(v0,v1));
    } else if (v0.type==HalSMVariableType_float||v1.type==HalSMVariableType_float) {
        return HalSMVariable_FromValue(hsmc.calcVars.mulFloat(v0,v1));
    } else if (v0.type==HalSMVariableType_int||v1.type==HalSMVariableType_int) {
        return HalSMVariable_FromValue(hsmc.calcVars.mulInt(v0,v1));
    }
    return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
}

HalSMVariable HalSMCompiler_divideVariables(HalSMCompiler hsmc,HalSMVariable v0,HalSMVariable v1)
{
    if (v0.type==HalSMVariableType_str&&v1.type==HalSMVariableType_str) {
        return HalSMVariable_init_str(StringReplace(*(char**)v0.value,*(char**)v1.value,""));
    } else if (v0.type==HalSMVariableType_str||v1.type==HalSMVariableType_str) {
        return HalSMVariable_init_str(hsmc.calcVars.divStr(v0,v1));
    } else if (v0.type==HalSMVariableType_float||v1.type==HalSMVariableType_float) {
        return HalSMVariable_FromValue(hsmc.calcVars.divFloat(v0,v1));
    } else if (v0.type==HalSMVariableType_int||v1.type==HalSMVariableType_int) {
        return HalSMVariable_FromValue(hsmc.calcVars.divInt(v0,v1));
    }
    return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
}

HalSMVariable HalSMCompiler_getArgsSetVar(HalSMCompiler hsmc,char* value)
{
    HalSMArray out=HalSMCompiler_getArgs(hsmc,value,1);
    int skip=0;
    int lout=out.size;
    int ou=0;

    HalSMVariable i;
    HalSMVariable v;
    HalSMArray temp;
    HalSMFunctionArray tempf;

    while (ou<lout) {
        if (HalSMArray_get(out,ou).type==HalSMVariableType_HalSMVar) {
            HalSMArray_set(&out,DictElementFindByKey(hsmc.variables,HalSMVariable_init_str((*(HalSMVar*)HalSMArray_get(out,ou).value).name)).value,ou);
        }
        ou++;
    }

    ou=0;

    while (ou<lout) {
        if (skip>0) {
            skip-=1;
            continue;
        }

        i=HalSMArray_get(out,ou);

        if (i.type==HalSMVariableType_HalSMFunctionArray) {
            tempf=*(HalSMFunctionArray*)i.value;
            temp=tempf.args;
            if (tempf.type==HalSMFunctionArrayType_function) {
                v=HalSMCompiler_isRunFunction(hsmc,0,*(char**)HalSMArray_get(temp,0).value);
                if (v.type!=HalSMVariableType_HalSMNull) {
                    HalSMFunctionC m=*(HalSMFunctionC*)HalSMArray_get(*(HalSMArray*)v.value,0).value;
                    HalSMArray args=*(HalSMArray*)HalSMArray_get(*(HalSMArray*)v.value,1).value;
                    HalSMArray_set(&out,HalSMFunctionC_run(hsmc,m,args),ou);
                } else if (StringIndexOf(*(char**)HalSMArray_get(temp,0).value,".")!=-1) {
                    HalSMArray_set(&out,HalSMCompiler_isGet(hsmc,*(char**)HalSMArray_get(temp,0).value,0),ou);
                } else {
                    //Error Function Not Found
                }
            } else if (tempf.type==HalSMFunctionArrayType_array) {
                HalSMArray_set(&out,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,*(char**)HalSMArray_get(temp,0).value,0)),ou);
            }
        } else if (i.type==HalSMVariableType_HalSMMult) {
            HalSMArray_set(&out,HalSMCompiler_multiplyVariables(hsmc,HalSMArray_get(out,ou-1),HalSMArray_get(out,ou+1)),ou-1);
            temp=HalSMArray_slice(out,0,ou);
            HalSMArray_appendArray(&temp,HalSMArray_slice(out,ou+2,out.size));
            out=temp;
            ou-=1;
            lout-=2;
            skip=1;
        } else if (i.type==HalSMVariableType_HalSMDivide) {
            HalSMArray_set(&out,HalSMCompiler_divideVariables(hsmc,HalSMArray_get(out,ou-1),HalSMArray_get(out,ou+1)),ou-1);
            temp=HalSMArray_slice(out,0,ou);
            HalSMArray_appendArray(&temp,HalSMArray_slice(out,ou+2,out.size));
            out=temp;
            ou-=1;
            lout-=2;
            skip=1;
        } else if (i.type==HalSMVariableType_HalSMSetArg) {
            (*(HalSMSetArg*)i.value).value=HalSMArray_get(out,ou+1);
            HalSMArray_set(&out,i,ou);
            HalSMArray_remove(&out,ou+1);
            lout-=1;
        }
        ou+=1;
    }

    skip=0;
    lout=out.size;
    ou=0;

    while (ou<lout) {
        if (skip>0) {
            skip-=1;
            continue;
        }

        i=HalSMArray_get(out,ou);

        if (i.type==HalSMVariableType_HalSMPlus) {
            HalSMArray_set(&out,HalSMCompiler_additionVariables(hsmc,HalSMArray_get(out,ou-1),HalSMArray_get(out,ou+1)),ou-1);
            temp=HalSMArray_slice(out,0,ou);
            HalSMArray_appendArray(&temp,HalSMArray_slice(out,ou+2,out.size));
            out=temp;
            ou-=1;
            lout-=2;
            skip=1;
        } else if (i.type==HalSMVariableType_HalSMMinus) {
            HalSMArray_set(&out,HalSMCompiler_subtractionVariables(hsmc,HalSMArray_get(out,ou-1),HalSMArray_get(out,ou+1)),ou-1);
            temp=HalSMArray_slice(out,0,ou);
            HalSMArray_appendArray(&temp,HalSMArray_slice(out,ou+2,out.size));
            out=temp;
            ou-=1;
            lout-=2;
            skip=1;
        } else if (i.type==HalSMVariableType_HalSMEqual) {
            i=HalSMArray_get(out,ou-1);
            v=HalSMArray_get(out,ou+1);
            if (i.type==HalSMVariableType_HalSMVar||v.type==HalSMVariableType_HalSMVar) {
                skip=1;
            } else {
                HalSMArray_set(&out,HalSMVariable_FromValue(HalSMVariable_Compare(i,v)),ou-1);
                HalSMArray_remove(&out,ou);
                HalSMArray_remove(&out,ou);
                lout-=2;
            }
        } else if (i.type==HalSMVariableType_HalSMNotEqual) {
            i=HalSMArray_get(out,ou-1);
            v=HalSMArray_get(out,ou+1);
            if (i.type==HalSMVariableType_HalSMVar||v.type==HalSMVariableType_HalSMVar) {
                skip=1;
            } else {
                HalSMArray_set(&out,HalSMVariable_FromValue(HalSMVariable_Compare(i,v)==0),ou-1);
                HalSMArray_remove(&out,ou);
                HalSMArray_remove(&out,ou);
                lout-=2;
            }
        } else if (i.type==HalSMVariableType_HalSMMore) {
            i=HalSMArray_get(out,ou-1);
            v=HalSMArray_get(out,ou+1);
            if (i.type==HalSMVariableType_HalSMVar||v.type==HalSMVariableType_HalSMVar) {
                skip=1;
            } else if ((i.type==HalSMVariableType_int||i.type==HalSMVariableType_float)&&(v.type==HalSMVariableType_int||v.type==HalSMVariableType_float)) {
                HalSMArray_set(&out,HalSMVariable_FromValue(HalSMCompiler_isMore(i,v)),ou-1);
                HalSMArray_remove(&out,ou);
                HalSMArray_remove(&out,ou);
                lout-=2;
            } else {
                //Error More (>) cannot without numeric args
            }
        } else if (i.type==HalSMVariableType_HalSMLess) {
            i=HalSMArray_get(out,ou-1);
            v=HalSMArray_get(out,ou+1);
            if (i.type==HalSMVariableType_HalSMVar||v.type==HalSMVariableType_HalSMVar) {
                skip=1;
            } else if ((i.type==HalSMVariableType_int||i.type==HalSMVariableType_float)&&(v.type==HalSMVariableType_int||v.type==HalSMVariableType_float)) {
                HalSMArray_set(&out,HalSMVariable_FromValue(HalSMCompiler_isLess(i,v)),ou-1);
                HalSMArray_remove(&out,ou);
                HalSMArray_remove(&out,ou);
                lout-=2;
            } else {
                //Error Less (<) cannot without numeric args
            }
        }
        ou+=1;
    }
    return HalSMArray_get(out,0);
}

HalSMArray HalSMCompiler_getArgs(HalSMCompiler hsmc,char* l,unsigned char tabs)
{
    HalSMArray out=HalSMArray_init();
    char isS='n';
    unsigned int isF=0;
    HalSMArray o=HalSMArray_init();
    unsigned int ind=0;
    unsigned int isA=0;
    unsigned int lind=strlen(l)-1;
    HalSMVariable isGet;
    unsigned int isNArgs=0;
    unsigned int ignore=0;
    char i;
    HalSMVariable buffo;
    char* buffs;

    for (int indexi=0;indexi<strlen(l);indexi++) {
        i=l[indexi];
        if (ignore>0) {
            ignore--;continue;
        }

        buffs=HalSMArray_chars_to_str(o);
        buffo=HalSMVariable_init_str(buffs);

        if (isNArgs>0&&i=='(') {
            isNArgs++;
            HalSMArray_add(&o,HalSMVariable_FromValue('('));
        } else if (isNArgs>0&&i==')') {
            isNArgs--;
            if (isNArgs==0) {
                HalSMArray_appendArray(&out,HalSMCompiler_getArgs(hsmc,buffs,tabs));
                o=HalSMArray_init();
            } else {HalSMArray_add(&o,HalSMVariable_FromValue(')'));}
        } else if (isNArgs>0) {
            HalSMArray_add(&o,HalSMVariable_FromValue(i));
        } else if (isA>0) {
            HalSMArray_add(&o,HalSMVariable_FromValue(i));
            if (i==']') {
                isA--;
                if (isA==0) {
                    HalSMFunctionArray tempfa={.type=HalSMFunctionArrayType_array,.args=HalSMArray_init_with_elements((HalSMVariable[]){HalSMVariable_init_str(SubString(buffs,0,o.size-1))},1)};
                    HalSMArray_add(&out,HalSMVariable_FromValue(tempfa));
                    o=HalSMArray_init();
                }
            } else if (i=='[') {isA++;}
        } else if (i=='['&&o.size==0) {isA++;}
        else if (isF>0) {
            HalSMArray_add(&o,HalSMVariable_FromValue(i));
            if (i==')') {
                isF--;
                if (isF==0) {
                    if (StringIndexOf(buffs,".")!=-1) {
                        HalSMArray_add(&out,HalSMCompiler_isGet(hsmc,buffs,0));
                    } else {
                        if (tabs) {
                            HalSMFunctionArray tempfa={.type=HalSMFunctionArrayType_array,.args=HalSMArray_init_with_elements((HalSMVariable[]){buffo},1)};
                            HalSMArray_add(&out,HalSMVariable_FromValue(tempfa));
                        } else {
                            HalSMArray fc=*(HalSMArray*)HalSMCompiler_isRunFunction(hsmc,0,HalSMArray_chars_to_str(o)).value;
                            HalSMArray args=*(HalSMArray*)HalSMArray_get(fc,1).value;
                            HalSMArray_add(&out,HalSMFunctionC_run(hsmc,*(HalSMFunctionC*)HalSMArray_get(fc,0).value,args));
                        }
                    }
                    o=HalSMArray_init();
                }
            } else if (i=='(') {isF++;}
        } else if (isS!='n') {
            if (i==isS) {
                isS='n';
                HalSMArray_add(&out,buffo);
                o=HalSMArray_init();
            } else {HalSMArray_add(&o,HalSMVariable_FromValue(i));}
        } else if (i=='"'||i=='\'') {
            isS=i;
            if (l[ind+1]==')') {
                HalSMArray_add(&out,buffo);
                o=HalSMArray_init();
            }
        } else if (i=='(') {
            if (isF==0) {
                if (o.size==0) {isNArgs++;}
                else {
                    isF++;
                    HalSMArray_add(&o,HalSMVariable_FromValue(i));
                }
            } else {
                isF++;
                HalSMArray_add(&o,HalSMVariable_FromValue(i));
            }
        } else if (i==' ') {

        } else if (i==',') {
            if (o.size!=0) {
                if (StringCompare(buffs,"true")) {HalSMArray_add(&out,HalSMVariable_FromValue((unsigned char)1));}
                else if (StringCompare(buffs,"false")) {HalSMArray_add(&out,HalSMVariable_FromValue((unsigned char)0));}
                else if (DictElementIndexByKey(hsmc.variables,buffo)!=-1) {
                    if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                    else {HalSMArray_add(&out,DictElementFindByKey(hsmc.variables,buffo).value);}
                } else if (DictElementIndexByKey(hsmc.localFunctions,buffo)!=-1) {HalSMArray_add(&out,DictElementFindByKey(hsmc.localFunctions,buffo).value);}
                else if (tabs){HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                else {
                    isGet=HalSMCompiler_isGet(hsmc,buffs,0);
                    if (HalSMIsInt(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseInt(buffs)));}
                    else if (HalSMIsFloat(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseFloat(buffs)));}
                    else if (isGet.type!=HalSMVariableType_HalSMNull) {HalSMArray_add(&out,isGet);}
                    else {/*Error Variable Not Found*/}
                }
                o=HalSMArray_init();
            }
        } else if (i=='+') {
            if (o.size!=0) {
                if (DictElementIndexByKey(hsmc.variables,buffo)!=-1) {
                    if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                    else {HalSMArray_add(&out,DictElementFindByKey(hsmc.variables,buffo).value);}
                } else {
                    isGet=HalSMCompiler_isGet(hsmc,buffs,0);
                    if (HalSMIsInt(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseInt(buffs)));}
                    else if (HalSMIsFloat(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseFloat(buffs)));}
                    else if (isGet.type!=HalSMVariableType_HalSMNull) {HalSMArray_add(&out,isGet);}
                    else if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                    else {/*Error Variable Not Found*/}
                }
                o=HalSMArray_init();
            }
            HalSMArray_add(&out,HalSMVariable_init(&plus,HalSMVariableType_HalSMPlus));
        } else if (i=='-') {
            if (o.size!=0) {
                if (DictElementIndexByKey(hsmc.variables,buffo)!=-1) {
                    if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                    else {HalSMArray_add(&out,DictElementFindByKey(hsmc.variables,buffo).value);}
                } else {
                    isGet=HalSMCompiler_isGet(hsmc,buffs,0);
                    if (HalSMIsInt(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseInt(buffs)));}
                    else if (HalSMIsFloat(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseFloat(buffs)));}
                    else if (isGet.type!=HalSMVariableType_HalSMNull) {HalSMArray_add(&out,isGet);}
                    else if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                    else {/*Error Variable Not Found*/}
                }
                o=HalSMArray_init();
            }
            HalSMArray_add(&out,HalSMVariable_init(&minus,HalSMVariableType_HalSMMinus));
        } else if (i=='*') {
            if (o.size!=0) {
                if (DictElementIndexByKey(hsmc.variables,buffo)!=-1) {
                    if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                    else {HalSMArray_add(&out,DictElementFindByKey(hsmc.variables,buffo).value);}
                } else {
                    isGet=HalSMCompiler_isGet(hsmc,buffs,0);
                    if (HalSMIsInt(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseInt(buffs)));}
                    else if (HalSMIsFloat(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseFloat(buffs)));}
                    else if (isGet.type!=HalSMVariableType_HalSMNull) {HalSMArray_add(&out,isGet);}
                    else if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                    else {/*Error Variable Not Found*/}
                }
                o=HalSMArray_init();
            }
            HalSMArray_add(&out,HalSMVariable_init(&mult,HalSMVariableType_HalSMMult));
        } else if (i=='/') {
            if (o.size!=0) {
                if (DictElementIndexByKey(hsmc.variables,buffo)!=-1) {
                    if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                    else {HalSMArray_add(&out,DictElementFindByKey(hsmc.variables,buffo).value);}
                } else {
                    isGet=HalSMCompiler_isGet(hsmc,buffs,0);
                    if (HalSMIsInt(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseInt(buffs)));}
                    else if (HalSMIsFloat(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseFloat(buffs)));}
                    else if (isGet.type!=HalSMVariableType_HalSMNull) {HalSMArray_add(&out,isGet);}
                    else if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                    else {/*Error Variable Not Found*/}
                }
                o=HalSMArray_init();
            }
            HalSMArray_add(&out,HalSMVariable_init(&divide,HalSMVariableType_HalSMDivide));
        } else if (i=='=') {
            if (ind+1<=lind&&l[ind+1]=='=') {
                if (o.size!=0) {
                    if (DictElementIndexByKey(hsmc.variables,buffo)!=-1) {
                        if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                        else {HalSMArray_add(&out,DictElementFindByKey(hsmc.variables,buffo).value);}
                    } else {
                        isGet=HalSMCompiler_isGet(hsmc,buffs,0);
                        if (HalSMIsInt(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseInt(buffs)));}
                        else if (HalSMIsFloat(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseFloat(buffs)));}
                        else if (isGet.type!=HalSMVariableType_HalSMNull) {HalSMArray_add(&out,isGet);}
                        else if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                        else {/*Error Variable Not Found*/}
                    }
                    o=HalSMArray_init();
                    HalSMArray_add(&out,HalSMVariable_init(&equal,HalSMVariableType_HalSMEqual));
                } else {
                    //Error Equal (==) cannot without args
                }
                ignore=1;
            } else {
                if (o.size!=0) {
                    HalSMArray_add(&out,HalSMVariable_FromValue(HalSMSetArg_init(buffs)));
                    o=HalSMArray_init();
                } else {HalSMArray_add(&o,HalSMVariable_FromValue('='));}
            }
        } else if (i=='!') {
            if (ind+1<=lind&&l[ind+1]=='=') {
                if (o.size!=0) {
                    if (DictElementIndexByKey(hsmc.variables,buffo)) {
                        if (tabs){HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                        else {HalSMArray_add(&out,DictElementFindByKey(hsmc.variables,buffo).value);}
                    } else {
                        isGet=HalSMCompiler_isGet(hsmc,buffs,0);
                        if (HalSMIsInt(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseInt(buffs)));}
                        else if (HalSMIsFloat(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseFloat(buffs)));}
                        else if (isGet.type!=HalSMVariableType_HalSMNull) {HalSMArray_add(&out,isGet);}
                        else if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                        else {/*Error Variable Not Found*/}
                    }
                    HalSMArray_add(&out,HalSMVariable_init(&notequal,HalSMVariableType_HalSMNotEqual));
                    o=HalSMArray_init();
                } else {
                    //Error Not Equal (!=) cannot without args
                }
                ignore=1;
            }
        } else if (i=='>') {
            if (o.size!=0) {
                if (DictElementIndexByKey(hsmc.variables,buffo)!=-1) {
                    if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                    else {HalSMArray_add(&out,DictElementFindByKey(hsmc.variables,buffo).value);}
                } else {
                    isGet=HalSMCompiler_isGet(hsmc,buffs,0);
                    if (HalSMIsInt(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseInt(buffs)));}
                    else if (HalSMIsFloat(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseFloat(buffs)));}
                    else if (isGet.type!=HalSMVariableType_HalSMNull) {HalSMArray_add(&out,isGet);}
                    else if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                    else {/*Error Variable Not Found*/}
                }
                HalSMArray_add(&out,HalSMVariable_init(&more,HalSMVariableType_HalSMMore));
                o=HalSMArray_init();
            } else {
                //Error More (>) cannot without args
            }
        }  else if (i=='<') {
            if (o.size!=0) {
                if (DictElementIndexByKey(hsmc.variables,buffo)!=-1) {
                    if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                    else {HalSMArray_add(&out,DictElementFindByKey(hsmc.variables,buffo).value);}
                } else {
                    isGet=HalSMCompiler_isGet(hsmc,buffs,0);
                    if (HalSMIsInt(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseInt(buffs)));}
                    else if (HalSMIsFloat(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseFloat(buffs)));}
                    else if (isGet.type!=HalSMVariableType_HalSMNull) {HalSMArray_add(&out,isGet);}
                    else if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
                    else {/*Error Variable Not Found*/}
                }
                HalSMArray_add(&out,HalSMVariable_init(&less,HalSMVariableType_HalSMLess));
                o=HalSMArray_init();
            } else {
                //Error Less (<) cannot without args
            }
        } else {HalSMArray_add(&o,HalSMVariable_FromValue(i));}
        ind++;
    }

    if (o.size!=0) {
        buffs=HalSMArray_chars_to_str(o);
        buffo=HalSMVariable_init_str(buffs);
        if (StringCompare(buffs,"true")) {HalSMArray_add(&out,HalSMVariable_FromValue((unsigned char)1));}
        else if (StringCompare(buffs,"false")) {HalSMArray_add(&out,HalSMVariable_FromValue((unsigned char)0));}
        else if (DictElementIndexByKey(hsmc.variables,buffo)!=-1) {
            if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
            else {HalSMArray_add(&out,DictElementFindByKey(hsmc.variables,buffo).value);}
        } else if (DictElementIndexByKey(hsmc.localFunctions,buffo)!=-1) {HalSMArray_add(&out,DictElementFindByKey(hsmc.localFunctions,buffo).value);}
        else {
            isGet=HalSMCompiler_isGet(hsmc,buffs,0);
            if (HalSMIsInt(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseInt(buffs)));}
            else if (HalSMIsFloat(buffs)) {HalSMArray_add(&out,HalSMVariable_FromValue(ParseFloat(buffs)));}
            else if (isGet.type!=HalSMVariableType_HalSMNull) {HalSMArray_add(&out,isGet);}
            else if (tabs) {HalSMArray_add(&out,HalSMVariable_FromValue(HalSMVar_init(buffs)));}
            else {/*Error Variable Not Found*/}
        }
    }

    unsigned int skip=0;
    unsigned int lout=out.size;
    unsigned int ou=0;

    HalSMVariable iv;
    HalSMVariable v;
    HalSMArray temp;
    HalSMFunctionArray tempf;

    while (ou<lout) {
        if (skip>0) {skip--;continue;}

        iv=HalSMArray_get(out,ou);

        if (iv.type==HalSMVariableType_HalSMFunctionArray) {
            tempf=*(HalSMFunctionArray*)iv.value;
            temp=tempf.args;
            if (tempf.type==HalSMFunctionArrayType_function) {
                if (tabs) {
                    HalSMArray arr=*(HalSMArray*)HalSMCompiler_isRunFunction(hsmc,1,*(char**)HalSMArray_get(temp,0).value).value;
                    HalSMArray_set(&arr,HalSMVariable_FromValue(HalSMRunFunc_init(*(HalSMFunctionC*)HalSMArray_get(arr,0).value,*(HalSMArray*)HalSMArray_get(arr,1).value)),0);
                    HalSMArray_set(&out,HalSMVariable_FromValue(arr),ou);
                } else {
                    v=HalSMCompiler_isRunFunction(hsmc,0,*(char**)HalSMArray_get(temp,0).value);
                    if (v.type!=HalSMVariableType_HalSMNull) {
                        HalSMFunctionC m=*(HalSMFunctionC*)HalSMArray_get(*(HalSMArray*)v.value,0).value;
                        HalSMArray args=*(HalSMArray*)HalSMArray_get(*(HalSMArray*)v.value,1).value;
                        HalSMArray_set(&out,HalSMFunctionC_run(hsmc,m,args),ou);
                    } else if (StringIndexOf(*(char**)HalSMArray_get(temp,0).value,".")!=-1) {
                        HalSMArray_set(&out,HalSMCompiler_isGet(hsmc,*(char**)HalSMArray_get(temp,0).value,0),ou);
                    } else {
                        //Error Function Not Found
                    }
                }
            } else if (tempf.type==HalSMFunctionArrayType_array) {
                HalSMArray_set(&out,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,*(char**)HalSMArray_get(temp,0).value,0)),ou);
            }
        } else if (iv.type==HalSMVariableType_HalSMMult) {
            if (tabs){skip=1;}
            else {
                HalSMArray_set(&out,HalSMCompiler_multiplyVariables(hsmc,HalSMArray_get(out,ou-1),HalSMArray_get(out,ou+1)),ou-1);
                temp=HalSMArray_slice(out,0,ou);
                HalSMArray_appendArray(&temp,HalSMArray_slice(out,ou+2,out.size));
                out=temp;
                ou--;
                lout-=2;
                skip=1;
            }
        } else if (iv.type==HalSMVariableType_HalSMDivide) {
            if (tabs){skip=1;}
            else {
                HalSMArray_set(&out,HalSMCompiler_divideVariables(hsmc,HalSMArray_get(out,ou-1),HalSMArray_get(out,ou+1)),ou-1);
                temp=HalSMArray_slice(out,0,ou);
                HalSMArray_appendArray(&temp,HalSMArray_slice(out,ou+2,out.size));
                out=temp;
                ou--;
                lout-=2;
                skip=1;
            }
        } else if (iv.type==HalSMVariableType_HalSMSetArg) {
            (*(HalSMSetArg*)iv.value).value=HalSMArray_get(out,ou+1);
            HalSMArray_set(&out,iv,ou);
            HalSMArray_remove(&out,ou+1);
            lout--;
        }
        ou++;
    }

    skip=0;
    lout=out.size;
    ou=0;

    while (ou<lout) {
        if (skip>0){skip--;continue;}

        iv=HalSMArray_get(out,ou);

        if (iv.type==HalSMVariableType_HalSMPlus) {
            if (tabs){skip=1;}
            else {
                HalSMArray_set(&out,HalSMCompiler_additionVariables(hsmc,HalSMArray_get(out,ou-1),HalSMArray_get(out,ou+1)),ou-1);
                temp=HalSMArray_slice(out,0,ou);
                HalSMArray_appendArray(&temp,HalSMArray_slice(out,ou+2,out.size));
                out=temp;
                ou--;
                lout-=2;
                skip=1;
            }
        } else if (iv.type==HalSMVariableType_HalSMMinus) {
            if (tabs){skip=1;}
            else {
                HalSMArray_set(&out,HalSMCompiler_subtractionVariables(hsmc,HalSMArray_get(out,ou-1),HalSMArray_get(out,ou+1)),ou-1);
                temp=HalSMArray_slice(out,0,ou);
                HalSMArray_appendArray(&temp,HalSMArray_slice(out,ou+2,out.size));
                out=temp;
                ou--;
                lout-=2;
                skip=1;
            }
        } else if (iv.type==HalSMVariableType_HalSMEqual) {
            if (tabs){skip=1;}
            else {
                iv=HalSMArray_get(out,ou-1);
                v=HalSMArray_get(out,ou+1);
                if (iv.type==HalSMVariableType_HalSMVar||v.type==HalSMVariableType_HalSMVar){skip=1;}
                else {
                    HalSMArray_set(&out,HalSMVariable_FromValue(HalSMVariable_Compare(iv,v)),ou-1);
                    HalSMArray_remove(&out,ou);
                    HalSMArray_remove(&out,ou);
                    lout-=2;
                }
            }
        } else if (iv.type==HalSMVariableType_HalSMNotEqual) {
            if (tabs){skip=1;}
            else {
                iv=HalSMArray_get(out,ou-1);
                v=HalSMArray_get(out,ou+1);
                if (iv.type==HalSMVariableType_HalSMVar||v.type==HalSMVariableType_HalSMVar){skip=1;}
                else {
                    HalSMArray_set(&out,HalSMVariable_FromValue((unsigned char)(HalSMVariable_Compare(iv,v)==0)),ou-1);
                    HalSMArray_remove(&out,ou);
                    HalSMArray_remove(&out,ou);
                    lout-=2;
                }
            }
        } else if (iv.type==HalSMVariableType_HalSMMore) {
            if (tabs){skip=1;}
            else {
                iv=HalSMArray_get(out,ou-1);
                v=HalSMArray_get(out,ou+1);
                if (iv.type==HalSMVariableType_HalSMVar||v.type==HalSMVariableType_HalSMVar){skip=1;}
                else if ((iv.type==HalSMVariableType_int||iv.type==HalSMVariableType_float)&&(v.type==HalSMVariableType_int||v.type==HalSMVariableType_float)) {
                    HalSMArray_set(&out,HalSMVariable_FromValue(HalSMCompiler_isMore(iv,v)),ou-1);
                    HalSMArray_remove(&out,ou);
                    HalSMArray_remove(&out,ou);
                    lout-=2;
                } else {
                    //Error More (>) cannot without numeric args
                }
            }
        } else if (iv.type==HalSMVariableType_HalSMLess) {
            if (tabs){skip=1;}
            else {
                iv=HalSMArray_get(out,ou-1);
                v=HalSMArray_get(out,ou+1);
                if (iv.type==HalSMVariableType_HalSMVar||v.type==HalSMVariableType_HalSMVar){skip=1;}
                else if ((iv.type==HalSMVariableType_int||iv.type==HalSMVariableType_float)&&(v.type==HalSMVariableType_int||v.type==HalSMVariableType_float)) {
                    HalSMArray_set(&out,HalSMVariable_FromValue(HalSMCompiler_isLess(iv,v)),ou-1);
                    HalSMArray_remove(&out,ou);
                    HalSMArray_remove(&out,ou);
                    lout-=2;
                } else {
                    //Error More (>) cannot without numeric args
                }
            }
        }
        ou++;
    }
    return out;
}

HalSMVariable HalSMCompiler_isRunFunction(HalSMCompiler hsmc,unsigned char tabs,char* l)
{
    if (StringEndsWith(l,")")) {
        HalSMArray array=HalSMArray_init();
        HalSMVariable buffl=HalSMArray_get(HalSMArray_split_str(SubString(l,0,strlen(l)-1),"("),0);
        HalSMArray argus=HalSMArray_split_str(SubString(l,0,strlen(l)-1),"(");
        char* args=HalSMArray_join_str(HalSMArray_slice(argus,1,argus.size),"(");
        HalSMFunctionArray out;
        out.type=HalSMFunctionArrayType_function;
        if (DictElementIndexByKey(hsmc.functions,buffl)!=-1) {
            HalSMArray_add(&array,DictElementFindByKey(hsmc.functions,buffl).value);
            HalSMArray_add(&array,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,args,tabs)));
            free(args);
            out.args=array;
            return HalSMVariable_FromValue(out);
        } else if (DictElementIndexByKey(hsmc.localFunctions,buffl)!=-1) {
            HalSMArray_add(&array,DictElementFindByKey(hsmc.localFunctions,buffl).value);
            HalSMArray_add(&array,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,args,tabs)));
            free(args);
            out.args=array;
            return HalSMVariable_FromValue(out);
        } else if (DictElementIndexByKey(hsmc.classes,buffl)!=-1) {
            HalSMArray_add(&array,DictElementFindByKey(hsmc.classes,buffl).value);
            HalSMArray_add(&array,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,args,tabs)));
            free(args);
            out.args=array;
            return HalSMVariable_FromValue(out);
        } else if (DictElementIndexByKey(hsmc.modules,buffl)!=-1) {
            if (DictElementFindByKey(hsmc.modules,buffl).value.type==HalSMVariableType_HalSMModule) {
                HalSMArray_add(&array,DictElementFindByKey((*(HalSMModule*)DictElementFindByKey(hsmc.modules,buffl).value.value).lfuncs,HalSMVariable_init_str("__init__")).value);
            } else {
                HalSMArray_add(&array,DictElementFindByKey((*(HalSMCModule*)DictElementFindByKey(hsmc.modules,buffl).value.value).lfuncs,HalSMVariable_init_str("__init__")).value);
            }
            HalSMArray_add(&array,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,args,tabs)));
            free(args);
            out.args=array;
            return HalSMVariable_FromValue(out);
        } else if (DictElementIndexByKey(hsmc.variables,buffl)!=-1) {
            if (DictElementFindByKey(hsmc.variables,buffl).value.type==HalSMVariableType_HalSMFunctionC||DictElementFindByKey(hsmc.variables,buffl).value.type==HalSMVariableType_HalSMLocalFunction) {
                HalSMArray_add(&array,DictElementFindByKey(hsmc.variables,buffl).value);
                HalSMArray_add(&array,HalSMVariable_FromValue(HalSMCompiler_getArgs(hsmc,args,tabs)));
                free(args);
                out.args=array;
                return HalSMVariable_FromValue(out);
            } else {
                //Error Variable is not function
            }
        }
        free(args);
        HalSMVariable isGet=HalSMCompiler_isGet(hsmc,l,1);
        if (isGet.type!=HalSMVariableType_HalSMNull) {
            return isGet;
        }
    }
    return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
}

unsigned char HalSMCompiler_isMore(HalSMVariable a,HalSMVariable b)
{
    if (a.type==HalSMVariableType_int&&b.type==HalSMVariableType_int){return *(int*)a.value>*(int*)b.value;}
    else if (a.type==HalSMVariableType_float&&b.type==HalSMVariableType_float){return *(float*)a.value>*(float*)b.value;}
    else if (a.type==HalSMVariableType_int&&b.type==HalSMVariableType_float){return *(int*)a.value>*(float*)b.value;}
    else if (a.type==HalSMVariableType_float&&b.type==HalSMVariableType_int){return *(float*)a.value>*(int*)b.value;}
    return 0;
}

unsigned char HalSMCompiler_isLess(HalSMVariable a,HalSMVariable b)
{
    if (a.type==HalSMVariableType_int&&b.type==HalSMVariableType_int){return *(int*)a.value<*(int*)b.value;}
    else if (a.type==HalSMVariableType_float&&b.type==HalSMVariableType_float){return *(float*)a.value<*(float*)b.value;}
    else if (a.type==HalSMVariableType_int&&b.type==HalSMVariableType_float){return *(int*)a.value<*(float*)b.value;}
    else if (a.type==HalSMVariableType_float&&b.type==HalSMVariableType_int){return *(float*)a.value<*(int*)b.value;}
    return 0;
}

HalSMVariable HalSMCompiler_getNameFunction(HalSMCompiler hsmc,char* l)
{
    HalSMArray name=HalSMArray_init();
    char s;

    for (int i=0;i<strlen(l);i++) {
        s=l[i];
        if (s=='(') {
            HalSMArray out=HalSMArray_init();
            HalSMArray_add(&out,HalSMVariable_init_str(HalSMArray_chars_to_str(name)));
            HalSMArray_add(&out,HalSMVariable_init_str(SubString(l,i+1,strlen(l)-2)));
            return HalSMVariable_FromValue(out);
        }
        HalSMArray_add(&name,HalSMVariable_FromValue(s));
    }

    //Error Is Not Function
    return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
}

HalSMVariable HalSMCompiler_isSetVar(char* l)
{
    char i;
    HalSMArray n=HalSMArray_init();
    if (StringStartsWith(l,"def ")){return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
    for (int ind=0;ind<strlen(l);ind++) {
        i=l[ind];
        if (i=='"'||i=='\''||i=='('||i==')') {return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
        else if (i=='='&&n.size!=0) {
            HalSMArray out=HalSMArray_init();
            HalSMArray_add(&out,HalSMVariable_init_str(HalSMArray_chars_to_str(n)));
            HalSMArray_add(&out,HalSMVariable_init_str(SubString(l,ind+1,strlen(l))));
            return HalSMVariable_FromValue(out);
        }
        HalSMArray_add(&n,HalSMVariable_FromValue(i));
    }
    return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
}

HalSMArray HalSMCompiler_getTabs(char* l)
{
    int i=0;
    while (1) {
        if (StringStartsWith(l,"    ")) {
            i++;
            l=SubString(l,4,strlen(l));
        } else {break;}
    }
    HalSMArray out=HalSMArray_init();
    HalSMArray_add(&out,HalSMVariable_FromValue(i));
    HalSMArray_add(&out,HalSMVariable_init_str(StringReplace(l,"\r","")));
    return out;
}

unsigned char HalSMCompiler_isNull(char* text)
{
    char i;
    for (int ind=0;ind<strlen(text);ind++) {
        i=text[ind];
        if (i!=' '){return 0;}
    }
    return 1;
}

HalSMArray HalSMCompiler_compile(HalSMCompiler hsmc,char* text)
{
    hsmc.line=1;
    hsmc.variables=DictInit();
    hsmc.modules=DictInit();
    hsmc.classes=DictInit();
    hsmc.localFunctions=DictInit();
    unsigned char isFunc=0;
    unsigned char isClass=0;
    HalSMVariable func=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    HalSMVariable cls=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    HalSMVariable clelem=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    HalSMVariable clif=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    HalSMArray tabs=HalSMArray_init();
    HalSMVariable isRunFunc=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    HalSMVariable isSetVar;
    char* tabsS;
    int tabsC;
    unsigned char isNull=0;
    HalSMLocalFunction f;
    HalSMVariable fc=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    HalSMArray nameFunc;
    HalSMArray spliti;
    char* joinSpliti;
    HalSMArray b;
    HalSMFunctionArray resRunFunc;
    HalSMVariable err;
    char* l;
    HalSMArray allLines=HalSMCompiler_getLines(text);
    HalSMArray temparray;

    for (int indexl=0;indexl<allLines.size;indexl++) {
        l=*(char**)HalSMArray_get(allLines,indexl).value;
        tabs=HalSMCompiler_getTabs(l);
        tabsS=*(char**)HalSMArray_get(tabs,1).value;
        tabsC=*(int*)HalSMArray_get(tabs,0).value;

        if (clelem.type!=HalSMVariableType_HalSMNull) {
            if (isClass&&isFunc) {tabsC=tabsC-2;}
            else if (isFunc) {tabsC=tabsC-1;}
        }

        if (!isFunc&&!isClass&&tabsC==0&&clelem.type!=HalSMVariableType_HalSMNull) {
            if (!isNull&&(StringStartsWith(tabsS,"if ")||StringStartsWith(tabsS,"while "))) {
                if (clif.type!=HalSMVariableType_HalSMNull){HalSMArray_add((HalSMArray*)clif.value,clelem);}
                clelem=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
            } else if (!isNull&&(StringStartsWith(tabsS,"elif ")||StringStartsWith(tabsS,"else"))) {
                if (clif.type==HalSMVariableType_HalSMNull) {/*Error Elif or Else cannot without If*/}
                HalSMArray_add((HalSMArray*)clif.value,clelem);
                clelem=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
            } else if (!isNull) {
                if (clif.type!=HalSMVariableType_HalSMNull) {
                    if (!isFunc&&!isClass) {
                        if (clelem.type!=HalSMVariableType_HalSMNull) {HalSMArray_add((HalSMArray*)clif.value,clelem);}
                        HalSMVariable r=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
                        HalSMVariable ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
                        HalSMCLElement d;
                        for (int indexclem=0;indexclem<(*(HalSMArray*)clif.value).size;indexclem++) {
                            d=*(HalSMCLElement*)(*(HalSMArray*)clif.value).arr[indexclem].value;
                            if (d.type==HalSMCLElementType_elif) {
                                if (ifr.type==HalSMVariableType_HalSMNull) {/*Error Elif cannot without If*/}
                                if (*(unsigned char*)ifr.value==0) {
                                    err=d.start(&d,&hsmc);
                                    if (err.type==HalSMVariableType_HalSMError) {/*Error*/}
                                    ifr=err;
                                }
                            } else if (d.type==HalSMCLElementType_else) {
                                if (ifr.type==HalSMVariableType_HalSMNull) {/*Error Else cannot without If*/}
                                if (*(unsigned char*)ifr.value==0) {
                                    err=d.start(&d,&hsmc);
                                    if (err.type==HalSMVariableType_HalSMError) {/*Error*/}
                                    ifr=err;
                                } else {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
                            } else if (d.type==HalSMCLElementType_if) {
                                err=d.start(&d,&hsmc);
                                if (err.type==HalSMVariableType_HalSMError) {/*Error*/}
                                ifr=err;
                            }
                        }
                        if (r.type==HalSMVariableType_HalSMError) {/*Error*/}
                    } else if (isFunc&&!isClass) {HalSMArray_add(&(*(HalSMLocalFunction*)func.value).func,clif);}
                } else if (clelem.type!=HalSMVariableType_HalSMNull) {
                    HalSMCLElement d=*(HalSMCLElement*)clelem.value;
                    err=d.start((HalSMCLElement*)clelem.value,&hsmc);
                    if (err.type==HalSMVariableType_HalSMError) {
                        //Error
                    }
                }
                clif=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
                clelem=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
            }
        }

        isSetVar=HalSMCompiler_isSetVar(tabsS);
        isRunFunc=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
        if (isSetVar.type==HalSMVariableType_HalSMNull) {isRunFunc=HalSMCompiler_isRunFunction(hsmc,tabsC>0,tabsS);}
        isNull=HalSMCompiler_isNull(tabsS);

        if (isClass) {
            if (tabsC==0&&!isNull) {
                isClass=0;
                if (isFunc) {PutDictElementToDict(&((*(HalSMClass*)fc.value).funcs),DictElementInit(HalSMVariable_init_str((*(HalSMLocalFunction*)func.value).name),func));}
                isFunc=0;
                if (clelem.type!=HalSMVariableType_HalSMNull) {HalSMArray_add(&((*(HalSMLocalFunction*)func.value).func),func);}
                clelem=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
                func=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
                cls=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
            }
            if (tabsC==1&&!isNull) {
                if (isFunc) {
                    PutDictElementToDict(&((*(HalSMClass*)fc.value).funcs),DictElementInit(HalSMVariable_init_str((*(HalSMLocalFunction*)func.value).name),func));
                    isFunc=0;
                    func=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
                }
                if (StringStartsWith(tabsS,"def ")) {
                    spliti=HalSMArray_split_str(tabsS,":");
                    spliti=HalSMArray_slice(spliti,0,spliti.size-1);
                    joinSpliti=HalSMArray_join_str(spliti,":");
                    spliti=HalSMArray_split_str(joinSpliti,"def ");
                    spliti=HalSMArray_slice(spliti,1,spliti.size);
                    joinSpliti=HalSMArray_join_str(spliti,"def ");
                    nameFunc=*(HalSMArray*)HalSMCompiler_getNameFunction(hsmc,joinSpliti).value;
                    f=HalSMLocalFunction_init(*(char**)nameFunc.arr[0].value,*(char**)nameFunc.arr[1].value,hsmc.variables);
                    PutDictElementToDict(&((*(HalSMClass*)cls.value).funcs),DictElementInit(HalSMVariable_init_str(f.name),HalSMVariable_FromValue(f)));
                    func=HalSMVariable_FromValue(f);
                    isFunc=1;
                }
            }
            if (isFunc) {
                if (isRunFunc.type!=HalSMVariableType_HalSMNull) {
                    resRunFunc=*(HalSMFunctionArray*)isRunFunc.value;
                    HalSMRunFunc ret=HalSMRunFunc_init(*(HalSMFunctionC*)resRunFunc.args.arr[0].value,*(HalSMArray*)resRunFunc.args.arr[1].value);
                    if (clelem.type!=HalSMVariableType_HalSMNull) {
                        b=(*(HalSMCLElement*)clelem.value).func;
                        while (1) {
                            if (b.size==0||b.arr[b.size-1].type!=HalSMVariableType_HalSMCLElement) {break;}
                            b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                        }
                        HalSMArray_add(&b,HalSMVariable_FromValue(ret));
                    } else {HalSMArray_add(&((*(HalSMLocalFunction*)func.value).func),HalSMVariable_FromValue(ret));}
                } else if (StringStartsWith(tabsS,"for ")) {
                    spliti=HalSMArray_split_str(tabsS," ");
                    char* vr=*(char**)spliti.arr[1].value;
                    joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,2,spliti.size)," ");
                    spliti=HalSMArray_split_str(joinSpliti,"in ");
                    joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size),"in ");
                    spliti=HalSMArray_split_str(joinSpliti,":");
                    if (spliti.size==1) {joinSpliti=*(char**)spliti.arr[0].value;}
                    else {joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,0,spliti.size-1),":");}
                    HalSMVariable args=HalSMCompiler_getArgs(hsmc,joinSpliti,0).arr[0];
                    if (args.type==HalSMVariableType_str) {
                        HalSMArray fdf=HalSMArray_init();
                        for (int indexc=0;indexc<strlen(*(char**)args.value);indexc++) {HalSMArray_add(&fdf,HalSMVariable_FromValue((*(char**)args.value)[indexc]));}
                        args=HalSMVariable_FromValue(fdf);
                    } else if (args.type==HalSMVariableType_HalSMArray) {
                        if ((*(HalSMArray*)args.value).arr[0].type==HalSMVariableType_HalSMArray) {args=(*(HalSMArray*)args.value).arr[0];}
                    }
                    if (clelem.type==HalSMVariableType_HalSMNull) {
                        clelem=HalSMVariable_FromValue(HalSMFor_init(HalSMVariable_init_str(vr),*(HalSMArray*)args.value));
                    } else {
                        b=(*(HalSMCLElement*)clelem.value).func;
                        while (1) {
                            //Remake
                            if (b.size==0||b.arr[b.size-1].type!=HalSMVariableType_HalSMCLElement){break;}
                            b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                        }
                        HalSMArray_add(&b,HalSMVariable_FromValue(HalSMFor_init(HalSMVariable_FromValue(vr),*(HalSMArray*)args.value)));
                    }
                } else if (StringStartsWith(tabsS,"if ")) {
                    spliti=HalSMArray_split_str(tabsS," ");
                    joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size)," ");
                    spliti=HalSMArray_split_str(joinSpliti,":");
                    if (spliti.size==1) {joinSpliti=*(char**)spliti.arr[0].value;}
                    else {joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,0,spliti.size-1),":");}
                    HalSMArray args=HalSMCompiler_getArgs(hsmc,joinSpliti,clelem.type!=HalSMVariableType_HalSMNull);
                    if (clelem.type==HalSMVariableType_HalSMNull) {
                        clelem=HalSMVariable_FromValue(HalSMIf_init(args));
                        clif=HalSMVariable_FromValue(HalSMArray_init());
                    } else {
                        //Remake
                        b=(*(HalSMCLElement*)clelem.value).func;
                        for (unsigned int i=0;i<tabsC-1;i++) {
                            b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                        }
                        HalSMArray_add(&b,HalSMVariable_FromValue(HalSMIf_init(args)));
                    }
                } else if (StringStartsWith(tabsS,"elif ")) {
                    spliti=HalSMArray_split_str(tabsS," ");
                    joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size)," ");
                    spliti=HalSMArray_split_str(joinSpliti,":");
                    if (spliti.size==1) {joinSpliti=*(char**)spliti.arr[1].value;}
                    else {joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,0,spliti.size-1),":");}
                    HalSMArray args=HalSMCompiler_getArgs(hsmc,joinSpliti,clelem.type!=HalSMVariableType_HalSMNull);
                    if (clelem.type==HalSMVariableType_HalSMNull) {clelem=HalSMVariable_FromValue(HalSMElif_init(args));}
                    else {
                        b=(*(HalSMCLElement*)clelem.value).func;
                        for (unsigned int i=0;i<tabsC-1;i++) {
                            b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                        }
                        HalSMArray_add(&b,HalSMVariable_FromValue(HalSMElif_init(args)));
                    }
                } else if (StringCompare(tabsS,"else:")) {
                    if (clelem.type==HalSMVariableType_HalSMNull) {
                        //Remake: make error
                        clelem=HalSMVariable_FromValue(HalSMElse_init());
                    }
                    else {
                        b=(*(HalSMCLElement*)clelem.value).func;
                        for (unsigned int i=0;i<tabsC-1;i++) {
                            b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                        }
                        HalSMArray_add(&b,HalSMVariable_FromValue(HalSMElse_init()));
                    }
                } else if (StringStartsWith(tabsS,"while ")) {
                    spliti=HalSMArray_split_str(tabsS," ");
                    joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size)," ");
                    spliti=HalSMArray_split_str(joinSpliti,":");
                    if (spliti.size==1) {
                        //Remake
                        joinSpliti=*(char**)spliti.arr[0].value;
                    } else {joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,0,spliti.size-1),":");}
                    HalSMArray args=HalSMCompiler_getArgs(hsmc,joinSpliti,1);
                    if (clelem.type==HalSMVariableType_HalSMNull) {clelem=HalSMVariable_FromValue(HalSMWhile_init(args));}
                    else {
                        b=(*(HalSMCLElement*)clelem.value).func;
                        for (unsigned int i=0;i<tabsC-1;i++) {
                            b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                        }
                        HalSMArray_add(&b,HalSMVariable_FromValue(HalSMWhile_init(args)));
                    }
                } else if (StringStartsWith(tabsS,"return ")) {
                    spliti=HalSMArray_split_str(tabsS,"return ");
                    joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size),"return ");
                    HalSMReturn ret=HalSMReturn_init(HalSMCompiler_getArgs(hsmc,joinSpliti,1));
                    HalSMArray_add(&(*(HalSMLocalFunction*)func.value).func,HalSMVariable_FromValue(ret));
                } else if (isSetVar.type!=HalSMVariableType_HalSMNull) {
                    isSetVar=HalSMVariable_FromValue(HalSMSetVar_init(*(char**)(*(HalSMArray*)isSetVar.value).arr[0].value,*(char**)(*(HalSMArray*)isSetVar.value).arr[1].value));
                    if (clelem.type==HalSMVariableType_HalSMNull) {HalSMArray_add(&(*(HalSMLocalFunction*)func.value).func,isSetVar);}
                    else {HalSMArray_add(&(*(HalSMLocalFunction*)((*(HalSMLocalFunction*)func.value).func.arr[(*(HalSMLocalFunction*)func.value).func.size-1]).value).func,isSetVar);}
                }
            }
        }

        if (isFunc&&!isClass) {
            if (tabsC==0&&!isNull) {
                isFunc=0;
                if(clelem.type!=HalSMVariableType_HalSMNull) {HalSMArray_add(&(*(HalSMLocalFunction*)func.value).func,clelem);}
                //Remake
                func=HalSMVariable_FromValue(0);
            } else if (isRunFunc.type!=HalSMVariableType_HalSMNull) {
                resRunFunc=*(HalSMFunctionArray*)isRunFunc.value;
                HalSMRunFunc ret=HalSMRunFunc_init(*(HalSMFunctionC*)resRunFunc.args.arr[0].value,*(HalSMArray*)resRunFunc.args.arr[1].value);
                if (clelem.type!=HalSMVariableType_HalSMNull) {
                    b=(*(HalSMCLElement*)clelem.value).func;
                    while (1) {
                        if (b.size==0||b.arr[b.size-1].type!=HalSMVariableType_HalSMCLElement) {break;}
                        b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                    }
                    HalSMArray_add(&b,HalSMVariable_FromValue(ret));
                } else {HalSMArray_add(&(*(HalSMLocalFunction*)func.value).func,HalSMVariable_FromValue(ret));}
            } else if (StringStartsWith(tabsS,"for ")) {
                spliti=HalSMArray_split_str(tabsS," ");
                char* vr=*(char**)spliti.arr[1].value;
                joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,2,spliti.size)," ");
                spliti=HalSMArray_split_str(joinSpliti,"in ");
                joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size),"in ");
                spliti=HalSMArray_split_str(joinSpliti,":");
                if (spliti.size==1) {joinSpliti=*(char**)spliti.arr[0].value;}
                else {joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,0,spliti.size-1),":");}
                HalSMVariable args=HalSMCompiler_getArgs(hsmc,joinSpliti,0).arr[0];
                if (args.type==HalSMVariableType_str) {
                    HalSMArray fdf=HalSMArray_init();
                    for (int indexc=0;indexc<strlen(*(char**)args.value);indexc++) {HalSMArray_add(&fdf,HalSMVariable_FromValue((*(char**)args.value)[indexc]));}
                    args=HalSMVariable_FromValue(fdf);
                } else if (args.type==HalSMVariableType_HalSMArray) {
                    if ((*(HalSMArray*)args.value).arr[0].type==HalSMVariableType_HalSMArray) {args=(*(HalSMArray*)args.value).arr[0];}
                }
                if (clelem.type==HalSMVariableType_HalSMNull) {
                    clelem=HalSMVariable_FromValue(HalSMFor_init(HalSMVariable_init_str(vr),*(HalSMArray*)args.value));
                } else {
                    b=(*(HalSMCLElement*)clelem.value).func;
                    while (1) {
                        //Remake
                        if (b.size==0||b.arr[b.size-1].type!=HalSMVariableType_HalSMCLElement){break;}
                        b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                    }
                    HalSMArray_add(&b,HalSMVariable_FromValue(HalSMFor_init(HalSMVariable_FromValue(vr),*(HalSMArray*)args.value)));
                }
            } else if (StringStartsWith(tabsS,"if ")) {
                spliti=HalSMArray_split_str(tabsS," ");
                joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size)," ");
                spliti=HalSMArray_split_str(joinSpliti,":");
                if (spliti.size==1) {joinSpliti=*(char**)spliti.arr[0].value;}
                else {joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,0,spliti.size-1),":");}
                HalSMArray args=HalSMCompiler_getArgs(hsmc,joinSpliti,clelem.type!=HalSMVariableType_HalSMNull);
                if (clelem.type==HalSMVariableType_HalSMNull) {
                    clelem=HalSMVariable_FromValue(HalSMIf_init(args));
                    clif=HalSMVariable_FromValue(HalSMArray_init());
                } else {
                    //Remake
                    b=(*(HalSMCLElement*)clelem.value).func;
                    for (unsigned int i=0;i<tabsC-1;i++) {
                        b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                    }
                    HalSMArray_add(&b,HalSMVariable_FromValue(HalSMIf_init(args)));
                }
            } else if (StringStartsWith(tabsS,"elif ")) {
                spliti=HalSMArray_split_str(tabsS," ");
                joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size)," ");
                spliti=HalSMArray_split_str(joinSpliti,":");
                if (spliti.size==1) {joinSpliti=*(char**)spliti.arr[1].value;}
                else {joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,0,spliti.size-1),":");}
                HalSMArray args=HalSMCompiler_getArgs(hsmc,joinSpliti,clelem.type!=HalSMVariableType_HalSMNull);
                if (clelem.type==HalSMVariableType_HalSMNull) {clelem=HalSMVariable_FromValue(HalSMElif_init(args));}
                else {
                    b=(*(HalSMCLElement*)clelem.value).func;
                    for (unsigned int i=0;i<tabsC-1;i++) {
                        b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                    }
                    HalSMArray_add(&b,HalSMVariable_FromValue(HalSMElif_init(args)));
                }
            } else if (StringCompare(tabsS,"else:")) {
                if (clelem.type==HalSMVariableType_HalSMNull) {
                    //Remake: make error
                    clelem=HalSMVariable_FromValue(HalSMElse_init());
                }
                else {
                    b=(*(HalSMCLElement*)clelem.value).func;
                    for (unsigned int i=0;i<tabsC-1;i++) {
                        b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                    }
                    HalSMArray_add(&b,HalSMVariable_FromValue(HalSMElse_init()));
                }
            } else if (StringStartsWith(tabsS,"while ")) {
                spliti=HalSMArray_split_str(tabsS," ");
                joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size)," ");
                spliti=HalSMArray_split_str(joinSpliti,":");
                if (spliti.size==1) {
                    //Remake
                    joinSpliti=*(char**)spliti.arr[0].value;
                } else {joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,0,spliti.size-1),":");}
                HalSMArray args=HalSMCompiler_getArgs(hsmc,joinSpliti,1);
                if (clelem.type==HalSMVariableType_HalSMNull) {clelem=HalSMVariable_FromValue(HalSMWhile_init(args));}
                else {
                    b=(*(HalSMCLElement*)clelem.value).func;
                    for (unsigned int i=0;i<tabsC-1;i++) {
                        b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                    }
                    HalSMArray_add(&b,HalSMVariable_FromValue(HalSMWhile_init(args)));
                }
            } else if (StringStartsWith(tabsS,"return ")) {
                spliti=HalSMArray_split_str(tabsS,"return ");
                joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size),"return ");
                HalSMReturn ret=HalSMReturn_init(HalSMCompiler_getArgs(hsmc,joinSpliti,1));
                HalSMArray_add(&(*(HalSMLocalFunction*)func.value).func,HalSMVariable_FromValue(ret));
            } else if (isSetVar.type!=HalSMVariableType_HalSMNull) {
                isSetVar=HalSMVariable_FromValue(HalSMSetVar_init(*(char**)(*(HalSMArray*)isSetVar.value).arr[0].value,*(char**)(*(HalSMArray*)isSetVar.value).arr[1].value));
                if (clelem.type==HalSMVariableType_HalSMNull) {HalSMArray_add(&(*(HalSMLocalFunction*)func.value).func,isSetVar);}
                else {HalSMArray_add(&(*(HalSMLocalFunction*)((*(HalSMLocalFunction*)func.value).func.arr[(*(HalSMLocalFunction*)func.value).func.size-1]).value).func,isSetVar);}
            }
        }

        if (!isFunc && !isClass) {
            if (StringStartsWith(l,"import ")) {
                spliti=HalSMArray_split_str(l,"import ");
                joinSpliti=StringReplace(StringReplace(HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size),"import "),"\n",""),"\r","");
                if (DictElementIndexByKey(hsmc.sys_modules,HalSMVariable_init_str(joinSpliti))) {
                    HalSMVariable v=DictElementFindByKey(hsmc.sys_modules,HalSMVariable_init_str(joinSpliti)).value;
                    if (v.type==HalSMVariableType_str) {
                        if(strlen(*(char**)HalSMCompiler_readFile(hsmc,HalSMArray_init_with_elements((HalSMVariable[]){HalSMVariable_init_str(ConcatenateStrings(hsmc.pathModules,*(char**)v.value))},1)).value)>0) {
                            PutDictElementToDict(
                                &hsmc.modules,
                                DictElementInit(
                                    HalSMVariable_init_str(joinSpliti),
                                    HalSMVariable_FromValue(HalSMCompiler_loadHalSMModule(hsmc,joinSpliti,ConcatenateStrings(hsmc.pathModules,*(char**)v.value)))
                                )
                            );
                        } else {
                            //error
                        }
                    } else {
                        PutDictElementToDict(&hsmc.modules,DictElementInit(HalSMVariable_init_str(joinSpliti),v));
                    }
                } else if (strlen(*(char**)HalSMCompiler_readFile(hsmc,HalSMArray_init_with_elements((HalSMVariable[]){HalSMVariable_init_str(ConcatenateStrings(ConcatenateStrings(ConcatenateStrings(hsmc.path,"\\"),joinSpliti),".halsm"))},1)).value)>0) {
                    PutDictElementToDict(&hsmc.modules,DictElementInit(HalSMVariable_init_str(joinSpliti),HalSMVariable_FromValue(HalSMCompiler_loadHalSMModule(hsmc,joinSpliti,ConcatenateStrings(ConcatenateStrings(ConcatenateStrings(hsmc.path,"\\"),joinSpliti),".halsm")))));
                } else {
                    //Error Module with name {joinSpliti} not found!
                }
            } else if (isRunFunc.type!=HalSMVariableType_HalSMNull) {
                resRunFunc=*(HalSMFunctionArray*)isRunFunc.value;
                if (clelem.type!=HalSMVariableType_HalSMNull) {
                    HalSMCLElement* elemn=(HalSMCLElement*)clelem.value;
                    for (unsigned int i=0;i<tabsC-1;i++) {
                        elemn=(HalSMCLElement*)elemn->func.arr[elemn->func.size-1].value;
                    }
                    elemn->addFunc(elemn,HalSMVariable_FromValue(HalSMRunFunc_init(*(HalSMFunctionC*)resRunFunc.args.arr[0].value,*(HalSMArray*)resRunFunc.args.arr[1].value)));
                } else {
                    err=HalSMFunctionC_run(hsmc,*(HalSMFunctionC*)resRunFunc.args.arr[0].value,*(HalSMArray*)resRunFunc.args.arr[1].value);
                    if (err.type==HalSMVariableType_HalSMError) {
                        //Error
                    }
                }
            } else if (StringStartsWith(tabsS,"def ")) {
                spliti=HalSMArray_split_str(tabsS,":");
                joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,0,spliti.size-1),":");
                spliti=HalSMArray_split_str(joinSpliti,"def ");
                joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size),"def ");
                nameFunc=*(HalSMArray*)HalSMCompiler_getNameFunction(hsmc,joinSpliti).value;
                f=HalSMLocalFunction_init(*(char**)nameFunc.arr[0].value,*(char**)nameFunc.arr[1].value,hsmc.variables);
                PutDictElementToDict(&hsmc.localFunctions,DictElementInit(HalSMVariable_init_str(f.name),HalSMVariable_FromValue(f)));
                func=HalSMVariable_FromValue(f);
                isFunc=1;
            } else if (StringStartsWith(tabsS,"class ")) {
                spliti=HalSMArray_split_str(tabsS,":");
                joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,0,spliti.size-1),":");
                spliti=HalSMArray_split_str(joinSpliti,"class ");
                joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size),"class ");
                fc=HalSMVariable_FromValue(HalSMClass_init(joinSpliti,hsmc.variables));
                PutDictElementToDict(&hsmc.classes,DictElementInit(HalSMVariable_init_str((*(HalSMClass*)fc.value).name),fc));
                cls=fc;
                isClass=1;
            } else if (StringStartsWith(tabsS,"for ")) {
                spliti=HalSMArray_split_str(tabsS," ");
                char* vr=*(char**)spliti.arr[1].value;
                spliti=HalSMArray_slice(spliti,2,spliti.size);
                joinSpliti=HalSMArray_join_str(spliti," ");
                spliti=HalSMArray_split_str(joinSpliti,"in ");
                joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size),"in ");
                spliti=HalSMArray_split_str(joinSpliti,":");
                if (spliti.size==1) {joinSpliti=*(char**)spliti.arr[0].value;}
                else {joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,0,spliti.size-1),":");}
                HalSMVariable args=HalSMCompiler_getArgs(hsmc,joinSpliti,0).arr[0];

                if (args.type==HalSMVariableType_str) {
                    HalSMArray fdf=HalSMArray_init();
                    for (int indexc=0;indexc<strlen(*(char**)args.value);indexc++) {HalSMArray_add(&fdf,HalSMVariable_FromValue((*(char**)args.value)[indexc]));}
                    args=HalSMVariable_FromValue(fdf);
                } else if (args.type==HalSMVariableType_HalSMArray) {
                    if ((*(HalSMArray*)args.value).arr[0].type==HalSMVariableType_HalSMArray) {args=(*(HalSMArray*)args.value).arr[0];}
                }
                if (clelem.type==HalSMVariableType_HalSMNull) {
                    clelem=HalSMVariable_FromValue(HalSMFor_init(HalSMVariable_init_str(vr),*(HalSMArray*)args.value));
                } else {
                    b=(*(HalSMCLElement*)clelem.value).func;
                    for (unsigned int i=0;i<tabsC-1;i++) {
                        b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                    }
                    HalSMArray_add(&b,HalSMVariable_FromValue(HalSMFor_init(HalSMVariable_FromValue(vr),*(HalSMArray*)args.value)));
                }
            } else if (StringStartsWith(tabsS,"if ")) {
                spliti=HalSMArray_split_str(tabsS," ");
                joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size)," ");
                spliti=HalSMArray_split_str(joinSpliti,":");
                if (spliti.size==1) {joinSpliti=*(char**)spliti.arr[0].value;}
                else {joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,0,spliti.size-1),":");}
                HalSMArray args=HalSMCompiler_getArgs(hsmc,joinSpliti,clelem.type!=HalSMVariableType_HalSMNull);
                if (clelem.type==HalSMVariableType_HalSMNull) {
                    clelem=HalSMVariable_FromValue(HalSMIf_init(args));
                    clif=HalSMVariable_FromValue(HalSMArray_init());
                } else {
                    //Remake
                    b=(*(HalSMCLElement*)clelem.value).func;
                    for (unsigned int i=0;i<tabsC-1;i++) {
                        b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                    }
                    HalSMArray_add(&b,HalSMVariable_FromValue(HalSMIf_init(args)));
                }
            } else if (StringStartsWith(tabsS,"elif ")) {
                spliti=HalSMArray_split_str(tabsS," ");
                joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size)," ");
                spliti=HalSMArray_split_str(joinSpliti,":");
                if (spliti.size==1) {joinSpliti=*(char**)spliti.arr[1].value;}
                else {joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,0,spliti.size-1),":");}
                HalSMArray args=HalSMCompiler_getArgs(hsmc,joinSpliti,clelem.type!=HalSMVariableType_HalSMNull);
                if (clelem.type==HalSMVariableType_HalSMNull) {clelem=HalSMVariable_FromValue(HalSMElif_init(args));}
                else {
                    b=(*(HalSMCLElement*)clelem.value).func;
                    for (unsigned int i=0;i<tabsC-1;i++) {
                        b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                    }
                    HalSMArray_add(&b,HalSMVariable_FromValue(HalSMElif_init(args)));
                }
            } else if (StringCompare(tabsS,"else:")) {
                if (clelem.type==HalSMVariableType_HalSMNull) {
                    //Remake: make error
                    clelem=HalSMVariable_FromValue(HalSMElse_init());
                }
                else {
                    b=(*(HalSMCLElement*)clelem.value).func;
                    for (unsigned int i=0;i<tabsC-1;i++) {
                        b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                    }
                    HalSMArray_add(&b,HalSMVariable_FromValue(HalSMElse_init()));
                }
            } else if (StringStartsWith(tabsS,"while ")) {
                spliti=HalSMArray_split_str(tabsS," ");
                joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,1,spliti.size)," ");
                spliti=HalSMArray_split_str(joinSpliti,":");
                if (spliti.size==1) {
                    //Remake
                    joinSpliti=*(char**)spliti.arr[0].value;
                } else {joinSpliti=HalSMArray_join_str(HalSMArray_slice(spliti,0,spliti.size-1),":");}
                HalSMArray args=HalSMCompiler_getArgs(hsmc,joinSpliti,1);
                if (clelem.type==HalSMVariableType_HalSMNull) {clelem=HalSMVariable_FromValue(HalSMWhile_init(args));}
                else {
                    b=(*(HalSMCLElement*)clelem.value).func;
                    for (unsigned int i=0;i<tabsC-1;i++) {
                        b=(*(HalSMCLElement*)b.arr[b.size-1].value).func;
                    }
                    HalSMArray_add(&b,HalSMVariable_FromValue(HalSMWhile_init(args)));
                }
            } else if (isSetVar.type!=HalSMVariableType_HalSMNull) {
                resRunFunc=*(HalSMFunctionArray*)isSetVar.value;
                if (clelem.type==HalSMVariableType_HalSMNull) {
                    PutDictElementToDict(&hsmc.variables,DictElementInit(resRunFunc.args.arr[0],HalSMCompiler_getArgs(hsmc,*(char**)resRunFunc.args.arr[1].value,clelem.type!=HalSMVariableType_HalSMNull).arr[0]));
                } else {
                    HalSMCLElement* elemn=(HalSMCLElement*)clelem.value;
                    for (unsigned int i=0;i<tabsC-1;i++) {
                        elemn=(HalSMCLElement*)elemn->func.arr[elemn->func.size-1].value;
                    }
                    elemn->addFunc(elemn,HalSMVariable_FromValue(HalSMSetVar_init(*(char**)resRunFunc.args.arr[0].value,*(char**)resRunFunc.args.arr[1].value)));
                }
            }
        }
        hsmc.line++;
    }
    
    if (clif.type!=HalSMVariableType_HalSMNull) {
        if (!isFunc && !isClass) {
            HalSMArray clifa=*(HalSMArray*)clif.value;
            if (clelem.type!=HalSMVariableType_HalSMNull) {HalSMArray_add(&clifa,clelem);}
            HalSMVariable ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
            HalSMCLElement d;
            for (int indexc=0;indexc<clifa.size;indexc++) {
                d=*(HalSMCLElement*)clifa.arr[indexc].value;
                if (d.type==HalSMCLElementType_elif) {
                    if (ifr.type==HalSMVariableType_HalSMNull) {
                        //Error Elif cannot be without If    
                    }
                    if ((*(unsigned char*)ifr.value)==0) {
                        err=d.start(&d,&hsmc);
                        if (err.type==HalSMVariableType_HalSMError) {
                            //Error
                        }
                        ifr=err;
                    } else if (d.type==HalSMCLElementType_else) {
                        if (ifr.type==HalSMVariableType_HalSMNull) {
                            //Error
                        }
                        if ((*(unsigned char*)ifr.value)==0) {
                            err=d.start(&d,&hsmc);
                            if (err.type==HalSMVariableType_HalSMError) {
                                //Error
                            }
                            ifr=err;
                        } else {
                            ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
                        }
                    } else if (d.type==HalSMCLElementType_if) {
                        err=d.start(&d,&hsmc);
                        if (err.type==HalSMVariableType_HalSMError) {
                            //Error
                        }
                        ifr=err;
                    }
                }
            }
        }
    } else if (clelem.type!=HalSMVariableType_HalSMNull) {
        HalSMCLElement d=*(HalSMCLElement*)clelem.value;
        err=d.start((HalSMCLElement*)clelem.value,&hsmc);
        if (err.type==HalSMVariableType_HalSMError) {
            //Error
        }
    }

    HalSMArray outArr=HalSMArray_init();
    HalSMArray_add(&outArr,HalSMVariable_FromValue(hsmc.variables));
    HalSMArray_add(&outArr,HalSMVariable_FromValue(hsmc.localFunctions));
    HalSMArray_add(&outArr,HalSMVariable_FromValue(hsmc.classes));
    return outArr;
}

HalSMModule HalSMCompiler_loadHalSMModule(HalSMCompiler hsmc,char* name,char* file)
{
    HalSMCompiler hsm=HalSMCompiler_init(
        *(char**)HalSMCompiler_readFile(hsmc,HalSMArray_init_with_elements((HalSMVariable[]){HalSMVariable_init_str(file)},1)).value,
        file,
        hsmc.externModules,
        hsmc.print,
        hsmc.printErrorf,
        hsmc.inputf,
        hsmc.readFilef,
        hsmc.pathModules
    );
    HalSMArray res=HalSMCompiler_compile(hsm,hsm.code);
    return HalSMModule_init(name,*(Dict*)res.arr[0].value,*(Dict*)res.arr[1].value,*(Dict*)res.arr[2].value);
}

HalSMCLElement HalSMCLElement_init(void(*addFunc)(void*,HalSMVariable),HalSMVariable(*start)(void*,HalSMCompiler*),HalSMCLElementType type,void* element)
{
    HalSMCLElement out;
    out.func=HalSMArray_init();
    out.addFunc=addFunc;
    out.start=start;
    out.type=type;
    out.element=element;
    return out;
}

HalSMCLElement HalSMFor_init(HalSMVariable var,HalSMArray arr)
{
    HalSMFor* out=malloc(sizeof(HalSMFor));
    out->var=var;
    out->arr=arr;
    return HalSMCLElement_init(HalSMFor_addFunc,HalSMFor_start,HalSMCLElementType_for,out);
}

HalSMVariable HalSMFor_run(HalSMArray func,HalSMCompiler* hsmc)
{
    HalSMArray args;
    HalSMVariable arg;
    unsigned char isFind=0;
    HalSMVariable err;
    HalSMVariable ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    HalSMVariable f;
    
    for (int indexf=0;indexf<func.size;indexf++) {
        f=func.arr[indexf];
        if (f.type==HalSMVariableType_HalSMRunFunc) {
            args=HalSMArray_copy((*(HalSMRunFunc*)f.value).args);
            for (int a=0;a<args.size;a++) {
                arg=args.arr[a];
                if (arg.type==HalSMVariableType_HalSMVar) {
                    isFind=0;
                    HalSMVar finalArg=*(HalSMVar*)arg.value;
                    DictForEach(entryKey,entryValue,hsmc->variables) {
                        if (StringCompare(finalArg.name,*(char**)entryKey.value)) {
                            args.arr[a]=entryValue;
                            isFind=1;
                            break;
                        }
                    }
                    if (isFind==0) {
                        //Error Variable Not Found
                    }
                }
            }
            err=HalSMFunctionC_run(*hsmc,(*(HalSMRunFunc*)f.value).func,args);
            if (err.type==HalSMVariableType_HalSMError) {return err;}
            if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
        } else if (f.type==HalSMVariableType_HalSMLocalFunction) {
            err=HalSMLocalFunction_run(*(HalSMLocalFunction*)f.value,*hsmc,HalSMArray_init_with_elements((HalSMVariable[]) {HalSMVariable_FromValue(hsmc->variables)},1));
            if (err.type==HalSMVariableType_HalSMError) {return err;}
            if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
        } else if (f.type==HalSMVariableType_HalSMCLElement) {
            HalSMCLElement clem=*(HalSMCLElement*)f.value;
            if (clem.type==HalSMCLElementType_elif) {
                if (ifr.type==HalSMVariableType_HalSMNull) {/*Error Elif cannot be without If*/}
                err=clem.start(clem.element,hsmc);
                if (err.type==HalSMVariableType_HalSMError) {return err;}
                ifr=err;
            } else if (clem.type==HalSMCLElementType_else) {
                if (ifr.type==HalSMVariableType_HalSMNull) {/*Error Else cannot be without If*/}
                if (*(unsigned char*)ifr.value) {
                    err=clem.start(clem.element,hsmc);
                    if (err.type==HalSMVariableType_HalSMError) {return err;}
                    ifr=err;
                } else {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
            } else if (clem.type==HalSMCLElementType_if) {
                err=clem.start(clem.element,hsmc);
                if (err.type==HalSMVariableType_HalSMError) {return err;}
                ifr=err;
            } else {
                if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
                err=clem.start(clem.element,hsmc);
                if (err.type==HalSMVariableType_HalSMError) {return err;}
            }
        } else if (f.type==HalSMVariableType_HalSMSetVar) {
            arg=HalSMCompiler_getArgsSetVar(*hsmc,(*(HalSMSetVar*)f.value).value);
            PutDictElementToDict(&hsmc->variables,DictElementInit(HalSMVariable_init_str((*(HalSMSetVar*)f.value).name),arg));
            if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
        }
    }
}

void HalSMFor_addFunc(void* element,HalSMVariable func)
{
    HalSMArray* temp=&((HalSMCLElement*)element)->func;
    HalSMArray_add(temp,func);
}

HalSMVariable HalSMFor_start(void* element,HalSMCompiler* hsmc)
{
    HalSMArray arr;
    HalSMArray args;
    HalSMCLElement clem=*(HalSMCLElement*)element;
    HalSMFor elementFor=*(HalSMFor*)clem.element;
    if (elementFor.arr.size==0) return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    HalSMVariable temp=elementFor.arr.arr[0];
    HalSMVariable v;
    if (temp.type==HalSMVariableType_HalSMVar) {
        v=DictElementFindByKey(hsmc->variables,HalSMVariable_init_str((*(HalSMVar*)temp.value).name)).value;
        arr=*(HalSMArray*)v.value;
    } else if (temp.type==HalSMVariableType_HalSMRunFunc) {
        arr=HalSMArray_copy(elementFor.arr);
        args=HalSMArray_copy(*(HalSMArray*)arr.arr[1].value);
        for (int arg=0;arg<args.size;arg++) {
            v=args.arr[arg];
            if (v.type==HalSMVariableType_HalSMVar){HalSMArray_set(&args,DictElementFindByKey(hsmc->variables,HalSMVariable_init_str((*(HalSMVar*)v.value).name)).value,arg);}
        }
        HalSMFunctionC func=(*(HalSMRunFunc*)temp.value).func;
        HalSMVariable arrr=HalSMFunctionC_run(*hsmc,func,args);
        arr=*(HalSMArray*)((*(HalSMArray*)arrr.value).arr[0].value);
    } else if (temp.type==HalSMVariableType_HalSMLocalFunction) {
        args=HalSMArray_copy(*(HalSMArray*)elementFor.arr.arr[1].value);
        for (int arg=0;arg<args.size;arg++) {
            v=args.arr[arg];
            if (v.type==HalSMVariableType_HalSMVar) {HalSMArray_set(&args,DictElementFindByKey(hsmc->variables,HalSMVariable_init_str((*(HalSMVar*)v.value).name)).value,arg);}
        }
        arr=*(HalSMArray*)HalSMLocalFunction_run(*(HalSMLocalFunction*)temp.value,*hsmc,args).value;
    } else if (temp.type==HalSMVariableType_HalSMArray) {
        arr=*(HalSMArray*)temp.value;
    } else {
        arr=elementFor.arr;
    }
        
    HalSMVariable r;
    HalSMArrayForEach(elem,arr) {
        HalSMVariable* copy=malloc(sizeof(HalSMVariable));
        *copy=elem;
        
        PutDictElementToDict(&hsmc->variables,DictElementInit(HalSMVariable_init_str(*(char**)elementFor.var.value),*copy));
        r=HalSMFor_run(clem.func,hsmc);
        if (r.type==HalSMVariableType_HalSMError) {return r;}
    }
    return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
}

HalSMCLElement HalSMIf_init(HalSMArray arr)
{
    HalSMIf out;
    out.arr=arr;
    return HalSMCLElement_init(HalSMIf_addFunc,HalSMIf_start,HalSMCLElementType_if,&out);
}

HalSMVariable HalSMIf_run(HalSMArray func,HalSMCompiler* hsmc)
{
    HalSMArray args;
    HalSMVariable arg;
    unsigned char isFind=0;
    HalSMVariable err;
    HalSMVariable ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    HalSMVariable f;

    for (int indexf=0;indexf<func.size;indexf++) {
        f=func.arr[indexf];
        if (f.type==HalSMVariableType_HalSMRunFunc) {
            args=HalSMArray_copy((*(HalSMRunFunc*)f.value).args);
            for (int a=0;a<args.size;a++) {
                arg=args.arr[a];
                if (arg.type==HalSMVariableType_HalSMVar) {
                    isFind=0;
                    HalSMVar finalArg=*(HalSMVar*)arg.value;
                    DictForEach(entryKey,entryValue,hsmc->variables) {
                        if (StringCompare(finalArg.name,*(char**)entryKey.value)) {
                            HalSMArray_set(&args,entryValue,a);
                            isFind=1;
                            break;
                        }
                    }
                    if (isFind==0) {
                        //Error
                        return HalSMVariable_FromValue(HalSMError_init(0,"Variable Not Found"));
                    }
                }
            }
            err=HalSMFunctionC_run(*hsmc,(*(HalSMRunFunc*)f.value).func,args);
            if (err.type==HalSMVariableType_HalSMError) {return err;}
            if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
        } else if (f.type==HalSMVariableType_HalSMLocalFunction) {
            err=HalSMLocalFunction_run(*(HalSMLocalFunction*)f.value,*hsmc,HalSMArray_init_with_elements((HalSMVariable[]){HalSMVariable_FromValue(hsmc->variables)},1));
            if (err.type==HalSMVariableType_HalSMError) {return err;}
            if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
        } else if (f.type==HalSMVariableType_HalSMCLElement) {
            HalSMCLElement clem=*(HalSMCLElement*)f.value;
            if (clem.type==HalSMCLElementType_elif) {
                if (ifr.type==HalSMVariableType_HalSMNull) {/*Error Elif cannot be without If*/}
                err=clem.start(clem.element,hsmc);
                if (err.type==HalSMVariableType_HalSMError) {return err;}
                ifr=err;
            } else if (clem.type==HalSMCLElementType_else) {
                if (ifr.type==HalSMVariableType_HalSMNull) {/*Error Else cannot be without If*/}
                if (*(unsigned char*)ifr.value) {
                    err=clem.start(clem.element,hsmc);
                    if (err.type==HalSMVariableType_HalSMError) {return err;}
                    ifr=err;
                } else {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
            } else if (clem.type==HalSMCLElementType_if) {
                err=clem.start(clem.element,hsmc);
                if (err.type==HalSMVariableType_HalSMError) {return err;}
                ifr=err;
            } else {
                if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
                err=clem.start(clem.element,hsmc);
                if (err.type==HalSMVariableType_HalSMError) {return err;}
            }
        } else if (f.type==HalSMVariableType_HalSMSetVar) {
            arg=HalSMCompiler_getArgsSetVar(*hsmc,(*(HalSMSetVar*)f.value).value);
            PutDictElementToDict(&hsmc->variables,DictElementInit(HalSMVariable_init_str((*(HalSMSetVar*)f.value).name),arg));
            if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
        }
    }
    return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
}

void HalSMIf_addFunc(void* element,HalSMVariable func)
{
    HalSMArray_add(&((HalSMCLElement*)element)->func,func);
}

HalSMVariable HalSMIf_start(void* element,HalSMCompiler* hsmc)
{
    HalSMArray oa=HalSMArray_init();
    HalSMCLElement* clelem=(HalSMCLElement*)element;
    HalSMIf elementIf=*(HalSMIf*)clelem->element;

    HalSMArrayForEach(af,elementIf.arr) {
        if (af.type==HalSMVariableType_HalSMVar) {HalSMArray_add(&oa,DictElementFindByKey(hsmc->variables,HalSMVariable_init_str((*(HalSMVar*)af.value).name)).value);}
        else {HalSMArray_add(&oa,af);}
    }

    unsigned int ind=0;
    unsigned int ignore=0;
    HalSMVariable v;
    HalSMVariable i;

    HalSMArrayForEach(a,oa) {
        if (ignore>0) {
            ignore--;
            ind++;
            continue;
        }

        if (a.type==HalSMVariableType_HalSMEqual) {
            v=oa.arr[ind-1];
            i=oa.arr[ind+1];
            if (HalSMVariable_Compare(v,i)==0) {return HalSMVariable_FromValue((unsigned char)0);}
            ignore++;
        } else if (a.type==HalSMVariableType_HalSMNotEqual) {
            v=oa.arr[ind-1];
            i=oa.arr[ind+1];
            if (HalSMVariable_Compare(v,i)) {return HalSMVariable_FromValue((unsigned char)0);}
            ignore++;
        } else if (a.type==HalSMVariableType_HalSMBool) {
            if ((*(unsigned char*)a.value)==0) {return HalSMVariable_FromValue((unsigned char)0);}
        }
        ind++;
    }
    HalSMVariable r=HalSMIf_run(clelem->func,hsmc);
    if (r.type==HalSMVariableType_HalSMError) {return r;}
    return HalSMVariable_FromValue((unsigned char)1);
}

HalSMCLElement HalSMElif_init(HalSMArray arr)
{
    HalSMIf out;
    out.arr=arr;
    return HalSMCLElement_init(HalSMIf_addFunc,HalSMIf_start,HalSMCLElementType_elif,&out);
}

HalSMCLElement HalSMElse_init()
{
    HalSMElse out;
    return HalSMCLElement_init(HalSMElse_addFunc,HalSMElse_start,HalSMCLElementType_else,&out);
}

HalSMVariable HalSMElse_run(HalSMArray func,HalSMCompiler* hsmc)
{
    HalSMArray args;
    HalSMVariable arg;
    unsigned char isFind=0;
    HalSMVariable err;
    HalSMVariable ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    HalSMVariable f;

    for (int indexf=0;indexf<func.size;indexf++) {
        f=func.arr[indexf];
        if (f.type==HalSMVariableType_HalSMRunFunc) {
            args=HalSMArray_copy((*(HalSMRunFunc*)f.value).args);
            for (int a=0;a<args.size;a++) {
                arg=args.arr[a];
                if (arg.type==HalSMVariableType_HalSMVar) {
                    isFind=0;
                    HalSMVar finalArg=*(HalSMVar*)arg.value;
                    DictForEach(entryKey,entryValue,hsmc->variables) {
                        if (StringCompare(finalArg.name,*(char**)entryKey.value)) {
                            HalSMArray_set(&args,entryValue,a);
                            isFind=1;
                            break;
                        }
                    }
                    if (isFind==0) {
                        //Error
                        return HalSMVariable_FromValue(HalSMError_init(0,"Variable Not Found"));
                    }
                }
            }
            err=HalSMFunctionC_run(*hsmc,(*(HalSMRunFunc*)f.value).func,args);
            if (err.type==HalSMVariableType_HalSMError) {return err;}
            if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
        } else if (f.type==HalSMVariableType_HalSMLocalFunction) {
            err=HalSMLocalFunction_run(*(HalSMLocalFunction*)f.value,*hsmc,HalSMArray_init_with_elements((HalSMVariable[]){HalSMVariable_FromValue(hsmc->variables)},1));
            if (err.type==HalSMVariableType_HalSMError) {return err;}
            if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
        } else if (f.type==HalSMVariableType_HalSMCLElement) {
            HalSMCLElement clem=*(HalSMCLElement*)f.value;
            if (clem.type==HalSMCLElementType_elif) {
                if (ifr.type==HalSMVariableType_HalSMNull) {/*Error Elif cannot be without If*/}
                err=clem.start(clem.element,hsmc);
                if (err.type==HalSMVariableType_HalSMError) {return err;}
                ifr=err;
            } else if (clem.type==HalSMCLElementType_else) {
                if (ifr.type==HalSMVariableType_HalSMNull) {/*Error Else cannot be without If*/}
                if (*(unsigned char*)ifr.value) {
                    err=clem.start(clem.element,hsmc);
                    if (err.type==HalSMVariableType_HalSMError) {return err;}
                    ifr=err;
                } else {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
            } else if (clem.type==HalSMCLElementType_if) {
                err=clem.start(clem.element,hsmc);
                if (err.type==HalSMVariableType_HalSMError) {return err;}
                ifr=err;
            } else {
                if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
                err=clem.start(clem.element,hsmc);
                if (err.type==HalSMVariableType_HalSMError) {return err;}
            }
        } else if (f.type==HalSMVariableType_HalSMSetVar) {
            arg=HalSMCompiler_getArgsSetVar(*hsmc,(*(HalSMSetVar*)f.value).value);
            PutDictElementToDict(&hsmc->variables,DictElementInit(HalSMVariable_init_str((*(HalSMSetVar*)f.value).name),arg));
            if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
        }
    }
    return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
}

void HalSMElse_addFunc(void* element,HalSMVariable func)
{
    HalSMArray_add(&((HalSMCLElement*)element)->func,func);
}

HalSMVariable HalSMElse_start(void* element,HalSMCompiler* hsmc)
{
    HalSMVariable err=HalSMElse_run(((HalSMCLElement*)element)->func,hsmc);
    if (err.type==HalSMVariableType_HalSMError) {return err;}
    return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
}

HalSMCLElement HalSMWhile_init(HalSMArray arr)
{
    HalSMWhile out;
    out.arr=arr;
    return HalSMCLElement_init(HalSMWhile_addFunc,HalSMWhile_start,HalSMCLElementType_while,&out);
}

HalSMVariable HalSMWhile_run(HalSMArray func,HalSMCompiler* hsmc)
{
    HalSMArray args;
    HalSMVariable arg;
    unsigned char isFind=0;
    HalSMVariable err;
    HalSMVariable ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    HalSMVariable f;

    for (int indexf=0;indexf<func.size;indexf++) {
        f=func.arr[indexf];
        if (f.type==HalSMVariableType_HalSMRunFunc) {
            args=HalSMArray_copy((*(HalSMRunFunc*)f.value).args);
            for (int a=0;a<args.size;a++) {
                arg=args.arr[a];
                if (arg.type==HalSMVariableType_HalSMVar) {
                    isFind=0;
                    HalSMVar finalArg=*(HalSMVar*)arg.value;
                    DictForEach(entryKey,entryValue,hsmc->variables) {
                        if (StringCompare(finalArg.name,*(char**)entryKey.value)) {
                            HalSMArray_set(&args,entryValue,a);
                            isFind=1;
                            break;
                        }
                    }
                    if (isFind==0) {
                        //Error
                        return HalSMVariable_FromValue(HalSMError_init(0,"Variable Not Found"));
                    }
                }
            }
            err=HalSMFunctionC_run(*hsmc,(*(HalSMRunFunc*)f.value).func,args);
            if (err.type==HalSMVariableType_HalSMError) {return err;}
            if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
        } else if (f.type==HalSMVariableType_HalSMLocalFunction) {
            err=HalSMLocalFunction_run(*(HalSMLocalFunction*)f.value,*hsmc,HalSMArray_init_with_elements((HalSMVariable[]){HalSMVariable_FromValue(hsmc->variables)},1));
            if (err.type==HalSMVariableType_HalSMError) {return err;}
            if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
        } else if (f.type==HalSMVariableType_HalSMCLElement) {
            HalSMCLElement clem=*(HalSMCLElement*)f.value;
            if (clem.type==HalSMCLElementType_elif) {
                if (ifr.type==HalSMVariableType_HalSMNull) {/*Error Elif cannot be without If*/}
                err=clem.start(clem.element,hsmc);
                if (err.type==HalSMVariableType_HalSMError) {return err;}
                ifr=err;
            } else if (clem.type==HalSMCLElementType_else) {
                if (ifr.type==HalSMVariableType_HalSMNull) {/*Error Else cannot be without If*/}
                if (*(unsigned char*)ifr.value) {
                    err=clem.start(clem.element,hsmc);
                    if (err.type==HalSMVariableType_HalSMError) {return err;}
                    ifr=err;
                } else {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
            } else if (clem.type==HalSMCLElementType_if) {
                err=clem.start(clem.element,hsmc);
                if (err.type==HalSMVariableType_HalSMError) {return err;}
                ifr=err;
            } else {
                if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
                err=clem.start(clem.element,hsmc);
                if (err.type==HalSMVariableType_HalSMError) {return err;}
            }
        } else if (f.type==HalSMVariableType_HalSMSetVar) {
            arg=HalSMCompiler_getArgsSetVar(*hsmc,(*(HalSMSetVar*)f.value).value);
            PutDictElementToDict(&hsmc->variables,DictElementInit(HalSMVariable_init_str((*(HalSMSetVar*)f.value).name),arg));
            if (ifr.type!=HalSMVariableType_HalSMNull) {ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
        }
    }
    return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
}

void HalSMWhile_addFunc(void* element,HalSMVariable func)
{
    HalSMArray_add(&((HalSMCLElement*)element)->func,func);
}

HalSMVariable HalSMWhile_start(void* element,HalSMCompiler* hsmc)
{
    HalSMArray oa=HalSMArray_init();
    unsigned int ind=0;
    unsigned int ignore=0;
    HalSMVariable v;
    HalSMVariable i;
    HalSMCLElement* clelem=(HalSMCLElement*)element;
    HalSMWhile elementWhile=*(HalSMWhile*)clelem->element;
    HalSMVariable r;

    while (1) {
        HalSMArrayForEach(af,elementWhile.arr) {
            if (af.type==HalSMVariableType_HalSMVar) {HalSMArray_add(&oa,DictElementFindByKey(hsmc->variables,HalSMVariable_init_str((*(HalSMVar*)af.value).name)).value);}
            else {HalSMArray_add(&oa,af);}
        }

        HalSMArrayForEach(a,oa) {
            if (ignore>0) {
                ignore--;
                ind++;
                continue;
            }

            if (a.type==HalSMVariableType_HalSMEqual) {
                v=oa.arr[ind-1];
                i=oa.arr[ind+1];
                if (HalSMVariable_Compare(v,i)==0) {return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
                ignore++;
            } else if (a.type==HalSMVariableType_HalSMNotEqual) {
                v=oa.arr[ind-1];
                i=oa.arr[ind+1];
                if (HalSMVariable_Compare(v,i)) {return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
                ignore++;
            } else if (a.type==HalSMVariableType_HalSMBool) {
                if ((*(unsigned char*)a.value)==0) {return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);}
            }
            ind++;
        }
        ind=0;
        ignore=0;
        r=HalSMWhile_run(clelem->func,hsmc);
        if (r.type==HalSMVariableType_HalSMError) {return r;}
        oa=HalSMArray_init();
    }
}

HalSMFloatGet HalSMFloatGet_init(char* st)
{
    HalSMFloatGet hfg;
    hfg.st=st;
    return hfg;
}

HalSMVar HalSMVar_init(char* name)
{
    HalSMVar out;
    out.name=name;
    return out;
}

HalSMSetArg HalSMSetArg_init(char* name)
{
    HalSMSetArg out;
    out.name=name;
    out.value=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    return out;
}

HalSMReturn HalSMReturn_init(HalSMArray val)
{
    HalSMReturn out;
    out.value=val;
    return out;
}

Dict DictInit()
{
    Dict dict;
    dict.size=0;
    dict.elements=malloc(0);
    return dict;
}

Dict DictInitWithElements(DictElement *elements,int size)
{
    Dict dict;
    dict.size=size;
    dict.elements=elements;
    return dict;
}

DictElement DictElementInit(HalSMVariable key,HalSMVariable value)
{
    DictElement elem;
    elem.key=key;
    elem.value=value;
    return elem;
}

DictElement DictElementFindByIndex(Dict dict,int index)
{
    DictElement temp;
    if (index<dict.size)temp=dict.elements[index];
    return temp;
}

DictElement DictElementFindByKey(Dict dict,HalSMVariable key)
{
    DictElement empty;
    if (dict.size==0) return empty;
    for (int i=0;i<dict.size;i++)
    {
        if (HalSMVariable_Compare(dict.elements[i].key,key)) return dict.elements[i];
    }
    return empty;
}

DictElement DictElementFindByValue(Dict dict,HalSMVariable value)
{
    DictElement empty;
    if (dict.size==0) return empty;
    for (int i=0;i<dict.size;i++)
    {
        if (HalSMVariable_Compare(dict.elements[i].value,value)) return dict.elements[i];
    }
    return empty;
}

void PutDictElementToDict(Dict *dict,DictElement elem)
{
    int index=DictElementIndexByKey(*dict,elem.key);
    if (index==-1) {
        dict->elements=realloc(dict->elements,(1+dict->size)*sizeof(DictElement));
        dict->elements[dict->size]=elem;
        dict->size=dict->size+1;
    } else {dict->elements[index]=elem;}
}

int DictElementIndexByKey(Dict dict,HalSMVariable key)
{
    DictElement temp;
    for (int i=0;i<dict.size;i++)
    {
        temp=dict.elements[i];
        if (HalSMVariable_Compare(temp.key,key)) return i;
    }
    return -1;
}

int DictElementIndexByValue(Dict dict,HalSMVariable value)
{
    DictElement temp;
    for (int i=0;i<dict.size;i++)
    {
        temp=dict.elements[i];
        if (HalSMVariable_Compare(temp.value,value)) return i;
    }
    return -1;
}

Dict DictCopy(Dict dict)
{
    return DictInitWithElements(dict.elements,dict.size);
}

unsigned char DictCompare(Dict a,Dict b)
{
    if (a.size!=b.size){return 0;}
    for (int i=0;i<a.size;i++) {
        if (HalSMVariable_Compare(a.elements[i].key,b.elements[i].key)==0||HalSMVariable_Compare(a.elements[i].value,b.elements[i].value)==0){return 0;}
    }
    return 1;
}

HalSMVariable HalSMVariable_init(void* value,HalSMVariableType type)
{
    HalSMVariable out;
    out.type=type;
    //void** outv=(void**)malloc(sizeof(void*));
    //outv=value;
    out.value=value;
    return out;
}

void HalSMVariable_AsVar(void* var,HalSMVariable arg)
{
    HalSMVariableType type=arg.type;
    void* value=arg.value;
    if(type==HalSMVariableType_int){*((int*)var)=*((int*)value);}
    else if(type==HalSMVariableType_char){*((char*)var)=*((char*)value);}
    else if(type==HalSMVariableType_float){*((float*)var)=*((float*)value);}
    else if(type==HalSMVariableType_void){*((void**)var)=*((void**)value);}
    else if(type==HalSMVariableType_HalSMArray){*((HalSMArray*)var)=*((HalSMArray*)value);}
    else if(type==HalSMVariableType_str){*((char**)var)=*((char**)value);}
    else if(type==HalSMVariableType_int_array){*((int**)var)=*((int**)value);}
    else if(type==HalSMVariableType_HalSMFunctionC){(*(HalSMFunctionC*)var)=*(HalSMFunctionC*)value;}
    else if(type==HalSMVariableType_HalSMRunClassC){(*(HalSMRunClassC*)var)=*(HalSMRunClassC*)value;}
    else if(type==HalSMVariableType_HalSMError){(*(HalSMError*)var)=*(HalSMError*)value;}
    else if(type==HalSMVariableType_HalSMNull){(*(HalSMNull*)var)=*(HalSMNull*)value;}
    else if(type==HalSMVariableType_HalSMRunFunc){(*(HalSMRunFunc*)var)=*(HalSMRunFunc*)value;}
    else if(type==HalSMVariableType_HalSMLocalFunction){(*(HalSMLocalFunction*)var)=*(HalSMLocalFunction*)value;}
    else if(type==HalSMVariableType_HalSMCModule){(*(HalSMCModule*)var)=*(HalSMCModule*)value;}
    else if(type==HalSMVariableType_HalSMModule){(*(HalSMModule*)var)=*(HalSMModule*)value;}
    else if(type==HalSMVariableType_HalSMClassC){(*(HalSMClassC*)var)=*(HalSMClassC*)value;}
    else if(type==HalSMVariableType_HalSMCompiler){(*(HalSMCompiler*)var)=*(HalSMCompiler*)value;}
    else if(type==HalSMVariableType_HalSMCompiler_source){(*(HalSMCompiler**)var)=*(HalSMCompiler**)value;}
    else if(type==HalSMVariableType_HalSMRunClassC_source){(*(HalSMRunClassC**)var)=*(HalSMRunClassC**)value;}
    else if(type==HalSMVariableType_HalSMRunClass_source){(*(HalSMRunClass**)var)=*(HalSMRunClass**)value;}
    else if(type==HalSMVariableType_HalSMRunClass){(*(HalSMRunClass*)var)=*(HalSMRunClass*)value;}
    else if(type==HalSMVariableType_HalSMFloatGet){(*(HalSMFloatGet*)var)=*(HalSMFloatGet*)value;}
    else if(type==HalSMVariableType_HalSMClass){(*(HalSMClass*)var)=*(HalSMClass*)value;}
    else if(type==HalSMVariableType_HalSMVar){(*(HalSMVar*)var)=*(HalSMVar*)value;}
    else if(type==HalSMVariableType_HalSMPlus){(*(HalSMPlus*)var)=*(HalSMPlus*)value;}
    else if(type==HalSMVariableType_HalSMMinus){(*(HalSMMinus*)var)=*(HalSMMinus*)value;}
    else if(type==HalSMVariableType_HalSMMult){(*(HalSMMult*)var)=*(HalSMMult*)value;}
    else if(type==HalSMVariableType_HalSMDivide){(*(HalSMDivide*)var)=*(HalSMDivide*)value;}
    else if(type==HalSMVariableType_HalSMEqual){(*(HalSMEqual*)var)=*(HalSMEqual*)value;}
    else if(type==HalSMVariableType_HalSMNotEqual){(*(HalSMNotEqual*)var)=*(HalSMNotEqual*)value;}
    else if(type==HalSMVariableType_HalSMMore){(*(HalSMMore*)var)=*(HalSMMore*)value;}
    else if(type==HalSMVariableType_HalSMLess){(*(HalSMLess*)var)=*(HalSMLess*)value;}
    else if(type==HalSMVariableType_HalSMBool){(*(unsigned char*)var)=*(unsigned char*)value;}
    else if(type==HalSMVariableType_HalSMCLElement){(*(HalSMCLElement*)var)=*(HalSMCLElement*)value;}
    else if(type==HalSMVariableType_HalSMDict){(*(Dict*)var)=*(Dict*)value;}
    else if(type==HalSMVariableType_HalSMSetVar){(*(HalSMSetVar*)var)=*(HalSMSetVar*)value;}
    else if(type==HalSMVariableType_HalSMReturn){(*(HalSMReturn*)var)=*(HalSMReturn*)value;}
    else if(type==HalSMVariableType_HalSMFunctionCTypeDef){(*(HalSMFunctionCTypeDef*)var)=*(HalSMFunctionCTypeDef*)value;}
    else if(type==HalSMVariableType_HalSMFunctionArray){(*(HalSMFunctionArray*)var)=*(HalSMFunctionArray*)value;}
}

void* HalSMVariable_Read(HalSMVariable arg){return arg.value;}

HalSMVariable HalSMVariable_init_str(char* str) {
    char** d=malloc(sizeof(char*));
    *d=calloc(strlen(str)+1,sizeof(char));
    strncpy(*d,str,strlen(str));
    return HalSMVariable_init(d,HalSMVariableType_str);
}

char* HalSMVariable_to_str(HalSMVariable var)
{
    char *out;
    HalSMVariableType type=var.type;
    if(type==HalSMVariableType_str){out=*(char**)var.value;}
    else if(type==HalSMVariableType_int){out=Int2Str(*(int*)var.value);}
    else if(type==HalSMVariableType_float){out=Float2Str(*(float*)var.value);}
    return out;
}

unsigned char HalSMVariable_Compare(HalSMVariable v0,HalSMVariable v1)
{
    HalSMVariableType type=v0.type;
    void* var=v0.value;
    void* value=v1.value;
    if(type==HalSMVariableType_int){return *(int*)var==*(int*)value;}
    else if(type==HalSMVariableType_char){return *(char*)var==*(char*)value;}
    else if(type==HalSMVariableType_float){return *(float*)var==*(float*)value;}
    else if(type==HalSMVariableType_void){return *(void**)var==*(void**)value;}
    else if(type==HalSMVariableType_HalSMArray){return HalSMArray_compare(*(HalSMArray*)var,*(HalSMArray*)value);}
    else if(type==HalSMVariableType_str){return StringCompare(*(char**)var,*(char**)value);}
    else if(type==HalSMVariableType_HalSMFunctionC){return (*(HalSMFunctionC*)var).func==(*(HalSMFunctionC*)value).func;}
    else if(type==HalSMVariableType_HalSMRunClassC){return StringCompare((*(HalSMRunClassC*)var).name,(*(HalSMRunClassC*)value).name)&&DictCompare((*(HalSMRunClassC*)var).vrs,(*(HalSMRunClassC*)value).vrs)&&DictCompare((*(HalSMRunClassC*)var).funcs,(*(HalSMRunClassC*)value).funcs);}
    else if(type==HalSMVariableType_HalSMError){return (*(HalSMError*)var).line==(*(HalSMError*)value).line&&StringCompare((*(HalSMError*)var).error,(*(HalSMError*)value).error);}
    else if(type==HalSMVariableType_HalSMNull){return 1;}
    else if(type==HalSMVariableType_HalSMRunFunc){return 1;}
    else if(type==HalSMVariableType_HalSMLocalFunction){return StringCompare((*(HalSMLocalFunction*)var).name,(*(HalSMLocalFunction*)value).name)&&HalSMArray_compare((*(HalSMLocalFunction*)var).args,(*(HalSMLocalFunction*)value).args)&&HalSMArray_compare((*(HalSMLocalFunction*)var).func,(*(HalSMLocalFunction*)value).func)&&DictCompare((*(HalSMLocalFunction*)var).vars,(*(HalSMLocalFunction*)value).vars);}
    else if(type==HalSMVariableType_HalSMCModule){return DictCompare((*(HalSMCModule*)var).lfuncs,(*(HalSMCModule*)value).lfuncs)&&DictCompare((*(HalSMCModule*)var).vrs,(*(HalSMCModule*)value).vrs)&&DictCompare((*(HalSMCModule*)var).classes,(*(HalSMCModule*)value).classes)&&(*(HalSMCModule*)var).getName==(*(HalSMCModule*)value).getName;}
    else if(type==HalSMVariableType_HalSMModule){return StringCompare((*(HalSMModule*)var).name,(*(HalSMModule*)value).name)&&DictCompare((*(HalSMModule*)var).vrs,(*(HalSMModule*)value).vrs)&&DictCompare((*(HalSMModule*)var).lfuncs,(*(HalSMModule*)value).lfuncs)&&DictCompare((*(HalSMModule*)var).classes,(*(HalSMModule*)value).classes);}
    else if(type==HalSMVariableType_HalSMClassC){return (*(HalSMClassC*)var).getName==(*(HalSMClassC*)value).getName&&(*(HalSMClassC*)var).init_runclass==(*(HalSMClassC*)value).init_runclass&&DictCompare((*(HalSMClassC*)var).vrs,(*(HalSMClassC*)value).vrs)&&DictCompare((*(HalSMClassC*)var).funcs,(*(HalSMClassC*)value).funcs);}
    else if(type==HalSMVariableType_HalSMCompiler){/*finish it later*/}
    else if(type==HalSMVariableType_HalSMRunClass){return StringCompare((*(HalSMRunClass*)var).name,(*(HalSMRunClass*)value).name)&&DictCompare((*(HalSMRunClass*)var).funcs,(*(HalSMRunClass*)value).funcs)&&DictCompare((*(HalSMRunClass*)var).vars,(*(HalSMRunClass*)value).vars);}
    else if(type==HalSMVariableType_HalSMFloatGet){return StringCompare((*(HalSMFloatGet*)var).st,(*(HalSMFloatGet*)value).st);}
    else if(type==HalSMVariableType_HalSMClass){return StringCompare((*(HalSMClass*)var).name,(*(HalSMClass*)value).name)&&DictCompare((*(HalSMClass*)var).funcs,(*(HalSMClass*)value).funcs)&&DictCompare((*(HalSMClass*)var).vars,(*(HalSMClass*)value).vars);}
    else if(type==HalSMVariableType_HalSMVar){return StringCompare((*(HalSMVar*)var).name,(*(HalSMVar*)value).name);}
    else if(type==HalSMVariableType_HalSMPlus){return 1;}
    else if(type==HalSMVariableType_HalSMMinus){return 1;}
    else if(type==HalSMVariableType_HalSMMult){return 1;}
    else if(type==HalSMVariableType_HalSMDivide){return 1;}
    else if(type==HalSMVariableType_HalSMEqual){return 1;}
    else if(type==HalSMVariableType_HalSMNotEqual){return 1;}
    else if(type==HalSMVariableType_HalSMMore){return 1;}
    else if(type==HalSMVariableType_HalSMLess){return 1;}
    else if(type==HalSMVariableType_HalSMBool){return (*(unsigned char*)var==*(unsigned char*)value);}
    else if(type==HalSMVariableType_HalSMCLElement){(*(HalSMCLElement*)var).type==(*(HalSMCLElement*)value).type&&HalSMArray_compare((*(HalSMCLElement*)var).func,(*(HalSMCLElement*)value).func)&&(*(HalSMCLElement*)var).addFunc==(*(HalSMCLElement*)value).addFunc&&(*(HalSMCLElement*)var).start==(*(HalSMCLElement*)value).start;}
    else if(type==HalSMVariableType_HalSMSetVar){return StringCompare((*(HalSMSetVar*)var).name,(*(HalSMSetVar*)value).name)&&StringCompare((*(HalSMSetVar*)var).value,(*(HalSMSetVar*)value).value);}
    else if(type==HalSMVariableType_HalSMReturn){return HalSMArray_compare((*(HalSMReturn*)var).value,(*(HalSMReturn*)value).value);}
    else if(type==HalSMVariableType_HalSMFunctionArray){return (*(HalSMFunctionArray*)var).type==(*(HalSMFunctionArray*)value).type&&HalSMArray_compare((*(HalSMFunctionArray*)var).args,(*(HalSMFunctionArray*)value).args);}
    return 0;
}

HalSMSetVar HalSMSetVar_init(char* name,char* value)
{
    HalSMSetVar out;
    out.name=name;
    out.value=value;
    return out;
}

HalSMArray HalSMArray_init()
{
    HalSMArray out;
    out.size=0;
    out.arr=calloc(0,sizeof(HalSMVariable));
    return out;
}

HalSMArray HalSMArray_split_str(char* str,char* spl)
{
    HalSMArray out;
    out.size=0;
    out.arr=calloc(0,sizeof(HalSMVariable));
    unsigned int slen=strlen(str);
    unsigned int plen=strlen(spl);
    if (slen<plen) {
        return HalSMArray_init_with_elements((HalSMVariable[]){HalSMVariable_init_str("")},1);
    }
    unsigned int i=0;
    char *arr;
    char* temp=calloc(0,sizeof(char));
    unsigned int d=0;

    while (i<slen) {
        if (i<slen-plen+1) {
            arr=SubString(str,i,i+plen);
            if (StringCompare(arr,spl)) {
                temp=realloc(temp,(d+1)*sizeof(char));
                temp[d]='\0';
                HalSMArray_add(&out,HalSMVariable_init_str(temp));
                i+=plen;
                d=0;
                temp=calloc(0,sizeof(char));
            } else {
                d++;
                temp=realloc(temp,d*sizeof(char));
                temp[d-1]=str[i];
                i++;
            }
        } else {
            d++;
            temp=realloc(temp,d*sizeof(char));
            temp[d-1]=str[i];
            i++;
        }
    }

    if (strlen(temp)>0) {
        temp=realloc(temp,(d+1)*sizeof(char));
        temp[d]='\0';
        HalSMArray_add(&out,HalSMVariable_init_str(temp));
    } else {
        HalSMArray_add(&out,HalSMVariable_init_str(""));
    }

    free(arr);
    free(temp);
    return out;
}

/*HalSMArray HalSMArray_split_str(char* str,char* spl)
{
    HalSMArray out;
    out.size=0;
    out.arr=malloc(0);
    int d=0;
    char b;
    int j=1;
    char *arr=malloc(0);
    int i=0;
    while (i<strlen(str))
    {   
        if (i<strlen(str)-strlen(spl)+1) {
            for (int h=0;h<strlen(spl);h++)
            {
                b=str[i+h];
                if (b!=spl[h]){j=0;}
            }
        } else {j=0;}
        if (j==1) {
            arr=realloc(arr,(d+1)*sizeof(char));
            arr[d]='\0';
            HalSMArray_add(&out,HalSMVariable_init_str(arr));
            arr=malloc(0);
            d=0;
            i+=strlen(spl);
        } else {
            b=str[i];
            j=1;
            d+=1;
            arr=realloc(arr,d*sizeof(char));
            arr[d-1]=b;
            i+=1;
        }
    }
    if (strlen(arr)>0){
        arr=realloc(arr,(d+1)*sizeof(char));
        arr[d]='\0';
        HalSMArray_add(&out,HalSMVariable_init_str(arr));
    }
    return HalSMArray_copy(out);
}*/

int HalSMArray_index(HalSMArray harr,HalSMVariable value)
{
    for (int i=0;i<harr.size;i++)
    {
        if (harr.arr[i].value==value.value)return i;
    }
    return -1;
}

void HalSMArray_add(HalSMArray *harr,HalSMVariable value)
{
    harr->arr=(HalSMVariable*)realloc(harr->arr,sizeof(HalSMVariable)*(harr->size+1));
    harr->arr[harr->size]=value;
    harr->size=harr->size+1;
}

void HalSMArray_set(HalSMArray *harr,HalSMVariable value,unsigned int index)
{
    if (index<harr->size) {
        harr->arr[index]=value;
    }
}

void HalSMArray_remove(HalSMArray *harr,unsigned int index)
{
    int b=0;
    HalSMVariable* arr=malloc(harr->size*sizeof(HalSMVariable));
    for (int i=0;i<harr->size;i++) {
        if(i!=index){arr[b]=harr->arr[i];b++;}
    }
    harr->size=harr->size-1;
    harr->arr=arr;
}

HalSMArray HalSMArray_reverse(HalSMArray harr)
{
    HalSMArray out=HalSMArray_init();
    for (int i=harr.size-1;i--;i>-1){HalSMArray_add(&out,harr.arr[i]);}
    return out;
}

void HalSMArray_appendArray(HalSMArray *harr,HalSMArray narr)
{
    harr->arr=realloc(harr->arr,(harr->size+narr.size)*sizeof(HalSMVariable));
    for (int i=0;i<narr.size;i++){harr->arr[harr->size+i]=narr.arr[i];}
    harr->size=harr->size+narr.size;
}

HalSMVariable HalSMArray_get(HalSMArray harr,unsigned int index)
{
    if (harr.size==0||harr.size<=index||index<0){HalSMVariable temp;return temp;}
    return harr.arr[index];
}

void AdditionStrings(char** c,char* f,unsigned int sizec,unsigned int sizef)
{
    char* tmp=calloc(sizec+1,sizeof(char));
    memcpy(tmp,*c,sizec);
    *c=calloc(sizec+sizef+1,sizeof(char));
    memcpy(*c,tmp,sizec);
    memcpy(*c+strlen(*c),f,sizef);
    free(tmp);
}

char* HalSMArray_join_str(HalSMArray harr,char* join)
{
    if(harr.size==0) {
        return "";
    } else if (harr.size==1) {
        return *(char**)harr.arr[0].value;
    }
    unsigned int size=0;
    unsigned int lj=strlen(join);
    char* out=calloc(1,sizeof(char));
    out[0]='\0';
    unsigned int i=0;
    size=0;
    HalSMArrayForEach(o,harr) {
        char* oc=*(char**)o.value;
        AdditionStrings(&out,oc,size,strlen(oc));
        size+=strlen(oc);
        if (i!=harr.size-1) {
            AdditionStrings(&out,join,size,lj);
            size+=lj;
        }
        i++;
    }
    out[size]='\0';
    return out;
}

char* HalSMArray_to_print(HalSMArray harr)
{
    HalSMArray out=HalSMArray_init();
    char* c;
    HalSMVariable a;
    for (int i=0;i<harr.size;i++) {
        a=harr.arr[i];
        if (a.type==HalSMVariableType_int) {
            HalSMArray_add(&out,HalSMVariable_init_str(Int2Str(*(int*)a.value)));
        } else if (a.type==HalSMVariableType_float) {
            HalSMArray_add(&out,HalSMVariable_init_str(Float2Str(*(float*)a.value)));
        } else if (a.type==HalSMVariableType_str) {
            HalSMArray_add(&out,a);
        } else if (a.type==HalSMVariableType_HalSMNull) {
            HalSMArray_add(&out,HalSMVariable_init_str("Null"));
        } else if (a.type==HalSMVariableType_char) {
            c=malloc(2);
            c[0]=*(char*)a.value;
            c[1]='\0';
            HalSMArray_add(&out,HalSMVariable_init(&c,HalSMVariableType_str));
        } else if (a.type==HalSMVariableType_HalSMArray) {
            HalSMArray_add(&out,HalSMVariable_init_str(HalSMArray_to_print(*(HalSMArray*)a.value)));
        } else if (a.type==HalSMVariableType_HalSMRunClassC) {
            c=malloc(21+strlen((*(HalSMRunClassC*)a.value).name));
            strcpy(c,"<Running Class C (");
            strcat(c,(*(HalSMRunClassC*)a.value).name);
            strcat(c,")>");
            c[strlen((*(HalSMRunClassC*)a.value).name)+20]='\0';
            HalSMArray_add(&out,HalSMVariable_init_str(c));
        } else if (a.type==HalSMVariableType_HalSMFunctionC) {
            char* name=malloc(17);
            sprintf(name,"0x%p",(*(HalSMFunctionC*)a.value).func);
            name[100]='\0';
            c=malloc(35);
            strcpy(c,"<Function C at (");
            strcat(c,name);
            strcat(c,")>");
            c[strlen(name)+18]='\0';
            HalSMArray_add(&out,HalSMVariable_init_str(c));
        } else {
            HalSMArray_add(&out,HalSMVariable_init_str(HalSMVariable_to_str(a)));
        }
    }
    char* joinout=HalSMArray_join_str(out,", ");
    char* outs=malloc(3+strlen(joinout));
    strcpy(outs,"[");
    strcat(outs,joinout);
    strcat(outs,"]");
    outs[2+strlen(joinout)]='\0';
    return outs;
}

char* HalSMArray_chars_to_str(HalSMArray harr)
{
    char* out=malloc(harr.size+1);
    for (int i=0;i<harr.size;i++) {out[i]=*(char*)harr.arr[i].value;}
    out[harr.size]='\0';
    return out;
}

HalSMArray HalSMArray_slice(HalSMArray harr,unsigned int s,unsigned int e)
{
    if (s>=e){
        //Error
    }
    HalSMArray out;
    out.arr=calloc(IntMathMin(e,harr.size)-s,sizeof(HalSMVariable));
    out.size=IntMathMin(e,harr.size)-s;

    for (unsigned int i=s,d=0;i<IntMathMin(e,harr.size);i++,d++) {out.arr[d]=harr.arr[i];}
    return out;
}

unsigned char HalSMArray_compare(HalSMArray harr,HalSMArray barr)
{
    if (harr.size!=barr.size){return 0;}
    for (int i=0;i<harr.size;i++) {
        if (HalSMVariable_Compare(HalSMArray_get(harr,i),HalSMArray_get(barr,i))==0){return 0;}
    }
    return 1;
}

HalSMArray HalSMArray_from_str(char* str,unsigned int size)
{
    HalSMArray out=HalSMArray_init();
    for (unsigned int i=0;i<size;i++) {HalSMArray_add(&out,HalSMVariable_FromValue(str[i]));}
    return out;
}

HalSMArray HalSMArray_make_args(unsigned int size,...)
{
    HalSMArray out;
    out.arr=calloc(size,sizeof(HalSMVariable));
    out.size=size;
    va_list args;
    va_start(args,size);
    for (int i=0;i<size;i++) {out.arr[i]=va_arg(args,HalSMVariable);}
    va_end(args);
    return out;
}

HalSMArray HalSMArray_copy(HalSMArray harr)
{
    HalSMArray out;
    out.size=harr.size;
    out.arr=calloc(harr.size,sizeof(HalSMVariable));
    memcpy(out.arr,harr.arr,harr.size*sizeof(HalSMVariable));
    return out;
}

HalSMArray HalSMArray_init_with_elements(HalSMVariable* arr,unsigned int size)
{
    HalSMArray out;
    out.arr=arr;
    out.size=size;
    return out;
}

HalSMFunctionC HalSMFunctionC_init(HalSMFunctionCTypeDef func)
{
    HalSMFunctionC out;
    out.func=func;
    return out;
}

HalSMVariable HalSMFunctionC_run(HalSMCompiler hsmc,HalSMFunctionC hfc,HalSMArray args) {
    return hfc.func(hsmc,args);
}

void HalSMFunctionC_GetArg(void* var,HalSMArray args,int index){HalSMVariable_AsVar(var,HalSMArray_get(args,index));}

HalSMRunClassC HalSMRunClassC_init(void(*init_runclass)(HalSMRunClassC*),char* name,Dict vrs,Dict funcs)
{
    HalSMRunClassC runclassc;
    runclassc.name=name;
    runclassc.vrs=vrs;
    runclassc.funcs=funcs;
    init_runclass(&runclassc);
    return runclassc;
}

HalSMRunClassC HalSMRunClassC__init__(HalSMCompiler hsmc,HalSMRunClassC runclassc,HalSMArray args)
{
    int indexInit=DictElementIndexByKey(runclassc.funcs,HalSMVariable_init("__init__",HalSMVariableType_str));
    if (indexInit!=-1){
        HalSMFunctionC func;
        HalSMVariable_AsVar(&func,DictElementFindByIndex(runclassc.funcs,indexInit).value);
        HalSMFunctionC_run(hsmc,func,args);
    }
    return runclassc;
}

HalSMClassC HalSMClassC_init(void(*init_runclass)(HalSMRunClassC*),char*(*getName)())
{
    HalSMClassC classc;
    classc.vrs=DictInit();
    classc.funcs=DictInit();
    classc.getName=getName;
    classc.init_runclass=init_runclass;
    return classc;
}

HalSMRunClassC HalSMClassC_run(HalSMCompiler hsmc,HalSMClassC classc,HalSMArray args)
{
    HalSMRunClassC o=HalSMRunClassC_init(classc.init_runclass,classc.getName(),classc.vrs,classc.funcs);
    return HalSMRunClassC__init__(hsmc,o,args);
}

HalSMClass HalSMClass_init(char* name,Dict vrs)
{
    HalSMClass out;
    out.vars=vrs;
    out.funcs=DictInit();
    out.name=name;
    return out;
}

HalSMRunClass HalSMClass_run(HalSMClass class,HalSMCompiler hsmc,HalSMArray args)
{
    HalSMRunClass out=HalSMRunClass_init(class.name,class.vars,class.funcs);
    return HalSMRunClass__init__(out,hsmc,args);
}

HalSMRunClass HalSMRunClass_init(char* name,Dict vrs,Dict funcs)
{
    HalSMRunClass out;
    out.name=name;
    out.vars=DictCopy(vrs);
    out.funcs=DictCopy(funcs);
    return out;
}

HalSMRunClass HalSMRunClass__init__(HalSMRunClass runclass,HalSMCompiler hsmc,HalSMArray args)
{
    if (DictElementIndexByKey(runclass.funcs,HalSMVariable_init_str("__init__"))!=-1) {
        HalSMLocalFunction func=*(HalSMLocalFunction*)DictElementFindByKey(runclass.funcs,HalSMVariable_init_str("__init__")).value.value;
        HalSMLocalFunction_run(func,hsmc,args);
    }
    return runclass;
}

HalSMCModule HalSMCModule_init(char*(*getName)())
{
    HalSMCModule o;
    o.lfuncs=DictInit();
    o.vrs=DictInit();
    o.classes=DictInit();
    o.getName=getName;
    return o;
}

HalSMModule HalSMModule_init(char* name, Dict vrs, Dict lfuncs, Dict classes)
{
    HalSMModule o;
    o.lfuncs=lfuncs;
    o.vrs=vrs;
    o.classes=classes;
    o.name=name;
    return o;
}

HalSMRunFunc HalSMRunFunc_init(HalSMFunctionC func,HalSMArray args)
{
    HalSMRunFunc out;
    out.func=func;
    out.args=args;
    return out;
}

unsigned char HalSMIsInt(char *c)
{
    for (int i=0;i<strlen(c);i++)
    {
        char b=c[i];
        if ((b=='-' && i>0) || HalSMArray_index(arrInt,HalSMVariable_init(&b,HalSMVariableType_char))!=-1){return 0;}
    }
    return 1;
}

unsigned char HalSMIsFloat(char *c)
{
    int ct=0;
    for (int i=0;i<strlen(c);i++)
    {
        char b=c[i];
        if ((b=='-' && i>0) || HalSMArray_index(arrInt,HalSMVariable_init(&b,HalSMVariableType_char))!=-1){return 0;}
        else if(b=='.' && (i==0 || i==strlen(c)-1)){return 0;}
        else if(b=='.' && i>0 && i<strlen(c)){ct+=1;if(ct==2)return 0;}
    }
    if (ct==0){return 0;}
    return 1;
}

char* Int2Str(int c)
{
    int length = snprintf(NULL,0,"%d",c);
    char *str=malloc(length+1);
    snprintf(str,length+1,"%d",c);
    return str;
}

char* Float2Str(float c)
{
    int length = snprintf(NULL,0,"%f",c);
    char *str=malloc(length+1);
    snprintf(str,length+1,"%f",c);
    return str;
}

int ParseInt(char* c){return atoi(c);}

HalSMVariable ParseHalSMVariableInt(char* c)
{
    int a=ParseInt(c);
    return HalSMVariable_init(&a,HalSMVariableType_int);
}

float ParseFloat(char* c){return atof(c);}

HalSMVariable ParseHalSMVariableFloat(char* c)
{
    float a=ParseInt(c);
    return HalSMVariable_init(&a,HalSMVariableType_float);
}

HalSMVariable HalSMLocalFunction_run(HalSMLocalFunction lf,HalSMCompiler hsmc,HalSMArray args)
{
    int ia=0;
    HalSMVariable v;
    Dict vrs=DictInitWithElements(lf.vars.elements,lf.vars.size);
    for (int arg=0;arg<args.size;arg++)
    {
        v=HalSMArray_get(args,arg);
        if (v.type==HalSMVariableType_HalSMSetArg)
        {
            PutDictElementToDict(&lf.vars,DictElementInit(HalSMVariable_init((*(HalSMSetArg*)v.value).name,HalSMVariableType_str),(*(HalSMSetArg*)v.value).value));
            ia++;
            continue;
        }
        PutDictElementToDict(&vrs,DictElementInit(HalSMArray_split_str(*(char**)HalSMArray_get(lf.args,arg-ia).value,"=").arr[0],v));
    }
    HalSMVariable ad;
    char* argi;
    char e='=';
    for (int a=0;a<lf.args.size;a++)
    {
        argi=*(char**)lf.args.arr[a].value;
        ad=HalSMArray_get(HalSMArray_split_str(argi,"="),0);
        if (DictElementIndexByKey(vrs,ad)!=-1){continue;}
        if (HalSMArray_index(HalSMArray_from_str(argi,strlen(argi)),HalSMVariable_init(&e,HalSMVariableType_char))!=-1) {
            v=HalSMArray_get(HalSMArray_split_str(argi,"="),1);
            if(HalSMIsInt(*(char**)v.value)==1){v=ParseHalSMVariableInt(*(char**)v.value);}
            else if(HalSMIsFloat(*(char**)v.value)==1){v=ParseHalSMVariableFloat(*(char**)v.value);}
            PutDictElementToDict(&vrs,DictElementInit(ad,v));
        } else {
            //Add calculation line number
            HalSMError err=HalSMError_init(0,"Not enough args");
            return HalSMVariable_init(&err,HalSMVariableType_HalSMError);
        }
    }

    HalSMArray arguss;
    HalSMVariable arg;
    int isFind;
    HalSMVariable err;
    HalSMVariable ifr=HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
    HalSMVariable f;

    for (int fi=0;fi<lf.func.size;fi++)
    {
        f=lf.func.arr[fi];
        if(f.type==HalSMVariableType_HalSMRunFunc) {

        } else if(f.type=HalSMVariableType_HalSMLocalFunction) {

        }
    }
    return HalSMVariable_init(&null,HalSMVariableType_HalSMNull);
}

HalSMLocalFunction HalSMLocalFunction_init(char* name,char* args,Dict vrs)
{
    HalSMLocalFunction out;
    out.name=name;
    out.args=HalSMArray_split_str(args,",");
    if(out.args.size>0 && strlen(*(char**)out.args.arr[0].value)==0){out.args=HalSMArray_init();}
    out.func=HalSMArray_init();
    out.vars=vrs;
}

unsigned char StringCompare(char* c,char* f) {
    if (strlen(c)!=strlen(f)){return 0;}
    for (int i=0;i<strlen(c);i++) {
        if (c[i]!=f[i]){return 0;}
    }
    return 1;
}

int StringIndexOf(char* c,char* f) {
    int fl=strlen(f);
    if (fl==0||strlen(c)==0||fl==0||strlen(c)<fl){return -1;}
    char *fa=malloc(fl+1);
    fa[fl]='\0';
    for (int i=0;i<strlen(c)-strlen(f)+1;i++) {
        memcpy(fa,&c[i],fl);
        if (StringCompare(fa,f)){return i;}
    }
    return -1;
}

int StringLastIndexOf(char* c,char* f) {
    int fl=strlen(f);
    if (fl==0||strlen(c)==0||fl==0||fl>=strlen(c)){return -1;}
    int out=-1;
    char *fa=malloc(fl+1);
    fa[fl]='\0';
    for (int i=0;i<strlen(c)-strlen(f)+1;i++) {
        memcpy(fa,&c[i],fl);
        if (StringCompare(fa,f)){out=i;}
    }
    return out;
}

unsigned char StringEndsWith(char* c,char* f)
{
    if (strlen(c)==0||strlen(f)==0) {
        return 0;
    } else if (strlen(c)==strlen(f)) {
        return StringCompare(c,f);
    } else if (strlen(c)<strlen(f)) {
        return 0;
    }
    return StringCompare(SubString(c,strlen(c)-strlen(f),strlen(c)),f);
}

unsigned char StringStartsWith(char* c,char* f)
{
    if (strlen(c)==0||strlen(f)==0) {
        return 0;
    } else if (strlen(c)==strlen(f)) {
        return StringCompare(c,f);
    } else if (strlen(c)<strlen(f)) {
        return 0;
    }
    return StringCompare(SubString(c,0,strlen(f)),f);
}

int IntMathMax(int f,int t) {
    return f>t?f:t;
}

int IntMathMin(int f,int t) {
    return f<t?f:t;
}

char* SubString(char* c,int start,int end) {
    int cl=strlen(c);
    if (start>=cl){
        //PRINT ERROR
        return "";
    }
    else if (cl==0||end>cl){return "";}
    int lo=IntMathMin(end,cl)-start;
    char* out=malloc(lo+1);
    memcpy(out,&c[start],lo);
    out[lo]='\0';
    return out;
}

char* ConcatenateStrings(char* c,char* f) {
    if (strlen(c)==0&&strlen(f)==0){return "";}
    char* out=malloc(strlen(c)+strlen(f)+1);
    strcpy(out,c);
    strcat(out,f);
    out[strlen(c)+strlen(f)]='\0';
    return out;
}

char* StringReplace(char* c,char* f,char* r) {
    int lf=strlen(f);
    int lr=strlen(r);
    if(strlen(c)<lf||lf==0){return c;}
    else if(strlen(c)==0){return "";}
    else if(c==f){return r;}
    char* out=malloc(0);
    int i=0;
    int size=0;
    while(i<strlen(c)-lf+1){
        if(StringCompare(SubString(c,i,i+lf),f)){
            if(lr>0){
                out=realloc(out,(size+lr));
                for (int j=0;j<lr;j++) {
                    out[size+j]=r[j];
                }
                size+=lr;
            }
            i+=lf;
        } else {
            out=realloc(out,(size+1));
            out[size]=c[i];
            size++;
            i++;
        }
    }
    out=realloc(out,size+1);
    out[size]='\0';
    return out;
}

HalSMCalculateVars HalSMCalculateVars_init()
{
    HalSMCalculateVars out;
    out.version="0.0.1";
    out.addStr=HalSMCalculateVars_addStr;
    out.subStr=HalSMCalculateVars_subStr;
    out.mulStr=HalSMCalculateVars_mulStr;
    out.divStr=HalSMCalculateVars_divStr;
    out.addInt=HalSMCalculateVars_addInt;
    out.subInt=HalSMCalculateVars_subInt;
    out.mulInt=HalSMCalculateVars_mulInt;
    out.divInt=HalSMCalculateVars_divInt;
    out.addFloat=HalSMCalculateVars_addFloat;
    out.subFloat=HalSMCalculateVars_subFloat;
    out.mulFloat=HalSMCalculateVars_mulFloat;
    out.divFloat=HalSMCalculateVars_divFloat;
    return out;
}

char* HalSMCalculateVars_addStr(HalSMVariable v0,HalSMVariable v1)
{
    return strcat(HalSMVariable_to_str(v0),HalSMVariable_to_str(v1));
}

char* HalSMCalculateVars_subStr(HalSMVariable v0,HalSMVariable v1)
{
    char* v0s=HalSMVariable_to_str(v0);
    char* v1s=HalSMVariable_to_str(v1);
    if (strlen(v0s)<strlen(v1s)){return v0s;};
    int v=StringLastIndexOf(v0s,v1s);
    if (v==-1){return v0s;}
    return ConcatenateStrings(SubString(v0s,0,v),SubString(v0s,v+strlen(v1s),strlen(v0s)));
}

char* HalSMCalculateVars_mulStr(HalSMVariable v0,HalSMVariable v1)
{
    char* st=HalSMVariable_GetValue(v0);
    int ch=*(int*)v1.value;
    if (ch==0){return "";}
    else if (ch==1){return st;}
    char* out=malloc(strlen(st)*ch+1);
    strcpy(out,st);
    for (int i=0;i<ch-1;i++) {
        strcat(out,st);
    }
    out[strlen(st)*ch]='\0';
    return out;
}

char* HalSMCalculateVars_divStr(HalSMVariable v0,HalSMVariable v1)
{
    if (v1.type==HalSMVariableType_str){return StringReplace(HalSMVariable_GetValue(v0),HalSMVariable_GetValue(v1),"");}
    char* s0=HalSMVariable_to_str(v0);
    int i1=*(int*)v1.value;
    int ls0=strlen(s0);
    if(ls0==0||i1==0){return "";}
    else if(i1==1){return s0;}
    int lout=strlen(s0)/i1;
    char* out=malloc(lout+1);
    for (int i=0;i<lout;i++) {
        out[i]=s0[i];
    }
    out[lout]='\0';
    return out;
}

int HalSMCalculateVars_addInt(HalSMVariable v0,HalSMVariable v1)
{
    int i0;
    if (v0.type==HalSMVariableType_str) {
        i0=ParseInt(HalSMVariable_to_str(v0));
    } else {
        i0=*(int*)v0.value;
    }

    int i1;
    if (v1.type==HalSMVariableType_str) {
        i1=ParseInt(HalSMVariable_to_str(v1));
    } else {
        i1=*(int*)v1.value;
    }
    return i0+i1;
}

int HalSMCalculateVars_subInt(HalSMVariable v0,HalSMVariable v1)
{
    int i0;
    if (v0.type==HalSMVariableType_str) {
        i0=ParseInt(HalSMVariable_to_str(v0));
    } else {
        i0=*(int*)v0.value;
    }

    int i1;
    if (v1.type==HalSMVariableType_str) {
        i1=ParseInt(HalSMVariable_to_str(v1));
    } else {
        i1=*(int*)v1.value;
    }
    return i0-i1;
}

int HalSMCalculateVars_mulInt(HalSMVariable v0,HalSMVariable v1)
{
    int i0;
    if (v0.type==HalSMVariableType_str) {
        i0=ParseInt(HalSMVariable_to_str(v0));
    } else {
        i0=*(int*)v0.value;
    }

    int i1;
    if (v1.type==HalSMVariableType_str) {
        i1=ParseInt(HalSMVariable_to_str(v1));
    } else {
        i1=*(int*)v1.value;
    }
    return i0*i1;
}

int HalSMCalculateVars_divInt(HalSMVariable v0,HalSMVariable v1)
{
    int i0;
    if (v0.type==HalSMVariableType_str) {
        i0=ParseInt(HalSMVariable_to_str(v0));
    } else {
        i0=*(int*)v0.value;
    }

    int i1;
    if (v1.type==HalSMVariableType_str) {
        i1=ParseInt(HalSMVariable_to_str(v1));
    } else {
        i1=*(int*)v1.value;
    }
    return i0/i1;
}

float HalSMCalculateVars_addFloat(HalSMVariable v0,HalSMVariable v1)
{
    float f0;
    if (v0.type==HalSMVariableType_str) {
        f0=ParseFloat(HalSMVariable_to_str(v0));
    } else if (v0.type==HalSMVariableType_int) {
        f0=(float)(*(int*)v0.value);
    } else {
        f0=*(float*)v0.value;
    }

    float f1;
    if (v1.type==HalSMVariableType_str) {
        f1=ParseFloat(HalSMVariable_to_str(v1));
    } else if (v1.type==HalSMVariableType_int) {
        f1=(float)(*(int*)v1.value);
    } else {
        f1=*(float*)v1.value;
    }
    return f0+f1;
}

float HalSMCalculateVars_subFloat(HalSMVariable v0,HalSMVariable v1)
{
    float f0;
    if (v0.type==HalSMVariableType_str) {
        f0=ParseFloat(HalSMVariable_to_str(v0));
    } else if (v0.type==HalSMVariableType_int) {
        f0=(float)(*(int*)v0.value);
    } else {
        f0=*(float*)v0.value;
    }

    float f1;
    if (v1.type==HalSMVariableType_str) {
        f1=ParseFloat(HalSMVariable_to_str(v1));
    } else if (v1.type==HalSMVariableType_int) {
        f1=(float)(*(int*)v1.value);
    } else {
        f1=*(float*)v1.value;
    }
    return f0-f1;
}
float HalSMCalculateVars_mulFloat(HalSMVariable v0,HalSMVariable v1)
{
    float f0;
    if (v0.type==HalSMVariableType_str) {
        f0=ParseFloat(HalSMVariable_to_str(v0));
    } else if (v0.type==HalSMVariableType_int) {
        f0=(float)(*(int*)v0.value);
    } else {
        f0=*(float*)v0.value;
    }

    float f1;
    if (v1.type==HalSMVariableType_str) {
        f1=ParseFloat(HalSMVariable_to_str(v1));
    } else if (v1.type==HalSMVariableType_int) {
        f1=(float)(*(int*)v1.value);
    } else {
        f1=*(float*)v1.value;
    }
    return f0*f1;
}
float HalSMCalculateVars_divFloat(HalSMVariable v0,HalSMVariable v1)
{
    float f0;
    if (v0.type==HalSMVariableType_str) {
        f0=ParseFloat(HalSMVariable_to_str(v0));
    } else if (v0.type==HalSMVariableType_int) {
        f0=(float)(*(int*)v0.value);
    } else {
        f0=*(float*)v0.value;
    }

    float f1;
    if (v1.type==HalSMVariableType_str) {
        f1=ParseFloat(HalSMVariable_to_str(v1));
    } else if (v1.type==HalSMVariableType_int) {
        f1=(float)(*(int*)v1.value);
    } else {
        f1=*(float*)v1.value;
    }
    return f0/f1;
}

HalSMInteger HalSMInteger_FromSignedInteger(signed int value)
{
    HalSMInteger out;
    out.size=value<128&&value>-129?1:(value<32768&&value>-32769?2:(value<8388608&&value>-8388609?3:4));
    out.value=malloc(out.size);
    unsigned char* temp=(unsigned char*)&value;
    for (int i=0;i<out.size;i++){out.value[i]=temp[i];}
    return out;
}

HalSMInteger HalSMInteger_Add(HalSMInteger a,HalSMInteger b)
{
    HalSMInteger out;
    out.size=IntMathMax(a.size,b.size);
    out.value=malloc(out.size);
    signed short temps;
    unsigned char* tempa;
    unsigned char tempc=0;
    for (int i=0;i<IntMathMin(a.size,b.size);i++) {
        temps=a.value[i]+b.value[i];
        tempa=(unsigned char*)&temps;
        out.value[i]=tempa[0]+tempc;
        tempc=tempa[1];
    }
    if (a.size>b.size) {
        for (int i=b.size;i<a.size;i++) {out.value[i]=a.value[i];}
    } else if (a.size<b.size) {
        for (int i=a.size;i<b.size;i++) {out.value[i]=b.value[i];}
    }
    return out;
}

HalSMInteger HalSMInteger_Sub(HalSMInteger a,HalSMInteger b)
{
    HalSMInteger out;
    out.size=IntMathMax(a.size,b.size);
    out.value=malloc(out.size);
    signed short temps;
    unsigned char* tempa;
    unsigned char tempc=0;
    for (int i=0;i<IntMathMin(a.size,b.size);i++) {
        temps=a.value[i]-b.value[i];
        tempa=(unsigned char*)&temps;
        out.value[i]=tempa[0]+tempc;
        tempc=tempa[1];
    }
    if (a.size>b.size) {
        for (int i=b.size;i<a.size;i++) {out.value[i]=a.value[i];}
    } else if (a.size<b.size) {
        for (int i=a.size;i<b.size;i++) {out.value[i]=b.value[i];}
    }
    return out;
}