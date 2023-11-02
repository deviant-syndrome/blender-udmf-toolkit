#!/bin/bash

if [ "$1" = "ci" ]; then
    echo "Running bootstrap.sh in CI mode"
else
    echo "Running bootstrap.sh in normal mode"
fi

# 1. Create a directory named "bundles"
echo "Creating 'bundles' directory..."
mkdir bundles

# 2. Clone the two repositories into it
echo "Cloning repositories into 'bundles'..."
git clone https://github.com/deviant-syndrome/udmfio.git bundles/udmfio
git clone https://github.com/deviant-syndrome/wadflow.git bundles/wadflow

# 3. Install dependencies of udmfio using poetry
echo "Installing dependencies for udmfio..."
cd bundles/udmfio || exit
poetry install

# 4. Execute /make_bundle.sh from udmfio
echo "Executing make_bundle.sh from udmfio..."
sh make_bundle.sh

# 5. Set the environment variable BUNDLES_SOURCE_DIR
cd ../../ || exit
export BUNDLES_SOURCE_DIR="$(pwd)/bundles"
echo "BUNDLES_SOURCE_DIR set to $BUNDLES_SOURCE_DIR"

# 6. Execute sync_bundles.sh from the addon root
echo "Syncing bundles..."
sh sync_bundles.sh "$1"
# 7. Package the addon into a ZIP file (excluding the 'bundles' directory)
if [ "$1" = "ci" ]; then
    echo "Not packaging the addon because the first argument is not 'ci'"
    exit 0
fi
echo "Packaging the addon..."
zip -r udmf_toolkit_addon.zip . -x "bundles/*" -x ".*"

echo "Done!"
