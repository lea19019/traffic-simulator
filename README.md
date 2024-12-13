# Traffic Lights Project CS 470


```bash
# Instructions to run simulator
python -m venv .venv
source .venv/bin/activate
pip install pygame
python simulator.py

# CURL command to send request to Tom Tom
curl -X 'GET' \
  "https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json?point=19.416682%2C-99.097782&unit=KMPH&openLr=false&key=${TOMKEY}" \
  -H 'accept: */*'
```

Coordinates of traffic lane in Mexico City
19.416682, -99.097782
19.417046, -99.097639
19.417005, -99.098338
[Google Maps Link](https://maps.app.goo.gl/DVwzAKLhCkY1rY9X7)

## To do

- Modify simulator.py to have dynamic traffic lights and traffic parameters 
- A traffic flow simulator (some sort of non-linear function)
- Given the traffic flow implement some sort of AI algorithm to change the waiting time in traffic lights

Bala Pilli and V. Adrian Castillo