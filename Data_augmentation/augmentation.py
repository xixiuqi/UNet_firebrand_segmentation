
import Augmentor

p = Augmentor.Pipeline("demo1")
p.ground_truth("demo2")

p.rotate(probability=0.8, max_left_rotation=10, max_right_rotation=10)

p.flip_top_bottom(probability=0.5)

p.flip_left_right(probability=0.5)

# p.scale(probability=1, scale_factor=1.3)

p.zoom_random(probability=0.4, percentage_area=0.9)

p.sample(200)