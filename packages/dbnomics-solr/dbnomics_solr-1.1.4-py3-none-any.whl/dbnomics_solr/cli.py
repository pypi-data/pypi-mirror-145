#! /usr/bin/env python3

# dbnomics-solr: Index DBnomics data into Apache Solr for full-text and faceted search.
# By: Christophe Benz <christophe.benz@cepremap.org>
#
# Copyright (C) 2017-2020 Cepremap
# https://git.nomics.world/dbnomics/dbnomics-solr
#
# dbnomics-solr is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# dbnomics-solr is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""Index DBnomics data into Apache Solr for full-text and faceted search."""


import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import daiquiri
import typer
from dbnomics_data_model import DatasetCode
from dbnomics_data_model.storage.adapters.filesystem import FileSystemStorage, FileSystemStoragePool
from environs import Env

from dbnomics_solr import services

from .dbnomics_solr_client import DBnomicsSolrClient

INDEXATION = "INDEXATION"
DELETION = "DELETION"
GIT_MODE_TREE_STR = "040000"


@dataclass
class AppArgs:
    """Represent script arguments common to all commands."""

    solr_url: str
    debug: bool = False


app = typer.Typer()
app_args: Optional[AppArgs] = None


logger = daiquiri.getLogger(__name__)

env = Env()
env.read_env()  # read .env file, if it exists


@app.callback()
def main(
    debug: bool = typer.Option(False, help="Display DEBUG log messages."),
    solr_url: str = typer.Option(env.str("SOLR_URL", default="http://localhost:8983/solr/dbnomics"), show_default=True),
):
    """Index DBnomics data to Solr."""
    global app_args
    app_args = AppArgs(debug=debug, solr_url=solr_url)

    # Setup logging
    daiquiri.setup()
    logging.getLogger("dbnomics_solr").setLevel(logging.DEBUG if app_args.debug else logging.INFO)

    logger.debug("Using app args: %r", app_args)


@app.command()
def index_providers(
    storage_base_dir: Path,
    delete_obsolete_series: bool = typer.Option(
        env.bool("DELETE_OBSOLETE_SERIES", default=False),
        help="After indexation, delete series that were not created or updated.",
    ),
    force: bool = typer.Option(env.bool("FORCE", default=False), help="Always index data (ignore dir hashes)."),
    limit: int = typer.Option(env.str("LIMIT", default=None), help="Index a maximum number of datasets per provider."),
):
    """Index many providers to Solr from storage_base_dir.

    In storage_base_dir each child directory is considered as the storage directory
    of a provider.
    """
    assert app_args is not None  # it is set by "main" function

    storage_pool = FileSystemStoragePool(storage_base_dir)
    for storage in storage_pool.iter_storages():
        services.index_provider(
            storage, delete_obsolete_series=delete_obsolete_series, force=force, limit=limit, solr_url=app_args.solr_url
        )


@app.command()
def index_provider(
    storage_dir: Path,
    datasets: List[DatasetCode] = typer.Option(
        env.list("DATASETS", default=[]), "--dataset", help="Index only the given datasets."
    ),
    delete_obsolete_series: bool = typer.Option(
        env.bool("DELETE_OBSOLETE_SERIES", default=False),
        help="After indexation, delete series that were not created or updated.",
    ),
    excluded_datasets: List[DatasetCode] = typer.Option(
        env.list("EXCLUDED_DATASETS", default=[]), "--exclude-dataset", help="Do not index the given datasets."
    ),
    force: bool = typer.Option(env.bool("FORCE", default=False), help="Always index data (ignore dir hashes)."),
    limit: int = typer.Option(env.str("LIMIT", default=None), help="Index a maximum number of datasets."),
    start_from: DatasetCode = typer.Option(None, help="Start indexing from dataset code."),
):
    """Index a single provider to Solr from storage_dir."""
    assert app_args is not None  # it is set by "main" function

    if limit is not None and limit <= 0:
        typer.echo("limit option must be strictly positive")
        raise typer.Abort()

    if not storage_dir.is_dir():
        typer.echo(f"storage_dir {str(storage_dir)} not found")
        raise typer.Abort()

    storage = FileSystemStorage(storage_dir)

    dataset_codes = [
        dataset_code
        for dataset_code in sorted(storage.iter_dataset_codes(on_error="log"))
        if is_desired_dataset(dataset_code, datasets, excluded_datasets, start_from)
    ]

    services.index_provider(
        storage,
        dataset_codes=dataset_codes,
        delete_obsolete_series=delete_obsolete_series,
        force=force,
        limit=limit,
        solr_url=app_args.solr_url,
    )


@app.command()
def delete_provider(
    provider_code: Optional[str] = typer.Option(None, "--code"),
    provider_slug: Optional[str] = typer.Option(None, "--slug"),
):
    """Delete all documents related to a provider from Solr index.

    Deletes provider document but also dataset and series documents.
    """
    assert app_args is not None  # it is set by "main" function

    if bool(provider_code) == bool(provider_slug):
        typer.echo("one of 'code' or 'slug' options must be provided, but not both")
        raise typer.Abort()

    dbnomics_solr_client = DBnomicsSolrClient(app_args.solr_url)

    if provider_code is None and provider_slug is not None:
        provider_code = dbnomics_solr_client.query_provider_by_slug(provider_slug)["code"]
    assert isinstance(provider_code, str)

    services.delete_provider_by_code(provider_code, dbnomics_solr_client=dbnomics_solr_client)


def is_desired_dataset(dataset_code, datasets, excluded_datasets, start_from):
    """Apply script arguments to detemine if a dataset has to be indexed."""
    if datasets and dataset_code not in datasets:
        logger.debug("Skipping dataset %r because it is not mentioned by the --dataset option", dataset_code)
        return False
    if excluded_datasets and dataset_code in excluded_datasets:
        logger.debug("Skipping dataset %r because it is mentioned by the --exclude-dataset " "option", dataset_code)
        return False
    if start_from is not None and dataset_code < start_from:
        logger.debug("Skipping dataset %r because of the --start-from option", dataset_code)
        return False
    return True


if __name__ == "__main__":
    app()
