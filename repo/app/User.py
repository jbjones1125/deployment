class User():
    def __init__(self, firstName, lastName, email, password):
        self.id = 0
        self.__firstName = firstName    # string
        self.__lastName = lastName      # string
        self.__email = email            # string
        self.__nickname = None          # string
        self.__password = password      # string | password is hashed before creating user
        self.__roles = []               # List of Roles

    def deleteUser(self, userId):
        '''
        Deletes an instance of the User class
        :param name: userId
        :return: None
        '''
        pass

    def setUserRole(self, role):
        '''
        Add a role to a user
        :param name: role of type SiteRole or GroupRole
        :return: None
        '''
        pass
    def getUserRoles(self, userId):
        '''
        :param userId: string user ID
        :return: list of a user's roles
        '''
    def deleteUserRole(self, role):
        '''
        Removes a role from a user
        :param name: SiteRole or GroupRole
        '''
        pass

    def hashPassword(self, password):
        '''
        Hashes a given password for secure storing
        :param name: password string
        :return: hashed password string
        '''
        pass

    '''
    Setters and Getters
    :param ____: All strings
    :return: Getters return strings
    '''
    def setUserId(self):
        pass

    def setfirstName(self):
        pass

    def setLastName(self):
        pass

    def setEmail(self):
        pass

    def setNickname(self):
        pass

    def setPassword(self):
        pass

    def getUserId(self):
        pass

    def getfirstName(self):
        pass

    def getLastName(self):
        pass

    def getEmail(self):
        pass

    def getNickname(self):
        pass

    def getPassword(self):
        pass