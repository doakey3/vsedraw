def get_fit_channel(scene, high_strip):
    """
    Gets the lowest channel in which a strip can fit without
    bumping into another strip.
    """
    channel_strips = {}
    try:
        all_strips = scene.sequence_editor.sequences_all
    except AttributeError:
        return 1

    if len(all_strips) == 0:
        return 1

    for strip in all_strips:
        try:
            channel_strips[str(strip.channel)].append(strip)
        except KeyError:
            channel_strips[str(strip.channel)] = [strip]

    numbers = []
    keys = list(channel_strips.keys())
    for i in range(len(keys)):
        numbers.append(int(keys[i]))

    max_channel = max(numbers)

    for i in range(1, max_channel + 1):
        try:
            neighbors = channel_strips[str(i)]
            stuck = False
            for neighbor in neighbors:
                if not neighbor == high_strip and neighbor.frame_start < high_strip.frame_final_end and neighbor.frame_final_end > high_strip.frame_start:
                    stuck = True
            if not stuck:
                return i
        except KeyError:
            return i
    return max_channel + 1
