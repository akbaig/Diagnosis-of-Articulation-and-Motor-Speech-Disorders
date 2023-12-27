from collections import OrderedDict
import math
import os
import fnmatch


def compare_verts(recorded_path, standards_path, word):

    false_words = os.listdir(standards_path)
    false_words.remove(word) #this now contains all other standards other than word
    false_words.remove("sentence") #exception

    print("Actual Word: ", word)
    actual_standard_path = os.path.join(standards_path, word, "meshes")
    actual_standard_score = compute(recorded_path, actual_standard_path)

    false_standard_score = 0

    for false_word in false_words:
        print("False Word: ", false_word)
        false_standard_path = os.path.join(standards_path, false_word, "meshes")
        false_standard_score += compute(recorded_path, false_standard_path)

    false_standard_score /= len(false_words)

    difference = false_standard_score - actual_standard_score

    verdict = ""
    accuracy = 0.0

    if(difference < 0):
        verdict = "Inaccurate"
        #factor = min(math.log10(abs(difference)) + 0.1, 1.0)
        factor = min(abs(difference)*50, 100)  
        accuracy = 100.0 - factor
    else:
        verdict = "Accurate"
        accuracy = 100.0
        


    output = f"Verdict: {verdict}\nActual: {round(actual_standard_score, 2)} - False: {round(false_standard_score, 2)} - Diff: {round(difference, 2)}"

    # verdict = "Accurate"

    # for false_word in false_words:
    #     false_standard_path = os.path.join(standards_path, false_word, "meshes")
    #     false_standard_score = compute(recorded_path, false_standard_path)
    #     if(false_standard_score < actual_standard_score):
    #         verdict = "Inaccurate"
    #         break

    # difference = false_standard_score - actual_standard_score

    # output = f"Verdict: {verdict}\nActual: {round(actual_standard_score, 2)} - False: {round(false_standard_score, 2)} - Diff: {round(difference, 2)}"

    return output

    

def compute(recorded, standard):
    #recorded has the path e.g. something/meshes
    #standard has the path e.g. voca/generated_animations/stream/meshes
    global_diffs = {}

    len_rec = len(fnmatch.filter(os.listdir(recorded), '*.obj'))
    len_std = len(fnmatch.filter(os.listdir(standard), '*.obj'))

    print(f"Lengths: {len_rec} - {len_std}")

    # if(len_rec != len_std):
    #     print("No. of meshes are not equal")
    #     return
    
    objects = min(len_std, len_rec)
    vertices = 5023
    diffs = []

    for file_index in range(objects):
        sub_filename = str(file_index).rjust(5, '0') + ".obj"
        file_name = os.path.join(standard, sub_filename)
        file_name2 = os.path.join(recorded, sub_filename)
        with open(file_name, "r") as reader:
            with open(file_name2, "r") as reader2:
                for i in range(vertices):
                    # for standard
                    splits = reader.readline().split(' ')
                    splits[3] = splits[3].replace("\n", "")
                    # for recorded
                    splits2 = reader2.readline().split(' ')
                    splits2[3] = splits2[3].replace("\n", "")
                    # storing x y z in variables
                    x_std, y_std, z_std = float(splits[1]), float(splits[2]), float(splits[3])
                    x_rec, y_rec, z_rec = float(splits2[1]), float(splits2[2]), float(splits2[3])
                    # print("Standard - ", f"Vertex {i}:", x_std, y_std, z_std)
                    # print("Recorded - ", f"Vertex {i}:", x_rec, y_rec, z_rec)
                    # copmarison through euclidean
                    diff_x = (x_std - x_rec)**2
                    diff_y = (y_std - y_rec)**2
                    diff_z = (z_std - z_rec)**2
                    
                    euclidean_dist = math.sqrt(diff_x + diff_y + diff_z)
                    diffs.append(euclidean_dist)

    diffs.sort(reverse=True)
    diffs = diffs[:100]
    sum_diffs = 0
    for diff in diffs:
        sum_diffs += diff
    #avg_diff = sum_diffs/len(diffs)
    avg_diff = sum_diffs
    return avg_diff
    
