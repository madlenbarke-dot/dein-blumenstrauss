from PIL import Image, ImageDraw
import os

def create_cursor(name, color, shape='circle'):
    size = (32, 32)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    padding = 2
    box = [padding, padding, size[0]-padding, size[1]-padding]
    
    if shape == 'circle':
        draw.ellipse(box, fill=color)
    else:
        draw.rectangle(box, fill=color)
        
    output_path = os.path.join('src/assets/cursors', f'{name}_32.png')
    img.save(output_path)
    print(f'Created {output_path}')

# Create directories if needed
os.makedirs('src/assets/cursors', exist_ok=True)

# Generate cursors
create_cursor('heart', (255, 100, 150, 255)) # Pink
create_cursor('hover', (255, 255, 100, 255)) # Yellow
create_cursor('cursor', (255, 255, 255, 255)) # White

print("Cursors generated successfully!")
