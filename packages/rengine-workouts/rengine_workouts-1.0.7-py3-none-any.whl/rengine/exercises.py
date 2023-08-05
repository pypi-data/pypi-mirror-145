"""Exercise object that can effectively be utilized in workout class"""
import random
from statistics import mean
from copy import deepcopy

import numpy as np
from .config import EXERCISE_CATEGORY_DATA, EquipmentAvailable, MuscleGroup
from .config import ExerciseLoad, ExerciseType, EXERCISE_DF
from .config import ExperienceLevel




def pick_random_exercise(
    muscle_groups_targeted: list[str], 
    exercise_type: ExerciseType, 
    allowed_loads: list[ExerciseLoad] = [ExerciseLoad.HEAVY, ExerciseLoad.MEDIUM, ExerciseLoad.LIGHT], 
    experience_levels = [ExperienceLevel.BEGINNER, ExperienceLevel.INTERMEDIATE, ExperienceLevel.EXPERIENCED], 
    equipment_available = EquipmentAvailable.ALL,
    excluded_exercise_names: list[str] = []
    ):
    """Picks random exercise based on many parameters"""
    global EXERCISE_DF
    df_copy = EXERCISE_DF.copy()
    if(equipment_available != EquipmentAvailable.ALL):  
        df_copy = df_copy[(df_copy.loc[:,equipment_available].sum(axis = 1) > 0)]
    df_with_exercises_of_muscle_group_targeted = df_copy[(df_copy.loc[:,muscle_groups_targeted].sum(axis = 1) > 0)]
    df_with_exercise_type = df_with_exercises_of_muscle_group_targeted[(df_with_exercises_of_muscle_group_targeted.loc[:,muscle_groups_targeted].sum(axis = 1) > 0)]
    df_with_experience_level = df_with_exercise_type[(df_with_exercise_type.loc[:,experience_levels].sum(axis = 1) > 0)]
    df_without_excluded_exercises = df_with_experience_level[~(df_with_experience_level["EXERCISE"].isin(excluded_exercise_names))]
    df_without_excluded_exercises = df_without_excluded_exercises.reindex()
    if(len(df_without_excluded_exercises) == 0):
        return None
    exercise_ind = random.randint(0, len(df_without_excluded_exercises.iloc[:,0]) - 1)
    exercise_chose = df_without_excluded_exercises.iloc[exercise_ind, :]
    return ExerciseFromTypePreset(exercise_chose["EXERCISE"], exercise_type, allowed_loads)

def listify_if_non_iterable(obj):
    obj = deepcopy(obj)
    if(type(obj) in [tuple, list]):
        return obj
    return [obj]
    
def get_variables_based_on_exercise_type_and_load(exercise_type: ExerciseType, exercise_load: ExerciseLoad):
    
    variables = EXERCISE_CATEGORY_DATA[exercise_type][exercise_load]

    return {
        "sets": variables["sets"],
        "rep_range": variables["rep_range"],
        "rest_time_range": variables["rest_time_range"]
    }


def get_muscle_group(exercise_name):
        """Finds muscle group based on exercise name. If does not exist returns 'UNKNOWN'"""
        exercise_row = EXERCISE_DF[EXERCISE_DF["EXERCISE"] == exercise_name].transpose()
        for muscle_group in MuscleGroup.ALL:
            if(exercise_row.loc[muscle_group].values[0]):
                return muscle_group
        return "UNKNOWN"


class Exercise:
    """Basic implementation of an exercise"""
    def __init__(self, exercise_name: str, sets, rep_range: tuple[int], rest_time_range: tuple[float], muscle_group: MuscleGroup = None):
        self.exercise_name = exercise_name
        self.sets = sets
        self.rep_range = rep_range
        self.rest_time_range = rest_time_range
        self.muscle_group = muscle_group

    @property
    def length(self):
        """Length in minutes. Currently with assumption that each set takes 1 minute"""
        rest_time = listify_if_non_iterable(self.rest_time_range)
        return self.sets * (1 + mean(rest_time))
    

    def __str__(self) -> str:
        return f"{{exercise_name: {self.exercise_name}, muscle_group: {self.muscle_group}, sets: {str(self.sets)}, rep_range: {str(self.rep_range)}, rest_time_range: {str(self.rest_time_range)}}}"
    

    
class ExerciseFromTypePreset(Exercise):
    """Similar to Exercise class but sets, rep_range and rest_time determined by ExerciseType"""
    def __init__(self, exercise_name: str, exercise_type: ExerciseType, allowed_loads: list[ExerciseLoad] = [ExerciseLoad.HEAVY, ExerciseLoad.MEDIUM, ExerciseLoad.LIGHT], exercise_load: ExerciseLoad = None):
        self.exercise_type = exercise_type
        self.exercise_load = exercise_load or self.pick_random_load(allowed_loads)
        super().__init__(exercise_name = exercise_name, muscle_group = get_muscle_group(exercise_name),**get_variables_based_on_exercise_type_and_load(self.exercise_type, self.exercise_load))

    


    def pick_random_load(self, allowed_loads):
        """Picks randomly the load based on ExerciseType and valid ExerciseLoad"""
        initial_probabilities = [EXERCISE_CATEGORY_DATA[self.exercise_type][load]["chance"] for load in allowed_loads]
        normalized_probabilities = [prob/sum(initial_probabilities) for prob in initial_probabilities]
        return np.random.choice(allowed_loads, p = normalized_probabilities)

    def __str__(self):
        return Exercise.__str__(self).rstrip("}") + f", exercise_type: {self.exercise_type}, exercise_load: {self.exercise_load}}}"


class StrengthExercise(ExerciseFromTypePreset):
    def __init__(self, exercise_name: str, allowed_loads: list[ExerciseLoad] = [ExerciseLoad.HEAVY, ExerciseLoad.MEDIUM, ExerciseLoad.LIGHT], exercise_load: ExerciseLoad = None):
        super().__init__(exercise_name = exercise_name, exercise_type = ExerciseType.STRENGTH, allowed_loads=allowed_loads, exercise_load=exercise_load)

class EnduranceExercise(ExerciseFromTypePreset):
    def __init__(self, exercise_name: str, allowed_loads: list[ExerciseLoad] = [ExerciseLoad.HEAVY, ExerciseLoad.MEDIUM, ExerciseLoad.LIGHT], exercise_load: ExerciseLoad = None):
        super().__init__(exercise_name = exercise_name, exercise_type = ExerciseType.ENDURANCE, allowed_loads=allowed_loads, exercise_load=exercise_load)

class HypertExercise(ExerciseFromTypePreset):
    def __init__(self, exercise_name: str, allowed_loads: list[ExerciseLoad] = [ExerciseLoad.HEAVY, ExerciseLoad.MEDIUM, ExerciseLoad.LIGHT], exercise_load: ExerciseLoad = None):
        super().__init__(exercise_name = exercise_name, exercise_type = ExerciseType.HYPERTROPHY, allowed_loads=allowed_loads, exercise_load=exercise_load)



    

    