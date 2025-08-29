# #!/usr/bin/env bash
# set -e

# # If DATABASE_URL is present, re-point hostname to the compose 'db' service so the backend
# # can connect to postgres inside the Docker network. Falls back to existing DATABASE_URL
# # if parsing fails.
# if [ -n "$DATABASE_URL" ]; then
#   NEW_URL=$(python - "$DATABASE_URL" <<'PY'
# import sys, urllib.parse
# u=sys.argv[1]
# parsed=urllib.parse.urlparse(u)
# scheme=parsed.scheme
# user = parsed.username or ''
# password = parsed.password or ''
# dbpath = parsed.path.lstrip('/') if parsed.path else ''
# port = parsed.port or 5432
# if user and password and dbpath:
#     # Use 'db' as the host for the Postgres container
#     new_url = f"{scheme}://{user}:{password}@db:{port}/{dbpath}"
#     print(new_url)
# else:
#     print(u)
# PY
# )
#   export DATABASE_URL="$NEW_URL"
#   echo "Using DATABASE_URL=$NEW_URL"
# fi

# # Start the backend app (create_all will run on startup via FastAPI startup handler)
# exec python -u src/app.py
