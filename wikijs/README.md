# Wiki.js with Podman (SQLite)

This container setup uses SQLite to run Wiki.js without a separate database container.

## How to Launch

Run the following command from the root of this project:

```bash
podman run -d \
  --name wikijs \
  -p 8080:3000 \
  -v $(pwd)/wikijs/data:/wiki/storage \
  -e DB_TYPE=sqlite \
  requarks/wiki:2
```

## Configuration

- **Port**: `8080` (mapped to container `3000`)
- **Storage**: Persistent data is stored in `./wikijs/data`.
- **Database**: Uses SQLite via `DB_TYPE=sqlite`.
