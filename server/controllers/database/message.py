"""Message database controller."""

import hashlib
from urllib.parse import quote
from fastapi import Request, HTTPException, status
from bson import ObjectId
from models.Messages import Message


async def create_and_save_new(request: Request, message_data: dict):
    """
    Create and save a new message.
    
    Args:
        request: FastAPI request object
        message_data: Message data from request body
        
    Returns:
        dict: Saved message data
    """
    try:
        # Create hash
        data_string = f"user={message_data.get('author')}&source={message_data.get('source')}&content={message_data.get('content')}"
        encoded_data = quote(data_string)
        message_hash = hashlib.sha256(encoded_data.encode()).hexdigest()
        
        # Check for duplicates
        db = request.app.state.db
        existing = await db.messages.count_documents({'hash': message_hash})
        
        if existing > 0:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Message already exists')
        
        # Create new message
        new_message = {
            'hash': message_hash,
            'author': message_data.get('author'),
            'source': message_data.get('source'),
            'content': message_data.get('content')
        }
        
        result = await db.messages.insert_one(new_message)
        new_message['_id'] = str(result.inserted_id)
        
        return new_message
        
    except HTTPException:
        raise
    except Exception as error:
        print(f'[fastapi://controllers/database/message.py] createAndSaveNew() {error}')
        raise HTTPException(status_code=500, detail='Internal server error')


async def delete_by_id(request: Request, id: str):
    """
    Delete a message by ID.
    
    Args:
        request: FastAPI request object
        id: Message ID
        
    Returns:
        dict: Success message
    """
    try:
        if len(id) != 24:
            raise HTTPException(status_code=400, detail='Invalid ID format')
            
        db = request.app.state.db
        result = await db.messages.delete_one({'_id': ObjectId(id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=410, detail='Message not found')
            
        return {'status': 'deleted'}
        
    except HTTPException:
        raise
    except Exception as error:
        print(f'[fastapi] Error deleting message: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')


async def delete_all_by_author(request: Request, author: str):
    """
    Delete all messages by an author.
    
    Args:
        request: FastAPI request object
        author: Author name
        
    Returns:
        dict: Success message with count
    """
    try:
        db = request.app.state.db
        
        # Find messages first
        messages = await db.messages.find({'author': author}).to_list(length=None)
        
        if not messages:
            raise HTTPException(status_code=404, detail='No messages found for author')
        
        # Delete all messages
        result = await db.messages.delete_many({'author': author})
        
        if result.deleted_count != len(messages):
            raise Exception('Unable to delete all messages')
            
        return {'status': 'deleted', 'count': result.deleted_count}
        
    except HTTPException:
        raise
    except Exception as error:
        print(f'[fastapi] Error deleting messages by author: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')


async def get_all(request: Request):
    """
    Get all messages.
    
    Args:
        request: FastAPI request object
        
    Returns:
        dict: All messages
    """
    try:
        db = request.app.state.db
        messages = await db.messages.find({}).to_list(length=None)
        
        # Convert ObjectId to string
        for msg in messages:
            msg['_id'] = str(msg['_id'])
        
        return {'total': len(messages), 'messages': messages}
        
    except Exception as error:
        print(f'[fastapi] Error getting all messages: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')


async def get_all_by_author(request: Request, author: str):
    """
    Get all messages by an author.
    
    Args:
        request: FastAPI request object
        author: Author name
        
    Returns:
        dict: Messages by author
    """
    try:
        db = request.app.state.db
        messages = await db.messages.find({'author': author}).to_list(length=None)
        
        if not messages:
            raise HTTPException(status_code=404, detail='No messages found')
        
        # Convert ObjectId to string
        for msg in messages:
            msg['_id'] = str(msg['_id'])
        
        return {'author': author, 'total': len(messages), 'messages': messages}
        
    except HTTPException:
        raise
    except Exception as error:
        print(f'[fastapi] Error getting messages by author: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')


async def get_one_by_id(request: Request, id: str):
    """
    Get a single message by ID.
    
    Args:
        request: FastAPI request object
        id: Message ID
        
    Returns:
        dict: Message data
    """
    try:
        if len(id) < 24:
            raise HTTPException(status_code=400, detail='Invalid ID format')
            
        db = request.app.state.db
        message = await db.messages.find_one({'_id': ObjectId(id)})
        
        if not message:
            raise HTTPException(status_code=404, detail='Message not found')
        
        message['_id'] = str(message['_id'])
        return message
        
    except HTTPException:
        raise
    except Exception as error:
        print(f'[fastapi] Error getting message by ID: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')
