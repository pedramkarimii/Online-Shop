from decouple import config # noqa
import redis
from kavenegar import *
import random
# import time
# import aioredis


class CodeGenerator:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host=config('REDIS_HOST'), port=config('REDIS_PORT'), db=0)

    def generate_and_store_code(self, phone_number):
        """
        Generate a verification code and store it in Redis associated with the phone number if it doesn't already exist.

        Args:
            phone_number (str): The phone number to associate the code with.

        Returns:
            str: The generated code or the existing code if it was already set.
        """
        code = ''.join(random.choices('0123456789', k=6))
        expiration_time = 120

        if self.redis_client.setnx(phone_number, code):
            self.redis_client.expire(phone_number, expiration_time)
            return code
        else:
            return self.redis_client.get(phone_number).decode()

    def get_code_for_number(self, phone_number):
        """
        Retrieve the verification code associated with a phone number from Redis.

        Args:
            phone_number (str): The phone number to retrieve the code for.

        Returns:
            str: The verification code associated with the phone number.
        """
        return self.redis_client.get(phone_number)

#
# class OtpCode:
#     def __init__(self, redis_uri='redis://localhost'):
#         self.redis_uri = redis_uri
#
#     async def generate_code(self, phone_number):
#         async with aioredis.from_url(self.redis_uri, encoding='utf-8') as redis_client:
#             request_key = f'request_count:{phone_number}'
#             last_request_key = f'last_request:{phone_number}'
#
#             request_count = await redis_client.get(request_key)
#             if request_count is not None and int(request_count) >= 3:
#                 last_request_time = await redis_client.get(last_request_key)
#                 if last_request_time is not None and time.time() - float(last_request_time) < 600:
#                     raise ValueError("Exceeded maximum request limit. Please try again later.")
#
#             otp = ''.join(random.choices("0123456789", k=6))
#
#             await redis_client.setex(f'otp_code:{phone_number}', 120, otp)
#
#             await redis_client.incr(request_key)
#             await redis_client.expire(request_key, 600)
#             await redis_client.set(last_request_key, time.time(), expire=600)
#
#             return otp
#
#     async def get_code(self, phone_number):
#         async with aioredis.from_url(self.redis_uri, encoding='utf-8') as redis_client:
#             return await redis_client.get(f'otp_code:{phone_number}')


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('XXXX')
        params = {
            'sender': 'XXXX',
            'receptor': phone_number,
            'message': f"Your verification code:"
                       f"{code}"
        }

        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(f'Error API: The identification code is not valid <<{KavenegarAPI}>> - {e}')
    except HTTPException as e:
        print(f'Error HTTP: {e}')
