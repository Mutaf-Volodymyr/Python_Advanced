## engine


- Движок - объект подключения к БД.


    engine = create_engine('sqlite:///:memmory', echo=True)

## connection
- движок сам по себе уже способен соединятся с базой данных.


    with engine.connect() as conn:
        result = conn.execute(text('select "hallo"'))

    logs:
    2025-01-31 10:14:39,744 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2025-01-31 10:14:39,744 INFO sqlalchemy.engine.Engine select "hallo"
    2025-01-31 10:14:39,744 INFO sqlalchemy.engine.Engine [generated in 0.00026s] ()
    2025-01-31 10:14:39,745 INFO sqlalchemy.engine.Engine ROLLBACK


## metadata

- методата содержит в себе информацию о всех таблицах, всех ее параметрах и связях, в создании которых она использовалась, а так же диалект
- методата содержит метды управление схемой или таблицей (создание, удаление и прочее)

- способ 1
 

    metadata = MetaData()

- способ 2 (старый способ)


    mapper_registry = registry()
    Base = mapper_registry.generate_base()

- способ 3 (новый)


    Base = declarative_base()

- способ 4 (если БД уже есть)


    Base = automap_base()
    Base.prepare(autoload_with=engine_sakila)



## models
- модели - представление таблицы на уровне ООП, что позволяет более эффективно строить запросы

#### создание моделей (при помощи metadata) - классический меппинг

    metadata = MetaData()

    user_table = Table(
        'users',  # название таблицы
        metadata,  # метадата
        Column('id', Integer, primary_key=True),  # колонки
        Column('category_id', Integer, ForeignKey('categories.id')),
        Column('name', String(30), unique=True, nullable=False)  # колонки
    )
    
    print(metadata.tables)
    print(user_table.c)  # с - обращение к колонкам
    print(user_table.c.keys())

- logs

      2025-01-31 10:35:43,512 INFO sqlalchemy.engine.Engine BEGIN (implicit)
      2025-01-31 10:35:43,512 INFO sqlalchemy.engine.Engine select "hallo"
      2025-01-31 10:35:43,512 INFO sqlalchemy.engine.Engine [generated in 0.00025s] ()
      2025-01-31 10:35:43,512 INFO sqlalchemy.engine.Engine ROLLBACK
      FacadeDict({'users': Table('users', MetaData(), Column('id', Integer(), table=<users>, primary_key=True, nullable=False), Column('category_id', Integer(), ForeignKey('categories.id'), table=<users>), Column('name', String(length=30), table=<users>, nullable=False), schema=None)})
      ReadOnlyColumnCollection(users.id, users.category_id, users.name)
      ['id', 'category_id', 'name']


#### создание моделей (при помощи Base) - декларативный стиль
В данном случае метадата будет общая для всех наследников `Base`

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String)

#### создание моделей (при помощи @as_declarative())
В данном случае метадата будет общая для всех наследников `AbstractModel`

    @as_declarative()
    class AbstractModel:
        id = Column(Integer, primary_key=True, autoincrement=True)
    
        @classmethod
        @declared_attr
        def __tablename__(cls):
            return cls.__name__.lower()
    
    
    class Product(AbstractModel):
        name = Column(String(100), nullable=False, unique=True)
        price = Column(Numeric(10, 2), nullable=False)
        in_stock = Column(Boolean, nullable=False)
        category_id = Column(Integer, ForeignKey('category.id'), nullable=False)



#### создание моделей (mapped_column, Mapped)
Возможность задавать тип данных через аннотацию. Есть проблемы в BigInt и др. 


    class User(Base):
        __tablename__ = 'user'
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column()


#### создание моделей (если БД уже сеть)
- работает если в БД прописаны ключи


    Base = automap_base()
    Base.prepare(autoload_with=engine_sakila)
    
    Film = Base.classes.film
    Film_category = Base.classes.film_category
    Category = Base.classes.category


#### создание таблиц

    metadata.create_all(engine)

