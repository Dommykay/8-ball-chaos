def Fade(time_in_seconds = 1, frame_rate = 60, fade_in = True, fade_from = 0, fade_to = 255,tween = "linear"):
    progression_steps = time_in_seconds * frame_rate
    progression_steps = round(progression_steps)
    opacity_list = []
    difference_between_points = fade_to - fade_from
    if tween == "quadratic_in":
        if fade_in is not True:
            for current_step in range(1, progression_steps + 1).__reversed__():
                x = (fade_from + (difference_between_points * (current_step / progression_steps)))
                opacity_list.append(
                    round((x**2)/fade_to)
                )
        else:
            for current_step in range(1, progression_steps + 1):
                x = (fade_from + (difference_between_points * (current_step / progression_steps)))
                opacity_list.append(
                    round((x**2)/fade_to)
                )
        return opacity_list
    elif tween == "quadratic_out":
        if fade_in is not True:
            for current_step in range(1, progression_steps + 1).__reversed__():
                x = (fade_from + (difference_between_points * (current_step / progression_steps)))
                opacity_list.append(
                    round(((2*fade_to*x)-x**2)/fade_to)
                )
        else:
            for current_step in range(1, progression_steps + 1):
                x = (fade_from + (difference_between_points * (current_step / progression_steps)))
                opacity_list.append(
                    round((x**2)/fade_to)
                )
        return opacity_list
    else: #Linear
        if fade_in is not True:
            for current_step in range(1, progression_steps + 1).__reversed__():
                opacity_list.append(
                    round(fade_from + (difference_between_points * (current_step / progression_steps)))
                )
        else:
            for current_step in range(1, progression_steps + 1):
                opacity_list.append(
                    round(fade_from + (difference_between_points * (current_step / progression_steps)))
                )
        return opacity_list