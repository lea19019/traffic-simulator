# Traffic Lights AI Agent Project CS 470

The traffic in Mexico City is bad, we want to try to create an agent that will contribute to the
process of reducing this problem. There are certain lanes that cross each other, lane A is a
big avenue with constant car movements, lane B on the other side is a smaller street with
fewer car movement. Within this crossing we have traffic lights, some for the big lane and
some for the smaller, the traffic lights controlling the smaller lane have less amount of
time to passthrough, this is okay in general, but at some points we want to increase the
time and reduce the time for the bigger lane. The times when this is necessary vary over the
day and the demand. Usually, when people head home from work, during peak traffic
times, the traffic intensifies, and this is when we want to apply this agent. Since these
lanes are close to popular concert venues we get high traffic because of concerts too,
there are other factors, but this is just to point out that traffic is not caused only because of
work. The time and moments will vary, which is why we want “smart” traffic agents to know
when to distribute time at the traffic lights.

## Problem Statement

**Goal:** Find a set of configurations for "green times" in a pair of traffic lights

**Description:** We have lane X and lane Y, they're an intersection, at some T time
with some F_x and F_y traffic flow values we start getting higher values in the V_y traffic volume
for lane Y. This is beacause generally the "green time" for the Y traffic light has a shorter span
of time since is an smaller venue. We will have distinct F_x, F_y, V_x, V_y values at different
T times, those values are uncertain and don't really have a way to have way to know what value
will be at T time.
We must also notice there will be a K probability that the F value readings are correct and a
L probability value that the V values are also correct.

```json
States
state_i = { # This is the traffic light for the X axis
    green_time=35
    traffic_flow=??? # Some value of whatever the flow is at T time
    traffic_volume=?? # Some value of whatever is the volume V at the X lane in T time
}
state_j # The state for the Y axis
```
**Actions:** This is simple, we will just have the actions to increase or decrease the green time values

**Reward functon** (Not sure if this applies in an Optimization Search Algorithm)
This function will calculate the V traffic volume simulating the flow of the cars using the
traffic flow of cars, the current V traffic volumes of both i and j states, their "green times",
the speed in which car cross the lane (this is some avg time). We will set a time, let's say
5 minutes, in which we will calculate how will the V traffic volume be after that time using
the parameters mentioned above.

## Dev Environment
```bash
# Envrionment recommended instructions
python -m venv .venv
source .venv/bin/activate
python pip install -r requirements.txt

# Run the simulator
python -m tl        # Runs simulator alone
python -m tl -o     # Runs simulator with optimization search algorithm (in progress)
python -m tl -d     # Runs simulator with data generator (in progress)
python -m tl -o -d  # Runs simulator with optimization search algorithm and data generator (in progress)

```

## Notes

```bash 
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

- Implement Optimization Search Algorithm
- Incorporate data generator to simulator

## Learning Notes

Started this problem trying to figure out what where the values that should be used.
After choosing the traffic volume and the traffic flow as the parameters that can help us,
which in fact already saw earlier but was not able to understand how they relate to our task,
started figuring out how things should work.

It took some time to come to an idea of what the end goal was, which in fact it turned out, we 
don't really have an end goal, but an optimal state given our current readings. In any case, we
kept the work gathering the inputs and outputs there should be, here is where the V, F, probability
accuracy, car speeds, etc. values showed up. Since I saw probability values I thought of transition 
models and that lead to thinking in the MDP algorithm. After some lengthy thought process I realized
that my "transition model" was in fact, deterministic, meaning that I wasn't really dealing with an
MDP. I was dealing with an Optimization Search problem!

Here I still need to figure out some more things, how to fit this structure and variables to the
search algorithm, maybe Hill climbing, maybe Simulated Annealing? Still to figure out

The code implementation for our simulator using the AI algorithm would be something like this:

In the function `repeat()` inside the first while loop we will want to check what is the
current "traffic flow", which we could calculate using the `vehicles` object that contains all the 
cars that has in each lane, we would need to set some artificial probability accuracy value because
here we know for sure but not in the real world.
In our reading, if we notice the traffic volume is higher than some value we choose we want to run
our Optimization Search algorithm and find the best configuration, then upate accordingly.

Inside the algorithm we would use some artificial traffic flow or call the tomtom API to get
a value, in an ideal world, we could had gotten historical values and create some function based on
it. In any case, use that traffic flow value to calculate using the speed values and some crossing
value we also defined here.

Bala Pilli and V. Adrian Castillo