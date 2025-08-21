from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    # Create a new image with a dark blue background
    width, height = 400, 200
    background_color = (10, 25, 47)  # Dark blue
    text_color = (100, 255, 218)     # Teal
    
    # Create a new image with RGBA mode (for transparency support)
    image = Image.new('RGBA', (width, height), background_color + (255,))
    draw = ImageDraw.Draw(image)
    
    try:
        # Try to load a nice font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except IOError:
            font = ImageFont.load_default()
        
        # Draw the text in the center of the image
        text = "JARVIS"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (width - text_width) / 2
        y = (height - text_height) / 2
        
        # Draw the text with a slight shadow for depth
        draw.text((x+2, y+2), text, fill=(0, 0, 0, 128), font=font)
        draw.text((x, y), text, fill=text_color, font=font)
        
        # Draw a decorative line under the text
        line_y = y + text_height + 10
        draw.line([(x, line_y), (x + text_width, line_y)], 
                 fill=text_color, width=3)
        
        # Save the image
        image.save("jarvis_logo.png")
        print("Logo created successfully as 'jarvis_logo.png'")
        return True
        
    except Exception as e:
        print(f"Error creating logo: {e}")
        return False

if __name__ == "__main__":
    create_logo()
