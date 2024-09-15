def calculate_attention_score(normalized_distance, motion_value, face_detected):
    """
    Calculate the likelihood that the user is paying attention based on normalized distance,
    motion intensity, and face detection.
    :param normalized_distance: Normalized distance value (0-1).
    :param motion_value: Motion intensity value (0-1).
    :param face_detected: 1 if a face is detected, -1 if not.
    :return: A score between 0 and 1 indicating how likely the user is paying attention.
    """
    # Weights for each factor
    w_d = 0.4  # Weight for distance
    w_m = 0.4  # Weight for motion
    w_f = 0.2  # Weight for face detection

    # Calculate the distance score (penalize if too far or too close)
    D_score = 1 - abs(0.5 - normalized_distance)  # Ideal is around 0.5

    # Calculate the motion score (low motion means paying attention)
    M_score = 1 - motion_value  # Less motion is better

    # Face detection score
    F_score = 1 if face_detected == 1 else 0

    # Calculate the final attention score as a weighted sum
    P_attention = (w_d * D_score) + (w_m * M_score) + (w_f * F_score)

    # Ensure the score is between 0 and 1
    P_attention = max(0, min(P_attention, 1))

    return P_attention
