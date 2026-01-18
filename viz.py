import matplotlib.pyplot as plt
import numpy as np
import os

def generate_skill_distribution(scores: dict, names: list, output_path: str):
    """
    Generates a professional bar chart for candidate matching scores.
    """
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(names)))
    bars = ax.barh(names, scores, color=colors, edgecolor='white', alpha=0.8)
    
    ax.set_title('TalentArch-AI: Candidate Matching Precision', fontsize=16, pad=20, color='#00ffcc')
    ax.set_xlabel('Hybrid Match Score (0.0 - 1.0)', fontsize=12, color='#cccccc')
    ax.set_xlim(0, 1.1)
    
    # Add values to bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.02, bar.get_y() + bar.get_height()/2, 
                f'{width:.2f}', va='center', fontsize=10, color='white')

    plt.grid(axis='x', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"[v] Saved chart to {output_path}")

def generate_pipeline_stats(output_path: str):
    """
    Generates a pie chart of the search weight distribution.
    """
    plt.style.use('dark_background')
    labels = ['Semantic Similarity', 'Keyword Matching (BM25)']
    sizes = [60, 40]
    colors = ['#440154', '#21918c']
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, 
           startangle=140, textprops={'color':"w"})
    
    ax.set_title('Experimental Weight Distribution', fontsize=14, color='#00ffcc')
    plt.savefig(output_path, dpi=300)
    print(f"[v] Saved pipeline stats to {output_path}")

if __name__ == "__main__":
    img_dir = os.path.join(os.path.dirname(__file__), "images")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        
    # Mock scores for visualization
    mock_names = ['Sarah Chen', 'Marcus Rodriguez', 'Elena Volkov', 'Jordan Smith', 'Aisha Khan']
    mock_scores = [0.92, 0.85, 0.78, 0.65, 0.54]
    
    generate_skill_distribution(mock_scores, mock_names, os.path.join(img_dir, "skill-distribution.png"))
    generate_pipeline_stats(os.path.join(img_dir, "pipeline-stats.png"))
