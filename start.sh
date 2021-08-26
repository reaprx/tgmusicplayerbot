echo "Cloning Repo, Please Wait..."
git clone https://github.com/reaprx/tgmusicplayerbot.git /tgmusicplayer
cd /tgmusicplayer
pip3 install -U -r requirements.txt
echo "Starting Bot, Please Wait..."
python3 main.py
