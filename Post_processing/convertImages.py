import cv2
import os

# Open the video file
video_path = 'C0019.MP4'
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Create a directory to save the frames
output_dir = 'frames'
os.makedirs(output_dir, exist_ok=True)

# Read and save each frame
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Save the frame as an image
    frame_path = os.path.join(output_dir, f"frame_{frame_count:06d}.jpg")
    cv2.imwrite(frame_path, frame)
    
    frame_count += 1

    print(frame_count)

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()

print(f"{frame_count} frames extracted and saved to '{output_dir}' directory.")
