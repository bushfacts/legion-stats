from Functions import *
from ComplexBinomial import *
import pathlib

currentPath = pathlib.Path(__file__).parent.resolve()
dataPath = currentPath.joinpath("Data\\Baer v BushFacts\\")
timeStart = "[08:34:04]"

ScrapeChatLog(dataPath.joinPath("chat_log.txt"), timeStart)

data = GetData(dataPath)
luckData = CalculateAttackProbabilities(data)
print(luckData)
