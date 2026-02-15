# Open Fibre Data Standard (OFDS) Public Data

A collection of fibre optic network data published in the [Open Fibre Data Standard](https://standard.ofds.info/) format. These datasets are digitized from publicly available network maps and provide structured, machine-readable representations of terrestrial fibre infrastructure.

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

## Contributing

Contributions and corrections are welcome. Please open an issue or pull request on the repository.
