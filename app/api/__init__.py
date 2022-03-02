from flask import Blueprint, jsonify, request

from app.client import Client

api = Blueprint('api', __name__)


@api.route('/is_authorized/<phone_number>/<api_id>/<api_hash>')
async def api_is_authorized(phone_number, api_id, api_hash):
    print(phone_number)
    print(api_id)
    print(api_hash)

    telegram_client = Client(phone_number=phone_number, api_id=int(api_id), api_hash=api_hash)
    is_authorized = await telegram_client.is_user_authorized()
    return jsonify({'isAuthorized': is_authorized})


@api.route('/send_signin_code', methods=['POST'])
async def api_send_signin_code():
    print(request.json)

    phone_number = request.json.get('phoneNumber')
    api_id = request.json.get('apiId')
    api_hash = request.json.get('apiHash')

    telegram_client = Client(phone_number=phone_number, api_id=int(api_id), api_hash=api_hash)
    phone_code_hash = await telegram_client.send_signin_code()
    return jsonify({'phoneCodeHash': phone_code_hash})


@api.route('/signin', methods=['POST'])
async def api_signin():
    print(request.json)

    phone_number = request.json.get('phoneNumber')
    api_id = request.json.get('apiId')
    api_hash = request.json.get('apiHash')
    code = request.json.get('code')
    phone_code_hash = request.json.get('phoneCodeHash')

    telegram_client = Client(phone_number=phone_number, api_id=int(api_id), api_hash=api_hash)
    is_authorized = await telegram_client.signin(code=code, phone_code_hash=phone_code_hash)
    return jsonify({'isAuthorized': is_authorized})


@api.route('/report', methods=['POST'])
async def api_report():
    print(request.json)

    phone_number = request.json.get('phoneNumber')
    api_id = request.json.get('apiId')
    api_hash = request.json.get('apiHash')
    channels = request.json.get('channels')

    telegram_client = Client(phone_number=phone_number, api_id=int(api_id), api_hash=api_hash)
    report_results = await telegram_client.report_channels(channels)

    return jsonify({'reportResults': report_results})
