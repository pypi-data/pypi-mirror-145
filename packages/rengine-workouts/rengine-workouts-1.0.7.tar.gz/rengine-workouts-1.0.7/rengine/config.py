from statistics import mean
from enum import Enum, auto
from .clean_data import clean_data

class MuscleGroup:
    BICEPS = "Biceps"
    BACK = "Back"
    CHEST = "Chest"
    TRICEPS = "Triceps"
    CALVES = "Calves"
    HAMSTRINGS = "Hamstrings"
    QUAD = "Quads"
    DELTOIDS = "Deltoids"
    ALL = ["Back", "Calves", "Chest", "Hamstrings", "Quads", "Deltoids", "Triceps", "Biceps"]
    LOWER_BODY = ["Calves", "Hamstrings", "Quads"]
    UPPER_BODY = ["Back", "Chest", "Deltoids", "Triceps", "Biceps"]

class ExerciseType:
    STRENGTH = "Strength"
    HYPERTROPHY = "Hypertrophy"
    ENDURANCE = "Endurance"
    ALL = ["Strength", "Hypertrophy", "Endurance"]


class ExerciseLoad:
    HEAVY = "heavy"
    MEDIUM = "medium"
    LIGHT = "light"
    ALL = ["heavy", "medium", "light"]


class ExperienceLevel:
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediated"
    EXPERIENCED = "Experienced"
    ALL = ["Beginner", "Intermediated", "Experienced"]

class WorkoutSplit:
    PPL = auto()
    BRO_SPLIT = auto()
    UPPER_LOWER_SPLIT = auto()
    FULL_BODY = auto()
    PHUl = auto()
    PHAT = auto()

class EquipmentAvailable:
    ALL = "all"
    BARBELL = "Barbell"
    DUMBBELLS = "Dumbells"
    EZ_BAR = "Ez-Bar"
    TRICEPS_BAR = "Triceps Bar"
    FLAT_BENCH = "Flat Bench"
    INCLINE_BENCH = "Incline Bench"
    ADJUSTABLE_BENCH = "Adjustable Bench"
    DECLINE_BENCH = "Decline Bench"
    WEIGHT_PLATES = "Weight Plates"
    AB_ROLLER_WHEEL = "Ab Roller Wheel"
    PULLUP_BAR = "Pullup Bar"
    DIP_BAR = "Dip Bar"
    SUSPENSION_TRAINER = "Suspension Trainer"
    GYMNASTIC_RINGS = "Gymnastic Rings"
    PLYO = "Plyo Box"
    MEDICINE = "Medicine Ball"
    KETTLEBELLS = "Kettlebells"
    CABLE_MACHINE = "Cable Machine"
    BICEP_CURL_MACHINE = "Bicep Curl Machine"
    SEATED_LEG_CURL_MACHINE = "Seated Leg Curl Machine"
    LYING_LEG_CURL_MACHINE = "Lying Leg Curl Machine"
    LEG_EXTENSION_MACHINE = "Leg Extension Machine"
    LEG_ABDUCTION_MACHINE = "Leg Abduction Machine"
    ROWING_MACHINE = "Rowing Machine"
    LAT_PULLDOWN_MACHINE = "Lat Pulldown Machine"
    LEG_PRESS_MACHINE = "Leg Press Machine"
    LYING_SQUAT_MACHINE = "Lying Squat Machine"
    HACK_SQUAT_MACHINE = "Hack Squat Machine"
    SEATED_CALF_MACHINE = "Seated Calf Machine"
    STANDING_CALF_MACHINE = "Standing Calf Machine"
    PEC_DEC_MACHINE = "Pec Fly Machine"
    CABLE_CROSSOVER_MACHINE ="Cable Crossover Machine"
    CHEST_PRESS_MACHINE = "Chest Press Machine"
    BUTT_BLASTER_MACHINE = "Butt Blaster Machine"
    AB_CRUNCH_MACHINE = "Ab Crunch Machine"
    PILATES_REFORMER_MACHINE = "Pilates Reformer Machine"
    CLIMBING_ROPE = "Climbing Rope"
    GLUTE_HAM_DEVELOPER = "Glute Ham Developer"
    HYPEREXTENSION_BENCH = "Hyperextension Bench"
    PREACHER_BENCH = "Preacher Bench"
    ABDOMINAL_BENCH = "Abdominal Bench"
    EXERCISE_BALL = "Exercise Ball"
    SQUAT_RACK = "Squat Rack"
    SMITH_MACHINE = "Smith Machine"
    POWER_RACK = "Power Rack"
    PUSH_UP_BARS = "Push Up Bars"
    RESISTANCE_BANDS = "Resistance Bands"
    MACHINE_ROW_MACHINE = "Machine Row Machine"
    CABLE_ROW_MACHINE = "Cable Row Machine"
    SHOULDER_PRESS_MACHINE = "Shoulder Press Machine"
    ASSISTED_DIP_MACHINE = "Assisted Dip Machine"
    DIP_MACHINE = "Dip Machine"
    TRICEP_EXTENSION_MACHINE = "Tricep Extension Machine"
    ASSISTED_DIP_MACHINE = "Assisted Pull-Up Machine"



