import asyncio

#
# async def a():
#     print('Suspending a')
#     await asyncio.sleep(0)
#     print('Resuming a')
#
#
# async def b():
#     print('In b')
#
#
# async def main():
#     await asyncio.gather(a(), b())
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
async def coroutine():
    print('in coroutine')
    return 'result'
if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    try:
        print('starting coroutine')
        coro = coroutine()
        print('entering event loop')
        # 通过调用事件循环的 run_until_complete() 启动协程
        result = event_loop.run_until_complete(coro)
        print(f'it returned: {result}')
    finally:
        print('closing event loop')
        event_loop.close() # 关闭事件循环