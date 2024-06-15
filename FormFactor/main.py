import vidanalyse, vidcapture


directory = "track.mp4"
vidcapture.capture(directory)
vidanalyse.graph(50)
