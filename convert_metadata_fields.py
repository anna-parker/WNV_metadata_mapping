import pandas as pd
from dataclasses import dataclass
import click
import yaml


@dataclass
class Config:
    metadata_mapping: dict[str, dict[str, str]]
    default_values: dict[str, str]
    unused_fields: list[str]
    taxon_id_map: dict[str, str]


@click.command()
@click.option("--input", required=True, type=click.Path(exists=True))
@click.option("--config-file", required=True, type=click.Path(exists=True))
@click.option("--output", required=True, type=click.Path())
def map_fields(config_file, input, output):
    with open(config_file, encoding="utf-8") as file:
        full_config = yaml.safe_load(file)
        relevant_config = {key: full_config[key] for key in Config.__annotations__}
        config = Config(**relevant_config)
    # df = pd.read_csv(input, sep=",", dtype=str, keep_default_na=False)
    df = pd.read_excel(input)
    rename_map = {
        key: value["loculus_name"] for key, value in config.metadata_mapping.items()
    }
    df = df.rename(columns=rename_map)
    df = df.drop(columns=config.unused_fields)
    for column_name, default_value in config.default_values.items():
        df[column_name] = default_value
    restructure_contents = rename_map = {
        value["loculus_name"]: value["custom"]
        for value in config.metadata_mapping.values()
        if "custom" in value.keys()
    }
    for column, custom_string in restructure_contents.items():
        df[column] = df[column].apply(
            lambda value: custom_string.replace("${value}", str(value))
            if pd.notnull(value)
            else None
        )
    df["hostTaxonId"] = df["hostNameScientific"].apply(
        lambda x: config.taxon_id_map.get(x, None)
    )

    df.to_csv(output, sep="\t", index=False)


if __name__ == "__main__":
    map_fields()
