
import asyncio
import logging
import time


logger = logging.getLogger('at')


STREAM_HANDLERS = [
    # {
    #     'queue': queue that receives the reply,
    #     'prefixes': [list of expected prefixes for the messages],
    #     'started': ms timestamp when this handler created,
    #     'timeout': ms within which this handler expires,
    # },
]
STREAM_LOCK = asyncio.Lock()


def now():
    return time.time()


class ATCommandError(Exception):
    pass

class ATCommandTimeout(Exception):
    pass


class Command:

    def __init__(self, command, w, timeout=None):
        self.command = command
        self.w = w
        self.timeout = timeout or 0.5

    async def __write_line(self, line):
        async with STREAM_LOCK:
            logger.debug('> %s', line)
            self.w.write(f'{line}\r\n'.encode())

    async def simple(self, param):
        # ATXXX0
        await self.__write_line(f'AT{self.command}{param}')

    async def execute(self):
        # AT+XXX
        await self.__write_line(f'AT+{self.command}')

    async def read(self):
        # AT+XXX?
        await self.__write_line(f'AT+{self.command}?')

    async def set(self, *args, noquote=False):
        # AT+XXX=1,2,"3"
        params = []
        for p in args:
            if isinstance(p, str) and not noquote:
                params.append(f'"{p}"')
            elif isinstance(p, bytes) and not noquote:
                params.append(f'"{p.decode()}"')
            else:
                params.append(str(p))
        params = ','.join(params)
        await self.__write_line(f'AT+{self.command}={params}')

    async def expect_ok_or_error(self, timeout=None):
        global STREAM_HANDLERS
        start = now()
        queue = asyncio.Queue()
        STREAM_HANDLERS.append({
            'started': start,
            'timeout': timeout or self.timeout,
            'queue': queue,
            'prefixes': ['OK', 'ERROR'],
        })
        try:
            reply = await asyncio.wait_for(queue.get(), timeout or self.timeout)
        except asyncio.TimeoutError:
            raise ATCommandTimeout(f'{self.command} timed out after {now() - start} ms')
        if reply == 'ERROR':
            raise ATCommandError(f'{self.command} ERROR')

    async def expect_reply(self, timeout=None):
        # +XXX reply
        global STREAM_HANDLERS
        start = now()
        queue = asyncio.Queue()
        STREAM_HANDLERS.append({
            'started': start,
            'timeout': timeout or self.timeout,
            'queue': queue,
            'prefixes': ['ERROR', f'+{self.command}'],
        })
        try:
            reply = await asyncio.wait_for(queue.get(), timeout or self.timeout)
        except asyncio.TimeoutError:
            raise ATCommandTimeout(f'{self.command} timed out after {now() - start} sec')
        if reply.startswith(f'+{self.command}:'):
            return reply.replace(f'+{self.command}:', '').strip()
        raise ATCommandError(f'{self.command} ERROR')


class AT:
    # https://en.wikipedia.org/wiki/Hayes_command_set

    def __init__(self, r, w, command_timeouts=None, default_timeout=0.5, log=None):
        # stream is an object with `write` and `readline` methods
        self.r = r
        self.w = w
        self.command_timeouts = command_timeouts or {}
        self.default_timeout = default_timeout
        self.log = None
        if log:
            self.log = open(log, 'w+')
        asyncio.create_task(self.listen_stream())

    async def listen_stream(self):
        global STREAM_HANDLERS
        try:
            while True:
                line = await self.r.readline()
                try:
                    line = (line.replace(b'\xff', b'')).decode().strip()
                except Exception as e:
                    logger.error(str(e))
                    continue
                if not line:
                    continue
                logger.debug('< %s', line)
                if self.log:
                    self.log.write(line + '\n')
                    self.log.flush()
                # cleanup handlers
                STREAM_HANDLERS = [x for x in STREAM_HANDLERS if not x.get('delete')]
                for handler in STREAM_HANDLERS:
                    if handler.get('timeout') is not None:
                        if now() > handler['started'] + handler['timeout']:
                            # handler expired
                            handler['delete'] = True
                            continue
                        for prefix in handler['prefixes']:
                            if line.startswith(prefix):
                                handler['queue'].put_nowait(line)
        except asyncio.CancelledError:
            logger.info('Exiting AT stream listener...')

    def __getattr__(self, name):
        return Command(
            name,
            w=self.w,
            timeout=self.command_timeouts.get(name, self.default_timeout),
        )
