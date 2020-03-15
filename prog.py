import git
import os

class UserTask:
  def __init__(self, userName, taskName, localPath):
    self.userName = userName
    self.taskName = taskName
    self.localPath = localPath

    self._cloneProject()
  
  def _cloneProject(self):
    self.path = os.path.join(self.localPath, self.userName)

    try:
      os.makedirs(self.path)
      git.Git(self.path).clone(f'https://github.com/{self.userName}/{self.taskName}.git')
    except OSError:
      print ("Creation of the directory %s failed" % self.path)


class UserList:
  def __init__(self, users, taskName, localPath):
    self.users = users
    self.taskName = taskName
    self.localPath = localPath
    self._createUserTasks()

  def _createUserTasks(self):
    self.usersTasks = []
    for user in self.users:
      self.usersTasks.append(UserTask(user, self.taskName, self.localPath))

if __name__ == "__main__":
  users = ['sovaz1997', 'hallovarvara', 'inq666', 'torchik-slava']
  userList = UserList(users, 'basic-js', os.path.join('.', 'data'))