#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# The first argument to the script is the optional Blender path
CUSTOM_BLENDER_PATH="$1"

# Function to run Blender with the given Python test script.
run_blender_test() {
  local test_file=$1
  local test_dir=$(dirname "$test_file")
  local test_name=$(basename "$test_file")

  # Use a subshell to change directories and run the test
  (
    cd "$test_dir" && \
    echo "Running tests in $test_name" && \
    "$BLENDER_PATH" --background --python-use-system-env --python-exit-code 14 --python "$test_name"
  )
  # The directory change is local to the subshell, so there's no need to 'popd'.
}


OS_NAME=$(uname)

if echo "$OS_NAME" | grep -q "Darwin"; then
  # MacOS systems
  BLENDER_PATH="/Applications/Blender.app/Contents/MacOS/Blender"
else
  # Rely on supplied path
  BLENDER_PATH="$CUSTOM_BLENDER_PATH/blender"
fi

# Verify that Blender exists at the specified path.
#if ! command -v "$BLENDER_PATH" &> /dev/null; then
#    echo "Blender could not be found. Please ensure it is installed and in your PATH."
#    exit 1
#fi

# Iterate over each .py file in the test directory and run the tests.
for file in tests/*.py; do
  run_blender_test "$file"
done

echo "All tests completed."
