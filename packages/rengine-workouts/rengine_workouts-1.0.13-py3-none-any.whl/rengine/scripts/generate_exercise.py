import argparse
from rengine.config import ExerciseLoad, ExerciseType, MuscleGroup
from rengine.exercises import pick_random_exercise
import pprint

def run():
    parser = argparse.ArgumentParser("Rengine Client")
    parser.add_argument("exercise_type", metavar="exercise-type", action="store" , default=ExerciseType.HYPERTROPHY, choices = ExerciseType.ALL, help="Type of exercise that will be generated.")
    parser.add_argument("--muscle-groups-targetted", dest="muscle_groups_targetted", action="store", default=MuscleGroup.ALL, choices = MuscleGroup.ALL, help="The muscle groups that the exercise may work.", nargs="*")
    parser.add_argument("--exercise-loads", dest = "exercise_loads", action="store" , default=ExerciseLoad.ALL, choices = ExerciseLoad.ALL, help="The allowed loads that the exercise may have.", nargs="*")
    args = vars(parser.parse_args())
    pprint.pprint(pick_random_exercise(muscle_groups_targeted=args["muscle_groups_targetted"], exercise_type=args["exercise_type"], allowed_loads= args["exercise_loads"]).__dict__)
