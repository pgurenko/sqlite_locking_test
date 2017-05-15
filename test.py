#!/usr/bin/python
# stress test the sqlite writing with several threads
from multiprocessing import Process, Lock, current_process

def proc_func(lock, counter):

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from sqlalchemy_declarative import Address, Base, Person

    engine = create_engine('sqlite:///sqlalchemy_example.db', connect_args={'timeout': 30})
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    while True:
        lock.acquire()
        counter += 1
        lock.release()

        print '[%s] adding person %d' % (current_process().name, counter)

        # Insert a Person in the person table
        new_person = Person(name='new person %d' % counter)
        session.add(new_person)
        session.commit()

        # Insert an Address in the address table
        new_address = Address(post_code='00000 %d' % counter, person=new_person)
        session.add(new_address)
        session.commit()

lock = Lock()
counter = 0

for num in range(2):
    Process(target=proc_func, args=(lock, counter)).start()