

def single_day(series):
    """
    Take timeseries of a position, and convert it to 3D surface
    """
    rX = []
    rY = []
    rZ = []
    cellA = 24  # for Y inclinometer
    cellB = (6 * 3) + (4.5 * 2)  # for X inclinometer

    # 4 cells, stacked.
    # X1 is vertical inclination in mm/m, Y1 is horizontal inclination in mm/m
    # i.e. AXES ARE SWAPPED!
    # Calculate first one
    x_offset = 0
    y_offset = 0

    def walk(offset1, offset2):
        return offset1, offset2 + cellB

    for incls in [
        (series.X1, series.Y1),
        (series.X2, series.Y2),
        (series.X3, series.Y3),
        (series.X4, series.Y4)
    ]:
        # calculate 4 points
        inclX = incls[0]
        inclY = incls[1]
        X = x_offset
        Y = y_offset
        Z = (inclX * (cellB / 2) + inclY * (cellA / 2)) / 1000
        rX.append(X)
        rY.append(Y)
        rZ.append(Z)

        X = x_offset + cellA
        Y = y_offset
        Z = (inclX * (cellB / 2) - inclY * (cellA / 2)) / 1000
        rX.append(X)
        rY.append(Y)
        rZ.append(Z)

        X = x_offset
        Y = y_offset + cellB
        Z = (-inclX * (cellB / 2) + inclY * (cellA / 2)) / 1000
        rX.append(X)
        rY.append(Y)
        rZ.append(Z)
        
        X = x_offset + cellA
        Y = y_offset + cellB
        Z = (-inclX * (cellB / 2) - inclY * (cellA / 2)) / 1000
        rX.append(X)
        rY.append(Y)
        rZ.append(Z)
        
        x_offset, y_offset = walk(x_offset, y_offset)
    
    return [rX, rY, rZ]
