#!/bin/bash

set -eu

DEVELOP_VERSION=$1
BRANCH_VERSION=$2

function semver_or_die() {
    local version
    version="$1"
    if [[ ! ${version} =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        printf >&2 'Error : %s is not a valid semver.\n' $version
        exit 1
    fi
}

semver_or_die $DEVELOP_VERSION
semver_or_die $BRANCH_VERSION


if [[ $# -eq 0 || -z $1 || -z $2 ]]; then
    printf >&2 'Error : missing required arguments.\n\n'
    exit 1
fi

IFS='.' read -r MAJOR MINOR PATCH <<< "$DEVELOP_VERSION"
MAJOR_DEVELOP=${MAJOR}
MINOR_DEVELOP=${MINOR}
PATCH_DEVELOP=${PATCH}
DEV_VERSION="$MAJOR_DEVELOP.$MINOR_DEVELOP.$PATCH_DEVELOP"

IFS='.' read -r MAJOR MINOR PATCH <<< "$BRANCH_VERSION"
MAJOR_BRANCH=${MAJOR}
MINOR_BRANCH=${MINOR}
PATCH_BRANCH=${PATCH}
BRANCH_VERSION="$MAJOR_BRANCH.$MINOR_BRANCH.$PATCH_BRANCH"


if [[ "$MAJOR_DEVELOP" < "$MAJOR_BRANCH" || "$MINOR_DEVELOP" < "$MINOR_BRANCH" ]]; then
    echo "Major Version cannot be decreased"
    exit 1
elif [[ "$MAJOR_DEVELOP" == "$MAJOR_BRANCH" && "$MINOR_DEVELOP" == "$MINOR_BRANCH" ]]; then
    PATCH_DEVELOP=$((PATCH_DEVELOP+1))
    NEW_VERSION="$MAJOR_DEVELOP.$MINOR_DEVELOP.$PATCH_DEVELOP"
    echo "::set-output name=stdout::New chart version $NEW_VERSION"
    VERSION=patch
elif [[ "$MAJOR_DEVELOP" == "$MAJOR_BRANCH" && "$MINOR_DEVELOP" < "$MINOR_BRANCH" ]]; then
    NEW_VERSION="$MAJOR_DEVELOP.$MINOR_DEVELOP.$PATCH_DEVELOP"
    echo "::set-output name=stdout::New chart version $NEW_VERSION"
    VERSION=minor
elif [[ "$MAJOR_DEVELOP" < "$MAJOR_BRANCH" ]]; then
    NEW_VERSION="$MAJOR_DEVELOP.$MINOR_DEVELOP.$PATCH_DEVELOP"
    echo "::set-output name=stdout::New chart version $NEW_VERSION"
    VERSION=major
fi

echo "NEWVERSION=$NEW_VERSION" >> $GITHUB_ENV
echo "VER_RELEASE=$VERSION" >> $GITHUB_ENV