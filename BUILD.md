# Build
Run the following commands. Tested with python 3.8.5
```console
git clone https://github.com/TomsonBoylett/simple-ical-filter.git

cd simple-ical-filter

python -m venv env

.\env\Scripts\activate

pip install -r requirements.txt

pyinstaller --noconfirm --onefile --windowed simple-ical-filter.py
```

simple-ical-filter.exe will be created in the dist folder