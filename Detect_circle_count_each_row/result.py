import numpy as np
from skimage.draw import line
from skimage.io import imread
import extract
object_coords = extract.extract_objects_from_circles('circle.jpg')

# Sort the list by x-value
object_coords.sort(key=lambda coord: coord[0])

# Initialize an empty dictionary to store the groups
groups = {}

# Loop through each set of coordinates
for coord in object_coords:
    # Get the x-value of the current set
    x = coord[0]

    # Check if there is a group with a similar x-value
    for key in groups.keys():
        if abs(key - x) <= 5:
            # If a group is found, add the current set to it
            groups[key].append(coord)
            break
    else:
        # If no group is found, create a new one with the current set
        groups[x] = [coord]

# Convert the dictionary to a list of lists
result = list(groups.values())
for i in result:
    if i[0][2] == 0:
        print("Red: ",len(i))
    elif i[0][2] == 1:
        print("Blue: ", len(i))
    else:
        break