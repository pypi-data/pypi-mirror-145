"""Update a storage dir with data from another storage dir."""

import logging
from pathlib import Path

import daiquiri
import typer

from dbnomics_data_model.storage.adapters.filesystem import FileSystemStorage
from dbnomics_data_model.storage.storage import update_strategies

app = typer.Typer()
logger = logging.getLogger(__name__)


@app.command()
def main(
    src_storage_dir: Path,
    dest_storage_dir: Path,
    category_tree_update_strategy: str = typer.Option("merge", envvar="CATEGORY_TREE_UPDATE_STRATEGY"),  # noqa: B008
    dataset_update_strategy: str = typer.Option("replace", envvar="DATASET_UPDATE_STRATEGY"),  # noqa: B008
    debug: bool = typer.Option(False, "--debug", help="display debug logging messages"),  # noqa: B008
    verbose: bool = typer.Option(False, "-v", "--verbose", help="display info logging messages"),  # noqa: B008
):
    """Update a storage directory with data from another storage directory."""
    daiquiri.setup()
    daiquiri.set_default_log_levels(
        [("dbnomics_data_model", logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING)]
    )

    if dataset_update_strategy not in update_strategies:
        logger.error(
            "Unsupported dataset update strategy %r (supported strategies: %r)",
            dataset_update_strategy,
            update_strategies,
        )
        raise typer.Abort()

    dest_storage = FileSystemStorage(dest_storage_dir)
    src_storage = FileSystemStorage(src_storage_dir)
    dest_storage.update(
        src_storage,
        category_tree_update_strategy=category_tree_update_strategy,
        dataset_update_strategy=dataset_update_strategy,
    )


if __name__ == "__main__":
    app()
