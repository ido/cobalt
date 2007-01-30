#!/usr/bin/env sh

name="cobalt"
repo="https://svn.mcs.anl.gov/repos/${name}"
version="${1}"
expath="/tmp/${name}-${version}/"
tarname="/tmp/${name}-${version}.tar.gz"

if [ -z "$version" ] ; then
    echo "must supply version number"
    exit 1
fi
tagstr=`echo ${version} | sed -e 's/\./_/g'`
svn copy "${repo}/trunk" "${repo}/tags/${name}_${tagstr}" -m "tagged ${tagstr} release"
svn export . "${expath}"
svn log -v "${repo}/tags/${name}_${tagstr}" > "${expath}/ChangeLog"
cd "${expath}" ; perl -p -i -e "s/\\\$Version\\\$/${version}/" src/clients/*.py ; rm src/clients/*.bak ; ./autogen.sh
cd /tmp

tar czf "${tarname}" "${name}-${version}"
gpg --armor --output "${tarname}".gpg --detach-sig "${tarname}"
scp "${tarname}"* terra.mcs.anl.gov:/nfs/ftp/pub/"${name}"

