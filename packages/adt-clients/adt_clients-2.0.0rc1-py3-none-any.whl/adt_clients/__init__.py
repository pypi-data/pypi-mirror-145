__version__ = "2.0.0.rc1"

__all__ = [
    "AnalyticDatasetClient",
    "AnalyticDatasetModel",
    "AnalyticDatasetDefinitionClient",
    "AnalyticDatasetDefinitionModel",
    "AnalyticDatasetMergeRequestModel",
    "JoinType",
    "ColumnSelectionType",
    "Granularity",
    "OutputType",
    "AnalyticDatasetFormat",  # backwards compat
]

try:
    # Attempts to import the client class
    # Allowed to fail importing so the package metadata can be read for building
    from .analytic_dataset_client import AnalyticDatasetClient
    from .analytic_dataset_definition_client import AnalyticDatasetDefinitionClient
    from .models import (
        AnalyticDatasetModel,
        AnalyticDatasetDefinitionModel,
        AnalyticDatasetMergeRequestModel,
        Granularity,
        OutputType,
        AnalyticDatasetFormat,  # backwards compat
        JoinType,
        ColumnSelectionType,
    )
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass  # pragma: no cover
