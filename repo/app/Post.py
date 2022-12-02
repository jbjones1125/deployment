#myPost = Post(12345, "Wow this is a cool post")
#INSERT INTO postTable(post_id, post_time, etc...) VALUES (post.__postId, post.__postDateTime, etc...);
class Post:
  postId = 0  
  def __init__(self, userId, groupId, timeString, postText, tagString, imageLocation):
    Post.postId += 1
    self.__postId = Post.postId
    self.__postDateTime = timeString
    self.__poster = userId            # options: None(unused), Global, Group
    self.__groupAssociation = groupId #Zero if belonging to the global feed
    self.__postText = postText
    self.__postTags = tagString
    self.__postImage = imageLocation
    self.__postLikesCount = 0
    self.__postLikesTracker = []
    pass