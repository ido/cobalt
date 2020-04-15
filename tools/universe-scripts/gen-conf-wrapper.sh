#!/bin/bash -e
# Generate a conf file wrapper for Cobalt commands.

usage="gen-conf-wrapper.sh suffix subdir conf_file [command_paths]"

if [ -z "$4" ]
then
  echo $usage
fi

suffix=$1
outdir=cmd-$suffix/$2
conf_file=$3

mkdir -p $outdir
for cmd in "${@:4}"
do
  cat > $outdir/$cmd-$suffix << EOF
#!/bin/bash
export COBALT_CONFIG_FILES=$conf_file
exec $cmd "\$@"
EOF
chmod 755 $outdir/$cmd-$suffix

done