- logs


    2025-01-31 11:44:24,800 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2025-01-31 11:44:24,800 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("users")
    2025-01-31 11:44:24,800 INFO sqlalchemy.engine.Engine [raw sql] ()
    2025-01-31 11:44:24,800 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("users")
    2025-01-31 11:44:24,800 INFO sqlalchemy.engine.Engine [raw sql] ()
    2025-01-31 11:44:24,800 INFO sqlalchemy.engine.Engine 
    CREATE TABLE users (
        id INTEGER NOT NULL, 
        name VARCHAR(30) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (name)
    )
    2025-01-31 11:44:24,801 INFO sqlalchemy.engine.Engine [no key 0.00008s] ()
    2025-01-31 11:44:24,801 INFO sqlalchemy.engine.Engine COMMIT


#### удаление таблиц


    metadata.drop_all(engine)


- logs


    2025-01-31 11:48:31,733 INFO sqlalchemy.engine.Engine [no key 0.00009s] ()
    2025-01-31 11:48:31,733 INFO sqlalchemy.engine.Engine COMMIT
    2025-01-31 11:48:31,734 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2025-01-31 11:48:31,734 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("users")
    2025-01-31 11:48:31,734 INFO sqlalchemy.engine.Engine [raw sql] ()
    2025-01-31 11:48:31,734 INFO sqlalchemy.engine.Engine 
    DROP TABLE users
    2025-01-31 11:48:31,734 INFO sqlalchemy.engine.Engine [no key 0.00009s] ()
    2025-01-31 11:48:31,735 INFO sqlalchemy.engine.Engine COMMIT


## core


### insert

#### вставка данных в core осуществляется при помощи `insert()`

способ 1


    metadata.create_all(engine)
    
    stmt = insert(user_table).values(name="Test1") # создает заготовку запроса
    # INSERT INTO users (name) VALUES (?)
    stmt = stmt.compile(engine) # создает запрос. Вторым аргументом можно передать диалект
    # INSERT INTO users (name) VALUES (?)
    
    with engine.begin() as conn:
        res = conn.execute(stmt) # производит запись в БД

    print(res.inserted_primary_key) # возвращает последний id

способ 2

    stmt = insert(user_table)
    
    with engine.begin() as conn:
        result = conn.execute(
            stmt, [{'name': 'Test2'}, {'name': 'Test3'}])
        
    print(result)

#### получение данных в core осуществляется при помощи `select()`

>
    with engine.begin() as conn:
        result = conn.execute(
            select(user_table).where(
                or_(                                  #
                user_table.c.name.startswith('Test'), # применяются строковые методы
                user_table.c.name.endswith('3'),  # применяются строковые методы
                )
            )
        ).all()
        print(result)  # [(1, 'Test1'), (2, 'Test2'), (3, 'Test3')]
>
    with engine.begin() as conn:
        result = conn.execute(
            select(user_table.c.name)
        )
        result = result.mappings().all() # создает словарь
        print(result) # [{'name': 'Test1'}, {'name': 'Test2'}, {'name': 'Test3'}]
    with engine.begin() as conn:
        result = conn.execute(
            select(
                (user_table.c.id),
                (user_table.c.name + ' lalala').label('surname')
            )
        )
        result = result.mappings().all() # создает словарь
        print(result) # [{'surname': 'Test1 lalala'}, {'surname': 'Test2 lalala'}, {'surname': 'Test3 lalala'}]
        print(result[0].surname) # Test1 lalala
        print(result[0].id) # 1
>
    with engine.begin() as conn:
        result = conn.execute(
            select(user_table).
            where(user_table.c.id > 0).
            join_from(user_table, address_table)
        )
        result = result.all()  # [(1, 'Test1'), (1, 'Test1')]
        print(result)

    with engine.begin() as conn:
        result = conn.execute(
            select(user_table).
            join_from(user_table, address_table, user_table.c.id == address_table.c.id)
        )
        result = result.all()  # [(1, 'Test1'), (2, 'Test2')]
        print(result)
