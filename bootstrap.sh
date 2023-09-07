#!/bin/bash

# 1. Create a directory named "bundles"
echo "Creating 'bundles' directory..."
mkdir bundles

# 2. Clone the two repositories into it
echo "Cloning repositories into 'bundles'..."
git clone git@github.com:deviant-syndrome/udmfio.git bundles/udmfio
git clone https://github.com/deviant-syndrome/wadflow.git bundles/wadflow

# 3. Install dependencies of udmfio using poetry
echo "Installing dependencies for udmfio..."
cd bundles/udmfio || exit
poetry install
cd ../..

# 4. Execute /make_bundle.sh from udmfio
echo "Executing make_bundle.sh from udmfio..."
sh bundles/udmfio/make_bundle.sh

# 5. Set the environment variable BUNDLES_SOURCE_DIR
export BUNDLES_SOURCE_DIR="$(pwd)/bundles"

# 6. Execute sync_bundles.sh from the addon root
echo "Syncing bundles..."
sh sync_bundles.sh

# 7. Package the addon into a ZIP file (excluding the 'bundles' directory)
echo "Packaging the addon..."
zip -r udmf_toolkit_addon.zip . -x "bundles/*" -x ".*"

echo "Done!"
