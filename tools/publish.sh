#!/usr/bin/env bash

name="cobalt"
version="${1}"
repo="${2}"
relname="${name}-${version}"

usage ()
{
    echo "usage: $0 <version> [repo]" >&2
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
    exit 1
}

if test -z "$version" ; then
    usage "Version number not supplied."
fi

if ! git tag | grep "^${relname}\$" >/dev/null 2>&1 ; then
    error "No tag was found for the ${relname} release."
fi

if test -n "${repo}" ; then
    if ! git remote | grep "^${repo}\$" >/dev/null 2>&1 ; then 
	error "\"${repo}\" is not a valid repository."
    fi
else
    repo=`git remote | head -1`
    if test -z "${repo}" ; then
	error "No remote git repository found."
    fi
    PS3="Answer: "
    echo ""
    echo "No remote repository was specified.  Would you like to use \"${repo}\"?"
    echo ""
    select ans in "yes" "no" ; do
	if test "${ans}" = "no" ; then
	    exit 1
	else
	    break
	fi
    done
fi

echo "Pushing the tag for the ${version} release to the \"${repo}\" repository"
git push ${repo} ${relname}
if test $? -ne 0 ; then
    error "Tag push failed." >&2
fi
