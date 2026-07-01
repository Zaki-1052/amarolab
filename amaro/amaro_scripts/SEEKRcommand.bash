echo "running fwd 9"
python hsp90seekr_fwd.py 9
echo "running rev 8"
python hsp90seekr_rev.py 8 10
echo "running fwd 8"
python hsp90seekr_fwd.py 8
echo "dig deeper 8"
python dig_deeper.py 8 ~/Seekrhsp90_lastframe/seekr_calc.pickle similar ~/thehsp90/holo.parm7 ~/thehsp90/holo.rst7 2N6

echo "umbrella 7 npt"
python hsp90newseekr_umbrella.py 7 npt 100000
echo "umbrella 7 nvt"
python hsp90newseekr_umbrella.py 7 nvt 100000000
echo "rev 7"
python hsp90seekr_rev.py 7
echo "running fwd 7"
python hsp90seekr_fwd.py 7
echo "dig deeper 7"
python dig_deeper.py 7 ~/Seekrhsp90_lastframe/seekr_calc.pickle similar ~/thehsp90/holo.parm7 ~/thehsp90/holo.rst7 2N6

echo "umbrella 6 npt"
python hsp90newseekr_umbrella.py 6 npt 100000
echo "umbrella 6 nvt"
python hsp90newseekr_umbrella.py 6 nvt 100000000
echo "rev 6"
python hsp90seekr_rev.py 6
echo "running fwd 6"
python hsp90seekr_fwd.py 6
echo "dig deeper 6"
python dig_deeper.py 6 ~/Seekrhsp90_lastframe/seekr_calc.pickle similar ~/thehsp90/holo.parm7 ~/thehsp90/holo.rst7 2N6

echo "umbrella 5 npt"
python hsp90newseekr_umbrella.py 5 npt 100000
echo "umbrella 5 nvt"
python hsp90newseekr_umbrella.py 5 nvt 100000000
echo "rev 5"
python hsp90seekr_rev.py 5
echo "running fwd 5"
python hsp90seekr_fwd.py 5
echo "dig deeper 5"
python dig_deeper.py 5 ~/Seekrhsp90_lastframe/seekr_calc.pickle similar ~/thehsp90/holo.parm7 ~/thehsp90/holo.rst7 2N6

echo "umbrella 4 npt"
python hsp90newseekr_umbrella.py 4 npt 100000
echo "umbrella 4 nvt"
python hsp90newseekr_umbrella.py 4 nvt 100000000
echo "rev 4"
python hsp90seekr_rev.py 4 100
echo "running fwd 4"
python hsp90seekr_fwd.py 4
echo "dig deeper 4"
python dig_deeper.py 4 ~/Seekrhsp90_lastframe/seekr_calc.pickle similar ~/thehsp90/holo.parm7 ~/thehsp90/holo.rst7 2N6

echo "umbrella 3 npt"
python hsp90newseekr_umbrella.py 3 npt 100000
echo "umbrella 3 nvt"
python hsp90newseekr_umbrella.py 3 nvt 100000000
echo "rev 3"
python hsp90seekr_rev.py 3 100
echo "running fwd 3"
python hsp90seekr_fwd.py 3
echo "dig deeper 3"
python dig_deeper.py 3 ~/Seekrhsp90_lastframe/seekr_calc.pickle similar ~/thehsp90/holo.parm7 ~/thehsp90/holo.rst7 2N6

echo "umbrella 2 npt"
python hsp90newseekr_umbrella.py 2 npt 100000
echo "umbrella 2 nvt"
python hsp90newseekr_umbrella.py 2 nvt 100000000
echo "rev 2"
python hsp90seekr_rev.py 2
echo "running fwd 2"
python hsp90seekr_fwd.py 2
echo "dig deeper 2"
python dig_deeper.py 2 ~/Seekrhsp90_lastframe/seekr_calc.pickle similar ~/thehsp90/holo.parm7 ~/thehsp90/holo.rst7 2N6

echo "umbrella 1 npt"
python hsp90newseekr_umbrella.py 1 npt 1000000
echo "umbrella 1 nvt"
python hsp90newseekr_umbrella.py 1 nvt 100000000
echo "rev 1"
python hsp90seekr_rev.py 1
echo "running fwd 1"
python hsp90seekr_fwd.py 1
echo "dig deeper 1"
python dig_deeper.py 1 ~/Seekrhsp90_lastframe/seekr_calc.pickle similar ~/thehsp90/holo.parm7 ~/thehsp90/holo.rst7 2N6
