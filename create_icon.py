"""
Improved icon generator for Bulk File Renamer application.
Creates a professional icon using PIL/Pillow with better error handling.
"""

def create_simple_icon():
    """
    Create a simple icon using PIL/Pillow if available.
    If not available, provides instructions for manual creation.
    """
    try:
        # Try importing PIL/Pillow
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            # Try alternative import
            import PIL
            from PIL import Image, ImageDraw, ImageFont
        
        print("[+] Pillow detected, creating icon...")
        
        # Create a 256x256 image with a blue gradient background
        size = 256
        img = Image.new('RGB', (size, size), '#2196F3')
        draw = ImageDraw.Draw(img)
        
        # Draw a folder icon (simplified)
        # Folder body
        folder_color = '#FFC107'
        draw.rectangle([40, 90, 216, 200], fill=folder_color, outline='#FFA000', width=3)
        
        # Folder tab
        draw.rectangle([40, 70, 120, 90], fill=folder_color, outline='#FFA000', width=3)
        
        # Draw an arrow (representing rename/transform)
        arrow_color = '#FFFFFF'
        # Arrow shaft
        draw.rectangle([80, 130, 176, 145], fill=arrow_color)
        # Arrow head
        draw.polygon([(176, 115), (216, 137), (176, 160)], fill=arrow_color)
        
        # Draw text "BR" (Bulk Renamer)
        try:
            # Try to use a nice font, fallback to default if not available
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            try:
                font = ImageFont.truetype("Arial.ttf", 40)
            except:
                font = ImageFont.load_default()
        
        text = "BR"
        # Get text bounding box for centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (size - text_width) // 2
        text_y = size - 60
        
        draw.text((text_x, text_y), text, fill='#FFFFFF', font=font)
        
        # Ensure assets directory exists
        import os
        if not os.path.exists('assets'):
            os.makedirs('assets')
            print("✓ Created 'assets' directory")
        
        # Save as ICO file with multiple sizes
        icon_path = 'assets/icon.ico'
        img.save(icon_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])
        
        print(f"✓ Icon created successfully: {icon_path}")
        print("  You can now use this icon or replace it with your own custom design.")
        
        # Also save as PNG for preview
        img.save('assets/icon_preview.png', format='PNG')
        print(f"✓ Preview saved as: assets/icon_preview.png")
        
        return True
        
    except ImportError as e:
        print("⚠ Pillow (PIL) is not installed.")
        print(f"\nImport error details: {e}")
        print("\nTo create an icon automatically, install Pillow:")
        print("  pip install Pillow")
        print("\nAlternatively, create an icon manually:")
        print("  1. Design a 256x256 pixel image")
        print("  2. Use an online converter: https://convertio.co/png-ico/")
        print("  3. Save as 'assets/icon.ico'")
        return False
    
    except Exception as e:
        print(f"✗ Error creating icon: {e}")
        print("\nYou can create an icon manually:")
        print("  1. Design a 256x256 pixel image")
        print("  2. Use an online converter: https://convertio.co/png-ico/")
        print("  3. Save as 'assets/icon.ico'")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Bulk File Renamer - Icon Generator")
    print("=" * 60)
    print()
    
    # Create the icon
    success = create_simple_icon()
    
    print()
    print("=" * 60)
    
    if success:
        print("\n✅ Icon generation complete!")
    else:
        print("\n⚠ Icon generation skipped - manual creation required")
