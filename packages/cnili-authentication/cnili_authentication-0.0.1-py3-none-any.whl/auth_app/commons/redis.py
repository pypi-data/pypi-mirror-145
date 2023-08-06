import redis
from decouple import config
from .singleton import SingletonMeta 


class Redis(metaclass=SingletonMeta):
    """Provide Redis Connection to execute commands on redis"""

    reset_token = "reset_token:%s"
    otp_code = "otp_code:%s"
    otp_token = "otp_token:%s"
    activation_token = "activation_token:%s"

    def __init__(self):
        pool = redis.ConnectionPool(
            host=config('REDIS_HOST'),
            db=int(config('REDIS_DB')),
            port=int(config('REDIS_PORT')),
        )

        self._conn = redis.Redis(connection_pool=pool, decode_responses=True)
        self._pipe = self._conn.pipeline()

    def execute(self):
        return self._pipe.execute()

    def set_reset_token(self, token, email):
        self._conn.set(
            self.reset_token % str(token), 
            email, 
            int(config('REDIS_TOKEN_EXPIRE_TIME'))
        )

    def get_reset_email(self, token):
        email_field = self._conn.get(self.reset_token % str(token))
        if email_field:
            return email_field
        return False

    def revoke_reset_token(self, token):
        self._conn.delete(self.reset_token % str(token))

    def set_otp_token(self, token, email):
        self._conn.set(
            self.activation_token % str(token), 
            email, 
            int(config('AUTHENTICATION_TOKEN_EXPIRE'))
        )

    def get_otp_email(self, token):
        email = self._conn.get(
            self.activation_token % str(token)
        )
        return email

    # Phone
    def set_otp_code(self, token, phone):
        self._conn.set(
            self.otp_token % str(token),
            phone,
            int(config('OTP_TOKEN_EXPIRE'))
        )

    def get_otp_phone(self, token):
        phone = self._conn.get(
            self.otp_token % str(token)
        )
        return phone
