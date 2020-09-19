from dataclasses import dataclass
from typing import List

from news_mining_db import Tag


def get_all_news():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from news_mining_db.models import News, Base

    engine = create_engine()
    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    results = session.query(News).all()
    return [{'id': news.id, 'text': news.text} for news in results]


@dataclass
class TagData:
    tag_name: str
    parent_name: str


def add_tags_to_news(news_id: int, tags: List[str]):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from news_mining_db.models import News, Base

    engine = create_engine("postgresql://postgres:@localhost/news-mining")
    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    news = session.query(News).filter_by(id=news_id).first()
    tags_obj = _get_tags(tags, session)
    news.tags = tags_obj
    session.commit()


def _get_tags(names: List[str], session) -> List[Tag]:
    tags = []
    for name in names:
        tag = session.query(Tag).filter_by(name=name).one_or_none()
        if tag:
            tags.append(tag)
        else:
            tags.append(Tag(name=name))

    session.add_all(tags)
    session.commit()
    return tags


def create_tags(tags: List[TagData]):
    def get_tag_id(tag_name) -> int:
        if tag_name in tags_id:
            return tags_id[tag_name]
        else:
            t = Tag(name=tag_name)
            session.add(t)
            session.commit()
            tags_id[tag_name] = t.id
            return t.id

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from news_mining_db.models import Base, Tag

    engine = create_engine("postgresql://postgres:@localhost/news-mining")
    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    session.query(Tag).delete()

    tags_id = {}
    for tag in tags:
        tag_id = get_tag_id(tag.tag_name)
        parent_tag_id = get_tag_id(tag.parent_name)
        tag_object = session.query(Tag).filter_by(id=tag_id).first()
        tag_object.parent_tag_id = parent_tag_id
        session.commit()


def add_vector_to_news(news_id: int, vector: dict):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from news_mining_db.models import Base, News

    engine = create_engine("postgresql://postgres:@localhost/news-mining")
    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    news = session.query(News).filter_by(id=news_id).first()
    news.vector = vector
    session.commit()


def get_news_vector(news_id: int) -> dict:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from news_mining_db.models import Base, News

    engine = create_engine("postgresql://postgres:@localhost/news-mining")
    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    news = session.query(News).filter_by(id=news_id).first()
    return news.vector


if __name__ == '__main__':
    print(create_tags([TagData(tag_name='2', parent_name='1'), TagData(tag_name='3', parent_name='1')]))
    # add_tags_to_news(897, ['1'])
    # add_vector_to_news(897, {'a': 2, 'b': 1})
    # print(get_news_vector(851))
    # print(get_all_news())
    # from sqlalchemy import create_engine
    # from sqlalchemy.orm import sessionmaker
    # from news_mining_db.models import Tag, Base
    #
    # engine = create_engine("postgresql://postgres:@localhost/news-mining")
    # Base.metadata.create_all(engine)
    #
    # session = sessionmaker(bind=engine)()
    #
    # results = session.query(Tag).all()
    #
    # print([[y.name for y in x.children_tags] for x in results])