EXERCISE_CATEGORY_DATA = {
    ExerciseType.STRENGTH:{
        ExerciseLoad.HEAVY: {
            "chance": 0.2,
            "sets": 5,
            "rep_range": (2,4),
            "rest_time_range": (3,5)
        },
        ExerciseLoad.MEDIUM: {
            "chance": 0.7,
            "sets": 4,
            "rep_range": (5,8),
            "rest_time_range": (2,4)
        },
        ExerciseLoad.LIGHT:{
            "chance": 0.1,
            "sets": 4,
            "rep_range": (9,10),
            "rest_time_range": (2,3)
        }
    },
    ExerciseType.HYPERTROPHY:{
        ExerciseLoad.HEAVY: {
            "chance": 0.1,
            "sets": 4,
            "rep_range": (6,7),
            "rest_time_range": (1,3)
        },
        ExerciseLoad.MEDIUM: {
            "chance": 0.8,
            "sets": 4,
            "rep_range": (8,12),
            "rest_time_range": (1,2)
        },
        ExerciseLoad.LIGHT:{
            "chance": 0.1,
            "sets": 3,
            "rep_range": (13,15),
            "rest_time_range": (1,2)
        }
    },
    ExerciseType.ENDURANCE:{
        ExerciseLoad.HEAVY: {
            "chance": 0.1,
            "sets": 4,
            "rep_range": (13,14),
            "rest_time_range": (1,2)
        },
        ExerciseLoad.MEDIUM: {
            "chance": 0.75,
            "sets": 3,
            "rep_range": (15,20),
            "rest_time_range": (1,2)
        },
        ExerciseLoad.LIGHT:{
            "chance": 0.15,
            "sets": 2,
            "rep_range": (21,30),
            "rest_time_range": (1,2)
        }
    }
}

