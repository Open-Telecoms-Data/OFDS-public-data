# OFDS Demonstration API

A FastAPI service that catalogs and serves [Open Fibre Data Standard](https://standard.ofds.info/) (OFDS) JSON datasets from this repository. GeoJSON is not served here; use the [map demo](https://ofds-demo.opentelecomdata.org) (PMTiles) for map clients.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/health` | Health check |
| `GET` | `/api/v1/catalog` | All networks with metadata and download links |
| `GET` | `/api/v1/countries` | Country directory names |
| `GET` | `/api/v1/countries/{country}/operators` | Operators in a country |
| `GET` | `/api/v1/networks/{country}/{operator}` | Network metadata |
| `GET` | `/api/v1/networks/{country}/{operator}/ofds-json` | Full OFDS JSON document |

Country and operator path segments match repository directory names (for example `Canada`, `Bell_Canada`).

Interactive OpenAPI docs are available at `/docs` when the server is running.

## Local development

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r api/requirements.txt
uvicorn api.main:app --host 127.0.0.1 --port 8742
```

Or:

```bash
python -m api.main
```

Smoke-test:

```bash
curl -s http://127.0.0.1:8742/api/v1/health
curl -s http://127.0.0.1:8742/api/v1/catalog | head
curl -s http://127.0.0.1:8742/api/v1/networks/Botswana/Bofinet/ofds-json | head -c 200
```

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATA_ROOT` | parent of `api/` (repo root) | Root containing `{Country}/{Operator}/` data |
| `UVICORN_HOST` | `127.0.0.1` | Bind address |
| `UVICORN_PORT` | `8742` | Bind port |
| `ENABLE_ADMIN_RELOAD` | unset | Set to `1` to enable `POST /api/v1/admin/reload` |

## Deploy behind nginx

1. Clone or update this repository on the server (example path: `/opt/OFDS-public-data`).
2. Create a virtualenv and install dependencies:

   ```bash
   cd /opt/OFDS-public-data
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r api/requirements.txt
   ```

3. Install the systemd unit (edit `WorkingDirectory`, `User`, and paths first):

   ```bash
   sudo cp api/deploy/systemd/ofds-api.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now ofds-api
   ```

4. Include the nginx snippet in your site config (for example next to the map demo at `/`):

   ```nginx
   include /opt/OFDS-public-data/api/deploy/nginx/ofds-api.conf;
   ```

   Then reload nginx:

   ```bash
   sudo nginx -t && sudo systemctl reload nginx
   ```

5. Verify:

   ```bash
   curl -s https://<host>/api/v1/health
   curl -s https://<host>/api/v1/catalog | head
   ```

The API listens on `127.0.0.1:8742` only. Public TLS and gzip for JSON responses are handled by nginx.

## Notes

- Data quality caveats apply as described in the [root README](../README.md); these maps are approximations.
- Authentication and field-level access profiles are not included in this version.
