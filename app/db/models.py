from sqlalchemy import Column, Float, String, ForeignKey


class Models:
    def __init__(self, base):
        self.base = base

    def _define_users(self):
        class User(self.base):
            __tablename__ = "users"
            id = Column(String, primary_key=True)
            name = Column(String, nullable=False)
            balance = Column(Float, default=0.0)
            status = Column(String, default="active")

        return User

    def _define_transactions(self):
        class Transaction(self.base):
            __tablename__ = "transactions"
            id = Column(String, primary_key=True)
            user_id = Column(String, ForeignKey("users.id"), nullable=False)
            opt = Column(String, nullable=False)
            amount = Column(Float, nullable=False)
            status = Column(String, default="pending")

        return Transaction

    def define(self):
        user = self._define_users()
        transactions = self._define_transactions()

        return (user, transactions)
