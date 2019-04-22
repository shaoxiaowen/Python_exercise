# findDuplicates方法来查找重复的曲目
import argparse
import plistlib

# 找到多个播放列表中共同的乐曲轨迹
import numpy as np
from matplotlib import pyplot


def findConnonTracks(fileNames):
    """
    Find common tracks in given playlist files, and save them
    to common.txt.
    """
    # alist of sets of track names
    trackNameSets = []
    for fileName in fileNames:
        # create a new set
        trackNames = set()
        # read in playlist
        plist = plistlib.readPlist(fileName)
        # get the tracks
        tracks = plist["Tracks"]
        # iterate through tracks
        for trackId, track in tracks.items():
            try:
                # add name to set
                trackNames.add(track["Name"])
            except:
                # ignore
                pass
        # add to list
        trackNameSets.append(trackNames)
    # get set of common tracks
    # intersection() 方法用于返回两个或更多集合中都包含的元素，即交集
    # 函数在调用多个参数时，在列表、元组、集合、字典及其他可迭代对象作为实参，并在前面加 *
    # 如   *（1,2,3）解释器将自动进行解包然后传递给多个单变量参数（参数个数要对应相等）

    # 使用set.intersection()方法来获得集合之间共同音轨的集合
    # (用Python*的运算符来展开参数列表)
    commonTracks = set.intersection(*trackNameSets)
    # write to file
    if len(commonTracks) > 0:
        # 以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件，
        # 并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
        # 一般用于非文本文件如图片等。
        f = open("common.txt", "wb")
        for val in commonTracks:
            s = "%s\n" % val
            f.write(s.encode("UTF-8"))
        f.close()
        print("%d common tracks found."
              "Track names written to common.txt" % len(commonTracks))
    else:
        print("No common tracks!")


# 针对音轨名称 收集评分和音轨时长，然后画图
def plotStats(fileName):
    """
    Plot some statistics by readin track information from playlist.
    """
    # read in playlist
    plist = plistlib.readPlist(fileName)
    # get the tracks
    tracks = plist['Tracks']
    # create lists of ratings and duration
    ratings = []
    durations = []

    # iterate through tracks
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            pass
    # ensure valid data was collected
    if ratings == [] or durations == []:
        print("No valid Albun Rating/Total Time data in %s." % fileName)
        return
    # cross plot
    # 将音轨时长数据放到32位整数数组中
    x = np.array(durations, np.int32)
    # convert to minutes
    # 利用numpy将操作应用于数组中的每个元素
    x = x / 60000.0
    #将音乐评分保存到另一个numpy数组y中
    y = np.array(ratings, np.int32)

    #用matplotlib在同一图像上绘制两张图

    # 告诉matplotlib 该图应该有两行(2) 一列(1),且下一个点应该在第一行(1)
    pyplot.subplot(2, 1, 1)
    # 通过plot()创建一个点，并且o告诉matplotlib用圆圈来表示数据
    pyplot.plot(x, y, 'o')
    # 为x轴和y轴设置略微大一点的范围，以便在图和轴之间留一些空间
    pyplot.axis([0, 1.05 * np.max(x), -1, 110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')

    # plot histogram
    pyplot.subplot(2, 1, 2)
    # 使用hist方法在同一张图中的第二行中，绘制时长直方图
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    pyplot.show()


# 找到重复的歌曲并写入文件
def findDuplicates(fileName):
    print('Finding duplicate tracks in %s...' % fileName)
    # read in a playlist
    # 接受一个p-list文件作为输入
    plist = plistlib.readPlist(fileName)
    # get the tracks from the Tracks dictionary
    # 访问Tracks字典
    tracks = plist['Tracks']
    # create a trace name dictionary,
    # 定义一个空的字典
    trackNames = {}
    # iterate through the tracks
    # 使用items()方法 迭代Tracks字典，这是Python在迭代字典时取得键和值的常用方法
    for trackId, track in tracks.items():
        try:
            # 取得字典中每一个音轨的名称和时长。
            name = track["Name"]
            duration = track["Total Time"]
            # look for existing entries
            # 用in关键字，检查当前乐曲是否已经在被构建的字典中
            if name in trackNames:
                # if a name and duration match,increment the count
                # round the track length to the nearest second

                # 如果trackNames已经有了同名歌曲，并且两首歌的时长相同
                # 用//操作符，将每隔音轨长度除以1000，由毫秒转为秒，并取整(四舍五入)
                if duration // 1000 == trackNames[name][0] // 1000:
                    count = trackNames[name][1]
                    # (duration, count)元组
                    trackNames[name] = (duration, count + 1)
            else:
                # add entry-duration and count
                # 使用元组记录相应歌曲的时长和数量，以歌曲名作为key
                trackNames[name] = (duration, 1)
        except:
            # ignore
            pass
    # 提取重复的音轨
    # store duplicates as(name,count) tuples
    # 创建空列表，保存重复乐曲
    dups = []
    # 迭代遍历traceNames字典
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))
    # save dups to file
    if len(dups) > 0:
        print("Found %duplicates. Track names saved to dup.txt" % len(dups))
    else:
        print("No duplicate tracks found!")
    # 使用open()方法将信息存入文件
    f = open("dups.txt", "w")
    for val in dups:
        f.write("[%d] %s\n" % (val[0], val[1]))
    f.close()


def main():
    # create parser
    descStr = """This program analyzes playlist files(.xml) exported from iTunes"""
    parser = argparse.ArgumentParser(description=descStr)
    # add a mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()

    # add expected arguments
    group.add_argument("--common", nargs='*', dest='plFiles', required=False)
    group.add_argument("--stats", dest='plFile', required=False)
    group.add_argument("--dup", dest='plFileD', required=False)

    args = parser.parse_args()
    if args.plFiles:
        # find common tracks
        findConnonTracks(args.plFiles)
    elif args.plFile:
        # plot stats
        plotStats(args.plFile)
    elif args.plFileD:
        # find duplicate tracks
        findDuplicates(args.plFileD)
    else:
        print("These are not the tracks you are looking for.")


#   main method
if __name__ == '__main__':
    # main()
    plotStats("test-data/rating.xml")
