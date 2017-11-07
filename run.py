#!flask/bin/python
# import asyncio
# import datetime
from ybsuggestions import app


# async def update():
#     now = datetime.datetime.now()
#     print('Update', now.strftime("%Y-%m-%d %H:%M"))
#
#
# async def constant_update():
#     while True:
#         await update()
#         await asyncio.sleep(3, loop=loop)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

