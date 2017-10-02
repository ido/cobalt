#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
"""Generate graphical representation of the current reservations in Blue Gene/L.
   gen_tree_view --
   mod_reserv_dict --
   gen_part_hits --
   ret_short_str --
   ret_all_reservs --
   detect_shared_parts --
   detect_conflicts --
   prnt_plain_conflicts --
   prnt_verbose_conflicts --
   gen_image --
"""
__revision__ = '$Revision: 1189 $'

# BASIC USAGE:
#
# Diagram.py -flag file_name file_format res_select w/wo_conflicts_legened
# e.g. Diagram.py -g my_file png 1 y
#
# PIL DOCUMENTATION:
#
# http://www.pythonware.com/library/pil/handbook/index.htm
#

import math, optparse, os, random, re, sys, time
import Image, ImageDraw, ImageFont 
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

orig_author = "Svetlin Denkov"
last_mod = "Svetlin Denkov"
prog_name = "Mapres OD"
ver_num = "1.0"
ver_date = "2006/09/20"

part_planes = ("R000", "R001") 
part_names = ("_J102", "_J104", "_J106", "_J108", "_J111", "_J113", "_J115", "_J117", \
              "_J203", "_J205", "_J207", "_J209", "_J210", "_J212", "_J214", "_J216")
part_size = "-32" # smallest reserv size = 32 nodes

reserv_part_hits = {} # key = curr reserv, val = 32-node partition hits

reserv_top_part = {} # key = curr reserv, val = reserv top partition; in */# notation

reserv_xy = {} # key = curr reserv, val = (x1, x2, y1, y2); in pixels

part_y = {} # key = partition name, val = (y1, y2); in pixels

part_conflicts = {} # key = (reserv1, reserv2), val = (list of all conflicting partitions)
                    # stores pairs of reservs with conflicting partitions
part_conflicts_times = {} # key = (reserv1, reserv2), val = (conflicting_start_time, conflicting_end_time)
                          # stores pairs of reservs with conflicting time zones; in epoch time

def gen_tree_view(tree_root, part_list, npart_dict):
    """Create a tree view of the partition names within a current reservation.
       tree_root --
       part_list --
       npart_dict --
       return value
       exceptions
    """
    if tree_root in part_list:
        part_list.remove(tree_root) # 'tree_root' is the 'head' of the original list
        part_list.insert(len(part_list), tree_root) # part_list.insert(0, tree_root) flips the tree
        for child in npart_dict[tree_root]["deps"]:
            gen_tree_view(child, part_list, npart_dict)
    else: 
        pass
    return

def mod_reserv_dict(reserv_dict, part_list, npart_dict, dep_info):
    """Modify the 'reservations' dictionary to reflect the generated tree view 
       of the partition names.
       reserv_dict --
       part_list --
       npart_dict --
       dep_info --
       return value
       exceptions
    """
    # changes number and order of tuple items of a single reserv (a dict key)
    for curr_part in part_list:  
        for curr_reserv in curr_part['reservations']:
            curr_reserv.append(curr_reserv[2] + curr_reserv[3]) # adds 'end time' in epoch format to the end
            curr_reserv.insert(0, curr_reserv[1]) # moves 'user' to the front
            del curr_reserv[2] # removes duplicate original 'user' 
            # generates the reserv dict - makes sures reservs are not processed multiple times
            if reserv_dict.has_key(tuple(curr_reserv)): # the curr reserv exists in 'reserv_dict' as key
                # adds partition name to the value list
                reserv_dict[tuple(curr_reserv)].append(curr_part['name']) 
            else:
                # adds key and the first entry in the key's value list
                reserv_dict[tuple(curr_reserv)] = [curr_part['name']] 
    # generates tree view of a reserv's partitions (key's value)
    for ((user, name, start, duration, end), part_list) in reserv_dict.iteritems():
        # finds partition with biggest node size
        max_size = max([npart_dict[curr_part].get('size') for curr_part in part_list]) 
        top_part = [npart_dict[curr_part] for curr_part in part_list \
                   if npart_dict[curr_part].get('size') == max_size][0].get('name')        
        # saves the following notation for each reservation into a new dictionary
        if len([curr_part for curr_part in part_list \
                   if curr_part in dep_info[top_part][1]]) == len(dep_info[top_part][1]):
            # including all partitions under the top partition 
            reserv_top_part[(user, name, start, duration, end)] = top_part + "*" 
        else: 
            # including some, but not all partitions under the top partition included 
            reserv_top_part[(user, name, start, duration, end)] = top_part + "#" 
        # sorts partitions into a binary tree view
        gen_tree_view(top_part, part_list, npart_dict)
    return

def gen_part_hits(reserv_dict):
    """Record which 32-node partitions from the entire system exist in each 
       individual reservation.
       reserv_dict --
       return value
       exceptions
    """
    for curr_reserv in reserv_dict.keys():
        temp_partition_list = [] # temp 32-node partition hit list for curr reserv     
        for curr_part in reserv_dict[curr_reserv]: # finds partition hits for curr reserv
            pattern = re.compile("R00[0|1]_J[1|2][0|1][0-9]-32") 
            if pattern.search(str(curr_part)): # checks for partitions matching the pattern 
                match_obj = pattern.search(str(curr_part))
                match = match_obj.group() # returns actual match
                temp_partition_list.append(match) # adds partition name to the temp list of partition hits
        reserv_part_hits[curr_reserv] = temp_partition_list # records the list of partition hits for the curr reserv
    return

def ret_short_str(epoch_time):
    """Return a human-readable string of epoch time in the format: 
       %Y-%m-%d/%H:%M.
       epoch_time --
       return value --
       exceptions
    """
    return time.strftime("%Y-%m-%d/%H:%M", time.localtime(epoch_time))

def ret_all_reservs(reserv_dict): 
    """Return a list of current reservations and their encapsulated 
       information (user, name, start time, duration, end time).
       reserv_dict --
       return value -- 
       exceptions
    """
    return reserv_dict.keys()

