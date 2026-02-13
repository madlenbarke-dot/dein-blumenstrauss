from PIL import Image, ImageDraw
import os

def create_cursor(name, color, type='circle'):
    size = (32, 32)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    padding = 2
    
    if type == 'heart':
        # Draw a heart shape
        # Bezier curve approximation or simple polygon
        # Simplified heart shape using polygon points
        points = [
            (16, 28), # Bottom tip
            (2, 14),  # Left side
            (2, 8),   # Top left curve start
            (8, 2),   # Top left curve top
            (16, 8),  # Middle top
            (24, 2),  # Top right curve top
            (30, 8),  # Top right curve start
            (30, 14)  # Right side
        ]
        # Smooth with multiple ellipses
        # Left lobe
        draw.ellipse([2, 2, 18, 18], fill=color)
        # Right lobe
        draw.ellipse([14, 2, 30, 18], fill=color)
        # Bottom triangle
        draw.polygon([(2, 10), (30, 10), (16, 28)], fill=color)
        
    elif type == 'ring':
        # Draw a ring (stroked circle)
        box = [padding, padding, size[0]-padding, size[1]-padding]
        draw.ellipse(box, outline=color, width=3)
        
    else: # Solid circle
        box = [padding, padding, size[0]-padding, size[1]-padding]
        draw.ellipse(box, fill=color)
        
    output_path = os.path.join('src/assets/cursors', f'{name}_32.png')
    img.save(output_path)
    print(f'Created {output_path}')

# Create directories if needed
os.makedirs('src/assets/cursors', exist_ok=True)

# Generate improved cursors
# Heart: Pink heart shape
create_cursor('heart', (255, 100, 150, 255), type='heart')

# Hover: Yellow ring
create_cursor('hover', (255, 200, 50, 255), type='ring')

# Cursor: White ring with shadow/outline for visibility
# Let's make a white circle with black outline for better visibility
size = (32, 32)
img = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
padding = 4
box = [padding, padding, size[0]-padding, size[1]-padding]
# Black outline
draw.ellipse([padding-1, padding-1, size[0]-padding+1, size[1]-padding+1], outline=(0,0,0,100), width=1)
# White fill
draw.ellipse(box, outline=(255,255,255,255), width=2)
# Center dot
draw.ellipse([14, 14, 18, 18], fill=(255,255,255,255))
img.save('src/assets/cursors/cursor_32.png')
print('Created src/assets/cursors/cursor_32.png')

# Disco: Purple ring for party mode
create_cursor('disco', (150, 100, 255, 255), type='ring')

print("Improved cursors generated successfully!")
