import sys
import os

# ensure `src` is on the import path so Controller/Service packages resolve
ROOT = os.path.dirname(__file__)
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from Controller.TodoListController import TodoListController


def main():
    print("Python Path:", sys.path)
    app = TodoListController()
    app.run()

if __name__ == "__main__":
    main()
