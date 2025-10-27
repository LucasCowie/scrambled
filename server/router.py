"""API router for Scrambled server."""

from fastapi import APIRouter, Depends
from controllers.tokens import validate_token, get_spotify_access_token, get_twitch_access_token
from controllers.spotify import now_playing
from controllers.twitch import get_broadcaster, get_ad_schedule, get_channel_info, get_followers
from controllers.database import message

router = APIRouter()

# Spotify routes
router.add_api_route(
    '/spotify',
    now_playing,
    methods=['GET'],
    dependencies=[Depends(validate_token), Depends(get_spotify_access_token)]
)

# Twitch routes
router.add_api_route(
    '/twitch',
    get_channel_info,
    methods=['GET'],
    dependencies=[Depends(validate_token), Depends(get_twitch_access_token), Depends(get_broadcaster)]
)

router.add_api_route(
    '/twitch/ads',
    get_ad_schedule,
    methods=['GET'],
    dependencies=[Depends(validate_token), Depends(get_twitch_access_token), Depends(get_broadcaster)]
)

router.add_api_route(
    '/twitch/followers',
    get_followers,
    methods=['GET'],
    dependencies=[Depends(validate_token), Depends(get_twitch_access_token), Depends(get_broadcaster)]
)

# Message routes
router.add_api_route('/messages', message.get_all, methods=['GET'], dependencies=[Depends(validate_token)])
router.add_api_route('/message/{id}', message.get_one_by_id, methods=['GET'], dependencies=[Depends(validate_token)])
router.add_api_route('/messages/{author}', message.get_all_by_author, methods=['GET'], dependencies=[Depends(validate_token)])
router.add_api_route('/message', message.create_and_save_new, methods=['POST'], dependencies=[Depends(validate_token)])
router.add_api_route('/message/{id}', message.delete_by_id, methods=['DELETE'], dependencies=[Depends(validate_token)])
router.add_api_route('/messages/{author}', message.delete_all_by_author, methods=['DELETE'], dependencies=[Depends(validate_token)])

# TODO: Request routes
# router.add_api_route('/request', create_and_save_unique_request, methods=['POST'])
# router.add_api_route('/requests', get_request_queue, methods=['GET'])
