'''
Make tiny adjustments to the given SRT file to fix slight voice/subtitle out-of-sync problems.

Usage: $python srtTimeShift.py [srt file name] [absolute time difference in hh:mm:ss,xxx] [mode]

    --> mode: p for positive, n for negative, early for e, late for l
    --> If the subtitles appear early: time difference will be added (ex: mode=p or e)
    --> If the subtitles appear late: time difference will be subtracted (ex: mode=n or l)
    
Output: original file will be overwritten!
'''

from SrtTimeModule import SrtTime, modeException

if __name__ == "__main__":
    import sys
    
    #Establish the parameters: filename, timeShift, mode
    errorFree = False
    try:
        filename, timeShift, mode = sys.argv[1: ]
    except ValueError:
        print("Error: Wrong number of arguments")
        print('''
        Usage: $python *****.py [srt file name] [absolute time difference in hh:mm:ss,xxx] [mode]
            --> mode: p for positive, n for negative
            --> If the subtitles appear early: time difference will be added (ex: mode=p)
            --> If the subtitles appear late: time difference will be subtracted (ex: mode=n)
        ''')
    except Exception:
        print("Fatal Error: General exception triggered!")
        
    else:
        try:
            if mode not in ['p', 'e', 'n', 'l']:
                raise modeException
        except modeException:
            print("Error: mode should be 'p' or 'n'")
        else:
            try:
                diff = SrtTime(timeShift)
            except Exception:
                print("Error: Can not make timeShift into object: format should be: [hh:mm:ss,xxx]")
            else:
                errorFree = True
        
    #Do the heavy lifting here if no errors occured
    if errorFree:
        with open(filename, 'r') as reader:
            line = reader.readline()
            stuff_to_write = ""
            while line:
                if " --> " not in line:
                    stuff_to_write += line
                else:
                    line = line.strip("\n").strip(" ").strip("\n").strip(" ") #paranoid here
                    begin = SrtTime(string=line.split(" --> ")[0])
                    end = SrtTime(string=line.split(" --> ")[1])
                    if mode == 'p' or mode == 'e':
                        begin = begin + diff
                        end = end + diff
                    else:
                        begin = begin - diff
                        end = end - diff
                    stuff_to_write += begin.getString() + " --> " + end.getString() + "\n"
                line = reader.readline()
        with open (filename, 'w') as writer:
            writer.write(stuff_to_write)