def detect_shared_parts(reserv_one, reserv_two, reserv_dict): 
    """Detect shared partitions across any two reservations with 
       conflicting times.
       reserv_one -- 
       reserv_two --
       reserv_dict --
       return value
       exceptions
    """
    curr_part_conflicts_all = [] # temp list for all conflicting partitions
    curr_part_conflicts_32 = [] # temp list for only 32-node conflicting partitions
    pattern = re.compile("R00[0|1]_J[1|2][0|1][0-9]-32") # search pattern for 32-node partitions
    for part_one in reserv_dict[reserv_one]:
        for part_two in reserv_dict[reserv_two]:
            if part_one == part_two: # compares regardless of partition size
                if pattern.search(str(part_one)): # checks for partitions matching the pattern (all 32-node partitions)
                    match_obj = pattern.search(str(part_one))
                    match = match_obj.group() # returns actual match, the partition name itself
                    curr_part_conflicts_32.append(match) # 32-node partition added to list and sorted alphabetically
                # adds curr shared partition to list of all conflicting partitions for the two reservs
                curr_part_conflicts_all.append(part_one) 
                # assigns updated list as value to the pair of time-conflicting reservs 
                part_conflicts[(reserv_one, reserv_two)] = curr_part_conflicts_all 
            else: # partitions != same
                pass
    if len(curr_part_conflicts_32) == 0: # temp list has no conflicting 32-node partitions
        # removes reserv pairs with conflicting times, but no conflicting partitions; no real conflict
        del part_conflicts_times[(reserv_one, reserv_two)] 
    else: # temp list has conflicting 32-node partitions 
        # appends list of sorted 32-node conflicting partitions
        part_conflicts_times[(reserv_one, reserv_two)].append(curr_part_conflicts_32)  
    return

def detect_conflicts(reserv_dict): 
    """Compare the start time of current reservation to end times 
       of remaining reservations, and also compare the end time of 
       current reservation to start times of remaining reservations. 
       Function is called on each reservation; after each function 
       calls the current reservation is removed from the set of 
       reservations to prevent duplicate comparisons.
       reserv_dict -- 
       npart_dict --
       return
       exceptions
    """
    reserv_list = ret_all_reservs(reserv_dict) # avoids direct mod of the 'reservations' dict by copying its keys
    iterator = 0  
    if len(reserv_dict) <= 1: # if 0 or 1 reservs conflicts cannot exist
        pass
    elif len(reserv_dict) > 1:
        for list_item in reserv_list: # chooses first reserv
            iterator += 1
            for next_item in reserv_list[iterator:]: # choose second reserv
            #if StartTime(a) >= EndTime(b) or EndTime(a) <= StartTime(b) 
                if list_item[2] >= next_item[4] or list_item[4] <= next_item[2]:
                    pass # no time conflict exists, partitions cannot be overlapped; nothing recorded
                else: 
                    # appends correct conflict zones' start and end times
                    if (list_item[2] < next_item[2]) or (list_item[2] == next_item[2]):
                        if list_item[4] > next_item[4]:
                            part_conflicts_times[(list_item, next_item)] = [next_item[2], next_item[4]]
                        elif list_item[4] == next_item[4]:
                            part_conflicts_times[(list_item, next_item)] = [next_item[2], next_item[4]]
                        elif list_item[4] < next_item[4]:
                            part_conflicts_times[(list_item, next_item)] = [next_item[2], list_item[4]]             
                    elif list_item[2] > next_item[2]:
                        if list_item[4] > next_item[4]:
                            part_conflicts_times[(list_item, next_item)] = [list_item[2], next_item[4]]
                        elif list_item[4] == next_item[4]:
                            part_conflicts_times[(list_item, next_item)] = [list_item[2], next_item[4]]
                        elif list_item[4] < next_item[4]:
                            part_conflicts_times[(list_item, next_item)] = [list_item[2], list_item[4]]
                    # time conflict exists, then check for partition conflicts
                    detect_shared_parts(list_item, next_item, reserv_dict) 
            reserv_list.remove(list_item) # removes from pool of reservs to avoid duplicate comparisons 
            reserv_list.insert(0, 0) # keeps the list's length constant, so correct indeces are selected
    return
    
def prnt_plain_conflicts(): 
    """Print a plain view of any conflicting reservations 
       pairs including the following information: username, 
       reservation name, start time, end time for each of 
       the two reservations.
       return value 
       exceptions
    """
    if (len(part_conflicts) == 0): # checks if entries exist in the global conflicts dict
        print("\nNo conflicts detected in 'plain mode'.\n")
    else:
        # header category names
        header = [("User1", "Reservation1", "StartTime1", "EndTime1", \
                   "User2", "Reservation2", "StartTime2", "EndTime2")] 
        format_conflicts = [] # data structure containing the actual information
        #all conflicts stored to single list and can be printed at once; eliminates multiple header printing
        next_index = 0 
        print("\nConflicts detected in 'plain mode'.\n")
        for pair in part_conflicts.keys():
            # pair[0][*] = attributes of first reserv; pair[1][*] = attributes of second reserv
            format_conflicts.insert(next_index, (pair[0][0], pair[0][1], ret_short_str(pair[0][2]), \
              ret_short_str(pair[0][4]), pair[1][0], pair[1][1], \
              ret_short_str(pair[1][2]), ret_short_str(pair[1][4]))) 
            next_index += 1 # advances index to placeholder of next reserv pair
        Cobalt.Util.print_tabular(header + format_conflicts) # prints info in org fashion
        print("\n")
    return

def prnt_verbose_conflicts():
    """Print a verbose view of any conflicting reservations 
       pairs including the following information: username, 
       reservation name, start time, end time for each of 
       the two reservations, and also a list of shared 
       partitions.
       return value 
       exceptions
    """
    if (len(part_conflicts) == 0): # checks if entries exist in the global conflicts dictionary
        print("\nNo conflicts detected in 'verbose mode'.\n")
    else:
        print("\nConflicts detected in 'verbose mode'.\n")
        # header category names
        header = [("User1", "Reservation1", "StartTime1", "EndTime1", \
                   "User2", "Reservation2", "StartTime2", "EndTime2")] 
        for pair in part_conflicts.keys():
            # pair[0][*] = attrbs of 1st reserv; pair[1][*] = attrbs of 2nd reserv; prints info in org fashion
            Cobalt.Util.print_tabular(header + [(pair[0][0], pair[0][1], ret_short_str(pair[0][2]), \
              ret_short_str(pair[0][4]), pair[1][0], pair[1][1], \
              ret_short_str(pair[1][2]), ret_short_str(pair[1][4]))]) 
            # for each pair prints the list of conflicting partitions separated by '|'
            print("|".join(part_conflicts[pair]) + "\n") 
    return

#optional
def R1(left, right, the_list):
    """recursive binary division test - horizontal line"""
    middle = int(math.ceil((left + right)/2))
    if middle == left or middle == right:
        pass
    elif middle != 0 and middle > 0:
        the_list.append(middle)
        print "D1: " + str(left) + " D2: " + str(right) + " Dm: " + str(middle)
        R1(left, middle, the_list)
        R1(middle, right, the_list)

