#! /usr/bin/env python3

"""Validate data of a storage directory."""

import logging
from itertools import chain
from pathlib import Path
from textwrap import indent
from typing import Iterator, List, Optional

import daiquiri
import typer
from toolz import take

from dbnomics_data_model.errors import DBnomicsDataModelError
from dbnomics_data_model.model.common import DatasetCode
from dbnomics_data_model.storage import Storage
from dbnomics_data_model.storage.adapters.filesystem import FileSystemStorage
from dbnomics_data_model.storage.errors import (
    CategoryTreeLoadError,
    DatasetMetadataLoadError,
    ProviderMetadataLoadError,
    ReleasesMetadataLoadError,
    StorageInitError,
)

app = typer.Typer()
logger = logging.getLogger(__name__)


@app.command()
def main(
    storage_dir: Path,
    datasets: List[DatasetCode] = typer.Option(  # noqa: B008
        [], envvar="DATASETS", help="Validate only those datasets"
    ),
    debug: bool = typer.Option(False, "--debug", help="Display debug logging messages"),  # noqa: B008
    series_limit: Optional[int] = typer.Option(  # noqa: B008
        None,
        envvar="SERIES_LIMIT",
        help="Maximum number of series to validate per dataset. If not set, validate all series.",
    ),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Display info logging messages"),  # noqa: B008
) -> None:
    """Validate data of a storage directory."""
    daiquiri.setup()
    daiquiri.set_default_log_levels(
        [("dbnomics_data_model", logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING)]
    )

    if series_limit is not None and series_limit <= 0:
        logger.error("series limit must be strictly positive, got %r", series_limit)
        raise typer.Abort()

    if series_limit is not None:
        logger.debug("Validating a maximum of %r series per dataset.", series_limit)

    logger.debug("Initializing storage from %r...", str(storage_dir))
    try:
        storage = FileSystemStorage(storage_dir)
    except StorageInitError:
        logger.exception("Could not initialize storage from %r", str(storage_dir))
        raise typer.Abort()

    exit_status_code = 0
    errors_iter = iter_storage_errors(storage, datasets=datasets, series_limit=series_limit)

    for error in errors_iter:
        exit_status_code = 1
        print(format_error_chain(error))  # noqa: T001

    raise typer.Exit(code=exit_status_code)


def format_error_chain(error: DBnomicsDataModelError) -> str:
    """Format the error chain with all causes as a tree."""
    depth = 0
    text = repr(error)
    current_error: BaseException = error

    while True:
        cause = current_error.__cause__
        if cause is None:
            break
        current_error = cause
        depth += 1
        text += "\n" + indent(repr(current_error), " " * 2 * depth)

    return text


def iter_category_tree_errors(storage: Storage) -> Iterator[DBnomicsDataModelError]:
    """Validate category tree."""
    logger.debug("Validating category tree...")

    try:
        storage.load_category_tree()
    except CategoryTreeLoadError as exc:
        yield exc
        return

    # Cross-entity checks

    yield from storage.check_dataset_references_of_category_tree(on_error="yield")


def iter_dataset_errors(
    storage: Storage,
    *,
    dataset_codes: List[DatasetCode],
    series_limit: Optional[int] = None,
) -> Iterator[DBnomicsDataModelError]:
    """Validata datasets of Storage."""
    dataset_count = storage.get_dataset_count()
    for dataset_index, dataset_code in enumerate(sorted(storage.iter_dataset_codes(on_error="log")), start=1):
        if dataset_codes and dataset_code not in dataset_codes:
            continue

        logger.debug("Validating dataset %r (%d/%d)...", dataset_code, dataset_index, dataset_count)

        yield from iter_dataset_metadata_errors(storage, dataset_code)
        yield from iter_series_errors(storage, dataset_code, series_limit=series_limit)


def iter_dataset_metadata_errors(storage: Storage, dataset_code: DatasetCode) -> Iterator[DBnomicsDataModelError]:
    """Validate dataset metadata."""
    logger.debug("Validating metadata of dataset %r...", dataset_code)

    try:
        storage.load_dataset_metadata(dataset_code)
    except DatasetMetadataLoadError as exc:
        yield exc


def iter_provider_metadata_errors(storage: Storage) -> Iterator[DBnomicsDataModelError]:
    """Validate provider metadata."""
    logger.debug("Validating provider metadata...")

    try:
        storage.load_provider_metadata()
    except ProviderMetadataLoadError as exc:
        yield exc


def iter_releases_metadata_errors(storage: Storage):
    """Validate releases metadata."""
    logger.debug("Validating releases metadata...")

    try:
        storage.load_releases_metadata()
    except ReleasesMetadataLoadError as exc:
        yield exc
        return

    # Cross-entity checks

    yield from storage.check_dataset_references_of_releases_metadata()


def iter_storage_errors(
    storage: Storage,
    *,
    datasets: List[DatasetCode],
    series_limit: Optional[int] = None,
) -> Iterator[DBnomicsDataModelError]:
    """Validate a Storage instance."""
    yield from chain(
        iter_provider_metadata_errors(storage),
        iter_category_tree_errors(storage),
        iter_releases_metadata_errors(storage),
        iter_dataset_errors(storage, dataset_codes=datasets, series_limit=series_limit),
    )


def iter_series_errors(
    storage: Storage,
    dataset_code: DatasetCode,
    *,
    series_limit: Optional[int] = None,
) -> Iterator[DBnomicsDataModelError]:
    """Validate series of a dataset, metadata and observations."""
    logger.debug("Validating series of dataset %r...", dataset_code)

    series_iter = storage.iter_dataset_series(dataset_code, on_error="yield", include_observations=True)

    if series_limit is not None:
        series_iter = take(series_limit, series_iter)

    yield from storage.check_dataset_series(dataset_code, series_iter)


if __name__ == "__main__":
    app()
