from telethon import TelegramClient, functions, types
from typing import List
import time


class Client:
    def __init__(self, phone_number: str, api_id: int, api_hash: str) -> None:
        self.phone_number = phone_number
        self.api_id = api_id
        self.api_hash = api_hash

        self._client = TelegramClient(self.phone_number, self.api_id, self.api_hash)
        self._is_connected = False

    async def is_user_authorized(self) -> bool:
        await self._try_connect()
        is_authorized = await self._client.is_user_authorized()
        await self._try_disconnect()

        return is_authorized

    async def send_signin_code(self) -> str:
        await self._try_connect()
        phone_code_hash = (await self._client.send_code_request(self.phone_number)).phone_code_hash
        await self._try_disconnect()

        return phone_code_hash

    async def signin(self, code, phone_code_hash) -> bool:
        await self._try_connect()
        await self._client.sign_in(phone=self.phone_number, code=code, phone_code_hash=phone_code_hash)
        is_authorized = await self.is_user_authorized()
        await self._try_disconnect()

        return is_authorized

    async def report_channels(self, channels: List[str]) -> List[dict]:
        result = []

        await self._try_connect()

        for channel in channels:
            channel = channel.strip()
            try:
                report_result = await self._client(functions.account.ReportPeerRequest(
                    peer=await self._client.get_entity(channel),
                    reason=types.InputReportReasonOther(),
                    message='Разжигание войны'
                ))
                result.append({
                    'channel': channel,
                    'status': report_result
                })
                time.sleep(0.3)
            except Exception as e:
                result.append({
                    'channel': channel,
                    'status': False
                })

        await self._try_disconnect()
        return result

    async def _try_connect(self) -> None:
        if not self._is_connected:
            await self._client.connect()
            self._is_connected = True

    async def _try_disconnect(self) -> None:
        if self._is_connected:
            await self._client.disconnect()
            self._is_connected = False
