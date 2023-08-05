from pathlib import Path
from typing import List, Optional

import ert
import ert3


# pylint: disable=too-many-arguments
async def load_record(
    workspace: ert3.workspace.Workspace,
    record_name: str,
    record_file: Path,
    record_mime: str,
    record_is_directory: bool = False,
    smry_keys: Optional[List[str]] = None,
) -> None:

    collection = await ert.data.load_collection_from_file(
        file_path=record_file,
        mime=record_mime,
        is_directory=record_is_directory,
        smry_keys=smry_keys,
    )
    await ert.storage.transmit_record_collection(
        collection, record_name, workspace.name
    )


def sample_record(
    parameters_config: ert3.config.ParametersConfig,
    parameter_group_name: str,
    ensemble_size: int,
) -> ert.data.RecordCollection:
    distribution = parameters_config[parameter_group_name].as_distribution()
    return ert.data.RecordCollection(
        records=tuple(distribution.sample() for _ in range(ensemble_size))
    )
