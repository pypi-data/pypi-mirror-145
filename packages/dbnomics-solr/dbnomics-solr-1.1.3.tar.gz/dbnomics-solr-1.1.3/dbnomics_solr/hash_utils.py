"""Hash utils."""

from pathlib import Path

from dirhash import dirhash


def compute_dir_hash(dir_path: Path) -> str:
    """Compute a hash for a directory in an opinionated way.

    Follows the [dirhash standard](https://github.com/andhus/dirhash).
    """
    return dirhash(dir_path, algorithm="sha1")
