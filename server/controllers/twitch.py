"""Twitch API controller."""

import os
from fastapi import Request, HTTPException
import aiohttp


async def get_broadcaster(request: Request):
    """
    Get broadcaster information (dependency for other Twitch endpoints).
    
    Args:
        request: FastAPI request object with twitch token in state
    """
    # This would typically fetch and store broadcaster info
    # For now, it's a pass-through dependency
    pass


async def get_channel_info(request: Request):
    """
    Get Twitch channel information.
    
    Args:
        request: FastAPI request object with twitch token in state
        
    Returns:
        dict: Channel information
    """
    try:
        endpoint = os.getenv('TWITCH_CREATOR_CHANNEL_ENDPOINT')
        access_token = request.state.twitch.get('access_token')
        client_id = os.getenv('TWITCH_CLIENT_ID')
        
        if not access_token:
            raise HTTPException(status_code=401, detail='No Twitch access token')
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Client-Id': client_id
                }
            ) as response:
                data = await response.json()
                return data
                
    except HTTPException:
        raise
    except Exception as error:
        print(f'[fastapi] Error getting channel info: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')


async def get_ad_schedule(request: Request):
    """
    Get Twitch ad schedule.
    
    Args:
        request: FastAPI request object with twitch token in state
        
    Returns:
        dict: Ad schedule data
    """
    try:
        endpoint = os.getenv('TWITCH_CREATOR_ADS_ENDPOINT')
        access_token = request.state.twitch.get('access_token')
        client_id = os.getenv('TWITCH_CLIENT_ID')
        
        if not access_token:
            raise HTTPException(status_code=401, detail='No Twitch access token')
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Client-Id': client_id
                }
            ) as response:
                data = await response.json()
                return data
                
    except HTTPException:
        raise
    except Exception as error:
        print(f'[fastapi] Error getting ad schedule: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')


async def get_followers(request: Request):
    """
    Get Twitch followers.
    
    Args:
        request: FastAPI request object with twitch token in state
        
    Returns:
        dict: Followers data
    """
    try:
        endpoint = os.getenv('TWITCH_CREATOR_FOLLOWERS_ENDPOINT')
        access_token = request.state.twitch.get('access_token')
        client_id = os.getenv('TWITCH_CLIENT_ID')
        
        if not access_token:
            raise HTTPException(status_code=401, detail='No Twitch access token')
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Client-Id': client_id
                }
            ) as response:
                data = await response.json()
                return data
                
    except HTTPException:
        raise
    except Exception as error:
        print(f'[fastapi] Error getting followers: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')
