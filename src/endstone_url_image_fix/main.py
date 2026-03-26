from endstone.plugin import Plugin
from endstone.event import event_handler, PacketSendEvent
from bedrock_protocol.packets.minecraft_packet_ids import MinecraftPacketIds
import re

class Main(Plugin):
    api_version = "0.10"
    prefix = "URL Image Fix"

    def on_enable(self) -> None:
        self.logger.info("The URL Image Fix plugin has been enabled!")
        self.register_events(self)

    @event_handler
    def on_packet_send(self, event: PacketSendEvent) -> None:
        if event.packet_id == MinecraftPacketIds.ShowModalForm:
            pattern = re.compile(
                rb'"data":"(https?://[^"]*)","type":"path"'
            )

            def replacer(match: re.Match):
                url = match.group(1)
                return b'"data":"' + url + b'","type":"url" '

            event.payload = pattern.sub(replacer, event.payload)

            pattern_spaced = re.compile(
                rb'"data":\s*"(https?://[^"]*)",\s*"type":\s*"path"'
            )

            def replacer_spaced(match: re.Match):
                url = match.group(1)
                return b'"data":"' + url + b'", "type":"url" '

            event.payload = pattern_spaced.sub(replacer_spaced, event.payload)

            if event.player is not None:
                self.server.scheduler.run_task(
                    self,
                    lambda player=event.player: player.send_message("§z"),
                    delay=10,
                )