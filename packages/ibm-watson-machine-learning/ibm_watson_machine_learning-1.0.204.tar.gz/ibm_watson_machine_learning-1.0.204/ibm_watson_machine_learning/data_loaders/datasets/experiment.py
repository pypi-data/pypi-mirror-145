__all__ = ["ExperimentIterableDataset"]

import os
import pandas as pd

from typing import Union, Optional

from ibm_watson_machine_learning.helpers.connections.flight_service import (
    FlightConnection,
)
from ibm_watson_machine_learning.helpers.connections.local import LocalBatchReader

# Note: try to import torch lib if available, this fallback is done based on
# torch dependency removal request
try:
    from torch.utils.data import IterableDataset

except ImportError:
    IterableDataset = object
# --- end note


class ExperimentIterableDataset(IterableDataset):
    """
        This dataset is intended to be an Iterable stream from Flight Service.
        It should iterate over flight logical batches and menages by Connection class
        how batches are downloaded and created. It should take into consideration only 2 batches at a time.
        If we have 2 batches already downloaded, it should block further download
        and wait for first batch to be consumed.

        Example
        -------
        >>> experiment_metadata = {
        >>>     "prediction_column": 'species',
        >>>     "prediction_type": "classification",
        >>>     "project_id": os.environ.get('PROJECT_ID'),
        >>>     'wml_credentials': wml_credentials
        >>> }

        >>> connection = DataConnection(data_asset_id='5d99c11a-2060-4ef6-83d5-dc593c6455e2')


        >>> iterable_dataset = ExperimentIterableDataset(connection=connection,
        >>>                                              with_subsampling=False,
        >>>                                              experiment_metadata=experiment_metadata,
        >>>                                              normal_read=True)
    """

    connection: Union[FlightConnection, LocalBatchReader] = None

    def __init__(
        self,
        connection: "DataConnection",
        experiment_metadata: dict = None,
        with_subsampling: bool = False,
        batch_size: int = 1073741824 if "32" in os.environ.get("MEM", "32") else 104857600,  # 1GB in Bytes,
        binary_data: bool = False,
        number_of_batch_rows: int = None,
        stop_after_first_batch: bool = False,
        **kwargs,
    ):
        super().__init__()
        self.experiment_metadata = experiment_metadata
        self.with_subsampling = with_subsampling
        self._wml_client = None
        self.binary_data = binary_data

        # Note: turn on/off normal read for Flight Service (only one batch up to 1GB)
        self.normal_read = False
        if "normal_read" in kwargs:
            self.normal_read = kwargs["normal_read"]
        # --- end note

        self.authorized = self._wml_check_authorization()

        # Note: convert to dictionary if we have object from WML client
        if not isinstance(connection, dict):
            dict_connection = connection._to_dict()

        else:
            dict_connection = connection
        # --- end note

        # if number_of_batch_rows is provided, batch_size does not matter anymore

        if self.authorized:
            self.connection = FlightConnection(
                headers=self._wml_client._get_headers() if self._wml_client is not None else self.experiment_metadata.get("headers"),
                label=self.experiment_metadata.get("prediction_column"),
                learning_type=self.experiment_metadata.get("prediction_type"),
                params=self.experiment_metadata,
                project_id=self.experiment_metadata.get("project_id"),
                space_id=self.experiment_metadata.get("space_id"),
                asset_id=dict_connection.get("location", {}).get("id"),
                connection_id=dict_connection.get("connection", {}).get("id"),
                data_location=dict_connection,
                data_size_limit=batch_size,
                flight_parameters=kwargs.get("flight_parameters", {}),
                fallback_to_one_connection=kwargs.get(
                    "fallback_to_one_connection", True
                ),
                number_of_batch_rows=number_of_batch_rows,
                stop_after_first_batch=stop_after_first_batch,
                _wml_client=kwargs.get('_wml_client')
            )

        else:
            if (
                dict_connection.get("type") == "fs"
                and "location" in dict_connection
                and "path" in dict_connection["location"]
            ):
                self.connection = LocalBatchReader(
                    file_path=dict_connection["location"]["path"], batch_size=batch_size
                )

            else:
                raise NotImplementedError(
                    "For local data read please use 'fs' (file system) connection type."
                    "To use remote data read please provide 'experiment_metadata'."
                )

    def _wml_check_authorization(self) -> bool:
        """Check if we can authorize with WML."""
        if self.experiment_metadata is None:
            return False

        if self.experiment_metadata.get("wml_credentials") is not None:
            from ibm_watson_machine_learning import APIClient

            self._wml_client = APIClient(
                wml_credentials=self.experiment_metadata["wml_credentials"]
            )
            return True

        elif self.experiment_metadata.get("headers") is not None:
            return True

        else:
            return False

    def write(
        self, data: Optional[pd.DataFrame] = None, file_path: Optional[str] = None
    ) -> None:
        """
        Writes data into data source connection.

        Parameters
        ----------
        data: pandas DataFrame, optional
            Structured data to be saved in dat source connection. (Either 'data' or 'file_path' need to be provided)

        file_path: str, optional
            Path to the local file to be saved in source data connection (binary transfer).
            (Either 'data' or 'file_path' need to be provided)
        """
        if (data is None and file_path is None) or (
            data is not None and file_path is not None
        ):
            raise ValueError("Either 'data' or 'file_path' need to be provided.")

        if data is not None and not isinstance(data, pd.DataFrame):
            raise TypeError(
                f"'data' need to be a pandas DataFrame, you provided: '{type(data)}'."
            )

        if file_path is not None and not isinstance(file_path, str):
            raise TypeError(
                f"'file_path' need to be a string, you provided: '{type(file_path)}'."
            )

        if data is not None:
            self.connection.write_data(data)

        else:
            self.connection.write_binary_data(file_path)

    def __iter__(self):
        """Iterate over Flight Dataset."""
        if self.authorized:
            if self.normal_read:
                if self.binary_data:
                    return self.connection.read_binary_data()

                else:
                    return self.connection.read()

            elif self.with_subsampling:
                self.connection.enable_subsampling = True
                return self.connection.iterable_read()

            else:
                return self.connection.iterable_read()

        else:
            return (batch for batch in self.connection)
