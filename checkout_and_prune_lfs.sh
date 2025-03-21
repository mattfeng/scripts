#!/bin/bash
# Script: checkout_and_prune_lfs.sh
# Purpose: For each Git LFS pointer file in the working copy, check it out from the cache
# and then immediately prune its cached object.

# Exit immediately if a command exits with a non-zero status.
set -e

# Get a list of LFS tracked files (filenames only) using git lfs ls-files.
lfs_files=$(git lfs ls-files -n)

if [ -z "$lfs_files" ]; then
    echo "No Git LFS pointer files found in the working directory."
    exit 0
fi

echo "Found the following Git LFS pointer files:"
echo "$lfs_files"
echo ""
echo "-----"

# Iterate over each file, checking out from cache then pruning.
while IFS= read -r file; do
    # Check out the file to ensure its content is restored from LFS
    ERROR=$(git lfs checkout "$file" 2>&1 >/dev/null)

    if grep -q 'version https://git-lfs.github.com/spec/v1' "$file"; then
        echo "$ERROR"
        echo "Did not successfully checkout '$file', skipping"
        continue
    else
        echo "Checked out '$file'."
    fi
  
    # Extract the SHA-256 hash from the pointer file.
    # The pointer file contains a line like: "oid sha256:<hash>"
    sha_line=$(git lfs pointer --file "$file" 2>/dev/null | grep '^oid sha256:')
    # Remove the "oid sha256:" prefix to get the hash only.
    sha=${sha_line#*sha256:}
    sha=$(echo $sha)  # Trim any surrounding whitespace
  
    if [ -z "$sha" ]; then
        echo "No SHA found for file $file, skipping."
        continue
    fi
  
    # Construct the cache object path. The cached object is assumed to be stored as:
    # .git/lfs/objects/<first-two-characters-of-hash>/<full-hash>
    cache_dir=".git/lfs/objects/${sha:0:2}"
    cache_object="$cache_dir/$sha"
  
    # Remove the cache object if it exists
    if [ -f "$cache_object" ]; then
        echo "Removing cache object: $cache_object"
        rm "$cache_object"
    else
        echo "Cache object not found: $cache_object"
    fi

    echo "-----"

done <<< "$lfs_files"

echo "Done."
