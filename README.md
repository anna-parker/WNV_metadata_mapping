# West Nile Virus - Metadata Mapping

This

```
micromamba create -f environment.yml
micromamba activate wnv-convert
```

Then use to convert data in the excel file:

```
python convert_metadata_fields.py --input all_successfully_sequenced.xlsx --output "converted_metadata.tsv" --config-file metadata_mapping.yaml
```
