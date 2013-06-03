#include<string.h>
#include<stdlib.h>
#include<unistd.h>
#include<libgen.h>
#include<stdio.h>
#include<ctype.h>

#if !defined(PYTHONPATH)
#   define PYTHONPATH ""
#endif

void strip_whitespace(char *s){
  int i, j;
  for (i=0, j=0; (s[j]=s[i]); j+=!isspace(s[i++]));
  return;
}


int main(int argc, char **argv){
  char **args;
  char *cmd;
  int i, match;
  FILE *f;
  char *cobalt_config_file;
  char line[1024];
  char python_exe[80];
  char poss_exe[80];
  char diag[80];

  strncpy(python_exe, "/usr/bin/python", 80);

  unsetenv("IFS");
  unsetenv("LD_PRELOAD");
  unsetenv("LD_LIBRARY_PATH");
  if (strlen(PYTHONPATH) > 0) {
      setenv("PYTHONPATH", PYTHONPATH, 1);
  } else {
      unsetenv("PYTHONPATH");
  }
  /* To disable the user's ability to override the default configuration file,
     uncomment the following line.  In addition, the argument processing code
     below should be modfied to strip the --config-files option from the
     arguments passed on to the python program. */
  /* unsetenv("COBALT_CONFIG_FILES"); */
  
  /* grab the python executable from the cobalt.conf file.  This should ultimately
   * be handled by a configure script.
   * --PMR */
  cobalt_config_file = getenv("COBALT_CONFIG_FILES");
  if (cobalt_config_file == NULL){
    cobalt_config_file = "/etc/cobalt.conf";
  }
  f = fopen(cobalt_config_file, "r");
  if(f == NULL){
    perror(argv[0]);
    return 1;
  }

  while ((fgets(line, 1024 ,f)) != NULL){
    match = sscanf(line, "[%[^]]]", diag);
    if (match && (!strncmp(diag, "components", 80))){
      break;
    }
  }
  while ((fgets(line, 1024 ,f)) != NULL){
    match = sscanf(line, "%[^=]=%s", diag, poss_exe);
    if (match != 2){
      match = sscanf(line, "%[^:]:%s", diag, poss_exe);
    }
    strip_whitespace(diag);
    strip_whitespace(poss_exe);
    if (match && (!strncmp(diag, "python", 80))){
      strncpy(python_exe, poss_exe, 80);
      break;
    }
    if (sscanf(line, "[%[^]]]", diag))
      break;
  }
  fclose(f);

  putenv("SSS_WRAPPER=1");
  args = malloc((argc+3) * sizeof(char *));
  /*prepend the python override*/
  args[0] = python_exe;
  args[1] = "-E";
  for (i=1;i<argc;i++)
    args[i+2] = argv[i];
  args[i+2] = NULL;
  if ( ( cmd = basename(argv[0]) ) == NULL ) {
    perror(argv[0]);
    return 1;
  }
  if (asprintf(&args[2], "%s/%s.py", PROGPREFIX, cmd) == -1) {
    perror(argv[0]);
    return 1;
  }
  /*for (i=0;i<argc+3;++i){
    printf("%s ", args[i]);
  }
  printf("\n");*/
  if (execv(args[0], args)) {
    perror(argv[0]);
    return 1;
  }

  return 0;
}
