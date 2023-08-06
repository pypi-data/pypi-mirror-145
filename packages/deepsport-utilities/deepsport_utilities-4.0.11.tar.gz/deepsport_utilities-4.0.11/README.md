# DeepSport Utilities toolkit

This toolkit offers a wide range of helpers to download, transform and use datasets following the DeepSport format.

## Installation
Package is released on PyPI for convenient installation:
```bash
pip install deepsport-utilities
```

## Available datasets

- [Basketball Instants Dataset](https://www.kaggle.com/datasets/deepsportradar/basketball-instants-dataset) is implemented by `deepsport_utilities.InstantsDataset` and provides raw images captured by the Keemotion system at different *instants*.
- Basketball Series Dataset, still hosted by Keemotion, will be soon available.
- Private Keemotion datasets

## Dataset format

The datasets are stored as a json file holding items metadata and multiple data files. The easiest approach to load the data is to use the `import_dataset` function as illustrated in the scripts provided in the `examples` folder.

The resulting datasets are based on `mlworkflow.Dataset`, a dataset implementation of (key, value) pairs where the keys are light and allow efficient querying of the dataset while the values contain the heavy data. For more information, refer to [mlworkflow repository](https://github.com/ispgroupucl/mlworkflow).

## Toolkit

Along with the provided datasets, the library comes with utility functions to draw Basketball courts on calibrated images.


## Contributing
This library is open-source and contributions are welcome. However, prior to any implementation, a discussion with the main maintainer Gabriel Van Zandycke is required.

## Authors and acknowledgment
While most of the library was developed by Gabriel Van Zandycke, this library benefited from the work of
- Maxime Istasse for the project initial kick-off 
- Cedric Verleysen for some functions in `court.py`