>
    with engine.begin() as conn:
        result = conn.execute(
            select(user_table, address_table).
            join(address_table).
            order_by(user_table.c.id)
        ).mappings().all()
        print(result)


- примечание. Есть способ ручного контроля 


    with engine.connect() as conn:
        trans = conn.begin()  # Явно начинаем транзакцию
        try:
            res = conn.execute(
                ...
            )
            trans.commit()  # Фиксируем изменения
        except:
            trans.rollback() 
            raise


#### обновление данных в core осуществляется при помощи `update()`
- один параметр


    with engine.begin() as conn:
        conn.execute(
            update(user_table).where(user_table.c.id == 1).values(name='Test4')
        )


- много параметров


    with engine.begin() as conn:
        stmt = update(user_table).where(
            user_table.c.name == bindparam("oldname")).values(name=bindparam("newname"))
        conn.execute(
            stmt,
            [
                {'oldname': 'Test1', 'newname': 'Test-1'},
                {'oldname': 'Test2', 'newname': 'Test-2'},
                {'oldname': 'Test3', 'newname': 'Test-3'},
    
            ]
        )
        print(conn.execute(select(user_table)).all()) # [(1, 'Test-1'), (2, 'Test-2'), (3, 'Test-3')]



#### удаление данных в core осуществляется при помощи `delete()`

- удаление полей ссылаясь на значение в другой таблице (нет в sqlite)


    with (engine.begin() as conn):
        del_stmt = delete(user_table).where(user_table.c.id == address_table.c.user_id).where(address_table.c.email_address.startswith('aaa'))
        print(del_stmt.compile(dialect=mysql.dialect()))

> DELETE FROM users USING users, address WHERE users.id = address.user_id AND (address.email_address LIKE concat(%s, '%%'))

- rowcount


    with (engine.begin() as conn):
        del_stmt = delete(user_table).where(user_table.c.id == 1)
        res = conn.execute(del_stmt)
        print(res.rowcount) # показывает значений было удалено

- returning


    with (engine.begin() as conn):
        res = conn.execute(
            delete(user_table) # удалить где?
            .where(user_table.c.id.in_([1, 2])) # в каком случае?
            .returning(user_table) # показать то, что было удалено
        ).all()
        print(res) # [(1, 'Test1'), (2, 'Test2')]



## session

Состояние объекта в сессии:
1) Transient (временный) - состояние объекта до его добавления в сессию. Просто объект в Пайтон
2) Pending (ожидающий) - после session_add, он еще не находиться в БД, но прошел проверку на интеграцию
3) Persistent (персистентный) - он уже имеет ассоциацию с БД. Все изменения над объект находят свое отражение в БД
4) Deleted (удаленный) - запись в БД существует, но объект пайтон помечен "на удаление"
5) Detached (отсоединенный) - объект отсоеденен от БД и уже не имеет с ним ассоциации. 


> inspect - показывает состояние объекта


    user = User(id=1, name='Test', age=30)
    insp = inspect(user)
    print(insp.transient) # True
    print(insp.pending) # False
    print(insp.persistent) # False
    print(insp.deleted) # False
    print(insp.detached) # False


> метод `add` объекта `session` переводить объект в состояние `pending`


    session.add(user)
    print(insp.transient) # False
    print(insp.pending) # True
    print(insp.persistent) # False
    print(insp.deleted) # False
    print(insp.detached) # False

> метод `flush` объекта `session` переводить объект в состояние `persistent`, то есть передает объект в транзакцию
    

    session.flush()
    print(insp.transient) # False
    print(insp.pending) # False
    print(insp.persistent) # True
    print(insp.deleted) # False
    print(insp.detached) # False

> метод `delete` объекта `session` переводит объект в состояние `deleted`, то есть помечает объект на удаление, но это состояние достигается при повторном вызове метода `flush`


    session.add(user)
    session.flush()
    session.delete(user)
    session.flush()
    print(insp.transient) # False
    print(insp.pending) # False
    print(insp.persistent) # False
    print(insp.deleted) # True
    print(insp.detached) # False

