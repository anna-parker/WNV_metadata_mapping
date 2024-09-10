# West Nile Virus - Metadata Mapping

This script transforms metadata according to `metadata_mapping.yaml` into the format expected by Pathoplexus (see https://pathoplexus.org/docs/concepts/metadataformat).

The script performs the following transformations:

1. sets default values for some Loculus metadata fields (values in `default_values`)
2. drops fields without a Loculus equivalent (fields in `unused_fields`)
3. maps metadata fields in `metadata_mapping` to their closest equivalent loculus metadata field (defined in `loculus_name`), if the `custom` subfield is specified the metadata values will be additionally modified, e.g.

```
'Trap Type':
    loculus_name: collectionDevice
    custom: "Mosquitos trapped using ${value}"
    description: 'The instrument or container used to collect the sample e.g. swab.'
```

will map `Trap Type: Light Trap` to `collectionDevice: Mosquitos trapped using Light Trap`.

## Installation

You can use this script in future by configuring a micromamba environment:

```
micromamba create -f environment.yml
micromamba activate wnv-convert
```

And then converting data in the excel file with the script:

```
python convert_metadata_fields.py --input all_successfully_sequenced.xlsx --output "converted_metadata.tsv" --config-file metadata_mapping.yaml
```

## Questions

1. Are the default values and mappings in the metadata_mapping.yaml accurate?
2. Do you have any information on the sequencingInstrument and sequencingProtocol used? This is not mandatory but is desired by INSDC. Also if you have details on authors or sequencedByContactName that would be great to give the data more attribution.
3. We will use your institution as your center name in ENA, please let us know if you would like to still modify this value. Center name is used by ENA as an identifier to facilitate the recognition and attribution of your sequences within the INSDC. It is important because if at any point in time Pathoplexus no longer exists and you need to modify your data you can use the center name to identify your group and request sequence revision.
