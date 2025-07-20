import numpy as np
import cv2

cap = cv2.VideoCapture('video/char_video.mp4')

fps = int(cap.get(cv2.CAP_PROP_FPS))
if fps == 0:
    fps = 30  # fallback in case camera doesn't provide FPS

COLOR_RANGES = {
    'Red': [
        (np.array([0, 100, 100]), np.array([10, 255, 255])),
        (np.array([160, 100, 100]), np.array([180, 255, 255]))
    ],
    'Green': [
        (np.array([36, 100, 100]), np.array([85, 255, 255]))
    ],
    'Blue': [
        (np.array([100, 150, 100]), np.array([125, 255, 255]))
    ]
}

COLOR_QUAD_TO_CHAR = {
    tuple(sorted(['R', 'R']) + sorted(['R', 'R'])): '0',
    tuple(sorted(['R', 'R']) + sorted(['G', 'G'])): '1',
    tuple(sorted(['R', 'R']) + sorted(['B', 'B'])): '2',
    tuple(sorted(['G', 'G']) + sorted(['R', 'R'])): '3',
    tuple(sorted(['G', 'G']) + sorted(['G', 'G'])): '4',
    tuple(sorted(['G', 'G']) + sorted(['B', 'B'])): '5',
    tuple(sorted(['B', 'B']) + sorted(['R', 'R'])): '6',
    tuple(sorted(['B', 'B']) + sorted(['G', 'G'])): '7',
    tuple(sorted(['B', 'B']) + sorted(['B', 'B'])): '8',
    tuple(sorted(['R', 'G']) + sorted(['R', 'R'])): '9',
    tuple(sorted(['R', 'G']) + sorted(['G', 'G'])): 'A',
    tuple(sorted(['R', 'G']) + sorted(['B', 'B'])): 'B',
    tuple(sorted(['R', 'B']) + sorted(['R', 'R'])): 'C',
    tuple(sorted(['R', 'B']) + sorted(['G', 'G'])): 'D',
    tuple(sorted(['R', 'B']) + sorted(['B', 'B'])): 'E',
    tuple(sorted(['G', 'B']) + sorted(['R', 'R'])): 'F',
    tuple(sorted(['G', 'B']) + sorted(['G', 'G'])): 'G',
    tuple(sorted(['G', 'B']) + sorted(['B', 'B'])): 'H',
    tuple(sorted(['G', 'R']) + sorted(['R', 'G'])): 'I',
    tuple(sorted(['R', 'G']) + sorted(['R', 'B'])): 'J',
    tuple(sorted(['G', 'R']) + sorted(['B', 'G'])): 'K',
    tuple(sorted(['B', 'R']) + sorted(['G', 'R'])): 'L',
    tuple(sorted(['B', 'R']) + sorted(['B', 'G'])): 'M',
    tuple(sorted(['B', 'R']) + sorted(['R', 'B'])): 'N',
    tuple(sorted(['G', 'B']) + sorted(['B', 'G'])): 'O',
    tuple(sorted(['G', 'B']) + sorted(['R', 'G'])): 'P',
    tuple(sorted(['G', 'B']) + sorted(['R', 'B'])): 'Q',
    tuple(sorted(['R', 'R']) + sorted(['R', 'G'])): 'R',
    tuple(sorted(['R', 'R']) + sorted(['R', 'B'])): 'S',
    tuple(sorted(['R', 'R']) + sorted(['G', 'B'])): 'T',
    tuple(sorted(['G', 'G']) + sorted(['G', 'R'])): 'U',
    tuple(sorted(['G', 'G']) + sorted(['R', 'B'])): 'V',
    tuple(sorted(['G', 'G']) + sorted(['G', 'B'])): 'W',
    tuple(sorted(['B', 'B']) + sorted(['G', 'B'])): 'X',
    tuple(sorted(['B', 'B']) + sorted(['R', 'B'])): 'Y',
    tuple(sorted(['B', 'B']) + sorted(['R', 'G'])): 'Z',
}


detected_colors_history = []
frame_number = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Video ended or cannot be read")
        break

    frame_number += 1
    interval =int(fps/2)
    if frame_number % interval != 0:
        continue

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color_pixel_counts = {}

    for color_name, ranges in COLOR_RANGES.items():
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for lower, upper in ranges:
            mask |= cv2.inRange(hsv, lower, upper)

        pixel_count = cv2.countNonZero(mask)
        if pixel_count > 500:
            color_pixel_counts[color_name] = pixel_count

    if color_pixel_counts:
        # Get top 2 dominant colors
        colors = sorted(color_pixel_counts.items(), key=lambda x: x[1], reverse=True)
        normalized_colors = [name for name, _ in colors[:2]]

        if len(normalized_colors) == 1:
            normalized_colors *= 2  # Duplicate if only one color
            
        if len(detected_colors_history) > 0 and detected_colors_history[-1][1] == ['Black']:
            detected_colors_history.append((frame_number, normalized_colors))

    else:
            
        # No dominant colors = black frame
        if len(detected_colors_history) == 0 or detected_colors_history[-1][1] != ['Black']:
            detected_colors_history.append((frame_number, ['Black']))

    # Display detected colors
    for idx, color in enumerate(color_pixel_counts.keys()):
        cv2.putText(frame, color, (10, 30 + 30 * idx),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow('Video Color Detection', frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# --- Decoding Logic (skip black frames, decode in pairs) ---
def color_code(name):
    return name[0].upper()

decoded_string = ''
buffer = []

for _, colors in detected_colors_history:
    if colors != ['Black']:

        buffer.append(colors)
        if len(buffer) == 2:
            frame1 = sorted([color_code(c) for c in buffer[0]])
            frame2 = sorted([color_code(c) for c in buffer[1]])
            key = tuple(sorted(frame1) + sorted(frame2))  # preserves frame order, but not intra-frame order
            decoded_string += COLOR_QUAD_TO_CHAR.get(key, '?')
            buffer = []

# Output results
print("\nDecoded Password:", decoded_string)
print("\nStored Frame Colors:")

for frame_num, colors in detected_colors_history:
    print(f"Frame {frame_num}: {colors}")
