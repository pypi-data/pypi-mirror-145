import argparse
from rengine.config import WorkoutSplit
from rengine.workout_plan import generate_workout_plan

def run():
    parser = argparse.ArgumentParser("Rengine Client")
    parser.add_argument("workout_split", metavar="workout-split", action="store" , choices = WorkoutSplit.ALL, help="The split that will be generated. Choices include: "+ str(WorkoutSplit.ALL) + ".")
    parser.add_argument("time", metavar="time", action="store", help="The target time for each workout.")
    parser.add_argument("n_days", metavar="n-days", action="store", help="The number of days per week.")
    args = vars(parser.parse_args())
    try:
        print(generate_workout_plan(args["workout_split"], int(args["time"]), int(args["n_days"])))
    except KeyError:
        print("Invalid option for number of days for this workout split.")
    
    