#optional
def R2(left, right, bottom, top):
    """recursive binary division test - horizontal and vertical lines"""
    middle_h = int(math.ceil((left + right) / 2))
    middle_v = int(math.ceil((bottom + top) / 2))
 
    if middle_h == left or middle_h == right:
        pass
    elif middle_h != 0 and middle_h > 0:
        R1(left, middle_h)
        R1(middle_h, right)  
    print ""
    if middle_v == bottom or middle_v == top:
        pass
    elif middle_v != 0 and middle_v > 0:
        R1(bottom, middle_v)
        R1(middle_v, top)  

def gen_image(reserv_dict):
    """Create a graphic of the current reservations in Blue Gene/L using PIL.
       reserv_dict --
       return 
       exceptions
    """
    # DETERMINES IMAGE RESOLUTION

    # The permisable resolutions are:
    # 1024 x 768, 1154 x 864, 1280 x 1024, 1400 x 1050, 1600 x 1200
    
    if int(options.graph[2]) == 1:
        res_x = 1024
        res_y = 768
    if int(options.graph[2]) == 2:
        res_x = 1154
        res_y = 864
    if int(options.graph[2]) == 3:
        res_x = 1280
        res_y = 1024
    if int(options.graph[2]) == 4:
        res_x = 1400
        res_y = 1050
    if int(options.graph[2]) == 5:
        res_x = 1600
        res_y = 1200
    elif int(options.graph[2]) < 1 or int(options.graph[2]) > 5:
        sys.exit("\nUnrecognized resolution selection! Available choices are 1 through 5.\n")    

    # GENERATES THE CANVAS AND ITS IMAGE

    canvas_x = int(res_x) # the canvas width 
    canvas_y = int(res_y) # the canvas height 
    # creates canvas image; mode = RGB, size = (canvas_x, canvas_y), color = white
    image = Image.new("RGB", (canvas_x, canvas_y), (255, 255, 255)) 
    canvas = ImageDraw.Draw(image) # draws the image onto the canvas
    def_font = ImageFont.load_default() # uses PIL's default font for drawing all text

    # DRAWS THE TITLE

    image_title = "Current Blue Gene/L Reservations"
    # draws title centered in terms of canvas's width; 'textsize' returns tuple (x, y) of last string character 
    # moves text 50% of its width to the left and 3% of the canvas's height towards the bottom
    # color = black, font = default
    canvas.text((canvas_x * 0.5 - canvas.textsize(image_title)[0] * 0.5, canvas_y * 0.03), \
        fill = (0, 0, 0), text = image_title, font = def_font) 

    # DRAWS THE STATISTIC INFORMATION

    user_s = os.environ['USER'] # user currently running the application
    host_s = os.environ['HOST'] # host machine currently running the application
    date_s = time.strftime("%m-%d-%Y", time.localtime(time.time())) # current date e.g. 09-15-2006
    time_s = time.strftime("%H:%M:%S", time.localtime(time.time())) # current time e.g. 15:13:43
    stat_info = "User: " + user_s + " || Host: " + host_s + " || Date: " + date_s + " || Time: " + time_s
    # draws statistic info centered in terms of canvas's width; 
    # 'textsize' returns tuple (x, y) of last string character 
    # moves text 50% of its width to the left and 5% of the canvas's height towards the bottom 
    # it does not overlap with the title (5% - 3% = 2% slack space) 
    # color = red, font = default   
    canvas.text((canvas_x * 0.5 - canvas.textsize(stat_info)[0] * 0.5, canvas_y * 0.05), \
        fill = (255, 0, 0), text = stat_info, font = def_font) 

    # CREATES DYNAMIC X-AXIS

    # e.g. 09/30/006-12:04:24
    start_date = time.mktime(time.strptime(options.graph[4], "%m/%d/%y-%H:%M:%S"))
    end_date = time.mktime(time.strptime(options.graph[5], "%m/%d/%y-%H:%M:%S"))
    num_days = int(math.floor((end_date - start_date) / (24 * 3600)))

    days_names = {} # coordinates of the day label names corresponding to major tics on the ruler
    start_res_x = start_date # first day = start date specified
    for day in xrange(0, num_days + 1): # +1 so rightmost day mark is included
        days_names[day] = start_res_x
        start_res_x = start_res_x + 24 * 3600 # increments by day in terms of seconds

    # SETS UP THE MESH	

    # generates complete partition name following the node notation
    part_label = part_planes[0] + part_names[0] + part_size 
    # 20 pixels slack space; 10 pixels on each side of the partition label 
    mesh_start_pixel = canvas.textsize(part_label)[0] + 20 
    # canvas total width - 100% label width - additional 30% label width, so mesh fits perfectly within the canvas; 
    # the smaller the mesh width, the better it fits within the canvas;
    # - 110% or - 1.1 label width will result in a wider mesh, which runs out of the canvas
    mesh_width = canvas_x - 1.3 * mesh_start_pixel 

    # rectangle width in the mesh; based on the duration of all reservs in days = num_days; MAKE rect_width dynamic 
    rect_width = mesh_width / num_days     
    # height of a single rectangle in the mesh; 1.5% the mesh width (do not change percentage)       
    rect_height = mesh_width * 0.015                                      

    # starting x-coordinate of the first rectangle in the mesh;  
    mesh_x = mesh_start_pixel 
    # starting y-coordinate of the first rectangle in the mesh; 8% of the mesh width (do not change percentage)
    mesh_y = canvas_y * 0.08   
                             
    mesh_x_copy = mesh_x # fresh unmodified copy
    mesh_y_copy = mesh_y # fresh unmodified copy

    label_width = mesh_start_pixel # the width of a 32-node partition label (20-pixel slack space included)

    label_names = [] # the list of complete partition names as labels 
    for plane in part_planes: # the list of planes
        for name in part_names: # the list of names
            partition = plane + name + part_size # combined partition name following the specified notation
            label_names.append(partition) # add current partition to the list label names   
    label_names.sort()    #'R000_J102-32', 'R000_J104-32',...'R001_J216-32'; sorted by name 
    label_names.reverse() #'R001_J216-32,'...'R000_J104-32', 'R000_J102-32'; reversed 

    # starting x-coordinate of the y-axis labels; 1% of the canvas width (do not change percentage)
    labels_x = canvas_x * 0.01 
    # starting y-coordinate of the y-axis labels; 8% of the canvas width (increases progressively) 
    labels_y = mesh_y            

    # GENERATES THE X COORDINATES (X1, X2) FOR ALL RESERVATIONS
    # (X1, Y1) and (X2, Y2) = 2 pts defining the reservations' rectangles

    time_per_pixel = float(end_date - start_date) / mesh_width # number epoch time units per pixel based on mesh width
    for curr_reserv in reserv_dict.keys():
        # reservation occurs before or after the currently observed time period
        # hence no need to draw it
        if (curr_reserv[2] < start_date and curr_reserv[4] <= start_date) or \
           (curr_reserv[2] >= end_date and curr_reserv[4] > end_date):
            #del reserv_dict[curr_reserv]
            start_pixel = -1 # x1; negative value so the 'dot' drawn off the canvas
            end_pixel = -1 # x2; negative value so the 'dot' drawn off the canvas
        else:
            # reservation occurs at the start date of the currently observed time period
            # hence 'cut off' any parts hanging to the left of the mesh
            if curr_reserv[4] > start_date and curr_reserv[2] <= start_date:
                particular_start_time = start_date - start_date
                particular_end_time = curr_reserv[4] - start_date
            # reservation occurs at the end date of the currently observed time period
            # hence 'cut off' any parts hanging to the right of the mesh
            elif curr_reserv[2] < end_date and curr_reserv[4] >= end_date:
                particular_start_time = curr_reserv[2] - start_date
                particular_end_time = end_date - start_date
            # reservation occurs within the currently observed time period
            # hence draw the entire reservation
            elif curr_reserv[2] > start_date and curr_reserv[4] < end_date:
                particular_start_time = curr_reserv[2] - start_date 
                particular_end_time = curr_reserv[4] - start_date
            # reserv start and end pixel based on mesh
            start_pixel = (particular_start_time / time_per_pixel) + label_width
            end_pixel = (particular_end_time / time_per_pixel) + label_width 
        reserv_xy[curr_reserv] = [int(math.ceil(start_pixel)), int(math.ceil(end_pixel))] # X1, X2
       
    # GENERATES THE Y COORDINATES (Y1, Y2) FOR ALL RESERVATIONS
    # (X1, Y1) and (X2, Y2) = 2 pts defining the reservations' rectangles

    # reserv_xy[curr_reserv].append(int(math.floor(part_y[reserv_part_hits[curr_reserv][-1]][0])))
    # reserv_xy[curr_reserv].append(int(math.floor(part_y[reserv_part_hits[curr_reserv][0]][1]))) 
    # these two lines can cause a problem if a reservation is scheduled, which includes
    # only the top partition and no other partitions (aka '#' notation)
    # e.g. ANL_R00, ANL_R001, ANL_R000 or R000_J102-128
    # it is a problem because no 32-node partitions are detected
    # in theory no such reservation should exist (hack used by admins for scheduling reservations)
    # breaks at reserv_part_hits[curr_reserv][0 or -1] because there is no such value (a 32-node hit)

    labels_y_copy = labels_y
    for partition in label_names: # take into account the reversed order
        part_y[partition] = (labels_y_copy, labels_y_copy + rect_height) # these remain constant
        labels_y_copy += rect_height
    for curr_reserv in reserv_dict.keys():  
        # X1 = X2 = -1; reserv located out of mesh, so it must not be drawn    
        if reserv_xy[curr_reserv][0] == 0 and reserv_xy[curr_reserv][1] == 0: 
            reserv_xy[curr_reserv].append(-1) # Y1 = -1
            reserv_xy[curr_reserv].append(-1) # Y2 = -1
        else:
            # reserv_part_hits[curr_reserv] is already sorted in incrementing order 102, 104...
            # reserv_part_hits[curr_reserv][-1] = top 32-node part by name for curr reserv e.g 216 
            # (upper in the graph image, hence smaller depth in pixels)
            # [0] = Y1, first of 2 values in tuple returned by part_y (y coords of curr part)
            reserv_xy[curr_reserv].append(int(math.floor(part_y[reserv_part_hits[curr_reserv][-1]][0]))) 
            # reserv_part_hits[curr_reserv][0] = first 32-node part by name for curr reserv e.g. 102
            # (lower in the graph image, hence bigger depth in pixels),
            # [1] = Y2, second of 2 values in tuple returned by part_y (y coords of curr part)
            reserv_xy[curr_reserv].append(int(math.floor(part_y[reserv_part_hits[curr_reserv][0]][1]))) 

    # CREATES THE RESERVATION COLORS

    reserv_colors = {} # key = reserv name, val = color (tuple form)
    colors = [(255, 131, 250), (139, 123, 139), (255, 215, 0), (165, 42, 42), (124, 252, 0), \
              (255, 64, 64), (30, 144, 255), (255, 255, 0), (205, 127, 50), (153, 204, 50), \
              (138, 43, 226), (255, 0, 255), (127, 255, 212), (139, 115, 85), (219, 219, 112),  \
              (255, 193, 193), (0, 0, 238), (244, 164, 96), (95, 159, 159), (165, 42, 42), \
              (193, 205, 193), (139, 105, 20), (70, 130, 180), (171, 130, 255), (240, 128, 128)]
    colors_copy = colors

    # DRAWS THE RESERVATIONS = LAYER 1

    for curr_reserv in reserv_xy.keys():
        # always selects the head of the list
        color = colors_copy[0] 
        # save the color for later so the legend can retrieve it based on reserv name only
        reserv_colors[curr_reserv[1]] = color 
        # unique colors; new copy of the array to keep the orig intact
        colors_copy.remove(color) 
        # no outline so it does not add to rectangle pixel size 
        canvas.rectangle([(reserv_xy[curr_reserv][0], reserv_xy[curr_reserv][2]), (reserv_xy[curr_reserv][1], \
            reserv_xy[curr_reserv][3])], fill = color) 
    
    # DRAWS CROSS-HATCHED CONFLICTS = LAYER 2

    for conflict in part_conflicts_times.keys():
        # takes care of the x-axis aspect of the conflict rectangles
        if (part_conflicts_times[conflict][0] < start_date and \
            part_conflicts_times[conflict][1] <= start_date) or \
           (part_conflicts_times[conflict][0] >= end_date and \
            part_conflicts_times[conflict][1] > end_date):
            # X1; negative value so the 'dot' drawn off the canvas
            conflict_start_pixel_x = -1
            # X2; negative value so the 'dot' drawn off the canvas
            conflict_end_pixel_x = -1
            # Y1; negative value so the 'dot' drawn off the canvas
            conflict_start_pixel_y = -1
            # Y2; negative value so the 'dot' drawn off the canvas
            conflict_end_pixel_y = -1 
        else:
            # conflict occurs at the start date of the currently observed time period
            # hence 'cut off' any parts hanging to the left of the mesh
            if part_conflicts_times[conflict][1] > start_date and \
                   part_conflicts_times[conflict][0] <= start_date:
                conflict_start_time = start_date - start_date
                conflict_end_time = part_conflicts_times[conflict][1] - start_date
            # reservation occurs at the end date of the currently observed time period
            # hence 'cut off' any parts hanging to the right of the mesh
            elif part_conflicts_times[conflict][0] < end_date and \
                     part_conflicts_times[conflict][1] >= end_date:
                conflict_start_time = part_conflicts_times[conflict][0] - start_date
                conflict_end_time = end_date - start_date
            # reservation occurs within the currently observed time period
            # hence draw the entire reservation
            elif part_conflicts_times[conflict][0] > start_date and \
                     part_conflicts_times[conflict][1] < end_date:
                conflict_start_time = part_conflicts_times[conflict][0] - start_date 
                conflict_end_time = part_conflicts_times[conflict][1] - start_date
            conflict_start_pixel_x = int(math.ceil((conflict_start_time / time_per_pixel) + label_width)) # X1
            conflict_end_pixel_x = int(math.ceil((conflict_end_time / time_per_pixel) + label_width)) # X2
            temp_node_names = part_conflicts_times[conflict][2] # list of overlapping 32-node partitions
            # temp_node_names already sorted in incrementing order e.g. 102, 104, 106...
            # temp_node_names[-1] = last 32-node part by name for curr conflict e.g. 216
            # (upper in the graph image, hence smaller depth in pixels)
            # [0] = Y1, first of 2 values in tuple returned by part_y (y coords of curr part)
            conflict_start_pixel_y = int(math.floor(part_y[temp_node_names[-1]][0]))   
            # temp_node_names[0] = first 32-node part by name for curr conflict e.g. 102
            # (lower in the graph image, hence bigger depth in pixels),
            # [1] = Y2, second of 2 values in tuple returned by part_y (y coords of curr part)
            conflict_end_pixel_y = int(math.floor(part_y[temp_node_names[0]][1]))       
        """
        canvas.rectangle([(conflict_start_pixel_x, conflict_start_pixel_y), \
             (conflict_end_pixel_x, conflict_end_pixel_y)], fill = (0, 0, 0)) #use black rectangles to map conflicts 
        """ 
        red_amount = random.randint(0, 255)
        green_amount = random.randint(0, 255)
        blue_amount = random.randint(0, 255)
        cross_hatch_color = (red_amount, green_amount, blue_amount) 
        #----------------------------------------------------------------------
         
        #----------------------------------------------------------------------
        duration_x = conflict_end_pixel_x - conflict_start_pixel_x # x-axis span for current conflict
        duration_y = conflict_end_pixel_y - conflict_start_pixel_y # y-axis span for current conflict

        """
        # Pattern 1 - optional
        # X within a circle within a square
        canvas.line([(conflict_start_pixel_x, conflict_start_pixel_y), \
                    (conflict_end_pixel_x, conflict_end_pixel_y)], \
                    fill = cross_hatch_color)
        canvas.line([(conflict_end_pixel_x, conflict_start_pixel_y), \
                    (conflict_start_pixel_x, conflict_end_pixel_y)], \
                    fill = cross_hatch_color)
        canvas.ellipse([(conflict_start_pixel_x, conflict_start_pixel_y), \
                    (conflict_end_pixel_x, conflict_end_pixel_y)], \
                    outline = cross_hatch_color)
        canvas.rectangle([(conflict_start_pixel_x, conflict_start_pixel_y), \
                    (conflict_end_pixel_x, conflict_end_pixel_y)], \
                    outline = cross_hatch_color)
        """
        
        copy_conflict_start_pixel_x = conflict_start_pixel_x # new copy; indirectly modify the var
        copy_conflict_start_pixel_y = conflict_start_pixel_y # new copy; indirectly modify the var   
        copy_conflict_end_pixel_x = conflict_end_pixel_x
        copy_conflict_end_pixel_y = conflict_end_pixel_y
        """
        # Pattern 2 - optional 
        # Mesh of Xs (not calculated properly)
        step = 0.75 * rect_height # step modifies copy_conflict_start_pixel_x
        step_x = int(0.20 * duration_x) 
        step_y = int(0.20 * duration_y) 
        for col in xrange(0, duration_y): # modify this; col does not play a role right now
            for row in xrange(0, duration_x): # modify this; row does not play a role right now
                #
                if (copy_conflict_start_pixel_y >= conflict_end_pixel_y) \
                   and (copy_conflict_start_pixel_x >= conflict_end_pixel_x):      
                    break              
                #
                if (copy_conflict_start_pixel_x >= conflict_end_pixel_x) \
                   and (copy_conflict_start_pixel_y < conflict_end_pixel_y):
                    copy_conflict_start_pixel_x = conflict_start_pixel_x # reset x
                    copy_conflict_start_pixel_y = copy_conflict_start_pixel_y + step_y # increment y
                #
                if (copy_conflict_start_pixel_y >= conflict_end_pixel_y) \
                   and (copy_conflict_start_pixel_x < conflict_end_pixel_x): # end of the y-coordinates
                    copy_conflict_start_pixel_y = conflict_start_pixel_y # reset y
                    copy_conflict_start_pixel_x = copy_conflict_start_pixel_x + step_x # increment x 
                #back slash of 'X'
                canvas.line([(copy_conflict_start_pixel_x, copy_conflict_start_pixel_y), \
                    (copy_conflict_start_pixel_x + step_x, copy_conflict_start_pixel_y + step_y)], \
                    fill = cross_hatch_color) 
                #forward slash of 'X'                   
                canvas.line([(copy_conflict_start_pixel_x, copy_conflict_start_pixel_y + step_y), \
                    (copy_conflict_start_pixel_x + step_x, copy_conflict_start_pixel_y)], \
                    fill = cross_hatch_color)
                copy_conflict_start_pixel_x = copy_conflict_start_pixel_x + step_x
                row = row + step_x
            copy_conflict_start_pixel_y = copy_conflict_start_pixel_y + step_y    
            col = col + step_y     
        """
        # draws the conflict rectangle
        canvas.rectangle([(conflict_start_pixel_x, conflict_start_pixel_y), \
                    (conflict_end_pixel_x, conflict_end_pixel_y)], \
                    outline = cross_hatch_color)
        while copy_conflict_start_pixel_x < conflict_end_pixel_x and \
              copy_conflict_end_pixel_y > conflict_start_pixel_y:
            canvas.line([(copy_conflict_start_pixel_x, copy_conflict_start_pixel_y), \
                   (copy_conflict_end_pixel_x, copy_conflict_end_pixel_y)], \
                   fill = cross_hatch_color)
            copy_conflict_start_pixel_x = copy_conflict_start_pixel_x + int(0.5 * duration_x)
            copy_conflict_end_pixel_y = copy_conflict_end_pixel_y - int(0.5 * duration_y)
        # reset variables
        copy_conflict_start_pixel_x = conflict_start_pixel_x 
        copy_conflict_start_pixel_y = conflict_start_pixel_y    
        copy_conflict_end_pixel_x = conflict_end_pixel_x
        copy_conflict_end_pixel_y = conflict_end_pixel_y
        while copy_conflict_end_pixel_x > conflict_start_pixel_x and \
              copy_conflict_start_pixel_y < conflict_end_pixel_y:
            canvas.line([(copy_conflict_end_pixel_x, copy_conflict_end_pixel_y), \
                   (copy_conflict_start_pixel_x, copy_conflict_start_pixel_y)], \
                   fill = cross_hatch_color)
            copy_conflict_end_pixel_x = copy_conflict_end_pixel_x - int(0.5 * duration_x)
            copy_conflict_start_pixel_y = copy_conflict_start_pixel_y + int(0.5 * duration_y)
        # reset variables
        copy_conflict_start_pixel_x = conflict_start_pixel_x 
        copy_conflict_start_pixel_y = conflict_start_pixel_y    
        copy_conflict_end_pixel_x = conflict_end_pixel_x
        copy_conflict_end_pixel_y = conflict_end_pixel_y 
        while copy_conflict_start_pixel_x < conflict_end_pixel_x and \
              copy_conflict_start_pixel_y < conflict_end_pixel_y:
            canvas.line([(copy_conflict_start_pixel_x, copy_conflict_end_pixel_y), \
                   (copy_conflict_end_pixel_x, copy_conflict_start_pixel_y)], \
                   fill = cross_hatch_color)
            copy_conflict_start_pixel_x = copy_conflict_start_pixel_x + int(0.5 * duration_x)
            copy_conflict_start_pixel_y = copy_conflict_start_pixel_y + int(0.5 * duration_y) 
        # reset variables 
        copy_conflict_start_pixel_x = conflict_start_pixel_x 
        copy_conflict_start_pixel_y = conflict_start_pixel_y    
        copy_conflict_end_pixel_x = conflict_end_pixel_x
        copy_conflict_end_pixel_y = conflict_end_pixel_y 
        while copy_conflict_end_pixel_x > conflict_start_pixel_x and \
              copy_conflict_end_pixel_y > conflict_start_pixel_y:
            canvas.line([(copy_conflict_start_pixel_x, copy_conflict_end_pixel_y), \
                   (copy_conflict_end_pixel_x, copy_conflict_start_pixel_y)], \
                   fill = cross_hatch_color)
            copy_conflict_end_pixel_x = copy_conflict_end_pixel_x - int(0.5 * duration_x)
            copy_conflict_end_pixel_y = copy_conflict_end_pixel_y - int(0.5 * duration_y)
      
        """
        # optional
        for column in xrange(0, duration_y):
            canvas.line([(copy_conflict_start_pixel_x, copy_conflict_start_pixel_y), \
                   (conflict_end_pixel_x, copy_conflict_start_pixel_y)], \
                   fill = cross_hatch_color) 
            if (copy_conflict_start_pixel_y + 8 < conflict_end_pixel_y):
                copy_conflict_start_pixel_y += 8
                column += 8
            else: 
               pass
        copy_conflict_start_pixel_x = conflict_start_pixel_x # new copy; indirectly modify the var
        copy_conflict_start_pixel_y = conflict_start_pixel_y # new copy; indirectly modify the var   
        for row in xrange(0, duration_x):
            canvas.line([(copy_conflict_start_pixel_x, copy_conflict_start_pixel_y), \
                   (copy_conflict_start_pixel_x, conflict_end_pixel_y)], \
                   fill = cross_hatch_color) 
            if (copy_conflict_start_pixel_x + 8 < conflict_end_pixel_x):
                copy_conflict_start_pixel_x += 8
                row += 8
            else: 
               pass
         """
    # DRAWS THE Y-AXIS = DRAWS THE 32-NODE PARTITION LABELS = LAYER 3A

    # currently labels exist for 32 partitions of 32 nodes each, 0 to 32 = 32
    for label_num in xrange(0, len(label_names)): 
        # PROBLEM; find proper ratio for labels_y + ? * rect_height
        # + 0.25 * rect_height for y so text centered in terms of 1st adjacent mesh rectangle
        canvas.text((labels_x, labels_y + 0.25 * rect_height), fill = (0, 0, 0), \
            text = label_names[label_num], font = def_font) 
        # increase the depth or y coordinate by the size of an individual rectangle
        labels_y = labels_y + rect_height 

    # DRAWS THE MESH = LAYER 3B

    num_columns = num_days + 1 # 1 to num_days + 1 = num_days columns
    num_rows = len(label_names) + 2 # 1 through 34 (32 partitions + 2) = 33 rows = 32 for partitions and 1 for ruler
    for day in xrange(1, num_columns): 
        for node_group in xrange(1, num_rows): 
            if node_group == num_rows - 1: # if last, row is yellow because it is the ruler 
                canvas.rectangle([(mesh_x, mesh_y), (mesh_x + rect_width , mesh_y + rect_height)], \
                    fill = (255, 246, 143), outline = (0, 0, 0)) 
            else: # else, row has no fill and is transparent
                canvas.rectangle([(mesh_x, mesh_y), (mesh_x + rect_width , mesh_y + rect_height)], \
                    outline = (0, 0, 0)) 
            # rectangles in rows forming cols, one above another, rows must have growing height
            mesh_y = mesh_y + rect_height 
        # break this coupling here = ruler must not be drawn a rectangle at a time but as a whole aka dynamic ruler

        # DRAWS THE X-AXIS = DRAWS THE RULER ONE RECTANGLE AT A TIME 

        # each rectangle acts as last row for current column

        tick_color = (255, 69, 0)
        # generates major tick marks          
        canvas.line([(mesh_x + 0.5 * rect_width, mesh_y - 10), \
            (mesh_x + 0.5 * rect_width, mesh_y + 10)], fill = tick_color)
        # generates minor tick marks
        canvas.line([(mesh_x + 0.25 * rect_width, mesh_y - 5), \
            (mesh_x + 0.25 * rect_width, mesh_y + 5)], fill = tick_color)
        canvas.line([(mesh_x + 0.75 * rect_width, mesh_y - 5), \
            (mesh_x + 0.75 * rect_width, mesh_y + 5)], fill = tick_color)
        # generates miniscule tick marks
        canvas.line([(mesh_x + 0.125 * rect_width, mesh_y - 3), \
            (mesh_x + 0.125 * rect_width, mesh_y + 3)], fill = tick_color)
        canvas.line([(mesh_x + 0.375 * rect_width, mesh_y - 3), \
            (mesh_x + 0.375 * rect_width, mesh_y + 3)], fill = tick_color)
        canvas.line([(mesh_x + 0.625 * rect_width, mesh_y - 3), \
            (mesh_x + 0.625 * rect_width, mesh_y + 3)], fill = tick_color)
        canvas.line([(mesh_x + 0.875 * rect_width, mesh_y - 3), \
            (mesh_x + 0.875 * rect_width, mesh_y + 3)], fill = tick_color)
        # generates date/time labels
        # day-1 because in days_names coordinates start at 0
        year_r = time.strftime("%Y", time.localtime(days_names[day-1]))     # ruler year
        month_r = time.strftime("%m/%d", time.localtime(days_names[day-1])) # ruler month and day
        day_r = time.strftime("%a", time.localtime(days_names[day-1]))      # weekday
        time_r = time.strftime("%H:%M", time.localtime(days_names[day-1]))  # ruler time
        canvas.text((mesh_x - canvas.textsize(year_r)[0] * 0.5, mesh_y + 20), \
            fill = (0, 0, 255), text = year_r, font = def_font)
        canvas.text((mesh_x - canvas.textsize(month_r)[0] * 0.5, mesh_y + 30), \
            fill = (0, 0, 255), text = month_r, font = def_font)
        canvas.text((mesh_x - canvas.textsize(day_r)[0] * 0.5, mesh_y + 40), \
            fill = (0, 0, 255), text = day_r, font = def_font)
        canvas.text((mesh_x - canvas.textsize(time_r)[0] * 0.5, mesh_y + 50), \
            fill = (0, 0, 255), text = time_r, font = def_font)
        # prints right-most time label
        if day == num_columns - 1:
            mesh_x_new = mesh_x_copy + num_days * rect_width
            mesh_y_new = mesh_y_copy + (len(label_names)+1) * rect_height # +1 because of the ruler
            # day and not day-1 because it is the rightmost mark
            year_r = time.strftime("%Y", time.localtime(days_names[day]))     # ruler year
            month_r = time.strftime("%m/%d", time.localtime(days_names[day])) # ruler month and day
            day_r = time.strftime("%a", time.localtime(days_names[day]))      # weekday
            time_r = time.strftime("%H:%M", time.localtime(days_names[day]))  # ruler time
            canvas.text((mesh_x_new - canvas.textsize(year_r)[0] * 0.5, mesh_y_new + 20), \
                fill = (0, 0, 255), text = year_r, font = def_font)
            canvas.text((mesh_x_new - canvas.textsize(month_r)[0] * 0.5, mesh_y_new + 30), \
                fill = (0, 0, 255), text = month_r, font = def_font)
            canvas.text((mesh_x_new - canvas.textsize(day_r)[0] * 0.5, mesh_y_new + 40), \
                fill = (0, 0, 255), text = day_r, font = def_font)
            canvas.text((mesh_x_new - canvas.textsize(time_r)[0] * 0.5, mesh_y_new + 50), \
                fill = (0, 0, 255), text = time_r, font = def_font)

        # rectangles' cols forming rows, one next to another
        mesh_x = mesh_x + rect_width 
        # mesh_y = canvas * 0.08 cols must have consistent height; resets to orig val for next iter
        mesh_y = mesh_y_copy 
       
    # DRAWS MIDPLANE SEPARATORS 

    # generates top line
    canvas.line([(labels_x, mesh_y_copy + rect_height * 0), \
       (mesh_x_copy, mesh_y_copy + rect_height * 0)], fill = (255, 0, 0))
    # generates middle line
    canvas.line([(labels_x, mesh_y_copy + rect_height * (num_rows - 2) / 2), \
       (mesh_x_copy, mesh_y_copy + rect_height * (num_rows - 2)/ 2)], fill = (255, 0, 0))
    # generates bottom line
    canvas.line([(labels_x, mesh_y_copy + rect_height * (num_rows - 2)), \
       (mesh_x_copy, mesh_y_copy + rect_height * (num_rows - 2))], fill = (255, 0, 0))
    
    # DRAWS RESERVATIONS LEGEND

    legend_x = mesh_x_copy # unmodified mesh_x, x-coordinate for the legend title text
    #33 rows * rectangle width + mesh start pixel + 50 pixels to jump of time labels
    legend_y = num_rows * rect_height + mesh_y_copy + 60 
    legend_square_side = 0.75 * rect_height # width=height=side of the square (10 to 35 are good values if static) 
    canvas.text((legend_x, legend_y), fill = (255, 0, 0), text = "RESERVATIONS: ") # draws legend title text
    legend_y += 20 # so 'RESERVATIONS' does not overlap with the first rectangle
    legend_y_copy = legend_y # fresh copy of legend_y needed for new columns 
    legend_longest_string = 0 # the length of the longest reservation text label  
    # finds the longest reservation text label 
    for curr_reserv in reserv_dict.keys():
        reserv_text = str(curr_reserv[0]) + "/" + str(curr_reserv[1]) + "/" + str(reserv_top_part[curr_reserv])
        if canvas.textsize(reserv_text)[0] > legend_longest_string:        
            legend_longest_string = canvas.textsize(reserv_text)[0] 
    # chooses reservation colors and draws the rectangles and their labels
    for curr_reserv in reserv_dict.keys():
        reserv_text = str(curr_reserv[0]) + "/" + str(curr_reserv[1]) + "/" + str(reserv_top_part[curr_reserv])
        # moves rectangles and their labels to a different column if drawn outside of the canvas
        if (legend_y + legend_square_side) > image.size[1]: # current depth + height of the rectangle
            #look at canvas.text... the x parameter
            legend_x = legend_x + legend_longest_string + legend_square_side + 20 
            # fresh copy since starting a new col with a reset depth
            legend_y = legend_y_copy      
        canvas.rectangle([(legend_x, legend_y), (legend_x + legend_square_side, legend_y + legend_square_side)], \
            fill = reserv_colors[curr_reserv[1]], outline = (0, 0, 0)) # draws color rectangle
        canvas.text((legend_x + legend_square_side + 10, legend_y + 0.25 * legend_square_side), \
            fill = (0, 0, 0), text = reserv_text) #draws reservation text
        legend_y += legend_square_side + 5 # introduces space between individual rectangles 

    if options.graph[3] == "y":

        # DRAWS CONFLICTS LEGEND

        #33 rows * rectangle width + mesh start pixel + 50 pixels to jump of time labels
        conflicts_y = num_rows * rect_height + mesh_y_copy + 60 
        conflicts_x = legend_x + legend_longest_string + legend_square_side + 30
        canvas.text((conflicts_x, conflicts_y), fill = (255, 0, 0), text = "CONFLICTS:") # title
        conflicts_y += 20 # space between entries and 'CONFLICTS'
        conflicts_y_copy = conflicts_y
        conflicts_longest_string = 0
        # finds the longest conflict text label
        if len(part_conflicts) > 0:
            for curr_conflict in part_conflicts.keys():
                conf_text = curr_conflict[0][0] + "/" + curr_conflict[0][1] + \
                    " | " + curr_conflict[1][0] + "/" + curr_conflict[1][1]
                if canvas.textsize(conf_text)[0] > conflicts_longest_string:
                    conflicts_longest_string = canvas.textsize(conf_text)[0]
            # draws the conflict text labels
            for curr_conflict in part_conflicts.keys():
                conf_text = curr_conflict[0][0] + "/" + curr_conflict[0][1] + \
                    " | " + curr_conflict[1][0] + "/" + curr_conflict[1][1]
                if (conflicts_y + legend_square_side) > image.size[1]: # current depth + height of the rectangle
                    conflicts_x = conflicts_x + conflicts_longest_string + 20 #look at canvas.text... the x parameter
                    conflicts_y = conflicts_y_copy # fresh copy since starting a new col with a reset depth     
                canvas.text((conflicts_x, conflicts_y + 0.25 * legend_square_side), fill = (0, 0, 0), text = conf_text)
                conflicts_y += legend_square_side + 5 
        else:
            canvas.text((conflicts_x, conflicts_y + 0.25 * legend_square_side), \
                fill = (0, 0, 0), text = "no conflicts exist")

    # EXPORTS THE IMAGE
    image_name = options.graph[0] + "_" + user_s + "@" + host_s + "_" \
        + time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time())) + "_" + str(canvas_x) + "x" + str(canvas_y)
    if options.graph[1] in ['png', 'tif', 'jpeg', 'pdf', 'gif']:
        image.save(image_name + "." + options.graph[1], options.graph[1].upper())
    else:
        sys.stderr("Unrecognized image format: %s" % options.graph[1])
        sys.exit("Exiting...")
    # comment out next line if image needs to be saved but not displayed
    """os.execl("/soft/apps/tools/ImageMagick/bin/display", "display", "./" \
        + image_name + "." + options.graph[1], "&") # views the generated image"""

    return

