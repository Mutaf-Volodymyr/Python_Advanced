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
В данном случае метадата будет общая для всех наследников Base

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String)

#### создание моделей (при помощи @as_declarative())
В данном случае метадата будет общая для всех наследников AbstractModel

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



## session

Состояние объекта в сессии:
1) объект создан, но не связан с сессией
2) объект связан с таблицей (пендинг. нет коммита)
3) объект сохранен, но сессия еще имеет к нему доступ (персистентное состояние)
4) объект отсоединяется от сессии (детачт)
5) объект удален (делитет)






