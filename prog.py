import git
import os

def cloneProject(userName, taskName, localPath):
  path = os.path.join(localPath, userName)
  print(path)
  try:
    os.makedirs(path)
    git.Git(path).clone(f'https://github.com/{userName}/{taskName}.git')
  except OSError:
    print ("Creation of the directory %s failed" % path)


def cloneProjectList(users, taskName, localPath):
  for user in users:
    cloneProject(user, taskName, localPath)

if __name__ == "__main__":
  users = ['sovaz1997', 'hallovarvara', 'inq666', 'torchik-slava']

  cloneProjectList(users, 'basic-js', os.path.join('.', 'data'))