from fastapi import Request


async def get_db(request: Request):
    return request.state.db
