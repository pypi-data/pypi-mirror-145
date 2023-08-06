import os
import warnings

ATLAS_ALGOLIA_APPLICATION_ID = os.environ.get("ATLAS_ALGOLIA_APPLICATION_ID", "")
ATLAS_ALGOLIA_API_KEY = os.environ.get("ATLAS_ALGOLIA_API_KEY", "")
ATLAS_ALGOLIA_INDEX_NAME = os.environ.get("ATLAS_ALGOLIA_INDEX_NAME", "")

if not ATLAS_ALGOLIA_APPLICATION_ID:
    warnings.warn("ATLAS_ALGOLIA_APPLICATION_ID environment variable is not set")

if not ATLAS_ALGOLIA_API_KEY:
    warnings.warn("ATLAS_ALGOLIA_API_KEY environment variable is not set")