# West Nile Virus - Metadata Mapping

This script transforms metadata according to `metadata_mapping.yaml` into the format expected by Pathoplexus (see https://pathoplexus.org/docs/concepts/metadataformat).

The script performs the following transformations:

1. sets default values for some Loculus metadata fields (values in `default_values`)
2. drops fields without a Loculus equivalent (fields in `fields_to_drop`)
3. maps metadata fields in `metadata_mapping` to their closest equivalent loculus metadata field (defined in `loculus_name`), if the `custom` subfield is specified the metadata values will be additionally modified, e.g.

```
'Trap Type':
    loculus_name: collectionDevice
    custom: "Mosquitos trapped using ${value}"
    description: 'The instrument or container used to collect the sample e.g. swab.'
```

will map `Trap Type: Light Trap` to `collectionDevice: Mosquitos trapped using Light Trap`.

4. Constructs some loculus metadata fields using a more complicated option-based mapping (in `option_based_mapping`), i.e. if field X is equal to a set loculus field Y to b.

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

How to get a subsample of the data, e.g. sequence 03:

```
i=3
metadata_row=$((i + 1))
fasta_header=$((2*i -1))
fasta_seq=$((2*i))
sed -n "1p;${metadata_row}p" results/converted_metadata.tsv > wnv_submission$i.tsv
sed -n "${fasta_header}p;${fasta_seq}p" results/All_CT_sequenced_WNV.fasta > wnv_submission$i.fasta
```