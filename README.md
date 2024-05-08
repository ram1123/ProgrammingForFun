# ProgrammingForFun

## One time

```bash
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

## To Run

```bash
source venv/bin/activate
# For single maze
python mazes.py --mode single --dimension 10

# For multiple mazes
python mazes.py --mode multiple --range_start 5 --range_end 21 --number 11

deactivate
```
