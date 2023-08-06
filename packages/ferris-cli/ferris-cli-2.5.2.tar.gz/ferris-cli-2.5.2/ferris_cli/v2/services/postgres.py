from sqlalchemy import create_engine
from sqlalchemy import text
from .config import ApplicationConfigurator


class PostgreSQL:

    def __init__(self):
        config = ApplicationConfigurator.get()
        self.engine = create_engine(
            f"postgresql://{config.get('DB_USERNAME')}:{config.get('DB_PASSWORD')}@"
            f"{config.get('DB_HOST')}:{config.get('DB_PORT')}/"
            f"{config.get('DB_NAME')}"
        )

    def execute_query(self, statement, params={}):
        stmt = text(statement)
        res = self.engine.execute(stmt, params)
        result = [dict(row) for row in res]

        return result
