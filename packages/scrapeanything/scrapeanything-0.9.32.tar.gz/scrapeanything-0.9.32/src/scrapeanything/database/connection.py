from contextlib import contextmanager
from scrapeanything.utils.config import Config
from scrapeanything.database.repository import Repository

@contextmanager
def Connection(config: Config):

    repository = Repository(config=config)
    try:
        yield repository
        repository.commit()
    except:
        repository.rollback()
    finally:
        repository.close()