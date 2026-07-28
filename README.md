# Open Fibre Data Standard (OFDS) Public Data

A collection of fibre optic network data published in the [Open Fibre Data Standard](https://standard.ofds.info/) format. These datasets are digitized from publicly available network maps and provide structured, machine-readable representations of terrestrial fibre infrastructure.  Datasets here are compliant with [version 0.4](https://standard.ofds.info/en/0.4/) of the Open Fibre Data Standard.

## About OFDS

The Open Fibre Data Standard is a common language for describing fibre optic networks. It addresses the lack of readily available, usable data on fibre infrastructure and enables interoperability, transparency, and informed decision-making in broadband expansion efforts.

## File Formats

For each network, data is provided in three formats:

- **`*_ofds-json_*.json`** — Full OFDS-compliant JSON (networks, nodes, spans)
- **`*_ofds-nodes_*.geojson`** — Network nodes as GeoJSON (Points of Presence)
- **`*_ofds-spans_*.geojson`** — Network spans/links as GeoJSON (line segments)

## Data Quality

These maps are digitized from publicly available sources and are **approximations**, not authoritative network records. Points of Presence (PoPs) may be approximate; routes between them are often notional rather than exact. See each operator's README for specific caveats.

## Resources

- [OFDS Specification](https://standard.ofds.info/)
- [OFDS Schema](https://github.com/Open-Telecoms-Data/open-fibre-data-standard)
- [How to Publish OFDS Data](https://standard.ofds.info/en/latest/guidance/publication.html)

## Workflow

The `generate-pmtiles.yml` GitHub Action workflow automatically generates a PMTiles file containing fibre network data organized by operator. It processes GeoJSON files from this repository's country/operator directory structure, combining both nodes and spans for each operator into consolidated artifacts.

The workflow follows a predictable pattern: countries are represented by top-level directories, with each country containing subdirectories for different operators. For each operator, the workflow locates files containing "nodes" and "spans" in their filenames and assigns them to a layer named using the `{country}_{operator}` convention. The workflow then uses [Tippecanoe](https://github.com/felt/tippecanoe) to generate PMTiles with appropriate zoom levels and density settings, uploads the results to Amazon S3, and invalidates the CloudFront cache.

Outputs include:

- `ofds_spans_by_layer.pmtiles` — spans organized as one vector layer per operator
- `ofds_nodes_combined.geojson` / `ofds_nodes_combined.pmtiles` — all nodes combined
- `pmtiles_metadata.json` — build metadata

These artifacts power the interactive map at [ofds-demo.opentelecomdata.org](https://ofds-demo.opentelecomdata.org).

## API

A demonstration HTTP API in [`api/`](api/) catalogs networks and serves OFDS JSON (not GeoJSON). See [`api/README.md`](api/README.md) for local development and nginx deployment.

Once deployed behind nginx, the base path is `/api/v1/` (for example `GET /api/v1/catalog` and `GET /api/v1/networks/{country}/{operator}/ofds-json`).

## Contributing

Contributions and corrections are welcome. Please open an issue or pull request on the repository.
