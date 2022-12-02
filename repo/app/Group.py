class Group():

    groupId=1

    def __init__(self, groupName, owner):
        Group.groupId +=1
        self.__groupId = Group.groupId
        self.__groupName = groupName
        self.__groupOwner = owner
        self.__usersInGroup = []
        self.__usersWaiting = []
        self.__groupModerators = []

    def getCreator(self): 
        """
        :params: None
        :returns: userID of the group creator
        """
        return self.__groupOwner

    def removeUser(self, userId):
        """
        Removes the user from the group
        :params: userId(Int)
        :returns: None
        """
        self.__usersInGroup.remove(userId)

    def deleteGroup():
        """
        Deletes the group
        :params: None
        :returns: None
        """
        pass
    
    def acceptUser(self, userId):
        """
        Accepts the user into the group to post and view posts
        User must be in the waiting state
        :params: userId
        :returns: None
        """
        self.__usersWaiting.remove(userId)
        self.__usersInGroup.append(userId)


    def areWaiting(self):
        """
        :params: None
        :returns: A list of users currently waiting to join the group
        """
        return self.__usersWaiting