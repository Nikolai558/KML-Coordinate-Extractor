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


if __name__ == '__main__':

    # exe_name.exe airport_name file_path
    # airport_name = the diagram description field.
    # file_path = Full file path of the diagram you want to complete
    #   NOTE: if exe is inside folder with files, only the file name is required,
    #         but this can be ran from anywhere if you include the full file path with the file name.

    # TODO Need to grab save directory path

    if len(sys.argv) != 3:
        name = sys.argv[1]
        read_file_path = sys.argv[2]

        write_geoMap(name, read_xml(read_file_path))
    else:
        print("Your arguments are invalid. Try again.")
        print("Correct format is:\n"
              "\tKML_Coord_Extractor\t{Diagram_Name}\t{Diagram_File_Path}\n")
