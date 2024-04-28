import cv2
import os

# Path to the folder containing frames
frames_folder = "output_frame"

# Output video filename
output_video = "annotated_video.mp4"

# Function to sort frames numerically
def sort_frames(frame):
    return int(frame.split('_')[-1].split('.')[0])

# Get list of frames
frames = os.listdir(frames_folder)
frames.sort(key=sort_frames)

# Get frame dimensions
frame = cv2.imread(os.path.join(frames_folder, frames[0]))
height, width, _ = frame.shape

# Define video codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video, fourcc, 120.0, (width, height))

# Write frames to video
for frame_name in frames:
    frame_path = os.path.join(frames_folder, frame_name)
    frame = cv2.imread(frame_path)
    out.write(frame)

    print(frame_name)

# Release VideoWriter object
out.release()

print("Video created successfully!")
