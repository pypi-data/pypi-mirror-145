class BaseModel:
    def __init__(self, client, model):
        self.client = client
        self.model = model

    def get_one(self, **kwargs):
        with self.client.get_session_context("stock.leader") as session:
            results = session.query(self.model).filter_by(**kwargs).one_or_none()
            return results.to_dict() if results else None

    def get_all(self, **kwargs):
        with self.client.get_session_context("stock.leader") as session:
            results = session.query(self.model).filter_by(**kwargs).all()
            return [r.to_dict() for r in results] if results else None

    def create(self, **kwargs):
        with self.client.get_session_context("stock.leader") as session:
            new_item = self.model(**kwargs)
            session.expire_on_commit = False
            session.add(new_item)
            session.commit()
            return new_item
