#include<string.h>
#include<stdlib.h>
#include<unistd.h>
#include<libgen.h>
#include<stdio.h>

int main(int argc, char **argv){
  char **args;
  char *cmd;
  int i;

  unsetenv("IFS");
  unsetenv("LD_PRELOAD");
  unsetenv("LD_LIBRARY_PATH");
  unsetenv("PYTHONPATH");
  /* To disable the user's ability to override the default configuration file,
     uncomment the following line.  In addition, the argument processing code
     below should be modfied to strip the --config-files option from the
     arguments passed on to the python program. */
  /* unsetenv("COBALT_CONFIG_FILES"); */
  
  putenv("SSS_WRAPPER=1");
  args = malloc((argc+1) * sizeof(char *));
  for (i=1;i<argc;i++)
    args[i] = argv[i];
  args[i] = NULL;

  if ( ( cmd = basename(argv[0]) ) == NULL ) {
    perror(argv[0]);
    return 1;
  }
  if (asprintf(&args[0], "%s/%s.py", PROGPREFIX, cmd) == -1) {
    perror(argv[0]);
    return 1;
  }
  if (execv(args[0], args)) {
    perror(argv[0]);
    return 1;
  }

  return 0;
}
