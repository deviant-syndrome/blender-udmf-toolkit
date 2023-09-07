#!/bin/bash

cd "$BUNDLES_SOURCE_DIR"/udmfio/ && pwd
rm -rf ./udmfio_bundled
./make_bundle.sh
cd - && pwd
cp -r $BUNDLES_SOURCE_DIR/udmfio/udmfio_bundled ./libs

cp -r $BUNDLES_SOURCE_DIR/wadflow/wadflow ./libs
