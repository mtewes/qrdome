


# the exec bash is to keep the screen alive after the command has ended

screen -S qrdome -dm bash -c 'cd /home/mtewes/qrdome;
source /home/mtewes/qrdome-venv/bin/activate;
python qrdome.py;
exec bash'
sleep 2
echo "qrdome"

echo "Started."



