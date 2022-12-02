from backend.app import securityQuestions


class SecurityQuestions:
  question1 = "In what city were you born?"
  question2 = "What is the name of your favorite pet?"
  question3 = "What is your mother's maiden name?"
  question4 = "What high school did you attend?"
  question5 = "What was the name of your elementary school?"
  question6 = "What was the make of your first car?"
  question7 = "What was your favorite food as a child?"
  question8 = "Where did you meet your spouse?"
  question9 = "What year was your father born?"
  question10 = "What year was your mother born?"
  questionList = [question1, question2, question3, question4, question5, question6, question7, question8, question9, question10]

  def __init__(self, userId, questionStringA, answerStringA, questionStringB, answerStringB):
    self.__userId = userId
    securityQuestion1 = questionStringA
    answer1 = answerStringA
    securityQuestion2 = questionStringB
    answer2 = answerStringB
    # self.__questionString = self.combineAB(questionStringA,questionStringB) #2 questions delimited via commas
    # self.__answerString = self.combineAB(answerStringA,answerStringB) #2 answers delimited via commas
    # self.sendDataToSQL(self.questionString)
    # self.sendDataToSQL(self.answerString)

  def sendDataToSQL(data: str):
    return  #temp for when I get with someone to send data to the SQL server

  def combineAB(stringA: str, stringB: str):
    return stringA + "," + stringB

# for i in range(0, len(SecurityQuestions.questionList)):
#   answer = SecurityQuestions.questionList[i]
#   print(SecurityQuestions.combineAB(str(i) , answer))