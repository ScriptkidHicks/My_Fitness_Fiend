cd BackEnd; 
rm -rf ./venv;
python3 -m venv ./venv;
source venv/bin/activate.fish;
pip3 install -r requirements.txt;
python3 app.py;