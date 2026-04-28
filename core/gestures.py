def check_hands_up(keypoints):
    """Проверяет, подняты ли руки выше плеч"""
    if keypoints is None or len(keypoints.xy[0]) < 11:
        return False
        
    # Координаты Y (индекс 1 в паре x,y)
    left_shoulder_y = keypoints.xy[0][5][1]
    right_shoulder_y = keypoints.xy[0][6][1]
    left_wrist_y = keypoints.xy[0][9][1]
    right_wrist_y = keypoints.xy[0][10][1]

    # Если хотя бы одно запястье выше плеча (в CV координатах 0 - это верх)
    if (left_wrist_y < left_shoulder_y > 0) or (right_wrist_y < right_shoulder_y > 0):
        return True
    return False
