"""Token validation and API token management."""

import os
import base64
from urllib.parse import urlencode
from fastapi import Request, HTTPException, status
import aiohttp


async def validate_token(request: Request):
    """
    Validate the API token from request body or query params.
    
    Args:
        request: FastAPI request object
        
    Raises:
        HTTPException: If token is missing or invalid
    """
    token = None
    
    # Check query params
    if 'token' in request.query_params:
        token = request.query_params.get('token')
        print(f'[fastapi] token=request.query, method={request.method}')
    
    # Check body (for POST/PUT/DELETE)
    if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
        try:
            body = await request.json()
            if 'token' in body:
                token = body.get('token')
                print(f'[fastapi] token=request.body, method={request.method}')
        except:
            pass
    
    # Validate token
    if token != os.getenv('SCRAMBLED'):
        print('[fastapi] missing or invalid token in query or body.')
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid or missing token'
        )
    
    return True


async def get_twitch_access_token(request: Request):
    """
    Get Twitch access token using refresh token.
    
    Args:
        request: FastAPI request object
        
    Returns:
        dict: Twitch token data
    """
    client_id = os.getenv('TWITCH_CLIENT_ID')
    client_secret = os.getenv('TWITCH_CLIENT_SECRET')
    refresh_token = os.getenv('TWITCH_REFRESH_TOKEN')
    token_endpoint = os.getenv('TWITCH_ACCESS_ENDPOINT')
    
    try:
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id,
            'client_secret': client_secret
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                token_endpoint,
                data=data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            ) as response:
                twitch_data = await response.json()
                request.state.twitch = twitch_data
                return twitch_data
                
    except Exception as error:
        print(f'[fastapi] Error getting Twitch token: {error}')
        raise HTTPException(status_code=500, detail='Failed to get Twitch token')


async def get_spotify_access_token(request: Request):
    """
    Get Spotify access token using refresh token.
    
    Args:
        request: FastAPI request object
        
    Returns:
        dict: Spotify token data
    """
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN')
    token_endpoint = os.getenv('SPOTIFY_ACCESS_ENDPOINT')
    
    try:
        # Create basic auth header
        credentials = f'{client_id}:{client_secret}'
        basic_auth = base64.b64encode(credentials.encode()).decode()
        
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                token_endpoint,
                data=data,
                headers={
                    'Authorization': f'Basic {basic_auth}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            ) as response:
                spotify_data = await response.json()
                request.state.spotify = spotify_data
                return spotify_data
                
    except Exception as error:
        print(f'[fastapi] Error getting Spotify token: {error}')
        raise HTTPException(status_code=500, detail='Failed to get Spotify token')
