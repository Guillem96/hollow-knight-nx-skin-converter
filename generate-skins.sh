#!/bin/bash

GAMEID=0100633007D48000
RELEASEDIR=release

counter=1
nSkins=$(ls -1 txt-packs/ | wc -l)

for skinPath in txt-packs/* ; do
    echo "-- Generate skins [${counter}/${nSkins}] ----------------------------"
    python hk-skin-nx.py \
        --dump-path ${GAMEID} \
        --skin "${skinPath}" --output ${RELEASEDIR}
    counter=$((counter+1))
done

counter=1

# Move to an "isolated area" so zip compressed files have the desired name
cwd=$(pwd)

ls -1 -d ${cwd}/${RELEASEDIR}/* | while read skinPath; do
    mkdir -p ${RELEASEDIR}/tmp/${GAMEID}/romfs
    cd ${RELEASEDIR}/tmp/

    echo "-- Compressing skins [${counter}/${nSkins}] -------------------------"
    zipFileName=$(echo ${skinPath} | tr -s '[:blank:]' '_')

    # Copy the needed files to the current working directory
    mkdir -p ${GAMEID}
    cp -r "${skinPath}/${GAMEID}/romfs" ${GAMEID}

    # Zip Game id folder
    zip -r ${zipFileName}.zip "${GAMEID}/"

    counter=$((counter+1))
done

rm -rf ${RELEASEDIR}/tmp