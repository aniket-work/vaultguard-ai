from PIL import Image, ImageDraw, ImageFont
import os
import time

def create_terminal_frame(text, width=800, height=500, cursor=True, frame_idx=0):
    # Dark terminal theme
    bg_color = (30, 30, 46)
    text_color = (205, 214, 244)
    header_color = (49, 50, 68)
    
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw Mac-style title bar
    draw.rectangle([0, 0, width, 30], fill=header_color)
    # Window controls
    draw.ellipse([10, 8, 22, 20], fill=(255, 95, 87)) # Red
    draw.ellipse([30, 8, 42, 20], fill=(255, 189, 46)) # Yellow
    draw.ellipse([50, 8, 62, 20], fill=(40, 200, 64)) # Green
    
    # Try to load a monospaced font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16)
    except:
        font = ImageFont.load_default()
        
    y_offset = 50
    lines = text.split('\n')
    for line in lines:
        draw.text((20, y_offset), line, font=font, fill=text_color)
        y_offset += 25
        
    if cursor and (frame_idx // 2) % 2 == 0:
        # Blinking cursor
        last_line_width = draw.textlength(lines[-1], font=font) if lines else 0
        draw.rectangle([20 + last_line_width, y_offset - 25, 20 + last_line_width + 10, y_offset - 5], fill=text_color)
        
    return img

def generate_gif(output_path):
    frames = []
    
    command = "$ python talent_arch.py --query 'Cloud Native Engineer'"
    output_log = [
        "[*] Initializing Hybrid Search Engine...",
        "[+] Connected to Local Vector DB (Qdrant)",
        "[+] Keyword Index (BM25) Initialized",
        "[*] Query: 'Cloud Native Engineer'",
        "[*] Performing Semantic Analysis (Weight: 0.6)...",
        "[*] Performing Keyword Match (Weight: 0.4)...",
        "[OK] Fusion Scoring Complete",
        "",
        "SUMMARY REPORT:",
        "--------------------------------------------------",
        "Jordan Smith      | Lead DevOps     | 0.82",
        "Sarah Chen        | Fullstack Dev   | 0.65",
        "--------------------------------------------------"
    ]
    
    # Part 1: Typing animation
    current_text = ""
    for i in range(len(command) + 1):
        current_text = command[:i]
        frames.append(create_terminal_frame(current_text, frame_idx=len(frames)))
        
    # Part 2: Wait & Hold
    for _ in range(5):
        frames.append(create_terminal_frame(command, frame_idx=len(frames)))
        
    # Part 3: Show execution logs incrementally
    current_content = command + "\n"
    for line in output_log:
        current_content += line + "\n"
        # Slow down for the summary
        repeat = 3 if "SUMMARY" in line else 1
        for _ in range(repeat):
            frames.append(create_terminal_frame(current_content, frame_idx=len(frames)))
            
    # Part 4: Transition and UI Component (Skill Distribution Chart)
    ui_img_path = os.path.join(os.path.dirname(__file__), "images", "skill-distribution.png")
    if os.path.exists(ui_img_path):
        ui_img = Image.open(ui_img_path).resize((800, 500))
        for _ in range(15): # Hold UI for 3-4s
            frames.append(ui_img)
            
    # Save GIF with global adaptive palette
    if frames:
        frames = [f.convert('P', palette=Image.ADAPTIVE) for f in frames]
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=120,
            loop=0,
            optimize=True
        )
        print(f"[v] Saved animated GIF to {output_path}")

if __name__ == "__main__":
    img_dir = os.path.join(os.path.dirname(__file__), "images")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    generate_gif(os.path.join(img_dir, "title-animation.gif"))
