class UserWorkout:
    def __init__(self, userId, muscleGroup, workoutList):
        '''
        Takes a userID integer
        Takes a muscleGroup string
        Takes a workoutList dictionary
        '''
        self.__userId = int(userId)
        self.__muscleGroup = muscleGroup
        self.__workoutList = workoutList
    
    def getUserId(self):
        return self.__userId
    
    def getMuscleGroup(self):
        return self.__muscleGroup
    
    def setMuscleGroup(self, muscleGroup):
        self.__muscleGroup = muscleGroup
    
    def getWorkoutList(self):
        return self.__workoutList
    
    def setWorkoutList(self, workoutList):
        self.__workoutList = workoutList
    
    def getWorkoutFromList(self, workout):
        '''
        Gets a specified workout (string: workout) from dictionary and returns the details of the workout
        '''
        return self.__workoutList[workout]
    

