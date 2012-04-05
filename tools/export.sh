#!/usr/bin/env sh

name="cobalt"
version="${1}"
commit="${2}"
relname="${name}-${version}"
tarname="${relname}.tar.gz"

usage ()
{
    echo "usage: $0 <version> [commit]" >&2
    echo >&2
    echo "ERROR: $1" >&2
    echo >&2
    exit 1
}

error ()
{
    echo >&2
    echo "ERROR: $1" >&2
    echo >&2
    if test -n "$tmpdir" ; then
	( cd ${tmpdir} ; rm -rf ${relname} ; rm -f git-archive.tar ) ; rmdir ${tmpdir}
    fi
    exit 1
}

if test -z "$version" ; then
    usage "Version number not supplied."
fi

tmpdir=`mktemp -d`
if test $? -ne 0 ; then
    error "Unable to create temporary directory."
fi

echo "Tagging ${relname} release"
git tag -m "tagged ${version} release" ${relname} ${commit}
if test $? -ne 0 ; then
    error "Tag failed.  Aborting." >&2
fi

echo "Extracting ${relname} from git repository"
git archive --format=tar --prefix=${relname}/ ${relname} >${tmpdir}/git-archive.tar
if test $? -ne 0 ; then
    error "Extraction of tag ${version} from repository failed."
fi

echo "Untarring ${relname} into ${tmpdir}"
( cd ${tmpdir} && tar xf git-archive.tar )
if test $? -ne 0 -o ! -d ${tmpdir}/${relname} ; then
    error "Untar of archive extracted from the repository failed"
fi

echo "Adding ChangeLog file"
git log --pretty=medium --name-status ${relname} >${tmpdir}/${relname}/ChangeLog
if test $? -ne 0 ; then
    error "Creation of ChangeLog failed."
fi

echo "Setting version in client programs and installation scripts"
( cd ${tmpdir}/${relname} && perl -p -i -e "s/\\\$Version\\\$/${version}/" \
    src/clients/*.py src/clients/POSIX/*.py setup.py misc/cobalt.spec )
if test $? -ne 0 ; then
    error "Version substitution in clients failed."
fi

echo "Creating tarball for ${relname} release"
gitwd=$PWD
( cd ${tmpdir} && tar czf ${gitwd}/${tarname} ${relname}/ )
if test $? -ne 0 ; then
    error "Creation of tarball failed."
fi

# gpg --armor --output "${tarname}".gpg --detach-sig "${tarname}"
# scp "${tarname}"* login.mcs.anl.gov:/mcs/ftp/pub/"${name}"

( cd ${tmpdir} ; rm -rf ${relname} ; rm -f git-archive.tar ) ; rmdir ${tmpdir}
