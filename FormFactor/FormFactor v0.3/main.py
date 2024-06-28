import vidanalyse, orangefinder


directory = "track.mp4"
orangefinder.detect_color_objects(1)
vidanalyse.graph(20, "capturedy.csv")
