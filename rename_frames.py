import os, sys

for idx, img in enumerate(os.listdir('original_frames')):
    new_name = f'{idx+1:0>4d}.png'
    os.rename(f'original_frames/{img}', f'original_frames/{new_name}')