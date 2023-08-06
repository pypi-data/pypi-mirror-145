"""Domain-level service to delete data related to a provider."""

import daiquiri

from dbnomics_solr.dbnomics_solr_client import DBnomicsSolrClient

__all__ = ["delete_provider_by_code"]


logger = daiquiri.getLogger(__name__)


def delete_provider_by_code(provider_code: str, *, dbnomics_solr_client: DBnomicsSolrClient):
    """Index Solr documents related to a provider."""
    logger.info("Deleting all the Solr documents related to the provider...", provider_code=provider_code)
    dbnomics_solr_client.delete_by_provider_code(provider_code)

    logger.debug("Committing deleted Solr documents...")
    dbnomics_solr_client.commit()
    logger.info("All the Solr documents related to the provider were deleted", provider_code=provider_code)
