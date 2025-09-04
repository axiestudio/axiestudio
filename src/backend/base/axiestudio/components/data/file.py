from copy import deepcopy
from typing import Any

from axiestudio.base.data.base_file import BaseFileComponent
from axiestudio.base.data.utils import TEXT_FILE_TYPES, parallel_load_data, parse_text_file_to_data
from axiestudio.io import BoolInput, FileInput, IntInput, Output
from axiestudio.schema.data import Data


class FileComponent(BaseFileComponent):
    """Hanterar laddning och bearbetning av enskilda eller zippade textfiler.

    Denna komponent stöder bearbetning av flera giltiga filer inom ett zip-arkiv,
    löser sökvägar, validerar filtyper och använder eventuellt flertrådning för bearbetning.
    """

    display_name = "Fil"
    description = "Laddar innehåll från en eller flera filer."
    documentation: str = "https://docs.axiestudio.org/components-data#file"
    icon = "file-text"
    name = "File"

    VALID_EXTENSIONS = TEXT_FILE_TYPES

    _base_inputs = deepcopy(BaseFileComponent._base_inputs)

    for input_item in _base_inputs:
        if isinstance(input_item, FileInput) and input_item.name == "path":
            input_item.real_time_refresh = True
            break

    inputs = [
        *_base_inputs,
        BoolInput(
            name="use_multithreading",
            display_name="[Föråldrad] Använd flertrådning",
            advanced=True,
            value=True,
            info="Sätt 'Bearbetningskonkurrens' större än 1 för att aktivera flertrådning.",
        ),
        IntInput(
            name="concurrency_multithreading",
            display_name="Bearbetningskonkurrens",
            advanced=True,
            info="När flera filer bearbetas, antalet filer att bearbeta samtidigt.",
            value=1,
        ),
    ]

    outputs = [
        Output(display_name="Rått innehåll", name="message", method="load_files_message"),
    ]

    def update_outputs(self, frontend_node: dict, field_name: str, field_value: Any) -> dict:
        """Visa dynamiskt endast relevant utdata baserat på antalet bearbetade filer."""
        if field_name == "path":
            # Add outputs based on the number of files in the path
            if len(field_value) == 0:
                return frontend_node

            frontend_node["outputs"] = []

            if len(field_value) == 1:
                # We need to check if the file is structured content
                file_path = frontend_node["template"]["path"]["file_path"][0]
                if file_path.endswith((".csv", ".xlsx", ".parquet")):
                    frontend_node["outputs"].append(
                        Output(display_name="Strukturerat innehåll", name="dataframe", method="load_files_structured"),
                    )
                elif file_path.endswith(".json"):
                    frontend_node["outputs"].append(
                        Output(display_name="Strukturerat innehåll", name="json", method="load_files_json"),
                    )

                # All files get the raw content and path outputs
                frontend_node["outputs"].append(
                    Output(display_name="Rått innehåll", name="message", method="load_files_message"),
                )
                frontend_node["outputs"].append(
                    Output(display_name="Filsökväg", name="path", method="load_files_path"),
                )
            else:
                # For multiple files, we only show the files output
                frontend_node["outputs"].append(
                    Output(display_name="Filer", name="dataframe", method="load_files"),
                )

        return frontend_node

    def process_files(self, file_list: list[BaseFileComponent.BaseFile]) -> list[BaseFileComponent.BaseFile]:
        """Bearbetar filer antingen sekventiellt eller parallellt, beroende på samtidighetsinställningar.

        Args:
            file_list (list[BaseFileComponent.BaseFile]): Lista över filer att bearbeta.

        Returns:
            list[BaseFileComponent.BaseFile]: Uppdaterad lista över filer med sammanslagen data.
        """

        def process_file(file_path: str, *, silent_errors: bool = False) -> Data | None:
            """Bearbetar en enskild fil och returnerar dess Data-objekt."""
            try:
                return parse_text_file_to_data(file_path, silent_errors=silent_errors)
            except FileNotFoundError as e:
                msg = f"Fil hittades inte: {file_path}. Fel: {e}"
                self.log(msg)
                if not silent_errors:
                    raise
                return None
            except Exception as e:
                msg = f"Oväntat fel vid bearbetning av {file_path}: {e}"
                self.log(msg)
                if not silent_errors:
                    raise
                return None

        if not file_list:
            msg = "Inga filer att bearbeta."
            raise ValueError(msg)

        concurrency = 1 if not self.use_multithreading else max(1, self.concurrency_multithreading)
        file_count = len(file_list)

        parallel_processing_threshold = 2
        if concurrency < parallel_processing_threshold or file_count < parallel_processing_threshold:
            if file_count > 1:
                self.log(f"Bearbetar {file_count} filer sekventiellt.")
            processed_data = [process_file(str(file.path), silent_errors=self.silent_errors) for file in file_list]
        else:
            self.log(f"Startar parallell bearbetning av {file_count} filer med samtidighet: {concurrency}.")
            file_paths = [str(file.path) for file in file_list]
            processed_data = parallel_load_data(
                file_paths,
                silent_errors=self.silent_errors,
                load_function=process_file,
                max_concurrency=concurrency,
            )

        # Use rollup_basefile_data to merge processed data with BaseFile objects
        return self.rollup_data(file_list, processed_data)
