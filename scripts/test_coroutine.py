import asyncio

def task1():
    print("hello")
    asyncio.sleep(3)
    print(" world")


async def task2():
    print("hello")
    await asyncio.sleep(3)
    print(" world")


async def say_after(delay, word):
    await asyncio.sleep(delay)
    print(word)
    return len(word)

async def main():
    tasks = [asyncio.create_task(say_after(len(word), word)) for word in ["hello", "world"]]

    for task in tasks:
        l = await task
        print(l)
        
asyncio.run(main())