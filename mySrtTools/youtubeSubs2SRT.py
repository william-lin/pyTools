'''
Converts youtube auto-generated subtitles into SRT files. 

Usage: $python youtubeSubs2SRT.py [source]
Output: [source_converted.srt]
'''

from SrtTimeModule import SrtTime, modeException

def _mergeDict(li_key_value_pair):
    ''' Return a dict of {common_key:[value1, value2]), key2:[value2]} from 
    li_key_value_pair = [(common_key, value11), (common_key, value22), (key2, value2)]
    
    Take a list of key value pairs [('12:12', 'First'), ('12:12', 'More'), ('12:20', 'Last')]
    and return {'12:12':['First', 'More'], '12:20':['Last']}
    '''
    
    return_dict = {}
    for (key, value) in li_key_value_pair:
        try:
            li = return_dict[key]
        except KeyError:
            return_dict[key] = [value, ]
        else:
            li.append(value)
    return return_dict


def _validateSource(times, texts):
    '''Return True if the times and texts as read from the lines are as expected
    Expected format of source:
        00:06
        teasamedi
        00:08
        rnd program manager for semiflextech
    '''
    if len(times) < 1 or len(texts) < 1 or len(times) != len(texts):
        return False
    return True
    

def _getMergedDict(lines):
    ''' Return a merged dict from the lines read from the source file specified.
    '''
    lines = [x.strip("\n") for x in lines if len(x) > 0] #remove empty strings in the lines and strip "\n"
    times = lines[::2]
    texts = lines[1::2]
    
    if _validateSource(times, texts):
        li_key_value_pair = []
        for (time, text) in zip(times, texts):
            li_key_value_pair.append((time, text))
        merged_dict = _mergeDict(li_key_value_pair)
        return merged_dict
    else:
        print("Cannot process: Unpected source file content")
   
  
def _generatePseudoSrt(merged_dict):
    '''Return a list of [(time, text), (time, text)..] to be used for srt construction
    '''
    return_list = []
    keys = merged_dict.keys()
    for k in keys: #k could be '134:13'
        srt_text = " ".join(merged_dict[k]) #join all the lines by space
        try:
            mins, secs = k.split(":")
        except Exception:
            print("Unknown Error!")
        else:
            srt_time = SrtTime(mins=int(mins), secs=int(secs)).getString()
        return_list.append((srt_time, srt_text))
    
    #set an end time of 10 secs from the last recorded time to be used as a dummy
    final_dummy_time = SrtTime(mins=int(mins), secs=int(secs)+10).getString()
    final_dummy_text = " "
    return_list.append((final_dummy_time, final_dummy_text))
    
    return return_list

def _writeSrt(filename, srt_lines):
    ''' srt_lines contain one last dummy line at the end, which will not be written into the srt
    '''
    combined_string = ""
    i = 1
    while i < len(srt_lines):
        #write all previous_text into the file (last of the current text will not be written)
        begin_time, previous_text = srt_lines[i-1]
        current_time, current_text = srt_lines[i]
        
        #quick fix:
        #begin_time = begin_time[:-1] + "1"
        
        combined_string += str(i) + "\n"
        combined_string += begin_time + " --> " + current_time + "\n"
        combined_string += previous_text + "\n"
        combined_string += "\n"
        i += 1
        
    with open(filename, 'w') as writer:
        writer.write(combined_string)
    return combined_string
        
       
if __name__ == '__main__':
    import sys, os
    try:
        source = sys.argv[1]   
    except IndexError:
        print('No source file given')

    try:
        with open(source, 'r') as reader:
            lines = reader.readlines()             
    except FileNotFoundError:
        print('Source file {} does not exist!'.format(source))    
    
    finally:
        merged_dict = _getMergedDict(lines)
    
        if merged_dict:
            srt_lines = _generatePseudoSrt(merged_dict)
            return_string = _writeSrt(source+"_converted.srt", srt_lines)
        
        
#Test file sample
'''
00:06
teasamedi
00:08
rnd program manager for semiflextech
00:12
i manage the rnd funding programs the r
00:16
d programs are managed by semi-flex tech
00:19
through public-private partnership
00:21
between government and industry
'''