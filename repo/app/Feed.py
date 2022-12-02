class Feed():
    def __init__(self, groupAssociation, searchString):
        self.__feedType = groupAssociation
        self.__searchModifier = searchString
    pass


def queryFeed(filter):
    """
    Queries the SQL database for a number of posts matching parameters passed through the string argument.
    :param filter: takes a string that will be pipe delimited as query parameters
    :return: Queried posts will be placed into an ordered list and returned
    """
    pass

def loadBufferedFeed(filter, positionPostId):
    """
    A continuation of the queryFeed() function. Queries more posts.
    :param filter: takes a string that will be pipe delimited as query parameters
    :param positionPostId: The range to which the previous queryFeed() or loadBufferedFeed() function returned
    :return: Queried posts will be placed into an ordered list and returned
    """
    pass

def getFilter():
    """
    Call the search querier to get a tag search string.
    :params: None
    :return: Provides the string used in queryFeed()
    """
    pass

def like(userId, postId):
    """
    Provides like counting functionality to posts by adding a user to a list of previous like'ers and increments the like counter.
    :param userId: Int of who is liking
    :param postId: Int of what post is being liked
    :return: None
    """
    pass

def deletePost(userId, postId):
    """
    Tells the SQL database to delete a post of a user when requested by a user. 
    :param userId: Int of who is requesting the deletion
    :param postId: Int of what post is being deleted
    :return: None
    """
    pass
