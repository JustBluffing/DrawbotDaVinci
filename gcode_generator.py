def convert_contours_to_gcode(contours, scale=1.0, pen_up_command="PEN_UP", pen_down_command="PEN_DOWN"):
    """
    Converts the detected contours into control commands (G-code).

    Args:
        contours (list): A list of contours obtained from OpenCV's findContours method.
        scale (float, optional): Scaling factor to convert the pixel coordinates to the desired unit (e.g., millimeters or steps).
        pen_up_command (str, optional): Command to lift the pen.
        pen_down_command (str, optional): Command to lower the pen.

    Returns:
        list: A list of G-code commands as strings.
    """
    gcode_commands = []

    # Iterate through each contour
    for contour in contours:
        if len(contour) == 0:
            continue

        # Assume that the contour is a list of points,
        # with the first point initializing the path and the rest describing the movement.
        start_point = contour[0][0]   # OpenCV contours store points as [ [[x, y]], ... ]
        # Move quickly to the first point with the pen lifted
        gcode_commands.append(f"G0 X{start_point[0] * scale:.2f} Y{start_point[1] * scale:.2f} ; Move to start position")
        # Lower the pen before starting the drawing
        gcode_commands.append(pen_down_command)

        # Iterate through the points and draw lines through them
        for point in contour[1:]:
            x, y = point[0]  # Coordinates of the point
            gcode_commands.append(f"G1 X{x * scale:.2f} Y{y * scale:.2f}")

        # At the end of the drawing, lift the pen to move to the next contour without drawing
        gcode_commands.append(pen_up_command)
    
    return gcode_commands

def write_gcode_to_file(gcode_commands, file_path):
    """
    Saves the G-code command list to a file.

    Args:
        gcode_commands (list): A list of G-code commands.
        file_path (str): The destination file path.
    """
    with open(file_path, "w") as file:
        for command in gcode_commands:
            file.write(command + "\n")

if __name__ == "__main__":
    # This section serves as a test when the module is run directly.
    # It is assumed that you have example contours (typically obtained from the image_processing module)
    import numpy as np

    # Example contours: a list containing two simple "squares".
    contour1 = np.array([[[10, 10]], [[20, 10]], [[20, 20]], [[10, 20]]], dtype=np.int32)
    contour2 = np.array([[[30, 30]], [[40, 30]], [[40, 40]], [[30, 40]]], dtype=np.int32)
    contours = [contour1, contour2]

    # Convert the contours to G-code
    gcode = convert_contours_to_gcode(contours, scale=0.1)

    # Display the generated G-code in the console
    for line in gcode:
        print(line)

    # You can also save the G-code to a file (e.g., "output.gcode")
    write_gcode_to_file(gcode, "output.gcode")