> метод `commit` объекта `session` заканчивает транзакцию. После этого объект приобретает статус `detached`


- new


    session.add(user1)
    session.add(user2)
    print(session.new) # IdentitySet([<__main__.User object at 0x10e144620>, <__main__.User object at 0x10c94dc70>])
    print(session.dirty) # IdentitySet([])
    session.flush()
    print(session.new) # IdentitySet([])
    print(session.dirty) # IdentitySet([])
    user1.age = 45
    print(session.dirty) # IdentitySet([<__main__.User object at 0x10e144620>])
    print(user1 in session.dirty) # True


При вызове `add` все объекты попадают в коллекцию `new`. Идентификация объекта происходит по `PrimaryKey`
`flush` забирает обьекты из new и передает их в транзакцию. Если обьект в будущем будет изменен, он попадет в `dirty`.
Что бы изменения вступили в силу (были переданы в транзакцию) - необходимо повторно применить `flush`

в логах ниже видно, что сначала выполняется `INSERT`, а потом `UPDATE`
>2025-02-01 13:01:46,936 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-02-01 13:01:46,937 INFO sqlalchemy.engine.Engine INSERT INTO user (id, name, age) VALUES (?, ?, ?)
2025-02-01 13:01:46,938 INFO sqlalchemy.engine.Engine [generated in 0.00018s] [(1, 'Test1', 30), (2, 'Test2', 25)]
2025-02-01 13:01:46,939 INFO sqlalchemy.engine.Engine UPDATE user SET age=? WHERE user.id = ?
2025-02-01 13:01:46,939 INFO sqlalchemy.engine.Engine [generated in 0.00013s] (20, 1)

    session.add(user1)
    session.add(user2)
    user1.age = 45
    print(session.dirty)
    print(user1 in session.dirty) # False
    print(user1 in session.new) # True

Если `flush` не был вызван, то `new` будет их содержать актуальные обьекты

- включение режима `autoflush`


    session = Session(bind=engine, autoflush=False)


## связи 

### one-to-one

- В БД связь обеспечивается за счет `ForeignKey`, но в ORM устанавливается дополнительная связь за счет `relationship`
- one-to-one вязь обеспечивается за счет `uselist=False`
- `back_populates` настраивает связь в обе стороны


    class User(Base):
        __tablename__ = 'user'
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str]
        age: Mapped[int]
        address: Mapped['Address'] = relationship(back_populates='user', uselist=False)
    
        def __repr__(self):
            return f'User: {self.name} : {self.age}'
    
    
    class Address(Base):
        __tablename__ = 'address'
    
        email: Mapped[str] = mapped_column(primary_key=True)
        user: Mapped["User"] = mapped_column(back_populates='address', uselist=False)
        user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    
        def __repr__(self):
            return f'Address: {self.email}'


#### добавление и работа 


-  способ 1


    user1 = User(id=1, name='Test1', age=20)
    address1 = Address(email='aaa@aaa.com')
    user1.address = address1

-  способ 2


    user2 = User(id=2, name='Test2', age=30, address=Address(email='bbb@bbb.com'))
    session.add_all([user1, address1, user2])
    session.commit()

- вызов `address` из `users`

 
    users = session.scalar(select(User))
    print(users.address)

>

    2025-02-01 13:54:09,921 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2025-02-01 13:54:09,922 INFO sqlalchemy.engine.Engine SELECT user.id, user.name, user.age 
    FROM user
    2025-02-01 13:54:09,922 INFO sqlalchemy.engine.Engine [generated in 0.00012s] ()
    2025-02-01 13:54:09,925 INFO sqlalchemy.engine.Engine SELECT address.email AS address_email, address.user_id AS address_user_id 
    FROM address 
    WHERE ? = address.user_id
    2025-02-01 13:54:09,925 INFO sqlalchemy.engine.Engine [generated in 0.00015s] (1,)
    Address: aaa@aaa.com: 1



### one-to-many

