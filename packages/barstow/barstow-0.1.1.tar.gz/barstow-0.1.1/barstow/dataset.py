from pathlib import Path
from typing import List, Optional, Union

import pyarrow as pa
import pyarrow.dataset as ds

from .io import write_dataset
from .query import Query


class Dataset:
    def __init__(
        self,
        location: Union[str, Path],
        partitioning: Optional[List[str]] = None,
        format: str = "parquet",
        filesystem: Optional[pa.fs.FileSystem] = None,
        batch_size: int = 1_000_000,
    ):
        self._location = location
        self._partitioning = partitioning
        self._format = format
        self._fs = filesystem
        self.batch_size = batch_size

        self._dataset = ds.dataset(
            location,
            format=format,
            filesystem=filesystem,
            partitioning=partitioning,
        )

    @property
    def location(self):
        return self._location

    @property
    def schema(self):
        return self._dataset.schema

    @property
    def nrows(self):
        return self._dataset.count_rows()

    @property
    def dataset(self):
        return self._dataset

    @property
    def query(self):
        """Returns a Query object that can be used to query the dataset"""
        return Query(self._dataset)

    def cast(self, **kwarg):
        """Cast a field in the dataset to another data type"""
        new_schema = self._dataset.schema

        for field, data_type in kwarg.items():
            idx = new_schema.get_field_index(field)
            new_schema = new_schema.set(idx, pa.field(field, data_type))

        if self._dataset.count_rows() > self.batch_size:
            # Dataset is too big to fit in memory, so we need to get it in batches and cast columns in each batch
            for batch in self._dataset.scanner(batch_size=self.batch_size).to_batches():
                table = pa.Table.from_batches([batch])
                new_table = table.cast(new_schema)

                dataset = ds.dataset(
                    [new_table],
                    schema=new_schema,
                )

                write_dataset(
                    dataset,
                    self.location,
                    new_schema,
                    format=self._format,
                    partitioning=self._partitioning,
                    filesystem=self._fs,
                    batch_size=self.batch_size,
                )
        else:
            table = self._dataset.to_table()
            new_table = table.cast(new_schema)

            dataset = ds.dataset([new_table], schema=new_schema)

            write_dataset(
                dataset,
                self.location,
                new_schema,
                format=self._format,
                partitioning=self._partitioning,
                filesystem=self._fs,
                batch_size=self.batch_size,
            )

    def to_pandas(self):
        """Returns the dataset as a Pandas DataFrame.

        Be aware that the dataset might be too large to fit in memory. Consider creating a query first."""
        return self._dataset.to_table().to_pandas()

    def __repr__(self):
        return f"Dataset(location={self._location})"
