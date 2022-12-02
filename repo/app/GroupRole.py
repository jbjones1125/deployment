class GroupRole():
    
    def __init__(self, userId, waiting):
        self.__userId = userId
        self.__isWaiting = waiting
        self.__permissions = 0

    def getRole(userId):
        """
        :params: None
        :returns if the user has permissions (Boolean)
        """
        return userId.__permissions

    def setPermissions(userId, givePower=True):
        """
        Sets the specified user to have or not have moderator roles
        :params: UserId(Int), givePower(Boolean)
        :returns: None
        """
        userId.__permissions = givePower

    def isWaiting(userId):
        """
        Sets the status of a user as waiting to join a group
        :params: userId
        :returns: None
        """
        return userId.__isWaiting