для того что бы создать связь 'one-to-many' нужно просто поменять 'uselist=True' необходимой таблице
В этом случае поле `address` в модели `User` будет иметь тип `list`, что так же нужно указать

    addresses: Mapped[list["Address"]] = relationship(back_populates='user', uselist=True)

Теперь добавление адресов будет осуществлятся при помощи методов списка


    user1 = User(id=1, name='Test1', age=20)
    address1 = Address(email='aaa@aaa.com')
    address2 = Address(email='bbb@aaa.com')
    user1.addresses.extend([address1, address2])
    session.add(user1)
    session.commit()
    
    users = session.scalars(select(User)).all()
    
    print(users[0].addresses)

>

    2025-02-01 14:21:36,827 INFO sqlalchemy.engine.Engine INSERT INTO user (id, name, age) VALUES (?, ?, ?)
    2025-02-01 14:21:36,827 INFO sqlalchemy.engine.Engine [generated in 0.00015s] (1, 'Test1', 20)
    2025-02-01 14:21:36,828 INFO sqlalchemy.engine.Engine INSERT INTO addresses (email, user_id) VALUES (?, ?)
    2025-02-01 14:21:36,828 INFO sqlalchemy.engine.Engine [generated in 0.00012s] [('aaa@aaa.com', 1), ('bbb@aaa.com', 1)]
    2025-02-01 14:21:36,828 INFO sqlalchemy.engine.Engine COMMIT
    2025-02-01 14:21:36,828 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2025-02-01 14:21:36,829 INFO sqlalchemy.engine.Engine SELECT user.id, user.name, user.age 
    FROM user
    2025-02-01 14:21:36,830 INFO sqlalchemy.engine.Engine [generated in 0.00010s] ()
    2025-02-01 14:21:36,832 INFO sqlalchemy.engine.Engine SELECT addresses.email AS addresses_email, addresses.user_id AS addresses_user_id 
    FROM addresses 
    WHERE ? = addresses.user_id
    2025-02-01 14:21:36,832 INFO sqlalchemy.engine.Engine [generated in 0.00013s] (1,)
    [Address: aaa@aaa.com: 1, Address: bbb@aaa.com: 1]




### many-to-many
Для создания связей `many-to-many`, необходимо переназначить `uselist=True` в обоих таблицах и переопределить `Mapped[list["Address"]]`.
Далее нам потребуется создать промежуточную модель `UserToAddress` и в наши первичные модели установить флаг `secondary="user_to_addresses"` с названием таблицы.



    class User(Base):
        __tablename__ = 'users'
    
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str]
        age: Mapped[int]
        addresses: Mapped[list["Address"]] = relationship(back_populates='users', uselist=True,
                                                          secondary="user_to_addresses")
    
        def __repr__(self):
            return f'id={self.id} | User:{self.name} | age={self.age}'
    
    
    class Address(Base):
        __tablename__ = 'addresses'
    
        email: Mapped[str] = mapped_column(primary_key=True)
        users: Mapped[list["User"]] = relationship(back_populates='addresses', uselist=True, secondary="user_to_addresses")
    
        def __repr__(self):
            return f'Address: {self.email}'
    
    
    class UserToAddress(Base):
        __tablename__ = 'user_to_addresses'
    
        user_fk = mapped_column(ForeignKey('users.id'), primary_key=True)
        address_fk = mapped_column(ForeignKey('addresses.email'), primary_key=True)
    
        def __repr__(self):
            return f'user_fk={self.user_fk} | address_fk:{self.address_fk}'
