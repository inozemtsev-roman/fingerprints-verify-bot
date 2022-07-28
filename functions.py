import asyncio
import json
import logging
import psycopg2
import requests

from address import detect_address
from config import russian, english, bot, CHAT_ID, COLLECTION, DATABASE


async def open_connection():
    connect = psycopg2.connect(DATABASE)
    cursor = connect.cursor()
    return connect, cursor


async def close_connection(connect):
    connect.commit()
    connect.close()


async def kick_user(tgid):
    """
    Лишение пользователя верификации и права присутствовать в чате.
    """
    try:
        connect, cursor = await open_connection()
        cursor.execute(
            f"delete from verify where tgid = '{tgid}'")
        await close_connection(connect)
    except Exception as e:
        logging.error(f"Failed to Delete {tgid} from Database\n"
                      f"{e}")
    try:
        await bot.ban_chat_member(CHAT_ID, tgid)
        await bot.unban_chat_member(CHAT_ID, tgid, only_if_banned=True)
    except Exception as e:
        logging.warning(f"Failed to Kick {tgid} from Chat {CHAT_ID}\n"
                        f"{e}")
    try:
        await bot.send_chat_action(tgid, 'typing')
        await bot.send_message(tgid,
                               f'{russian["no_longer_owner"]}\n\n{english["no_longer_owner"]}')
    except Exception as e:
        logging.warning(f"Failed to Send Message to {tgid}\n"
                        f"{e}")


async def get_ton_addresses(address):
    addresses = detect_address(address)
    return {'b64': addresses['bounceable']['b64'],
            'b64url': addresses['bounceable']['b64url'],
            'n_b64': addresses['non_bounceable']['b64'],
            'n_b64url': addresses['non_bounceable']['b64url'],
            'raw': addresses['raw_form']}


async def get_user_nfts(address):
    address = (await get_ton_addresses(address))['b64url']
    await asyncio.sleep(1)
    all_nfts = json.loads(requests.get(f"https://tonapi.io/v1/nft/searchItems",
                                       params={"owner": address,
                                               "collection": COLLECTION,
                                               "include_on_sale": "true",
                                               "limit": "50",
                                               "offset": 0}).text)['nft_items']
    nfts = []
    for nft in all_nfts:
        try:
            name = nft['metadata']['name']
            address = (await get_ton_addresses(nft['address']))['b64url']
            image = nft['metadata']['image']
            nfts += [{'address': address, 'name': name, 'image': image}]
        except:
            pass
    return nfts
    