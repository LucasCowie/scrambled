"""Spotify API controller."""

import os
from fastapi import Request, HTTPException
import aiohttp


async def now_playing(request: Request):
    """
    Get currently playing track from Spotify.
    
    Args:
        request: FastAPI request object with spotify token in state
        
    Returns:
        dict: Currently playing track data
    """
    try:
        endpoint = os.getenv('SPOTIFY_NOWPLAYING_ENDPOINT')
        access_token = request.state.spotify.get('access_token')
        
        if not access_token:
            raise HTTPException(status_code=401, detail='No Spotify access token')
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers={'Authorization': f'Bearer {access_token}'}
            ) as response:
                if response.status == 204:
                    return {'playing': False, 'message': 'No track currently playing'}
                    
                data = await response.json()
                return data
                
    except HTTPException:
        raise
    except Exception as error:
        print(f'[fastapi] Error getting now playing: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')
