# pylint: disable=attribute-defined-outside-init
from __future__ import annotations

import abc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from tagesschau import config
from tagesschau.adapters import repository


class AbstractTeaserUnitOfWork(abc.ABC):
    teasers: repository.AbstractTeaserRepository

    def __enter__(self) -> AbstractTeaserUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_postgres_uri(),
    )
)


class SqlAlchemyTeaserUnitOfWork(AbstractTeaserUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.teasers = repository.SqlAlchemyTeaserRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class CsvTeaserUnitOfWork(AbstractTeaserUnitOfWork):
    def __init__(self, folder):
        # init folder
        pass

    def __enter__(self):
        pass

    def __exit__(self):
        pass
