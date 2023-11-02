#!/bin/bash
# Check if the first argument is "ci", if not, execute the first four commands
if [ "$1" != "ci" ]; then
    cd "$BUNDLES_SOURCE_DIR"/udmfio/ && pwd
    rm -rf ./udmfio_bundled
    ./make_bundle.sh
    cd - && pwd
fi

# Continue with the rest of the script
cp -r $BUNDLES_SOURCE_DIR/udmfio/udmfio_bundled ./libs
cp -r $BUNDLES_SOURCE_DIR/wadflow/wadflow ./libs
