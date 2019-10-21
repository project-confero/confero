# Messing around with data

## Steps:

1. Download Data
   ```bash
   wget https://www.fec.gov/files/bulk-downloads/2020/cn20.zip
   wget https://www.fec.gov/files/bulk-downloads/2020/ccl20.zip
   wget https://www.fec.gov/files/bulk-downloads/2020/indiv20.zip
   ```

1. Unzip Data

    ```bash
    unzip cn20.zip
    unzip ccl20.zip
    unzip itcont.txt

    mv cn.txt candidates.txt
    mv ccl.txt committees.txt
    mv by_date/itcont_2020_20190629_20190930.txt contributions.txt
    ```

1. Add the headers from [./headers](./headers) to the tip of the files
1. Install xsv
   ```bash
   brew install xsv
   ```
1. Install [Gephi](https://gephi.org/users/download) (if you want to generate network graphs)
1. Run commands in [./import.bash](./import.bash) (probably one at a time to make sure they work) to create a DB and format and import the data.
1. Run commands in [./export.bash](./export.bash)
