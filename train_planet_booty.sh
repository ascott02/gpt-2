source venv/bin/activate

PYTHONPATH=src python encode.py planet_booty_songs.txt planet_booty_songs.npz

PYTHONPATH=src python train.py --dataset planet_booty_songs.npz

ln -s checkpoint/run1 models/run1

