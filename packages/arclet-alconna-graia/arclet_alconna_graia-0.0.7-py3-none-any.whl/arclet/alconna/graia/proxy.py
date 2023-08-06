from typing import Dict, Callable, Optional, Coroutine, Union, AsyncIterator, Literal, Tuple

# from graia.amnesia.message import MessageChain
from graia.ariadne import Ariadne, get_running
from graia.ariadne.dispatcher import ContextDispatcher
from graia.ariadne.util import resolve_dispatchers_mixin
from graia.broadcast import Broadcast, Dispatchable
from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from graia.ariadne.event.message import FriendMessage, GroupMessage, MessageEvent
from graia.ariadne.message.chain import MessageChain
from arclet.alconna.arpamar import Arpamar
from arclet.alconna.proxy import AlconnaMessageProxy, AlconnaProperty, runAlwaysAwait
from arclet.alconna.manager import commandManager

from . import Alconna


class AlconnaHelpDispatcher(BaseDispatcher):
    mixin = [ContextDispatcher]

    def __init__(self, alconna: "Alconna", help_string: str, source_event: MessageEvent):
        self.command = alconna
        self.help_string = help_string
        self.source_event = source_event

    async def catch(self, interface: "DispatcherInterface"):
        if interface.name == "help_string" and interface.annotation == str:
            return self.help_string
        if isinstance(interface.annotation, Alconna):
            return self.command
        if issubclass(interface.annotation, MessageEvent) or interface.annotation == MessageEvent:
            return self.source_event


class AlconnaHelpMessage(Dispatchable):
    """
    Alconna帮助信息发送事件
    如果触发的某个命令的帮助选项, 当AlconnaDisptcher的reply_help为False时, 会发送该事件
    """

    command: "Alconna"
    """命令"""

    help_string: str
    """帮助信息"""

    source_event: MessageEvent
    """来源事件"""


class GraiaAMP(AlconnaMessageProxy):
    preTreatments: Dict[
        Alconna, Callable[[MessageChain, Arpamar, Optional[str], Optional[MessageEvent]],
                          Coroutine[None, None, AlconnaProperty[MessageChain, MessageEvent]]
        ]
    ]

    def __init__(self, broadcast: Broadcast, skip_for_unmatch: bool = True):
        self.broadcast = broadcast
        self.skip_for_unmatch = skip_for_unmatch
        super().__init__(broadcast.loop)

        _queue = self.exportResults

        @self.broadcast.prelude_dispatchers.append
        class ExportResultDispatcher(BaseDispatcher):
            @staticmethod
            async def catch(interface: DispatcherInterface):
                if issubclass(interface.annotation, AlconnaProperty):
                    return await _queue.get()
                if interface.annotation == Arpamar:
                    return (await _queue.get()).result

        @self.broadcast.receiver(FriendMessage, priority=8)
        async def _(event: FriendMessage):
            await self.pushMessage(event.messageChain, event)

        @self.broadcast.receiver(GroupMessage, priority=8)
        async def _(event: GroupMessage):
            await self.pushMessage(event.messageChain, event)

    def addProxy(
            self,
            command: Union[str, Alconna],
            preTreatment: Optional[
                Callable[
                    [MessageChain, Arpamar, Optional[str], Optional[MessageEvent]],
                    Coroutine[None, None, AlconnaProperty[MessageChain, MessageEvent]]
                ]
            ] = None,
            help_flag: Literal["reply", "post", "stay"] = "stay",
            help_handler: Optional[Callable[[str], MessageChain]] = None,
    ):
        if isinstance(command, str):
            command = commandManager.getCommand(command)  # type: ignore
            if not command:
                raise ValueError(f'Command {command} not found')

        async def reply_help_message(
                origin: MessageChain,
                result: Arpamar,
                help_text: Optional[str] = None,
                source: Optional[MessageEvent] = None,
        ) -> AlconnaProperty[MessageChain, MessageEvent]:
            app: Ariadne = get_running()
            if result.matched is False and help_text:
                if help_flag == "reply":
                    help_text = await runAlwaysAwait(help_handler, help_text)
                    if isinstance(source, GroupMessage):
                        await app.sendGroupMessage(source.sender.group, help_text)
                    else:
                        await app.sendMessage(source.sender, help_text)
                    return AlconnaProperty(origin, result, None, source)
                if help_flag == "post":
                    dispatchers = resolve_dispatchers_mixin(
                        [AlconnaHelpDispatcher(command, help_text, source), source.Dispatcher]
                    )
                    for listener in self.broadcast.default_listener_generator(AlconnaHelpMessage):
                        await self.broadcast.Executor(listener, dispatchers=dispatchers)
                    return AlconnaProperty(origin, result, None, source)
            return AlconnaProperty(origin, result, help_text, source)

        self.pre_treatments.setdefault(command, preTreatment or reply_help_message)  # type: ignore

    async def fetchMessage(self) -> AsyncIterator[Tuple[MessageChain, MessageEvent]]:
        pass

    def laterCondition(self, result: AlconnaProperty[MessageChain, MessageEvent]) -> bool:
        if not result.result.matched and not result.helpText:
            if "-h" in str(result.origin):
                return False
            if self.skip_for_unmatch:
                return False
        return True