class ScheduleDiagram:
    '''Provides Visualization of Schedules'''
    def __init__(self, schedule, partitions, reservations):
        self.schedule = schedule
        self.partitions = partitions
        self.reservations = reservations
        self.window = (-1, -1)

    def setWindow(self, start, stop):
        '''Set visible window for diagram'''
        self.window = (start, stop)

    def Diagram(self, name, format):
        '''Output diagram in location and format specified'''
        pass

if __name__ == '__main__':
    """
    # Calculating midpoints for the mesh's Xs - optional
    A = []
    R1(0, 10, A)
    print A
    B = []
    R1(0, 20, B)
    print B
    #print R2(0, 10, 0, 20)"""
    
    scheduler = Cobalt.Proxy.scheduler()
    reservations = {}
    npart = {}
    partitions = scheduler.GetPartition([{'size':'*', 'tag':'partition', 'name':'*', 'reservations':'*', 'deps':'*'}])

    [npart.__setitem__(partition.get('name'), partition) for partition in partitions]
    # builds topology; key = partition, val = ((parents), (children))
    depinfo = Cobalt.Util.buildRackTopology(partitions) 
    
    #modifies the 'reservation' dictionary to a different format
    mod_reserv_dict(reservations, partitions, npart, depinfo) 
    # builds data structure of reservations and their lists of 32-node partition 
    gen_part_hits(reservations) 
    # stores any detected conflicts to the data structure 'part_conflicts_times'
    detect_conflicts(reservations) 

    parser = optparse.OptionParser(usage = "%prog [-options]", version = "\n'%prog' written by " + orig_author  
        + " (denkov@mcs.anl.gov)\nversion: " + ver_num + " date: " + ver_date + " modified by: " 
        + last_mod + "\n\nACKNOWLEDGEMENTs:" + "\nSusan Coghlan - advice and supervision" 
        + "\nAndrew Cherry - advice and supervision" + "\nNarayan Desai - source code contribution" 
        + "\nRichard Bradshaw - source code contribution" + "\nJohn Valdez - advice\n")

    parser.add_option("-p", "--plain", action = "store_true", dest = "confplain", \
                      help = "print a plain summary of conflicting reservations pairs") 
    parser.add_option("-v", "--verbose", action = "store_true", dest = "confverbose", \
                      help = "print a verbose summary of conflicting reservations pairs")
    parser.add_option("-g", "--graph", nargs = 6, dest = "graph", \
                      help = "generates an image representing the current reservations in the system")
    parser.add_option("-s", "--showres", action = "store_true", dest = "showres", \
                      help = "call the 'showres' command with the -l option selected")
    (options, args) = parser.parse_args()
    
    if options.confplain and options.confverbose: # -p and -v
        parser.error("\n\tOptions -p and -v are mutually exclusive." 
                     + "\n\tUse -h for a list of available options and their usage.")
 
    if options.confplain and len(args) == 0:   # -p and no args
        prnt_plain_conflicts() 
    elif options.confplain and len(args) != 0: # -p and args
        parser.error("\n\tOption -p has no arguments." 
                     + "\n\tUse -h for a list of available options and their usage.\n")

    if options.confverbose and len(args) == 0:   # -v and no args
        prnt_verbose_conflicts()
    elif options.confverbose and len(args) != 0: # -v and args
        parser.error("\n\tOption -v has no arguments."  
                     + "\n\tUse -h for a list of available options and their usage.\n")

    if options.showres:
        os.execl("/usr/bin/showres", "showres", "-l") # 2 os.execl statements cannot work together. why?

    if options.graph: 
        gen_image(reservations)

    if options.graph and options.confplain:   # -g and -p
        prnt_plain_conflicts() 
        gen_image(reservations)

    if options.graph and options.confverbose: # -g and -v
        prnt_verbose_conflicts()
        gen_image(reservations)
  
        

   
