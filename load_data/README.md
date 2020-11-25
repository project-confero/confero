# Messing around with data

## Steps:

1. Download Data

   ```bash
   ./sandbox/bin/download
   ```

1. Add data to DB

   Run the script:

   ```bash
   pipenv shell
   python sandbox/script.py
   ```

   Or use Juypter to run it piece-by-piece

1. Download a DB snapshot

   ```bash
   ./sandbox/bin/download.sh
   ```

1. Upload the DB snapshot somewhere like dropbox

   ```bash
   heroku pg:backups:restore 'https://dl.dropboxusercontent.com/s/FILE_ID/confero.dump?dl=0' DATABASE_URL -a project-confero --confirm project-confero
   ```
