# Write your code here
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)


def print_tasks(cur_row):
    if cur_row:
        for cur_index, cur_item in enumerate(cur_row):
            print(f"{cur_index + 1}. {cur_item}")
    else:
        print("Nothing to do!")
    print()


def print_tasks_with_deadline(cur_row, msg=None):
    if cur_row:
        for index, item in enumerate(cur_row):
            print(f"{index + 1}. {item}. {item.deadline.day} {item.deadline.strftime('%b')}")
    elif msg:
        print(msg)
    print()


while True:
    print("1) Today's tasks\n"
          "2) Week's tasks\n"
          "3) All tasks\n"
          "4) Missed tasks\n"
          "5) Add task\n"
          "6) Delete task\n"
          "0) Exit")
    try:
        inp = int(input())
    except ValueError:
        break
    if inp == 1:
        print_tasks(session.query(Task)
                    .filter(Task.deadline == datetime.today().date()).all())
    elif inp == 2:
        for i in range(7):
            today = datetime.today() + timedelta(days=i)
            days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                                'Friday', 'Saturday', 'Sunday']
            print(f"{days_of_the_week[today.weekday()]} "
                  f"{today.day} {today.strftime('%b')}:")
            print_tasks(session.query(Task)
                        .filter(Task.deadline == today.date()).all())
    elif inp == 3:
        print_tasks_with_deadline(session.query(Task)
                                  .order_by(Task.deadline).all(), "Nothing to do!")
    elif inp == 4:
        print("Missed tasks:")
        print_tasks_with_deadline(session.query(Task).filter(
            Task.deadline < datetime.today().date())
                                  .order_by(Task.deadline).all(), "Nothing is missed!")
    elif inp == 5:
        print("Enter task.")
        new_task_name = input()
        print("Enter deadline in the format YYYY-MM-DD.")
        try:
            new_task = Task(task=new_task_name, deadline=datetime.strptime(input(), '%Y-%m-%d').date())
            session.add(new_task)
            session.commit()
            print("The task has been added!")
        except ValueError:
            print("Please enter a correct date, in the format YYYY-MM-DD.")
    elif inp == 6:
        print("Choose the number of the task you want to delete:")
        row = session.query(Task).order_by(Task.deadline).all()
        print_tasks_with_deadline(row)
        if row:
            task_to_delete = row[int(input()) - 1]
            session.delete(task_to_delete)
            session.commit()
            print("The task has been deleted!")
        else:
            print("There is no such task.")
    else:
        break
