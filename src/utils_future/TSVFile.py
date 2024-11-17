from utils import File
from utils import TSVFile as TSVFileOld


class TSVFile(TSVFileOld):
    def write(self, d_list: list[dict]):
        super().write(d_list)
        lines = File(self.path).read_lines()
        lines = [line for line in lines if line.strip()]
        File(self.path).write_lines(lines)
