import os
import time
from PIL import Image, ImageDraw, ImageFont

def create_terminal_frame(text, step, total_steps, mode="typing"):
    # Mac terminal dimensions
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([0, 0, width, 40], fill=(60, 60, 60))
    # Window controls
    draw.ellipse([15, 12, 30, 27], fill=(255, 95, 87)) # Red
    draw.ellipse([40, 12, 55, 27], fill=(255, 189, 46)) # Yellow
    draw.ellipse([65, 12, 80, 27], fill=(39, 201, 63)) # Green
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 24)
    except:
        font = ImageFont.load_default()

    y_offset = 60
    prompt = "aniket@mac:~/VaultGuard-AI$ "
    draw.text((20, y_offset), f"{prompt}{text[:step]}", fill=(200, 200, 200), font=font)
    
    # Blinking cursor
    if (int(time.time() * 2) % 2 == 0):
        draw.text((20 + draw.textlength(f"{prompt}{text[:step]}", font=font), y_offset), "_", fill=(255, 255, 255), font=font)

    if mode == "output":
        output = """
[INFO] Initializing VaultGuard Engine...
[INFO] Loading: sample_report.txt
[INFO] Chunks Created: 4
[INFO] Indexing ChromaDB... Done.
[INFO] Indexing BM25... Done.

[RESULT] ----------------------------------------
| Metric         | Value                        |
|----------------|------------------------------|
| Expected IRR   | 25%                          |
| Strategy       | Private Equity               |
| Region         | Southeast Asia               |
| Compliance     | SEC Reg D (Simulated)        |
-------------------------------------------------
        """
        draw.text((20, y_offset + 40), output, fill=(0, 255, 0), font=font)

    return img

def create_ui_frame(step):
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), color=(240, 242, 246))
    draw = ImageDraw.Draw(img)
    
    # Sidebar
    draw.rectangle([0, 0, 300, height], fill=(14, 38, 74))
    
    # Main Content Area
    draw.text((350, 50), "VaultGuard-AI Dashboard", fill=(30, 30, 30), font=ImageFont.load_default())
    
    # Card 1: Results
    draw.rectangle([350, 100, 1150, 300], fill=(255, 255, 255), outline=(200, 200, 200))
    draw.text((370, 120), "Analysis Result:", fill=(0, 0, 0), font=ImageFont.load_default())
    draw.text((370, 150), "The Southeast Asian market shows high volatility but the Project X IRR", fill=(50, 50, 50), font=ImageFont.load_default())
    draw.text((370, 170), "stays robust at 25% due to hedging strategies mentioned in the PPM.", fill=(50, 50, 50), font=ImageFont.load_default())

    # Card 2: Chart
    draw.rectangle([350, 350, 1150, 750], fill=(255, 255, 255), outline=(200, 200, 200))
    # Dummy chart lines
    for i in range(10):
        h = 100 + (i * 20)
        draw.rectangle([400 + (i*60), 730 - h, 430 + (i*60), 730], fill=(22, 163, 74))

    return img

def generate_gif():
    print("Generating Title Animation GIF...")
    frames = []
    
    # Part 1: Terminal Typing
    cmd = "python main.py"
    for i in range(len(cmd) + 1):
        frames.append(create_terminal_frame(cmd, i, len(cmd)))
    
    # Part 2: Terminal Output (Hold)
    for _ in range(15):
        frames.append(create_terminal_frame(cmd, len(cmd), len(cmd), mode="output"))
    
    # Part 3: UI Transition
    for i in range(10):
        frames.append(create_ui_frame(i))
    
    # Save GIF
    if not os.path.exists("images"):
        os.makedirs("images")
        
    frames[0].save(
        "images/title-animation.gif",
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        optimize=True,
        palette=Image.ADAPTIVE
    )
    print("Successfully generated images/title-animation.gif")

if __name__ == "__main__":
    generate_gif()
