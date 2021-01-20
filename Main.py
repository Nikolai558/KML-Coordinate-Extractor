import sys


def read_xml(file_path="exampleData.xml"):
    diagram_coordinates = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

        grab_next_line = False
        count = 0

        for line in lines:
            if grab_next_line:
                for coordinate_pair in line.split(",0 "):

                    coordinate_pair = coordinate_pair.replace("\t", "")
                    coordinate_pair = coordinate_pair.replace("\n", "")

                    try:
                        diagram_coordinates[count].append(coordinate_pair)
                    except KeyError:
                        diagram_coordinates[count] = []
                        diagram_coordinates[count].append(coordinate_pair)

            if "<coordinates>" in line:
                count += 1
                grab_next_line = True
            else:
                grab_next_line = False

    return diagram_coordinates


def write_geoMap(diagram_name, diagram_dictionary, save_file_path="output.xml"):
    with open(save_file_path, "w") as file:
        file.writelines(f"        <GeoMapObject Description=\"{diagram_name}\" TdmOnly=\"false\">\n"
                        "          <LineDefaults Bcg=\"20\" Filters=\"20\" Style=\"Solid\" Thickness=\"1\" />\n"
                        "          <Elements>\n")

        for diagram, coordinates in diagram_dictionary.items():
            index_count = 0
            # coordinate_pair[index_count + 1]

            for coordinate_pair in coordinates:
                try:

                    start_lat = coordinate_pair.split(",")[1]
                    start_lon = coordinate_pair.split(",")[0]

                    end_lat = coordinates[index_count + 1].split(",")[1]
                    end_lon = coordinates[index_count + 1].split(",")[0]

                    file.writelines("            <Element xsi:type=\"Line\" Filters=\"\" StartLat=\"{}\" StartLon=\"{}\" EndLat=\"{}\" EndLon=\"{}\" />\n".format(
                        start_lat, start_lon, end_lat, end_lon
                    ))

                except IndexError:
                    pass

                index_count += 1

        file.writelines("          </Elements>\n"
                        "        </GeoMapObject>\n")


def write_sct2(diagram_name, diagram_dictionary, save_file_path="output.sct2"):
    with open(save_file_path, "w") as file:
        file.writelines(f"- {diagram_name}{' '*(24-len(diagram_name))}N000.00.00.000 E000.00.00.000 N000.00.00.000 E000.00.00.000\n")

        for diagram, coordinates in diagram_dictionary.items():
            index_count = 0
            # coordinate_pair[index_count + 1]

            for coordinate_pair in coordinates:
                try:

                    start_lat = convert_decimal(float(coordinate_pair.split(",")[1]))
                    start_lon = convert_decimal(float(coordinate_pair.split(",")[0]), False)

                    end_lat = convert_decimal(float(coordinates[index_count + 1].split(",")[1]))
                    end_lon = convert_decimal(float(coordinates[index_count + 1].split(",")[0]), False)

                    file.writelines(f"{' '*26}{start_lat} {start_lon} {end_lat} {end_lon}\n")

                except IndexError:
                    pass

                index_count += 1


def convert_decimal(dd, lat=True):
    negative = dd < 0
    dd = abs(dd)
    minutes, seconds = divmod(dd*3600, 60)
    degrees, minutes = divmod(minutes, 60)
    if negative:
        if degrees > 0:
            degrees = -degrees
        elif minutes > 0:
            minutes = -minutes
        else:
            seconds = -seconds

    milliseconds = str(round(seconds, 3)).split('.')[1]
    degrees = str(degrees).replace('.0', '')
    minutes = str(minutes).replace('.0', '')
    seconds = str(seconds).split('.')[0]

    if len(degrees.replace('-', '')) < 3:
        degrees = f"{0*(len(milliseconds)-3)}{degrees}"
    if len(minutes) < 2:
        minutes = f"{0*(len(minutes)-2)}{minutes}"
    if len(seconds) < 2:
        seconds = f"{0*(len(seconds)-2)}{seconds}"
    if len(milliseconds) < 3:
        milliseconds = f"{milliseconds}{0*(len(milliseconds)-3)}"

    dms = f"{degrees}.{minutes}.{seconds}.{milliseconds}"

    if lat:
        # N or S
        if negative:
            dms = f"S{dms[1:]}"
        else:
            dms = f"N{dms}"
    else:
        # W or E
        if negative:
            dms = f"W{dms[1:]}"
        else:
            dms = f"E{dms}"

    return dms


if __name__ == '__main__':

    # exe_name.exe airport_name file_path
    # airport_name = the diagram description field.
    # file_path = Full file path of the diagram you want to complete
    #   NOTE: if exe is inside folder with files, only the file name is required,
    #         but this can be ran from anywhere if you include the full file path with the file name.

    # TODO Need to grab save directory path

    if len(sys.argv) == 3:
        name = sys.argv[1]
        read_file_path = sys.argv[2]

        write_geoMap(name, read_xml(read_file_path), f"{name}.xml")
        # write_sct2(name, read_xml(read_file_path), f"{name}.sct2")
    else:
        print("Your arguments are invalid. Try again.")
        print("Correct format is:\n"
              "\tKML_Coord_Extractor\t{Diagram_Name}\t{Diagram_File_Path}\n")