"""
For time based conditions using following dictionary.
include_strength: Bool                  -> Whether or not auto generate should include the strength exercise
set_reductions: dict                    -> Set reductions for each exercise load in each exercise type
endurance_exercises_probabilities: list -> Each additional float in this list represents the probability the an endurance exercise is generated
caps: dict                              -> Limit the amount of exercises of a certain muscle group that can be generated based on the time of the workout
"""
TIME_BASED_CONDITIONS = {
    15: {
        "allowed_strength_loads": [],
        "set_reductions": {
            ExerciseType.HYPERTROPHY: {ExerciseLoad.HEAVY: 2, ExerciseLoad.MEDIUM: 2, ExerciseLoad.LIGHT:1}
        },
        "endurance_exercises_probabilities": [],
        "caps": {MuscleGroup.BICEPS: 1, MuscleGroup.TRICEPS:1, MuscleGroup.DELTOIDS:1, MuscleGroup.CALVES:1}
    },
    30: {
        "allowed_strength_loads": [],
        "set_reductions": {
            ExerciseType.HYPERTROPHY: {ExerciseLoad.HEAVY: 1, ExerciseLoad.MEDIUM: 1, ExerciseLoad.LIGHT:1}
        },
        "endurance_exercises_probabilities": [],
        "caps": {MuscleGroup.BICEPS: 1, MuscleGroup.TRICEPS:1, MuscleGroup.DELTOIDS:1, MuscleGroup.CALVES:1}
    },
    45: {
        "allowed_strength_loads": [ExerciseLoad.MEDIUM, ExerciseLoad.LIGHT],
        "set_reductions": {
            ExerciseType.STRENGTH: {ExerciseLoad.MEDIUM: 1, ExerciseLoad.LIGHT:1},
            ExerciseType.HYPERTROPHY: {ExerciseLoad.HEAVY: 1, ExerciseLoad.MEDIUM: 1, ExerciseLoad.LIGHT:1},
            ExerciseType.ENDURANCE: {ExerciseLoad.HEAVY: 1, ExerciseLoad.MEDIUM: 1}
        
        },
        "endurance_exercises_probabilities": [0.5],
        "caps": {MuscleGroup.BICEPS: 1, MuscleGroup.TRICEPS:1, MuscleGroup.DELTOIDS:1, MuscleGroup.CALVES:1}
    },
    60: {
        "allowed_strength_loads": ExerciseLoad.ALL,
        "set_reductions": {},
        "endurance_exercises_probabilities": [1],
        "caps": {MuscleGroup.BICEPS: 2, MuscleGroup.TRICEPS:2, MuscleGroup.DELTOIDS:2, MuscleGroup.CALVES:1}
    },
    75: {
        "allowed_strength_loads": ExerciseLoad.ALL,
        "set_reductions": {},
        "endurance_exercises_probabilities": [1],
        "caps": {MuscleGroup.BICEPS: 2, MuscleGroup.TRICEPS:2, MuscleGroup.DELTOIDS:2, MuscleGroup.CALVES:2}
    },
    90: {
        "allowed_strength_loads": ExerciseLoad.ALL,
        "set_reductions": {},
        "endurance_exercises_probabilities": [1],
        "caps": {MuscleGroup.BICEPS: 3, MuscleGroup.TRICEPS:3, MuscleGroup.DELTOIDS:3, MuscleGroup.CALVES:2}
    },
    105: {
        "allowed_strength_loads": ExerciseLoad.ALL,
        "set_reductions": {},
        "endurance_exercises_probabilities": [1,0.5],
        "caps": {MuscleGroup.BICEPS: 3, MuscleGroup.TRICEPS:3, MuscleGroup.DELTOIDS:3, MuscleGroup.CALVES:2}
    },
    120: {
        "allowed_strength_loads": ExerciseLoad.ALL,
        "set_reductions": {},
        "endurance_exercises_probabilities": [1,0.5],
        "caps": {MuscleGroup.BICEPS: 3, MuscleGroup.TRICEPS:3, MuscleGroup.DELTOIDS:3, MuscleGroup.CALVES:2}
    },
}



STRENGTH_EXERICSE_PRIORTIES = {
    MuscleGroup.HAMSTRINGS:{
        "squat":{
            "priority": 1,
            "variation_priorities":{
                "Squat Rack":"Barbell Squat",
                "Smith Machine":"Smith Machine Squat",
                "Dumbbells":"Dumbbell Squat"       #not in strength exercises
            }
        },
        "deadlift":{
            "priority": 1,
            "variation_pri orities":{
                "Romanian Deadlift": 1,
                "Sumo-Deadlift": 1,
                "Smith Machine Deadlift":2,
                "Smith Machine Sumo Deadlift":2
            }
        },
    

    

},
    "bench_press":{
        "priority": 1,
        "muscle_groups": [MuscleGroup.CHEST],
        "variation_priorities":{
            "Barbell Bench Press": 1,
            "Smith Machine Bench Press": 2,
            "Dumbell Bench Press":3   #Not in strength exercises
        }
    },
    "shoulder_press":{
        "priority": 2,
        "muscle_groups": [MuscleGroup.DELTOIDS],
        "variation_priorities":{
            "Barbell Shoulder Press": 1,
            "Smith Machine Shoulder Press": 2,   #Not in strength exercises
            "Dumbell Shoulder Press":3   #Not sure if this is the name
        }
    },
    "barbell_row":{
        "priority": 2,
        "muscle_groups": [MuscleGroup.BACK],
        "variation_priorities":{
            "Bent-Over Barbell Row",
            "Bent-Over Smith Machine Row",   #Not in strength exercises
            "Bent-Over Dumbbell Row"
        }
    },
    "pull_ups":{
        "priority": 2,
        "muscle_groups": [MuscleGroup.BACK],
        "variation_priorities":{
            "Weighted Pull-Ups":1
        }
    }
}



EXERCISE_DF = clean_data()



ExerciseTypeValues = dict(
    Strength = 3,
    Hypertrophy = 2,
    Endurance = 1,
)
ExerciseLoadValues = dict(
    heavy = 3,
    medium = 2,
    light = 1
)