>

    2025-02-01 14:39:07,312 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2025-02-01 14:39:07,314 INFO sqlalchemy.engine.Engine SELECT users.id, users.name, users.age 
    FROM users
    2025-02-01 14:39:07,314 INFO sqlalchemy.engine.Engine [generated in 0.00015s] ()
    2025-02-01 14:39:07,315 INFO sqlalchemy.engine.Engine SELECT user_to_addresses.user_fk, user_to_addresses.address_fk 
    FROM user_to_addresses
    2025-02-01 14:39:07,315 INFO sqlalchemy.engine.Engine [generated in 0.00013s] ()
    id=1 | User:Test1 | age=20
    2025-02-01 14:39:07,319 INFO sqlalchemy.engine.Engine SELECT addresses.email AS addresses_email 
    FROM addresses, user_to_addresses 
    WHERE ? = user_to_addresses.user_fk AND addresses.email = user_to_addresses.address_fk
    2025-02-01 14:39:07,319 INFO sqlalchemy.engine.Engine [generated in 0.00018s] (1,)
    [Address: aaa@aaa.com, Address: bbb@aaa.com]
    user_fk=1 | address_fk:aaa@aaa.com user_fk=2 | address_fk:aaa@aaa.com user_fk=1 | address_fk:bbb@aaa.com user_fk=2 | address_fk:bbb@aaa.com


### стратегия загрузки `lazy`


    user1 = User(id=1, name='Test1', age=20)
    address1 = Address(email='aaa@aaa.com')
    address2 = Address(email='bbb@aaa.com')
    user1.addresses.extend([address1, address2])
    session.add(user1)
    session.commit()
    
    user = session.scalar(select(User))
    print(user)
    print(user.addresses)

> select (по умолчанию) - не работает с асинхронностью 

    2025-02-01 15:17:26,708 INFO sqlalchemy.engine.Engine SELECT user.id, user.name, user.age 
    FROM user
    2025-02-01 15:17:26,708 INFO sqlalchemy.engine.Engine [generated in 0.00012s] ()
    id=1 | User:Test1 | age=20
    2025-02-01 15:17:26,711 INFO sqlalchemy.engine.Engine SELECT addresses.email AS addresses_email, addresses.user_fk AS addresses_user_fk 
    FROM addresses 
    WHERE ? = addresses.user_fk
    2025-02-01 15:17:26,711 INFO sqlalchemy.engine.Engine [generated in 0.00015s] (1,)


> selectin (хорошо если обьекты пересекаются)


    2025-02-01 15:08:47,275 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2025-02-01 15:08:47,276 INFO sqlalchemy.engine.Engine SELECT user.id, user.name, user.age 
    FROM user
    2025-02-01 15:08:47,276 INFO sqlalchemy.engine.Engine [generated in 0.00010s] ()
    2025-02-01 15:08:47,278 INFO sqlalchemy.engine.Engine SELECT addresses.user_fk AS addresses_user_fk, addresses.email AS addresses_email 
    FROM addresses 
    WHERE addresses.user_fk IN (?)
    2025-02-01 15:08:47,278 INFO sqlalchemy.engine.Engine [generated in 0.00016s] (1,)


> joined (хорошо если обьектов до 10 000)

    2025-02-01 15:10:47,353 INFO sqlalchemy.engine.Engine SELECT user.id, user.name, user.age, addresses_1.email, addresses_1.user_fk 
    FROM user LEFT OUTER JOIN addresses AS addresses_1 ON user.id = addresses_1.user_fk
    2025-02-01 15:10:47,353 INFO sqlalchemy.engine.Engine [generated in 0.00012s] ()


> subquery (хорошо если обьектов очень много  100 000)

    025-02-01 15:12:44,779 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2025-02-01 15:12:44,780 INFO sqlalchemy.engine.Engine SELECT user.id, user.name, user.age 
    FROM user
    2025-02-01 15:12:44,780 INFO sqlalchemy.engine.Engine [generated in 0.00011s] ()
    2025-02-01 15:12:44,784 INFO sqlalchemy.engine.Engine SELECT addresses.email AS addresses_email, addresses.user_fk AS addresses_user_fk, anon_1.user_id AS anon_1_user_id 
    FROM (SELECT user.id AS user_id 
    FROM user) AS anon_1 JOIN addresses ON anon_1.user_id = addresses.user_fk
    2025-02-01 15:12:44,784 INFO sqlalchemy.engine.Engine [generated in 0.00012s] ()


