from LinuxServerStatsTelegramBot.DI import DI
from LinuxServerStatsTelegramBot.commmand.Command import Command
from LinuxServerStatsTelegramBot.commmand.ConvertTextToImage import ConvertTextToImage
from LinuxServerStatsTelegramBot.commmand.SendProgrammerBeeSticker import SendProgrammerBeeSticker

from LinuxServerStatsTelegramBot.commmand.CronStats import CronStats
from LinuxServerStatsTelegramBot.commmand.DiskStats import DiskStats
from LinuxServerStatsTelegramBot.commmand.DockerStats import DockerStats
from LinuxServerStatsTelegramBot.commmand.MemoryStats import MemoryStats
from LinuxServerStatsTelegramBot.commmand.DateAndLocation import DateAndLocation


class Invoker:
    @staticmethod
    def send_server_stats():
        # Invoker.send_sticker()
        # Invoker.send_data_as_image(DateAndLocation())
        Invoker.send_data_as_image(MemoryStats())
        # Invoker.send_data_as_image(DiskStats())
        # Invoker.send_data_as_image(DockerStats())
        # Invoker.send_data_as_image(CronStats())

    @staticmethod
    def send_data_as_image(command: Command):
        command_name = command.__class__.__name__
        sender = DI.get_sender()
        data = command.execute()
        image_path = f"/tmp/{command_name}.png"
        ConvertTextToImage(data=data, image_path=image_path).execute()
        sender.send_image(image_path=image_path)

    @staticmethod
    def send_sticker():
        sticker_path = SendProgrammerBeeSticker().execute()
        sender = DI.get_sender()
        sender.send_sticker(sticker_path=sticker_path)
