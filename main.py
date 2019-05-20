from server.api import create


# Use AppEngine default entrypoint (gunicorn)
app = create()
