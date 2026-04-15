from sqlalchemy import DateTime, String, Text, ForeignKey, func, BigInteger, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(150))
    subscribed_sources: Mapped[set["NewsSources"]] = relationship("NewsSources",
                                                      secondary='users_news_sources',
                                                      collection_class=set,
                                                      back_populates="users")
    default_news_count: Mapped[int] = mapped_column(Integer, default=10)


class NewsSources(Base):
    __tablename__ = 'news_sources'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    api_id: Mapped[str] = mapped_column(String(255))
    domain: Mapped[str] = mapped_column(String(255))
    language: Mapped[str] = mapped_column(String(10))
    users: Mapped[list["Users"]] = relationship("Users",
                                                      secondary='users_news_sources',
                                                      back_populates="subscribed_sources")
    news: Mapped[list["News"] ]= relationship("News", back_populates = "source")


class UsersNewsSources(Base):
    __tablename__ = 'users_news_sources'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))
    news_source_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_sources.id', ondelete='CASCADE'))


class News(Base):
    __tablename__ = 'news'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    source_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_sources.id'), nullable=False)
    source: Mapped["NewsSources"] = relationship("NewsSources", back_populates="news")
    title: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(Text)