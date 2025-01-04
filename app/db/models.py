from sqlalchemy import Column, Integer, Float, String, ForeignKey


class Models:
    def __init__(self, Base):
        self.Base = Base

    def _define_users(self):
        class User(self.Base):
            __tablename__ = "users"
            id = Column(Integer, primary_key=True)
            name = Column(String, nullable=False)
            balance = Column(Float, default=0.0)
            status = Column(Integer, default=0)

        return User

    def _define_transactions(self):
        class Transaction(self.Base):
            __tablename__ = "transactions"
            id = Column(Integer, primary_key=True)
            user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
            opt = Column(String, nullable=False)
            amount = Column(Float, nullable=False)
            status = Column(String, default="completed")

        return Transaction

    def define(self):
        user = self._define_users()
        transactions = self._define_transactions()

        return (user, transactions)
