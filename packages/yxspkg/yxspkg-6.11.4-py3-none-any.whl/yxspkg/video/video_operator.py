from asyncio import streams
import os
import subprocess
import click 
from pathlib import Path
import subprocess
import json
import time

@click.command()
@click.argument('args',nargs=-1)
@click.option('--rotate',default=None,help='旋转视频')
@click.option('--replace',default=False,help='是否替换该文件',is_flag=True)
@click.option('--ffmpeg_parameter','-f',default='-c copy',help='ffmpeg 参数')
@click.option('--to_mp4','-t',default=False,help='将文件转化为mp4格式',is_flag=True)
@click.option('--delete','-d',default=False,help='删除源文件',is_flag=True)
@click.option('--copy_only','-c',default=False,help='是否只进行copy转码的任务，其它需要解码的则跳过',is_flag=True)
@click.option('--subtitle','-s',default=False,help='提取文件字幕',is_flag=True)
def main(args,replace,rotate,ffmpeg_parameter,to_mp4,delete,copy_only,subtitle):
    if subtitle:
        extract_subtitle(args[0])
    if to_mp4:
        convert2mp4(args,delete,copy_only)
        return 
    input_file = Path(args[0]).absolute()
    if len(args) > 1:
        output_file = Path(args[1]).absolute()
    else:
        output_file = input_file.parent / (input_file.stem+'_output'+input_file.suffix)
    if input_file.is_file():
        temp_file = output_file.parent / (output_file.stem+'_temp'+output_file.suffix)
        ffmpeg_i = f'ffmpeg -i "{input_file}" '
        if rotate:
            ffmpeg_command = ffmpeg_i + f' -metadata:s:v:0 rotate={rotate} ' + ffmpeg_parameter +f' "{temp_file}"'
        t = subprocess.call(ffmpeg_command,shell=True)
        assert t == 0
        if replace:
            os.rename(temp_file,input_file)
        else:
            os.rename(temp_file,output_file)
def convert2mp4(args,delete=False,copy_only=False):
    other_video = {'.avi','.mkv','.rmvb','.wmv','.mpg','.mov','.rm','.flv','3gp','.asf','.mod','.rmvb'}
    if len(args) > 0:
        pnw = Path(args[0])
    else:
        pnw = Path('./')
    norr = list()
    for root,_,fs in os.walk(pnw):
        for f in fs:
            if Path(f).suffix.lower() in other_video:
                vfile = Path(root) / f
                params = get_video_parameter(vfile)
                if 'streams' not in params:
                    norr.append(vfile)
                code_names = set([i['codec_name'].lower() for i in params['streams']])
                codea = None
                for ac in ['aac','ac3']: #['aac','eac3','ac3']
                    for j in code_names:
                        if j.find(ac) != -1:
                            codea = 'copy'
                            break
                    if codea == 'copy':
                        break
                else:
                    codea = 'aac'
                for vc in ['264']:
                    for j in code_names:
                        if j.find(vc) != -1:
                            codev = 'copy'
                            break
                    if codev == 'copy':
                        break
                else:
                    codev = 'h264'
                if copy_only:
                    if codea != 'copy' or codev != 'copy':
                        norr.append(vfile)
                        continue
                mp4file = vfile.with_suffix('.mp4')
                aa = subprocess.call(f'ffmpeg -i "{vfile}" -c:v {codev} -c:a {codea} -y "{mp4file}"',shell=True)
                if aa==0 and delete:
                    time.sleep(0.1)
                    os.remove(vfile)
    print('未处理文件：')
    for i in norr:
        print(i)
    print('处理完成')
def get_video_parameter(video_path):
    def filter_parameter(params):
        pl = [i for i in params.splitlines() if not i.startswith('Cannot')]
        return '\n'.join(pl)
    t = f'ffprobe -i "{str(video_path)}" -print_format json -show_format -show_streams -v quiet'
    all_parameter=subprocess.getoutput(t)
    all_parameter = filter_parameter(all_parameter)
    all_parameter=json.loads(all_parameter)
    return all_parameter
def extract_subtitle(pdir):
    videos = {'.avi','.mkv','.rmvb','.wmv','.mpg','.mov','.rm','.flv','3gp','.asf','.mod','.rmvb','.mp4'}
    pnw = Path(pdir)
    if pnw.is_dir():
        fs = [Path(root) / f for root,_,fs in os.walk(pnw) for f in fs if Path(f).suffix.lower() in videos]
    else:
        fs = [pnw]
    for vfile in fs:
        params = get_video_parameter(vfile)
        if 'streams' not in params:
            continue
        subtitles = [i for i in params['streams'] if i['codec_type']=='subtitle']
        if subtitles:
            for ii,sf in enumerate(subtitles):
                tag = sf['tags'].get('title','')
                sfile = vfile.with_name(f'{vfile.stem}_{ii}{tag}.srt')
                aa = subprocess.call(f'ffmpeg -i "{vfile}" -y "{sfile}"',shell=True)

if __name__=='__main__':
    main()