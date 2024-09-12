import pandas as pd
from dataclasses import dataclass
import click
import yaml


@dataclass
class Config:
    metadata_mapping: dict[str, dict[str, str]]
    default_values: dict[str, str]
    fields_to_drop: list[str]
    option_based_mapping: dict[str, list[dict[str, str]]]


@click.command()
@click.option("--input", required=True, type=click.Path(exists=True))
@click.option("--config-file", required=True, type=click.Path(exists=True))
@click.option("--output", required=True, type=click.Path())
def map_fields(config_file, input, output):
    with open(config_file, encoding="utf-8") as file:
        full_config = yaml.safe_load(file)
        relevant_config = {key: full_config[key] for key in Config.__annotations__}
        config = Config(**relevant_config)
    df = pd.read_excel(input)

    # Create loculus fields using option-based map
    # if multiple options exist, later options override previous ones
    for loculus_field, item_list in config.option_based_mapping.items():
        for item in item_list:
            if loculus_field not in df.columns:
                # Case 1: loculus_field does not exist
                if "map" in item:
                    df[loculus_field] = df[item["field"]].apply(
                        lambda x: item["map"].get(x, None)
                    )
                else:
                    df[loculus_field] = df[item["field"]].apply(
                        lambda x: item["value"]
                        if x >= item["start"] and x <= item["end"]
                        else None
                    )
            else:
                # Case 2: loculus_field exists, update only non-None values
                if "map" in item:
                    df[loculus_field] = df.apply(
                        lambda row: item["map"].get(
                            row[item["field"]], row[loculus_field]
                        )
                        if item["map"].get(row[item["field"]], None) is not None
                        else row[loculus_field],
                        axis=1,
                    )
                else:
                    df[loculus_field] = df.apply(
                        lambda row: item["value"]
                        if row[item["field"]] >= item["start"]
                        and row[item["field"]] <= item["end"]
                        else row[loculus_field],
                        axis=1,
                    )

    # Rename columns
    rename_map = {
        key: value["loculus_name"] for key, value in config.metadata_mapping.items()
    }
    df = df.rename(columns=rename_map)
    for column_name, default_value in config.default_values.items():
        df[column_name] = default_value
    # Reformat metadata values according to custom string
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
    # Drop unused columns
    df = df.drop(columns=config.fields_to_drop)

    df.to_csv(output, sep="\t", index=False)


if __name__ == "__main__":
    map_fields()
