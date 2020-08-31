# coding: utf8
from emmett.helpers import stream_dbfile
from backend import app, db

@app.route("/download/<str:filename>")
async def download(filename):
    stream_dbfile(db, filename)