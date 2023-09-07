.PHONY: all clone install make_bundle sync clean package

all: clone install make_bundle sync package

# 1. Create a directory named "bundles"
# 2. Clone the two repositories into it
clone:
	@echo "Creating 'bundles' directory..."
	@mkdir -p bundles

	@echo "Cloning repositories into 'bundles'..."
	@git clone git@github.com:deviant-syndrome/udmfio.git bundles/udmfio
	@git clone https://github.com/deviant-syndrome/wadflow.git bundles/wadflow

# 3. Install dependencies of udmfio using poetry
install:
	@echo "Installing dependencies for udmfio..."
	@cd bundles/udmfio && poetry install

# 4. Execute /make_bundle.sh from udmfio
make_bundle:
	@echo "Executing make_bundle.sh from udmfio..."
	@sh bundles/udmfio/make_bundle.sh

# 5. Set the environment variable BUNDLES_SOURCE_DIR
# 6. Execute sync_bundles.sh from the addon root
sync:
	@echo "Syncing bundles..."
	@export BUNDLES_SOURCE_DIR="$(shell pwd)/bundles" && sh sync_bundles.sh

# 7. Package the addon into a ZIP file (excluding the 'bundles' directory)
package:
	@echo "Packaging the addon..."
	@zip -r udmf_toolkit_addon.zip . -x "bundles/*"

clean:
	@echo "Cleaning up..."
	@rm -rf bundles
	@rm udmf_toolkit_addon.zip
