#command

# python3 pipeline.py -i inputs/stream.mp4 -s stream


from re import sub
import sys
import os
import subprocess
import argparse
from compare_vertices import compare_verts

voca_folder = '../voca'
deca_folder = '../deca'

def get_frame_rate(filename):
    if not os.path.exists(filename):
        sys.stderr.write("ERROR: filename %r was not found!" % (filename,))
        return -1         
    out = subprocess.check_output(["ffprobe",filename,"-v","0","-select_streams","v:0","-print_format","flat","-show_entries","stream=avg_frame_rate"])
    rate = out.split('=')[1].strip()[1:-1].split('/')
    if len(rate)==1:
        return float(rate[0])
    if len(rate)==2:
        return float(rate[0])/float(rate[1])
    return -1

def get_duration(filename):
    if not os.path.exists(filename):
        sys.stderr.write("DURATION FIND ERROR: filename %r was not found!" % (filename,))
        return -1         
    out = subprocess.check_output(["ffprobe","-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename])
    return float(out)


def change_frame_rate(input, frame_rate, output):

    print("Reducing video frame rate to 24")
    if not os.path.exists(input):
        sys.stderr.write("ERROR: filename %r was not found!" % (input,))
        return -1
    
    if os.path.exists(output):
        subprocess.call(["rm", output])
    cmd = ("ffmpeg -i {0} -strict -2 -filter:v fps=fps={1} {2}".format(input, str(frame_rate), output)).split()
    subprocess.call(cmd)

def remove_silence(input, output):

    print("Removing silence using auto-editor")
    if not os.path.exists(input):
        sys.stderr.write("ERROR: filename %r was not found!" % (input,))
        return -1
    
    if os.path.exists(output):
        subprocess.call(["rm", output])
    subprocess.call(["conda", "run", "-v", "-v", "-n", "autoeditor", "./bash_files/auto-editor.sh", input])

def extract_audio(input, output):

    print("Extracting audio from video")
    if not os.path.exists(input):
        sys.stderr.write("ERROR: video file to extract audio from %r was not found!" % (input,))
        return -1

    if os.path.exists(output):
        subprocess.call(["rm", output])

    cmd = ('ffmpeg -i {0} -map 0:a -c copy {1}'.format(input, output)).split()
    subprocess.call(cmd)

def frames_to_deca(deca, input, output, audio):

    print("Creating meshes using deca")
    if not os.path.exists(input):
        sys.stderr.write("ERROR: folder %r was not found!" % (input,))
        return -1
    if not os.path.exists(audio):
        sys.stderr.write("ERROR: standard audio file %r was not found!" % (audio + ".wav",))
        return -1
    
    if os.path.exists(output):
        subprocess.call(["rm", "-r", output])
    subprocess.call(["mkdir", output])
    subprocess.call(["conda", "run", "-v", "-v", "-n", "deca", "./bash_files/run_deca.sh", deca, input, output, audio])

def adjust_duration(input, standard_path, output):
    
    print("Adjusting duration according to standard")
    if not os.path.exists(standard_path):
        sys.stderr.write("ERROR: standard audio file %r was not found!" % (standard_path + ".wav",))
        return -1

    input_duration = get_duration(input)
    standard_duration = get_duration(standard_path)
    if(input_duration == -1 or standard_duration == -1):
        return -1

    if os.path.exists(output):
        subprocess.call(["rm", output])
 
    adjust_factor = input_duration/standard_duration
    print("factors", input_duration, standard_duration)
    print("factor", adjust_factor)
    cmd = ('ffmpeg -i {0} -filter_complex [0:v]setpts={1}*PTS[v] -map [v] {2}'.format(input, 1.00/adjust_factor, output)).split()
    subprocess.call(cmd)

def adjust_audio(input, standard_path, output):
    
    print("Adjusting audio according to standard")
    if not os.path.exists(standard_path):
        sys.stderr.write("ERROR: standard audio file %r was not found!" % (standard_path + ".wav",))
        return -1

    input_duration = get_duration(input)
    standard_duration = get_duration(standard_path)
    if(input_duration == -1 or standard_duration == -1):
        return -1

    if os.path.exists(output):
        subprocess.call(["rm", output])
 
    adjust_factor = input_duration/standard_duration
    cmd = ('ffmpeg -i {0} -filter:a atempo={1} -vn {2}'.format(input, adjust_factor, output)).split()
    subprocess.call(cmd)

def video_to_frames(input, output):

    print("Extracting frames from video")
    if not os.path.exists(input):
        sys.stderr.write("ERROR: filename %r was not found!" % (input,))
        return -1
    if os.path.exists(output):
        subprocess.call(["rm", "-r", output])
    subprocess.call(["mkdir", output])
    subprocess.call(["ffmpeg", "-i", input, "{0}/%05d.jpg".format(output)])

def compute_score_for_app(ui, input, standard, send_msg, set_progress, voca=voca_folder, deca=deca_folder):

    current_dir = os.path.abspath(os.getcwd())
    out1 = "inputs/24_frame_rate.mp4"
    out2 = "inputs/24_frame_rate_ALTERED.mp4"
    out3 = "inputs/adjusted.mp4"
    out4 = "inputs/adjusted.wav"
    out5 = "inputs/frames"
    out6 = "outputs"
    out7 = os.path.join(out6, "meshes")
    out8 = os.path.join(out6, "diff.txt")
    standard_meshes = os.path.join(voca, "generated_animations")
    standard_wav = os.path.join(voca, "preprocess_audios/standard", standard + ".wav")
    send_msg(ui, "notify", "Setting frame rate to 24")
    set_progress(ui, int(1/8 * 100))
    change_frame_rate(input, 24, out1)
    send_msg(ui, "notify", "Removing silence")
    set_progress(ui, int(2/8 * 100))
    remove_silence(out1, out2)
    send_msg(ui, "notify", "Adjusting duration")
    set_progress(ui, int(3/8 * 100))
    adjust_duration(out2, standard_wav, out3)
    send_msg(ui, "notify", "Extracting audio from video")
    set_progress(ui, int(4/8 * 100))
    adjust_audio(out2, standard_wav, out4)
    send_msg(ui, "notify", "Converting video to frames")
    set_progress(ui, int(5/8 * 100))
    video_to_frames(out3, out5)
    send_msg(ui, "notify", "Converting frames to 3d meshes")
    set_progress(ui, int(6/8 * 100))
    frames_to_deca(deca, os.path.join(current_dir, out5), os.path.join(current_dir, out6), os.path.join(current_dir, out4))
    send_msg(ui, "notify", "Comparing to meshes with standard")
    set_progress(ui, int(7/8 * 100))
    diff = compare_verts(out7, standard_meshes, standard)
    send_msg(ui, "success", diff)
    set_progress(ui, int(8/8 * 100))
    with open(out8, "w") as writer:
        writer.write(diff)

def main(args):

    def empty_func(param1, param2, param3 = None):
        pass

    compute_score_for_app(None, args.inputpath, args.standard, empty_func, empty_func, args.voca, args.deca)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Speech Therapy')
    parser.add_argument('-i', '--inputpath', default='inputs/input.mp4', type=str, help='path to the video input')
    parser.add_argument('-s', '--standard', required=True, type=str, help='standard word to compare with')
    parser.add_argument('-v', '--voca', default=voca_folder, type=str, help='path to voca model')
    parser.add_argument('-d', '--deca', default=deca_folder, type=str, help='path to deca model')
    main(parser.parse_args())
