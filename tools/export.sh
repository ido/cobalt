#!/usr/bin/env bash

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
    usage "A version number was not supplied."
fi

if git tag | grep "^${relname}\$" >/dev/null 2>&1 ; then
    PS3="Answer: "
    echo ""
    echo "A tag for ${relname} already exists.  Would you like to replace it?"
    echo ""
    select ans in "yes" "no" ; do
        if test "$ans" = "no" ; then
	    exit 1
	else
	    git tag -d ${relname}
	    if test $? -ne 0 ; then
		error "Tag deletion failed.  Aborting."
	    fi
	    echo ""
	    break
	fi
    done
fi

tmpdir=`mktemp -d 'cobalt-export-XXXXXXXXXXXXXXXX'`
if test $? -ne 0 ; then
    error "Unable to create a temporary directory."
fi

echo "Tagging the ${version} release as ${relname}"
git tag -m "tagged ${version} release" ${relname} ${commit}
if test $? -ne 0 ; then
    error "Tagging failed.  Aborting." >&2
fi

echo "Extracting ${relname} from the git repository"
git archive --format=tar --prefix=${relname}/ ${relname} >${tmpdir}/git-archive.tar
if test $? -ne 0 ; then
    error "Extraction of \"${version}\" from the repository failed."
fi

echo "Untarring ${version} into ${tmpdir}"
( cd ${tmpdir} && tar xf git-archive.tar )
if test $? -ne 0 -o ! -d ${tmpdir}/${relname} ; then
    error "Untar of the archive extracted from the repository failed"
fi

echo "Adding the ChangeLog file"
git log --pretty=medium --name-status ${relname} >${tmpdir}/${relname}/ChangeLog
if test $? -ne 0 ; then
    error "Creation of ChangeLog failed."
fi

echo "Setting the version in the client programs and installation scripts"
( cd ${tmpdir}/${relname} && perl -p -i -e "s/\\\$Version\\\$/${version}/" \
    src/clients/*.py src/clients/POSIX/*.py setup.py misc/cobalt.spec )
if test $? -ne 0 ; then
    error "Version substitution failed."
fi

echo "Creating a tarball for the ${version} release"
gitwd=$PWD
( cd ${tmpdir} && tar czf ${gitwd}/${tarname} ${relname}/ )
if test $? -ne 0 ; then
    error "Creation of the tarball failed."
fi

# gpg --armor --output "${tarname}".gpg --detach-sig "${tarname}"
# scp "${tarname}"* login.mcs.anl.gov:/mcs/ftp/pub/"${name}"

( cd ${tmpdir} ; rm -rf ${relname} ; rm -f git-archive.tar ) ; rmdir ${tmpdir}

echo ""
echo "The release tarball, ${tarname}, is located in current working"
echo "directory.  Once you have tested and are satisfied with the release, run"
echo "'tools/publish.sh ${version}' to complete the process."
echo ""
