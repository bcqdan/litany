from PIL import Image, ImageDraw, ImageFont
import argparse

def add_text_with_rounded_rectangle(image_path, text_file, output_image, width_percentage, height_percentage, center_x_percentage, center_y_percentage, rect_color, opacity, font_size):
    # Open the image
    image = Image.open(image_path).convert("RGBA")
    
    # Open and read the text file, preserving line breaks
    with open(text_file, 'r') as file:
        text_lines = file.readlines()  # This keeps each line as it is in the file
    
    # Calculate dimensions and position based on percentages
    img_width, img_height = image.size
    width = int(width_percentage / 100 * img_width)
    height = int(height_percentage / 100 * img_height)
    x = (img_width - width) // 2  # Center the rectangle horizontally
    y = int((center_y_percentage / 100) * img_height - height / 2)
    
    # Create a new image for the rectangle and text with transparency
    txt_img = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_img)
    
    # Draw a rounded rectangle
    rect = (x, y, x + width, y + height)
    rect_color_with_opacity = rect_color + (opacity,)
    draw.rounded_rectangle(rect, radius=20, fill=rect_color_with_opacity)  # Adjust radius as needed
    
    # Load a font with specified font size
    try:
        font = ImageFont.truetype("Avenir.ttc", font_size)
    except IOError:
        font = ImageFont.load_default(font_size)
        print("Custom font not found. Using default font.")

    # Calculate line height for multiline text
    line_height = font.getbbox("A")[3]  # Height of a line of text

    # Calculate starting text position (centered within the rectangle)
    total_text_height = line_height * len(text_lines)
    text_y = y + (height - total_text_height) // 2
    
    # Draw each line of text
    for line in text_lines:
        text_width = draw.textlength(line.strip(), font=font)
        text_x = x + (width - text_width) // 2
        draw.text((text_x, text_y), line.strip(), fill=(255, 255, 255, 255), font=font)
        text_y += line_height  # Move down to the next line

    # Combine original image with the text image
    combined = Image.alpha_composite(image, txt_img)
    
    # Save the final image
    combined.convert("RGB").save(output_image, format="PNG")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add text with a rounded rectangle overlay on an image.")
    parser.add_argument("image_path", help="Path to the input image (webp format)")
    parser.add_argument("text_file", help="Path to the text file")
    parser.add_argument("output_image", help="Path to the output image (PNG format)")
    parser.add_argument("--width_percentage", type=float, required=True, help="Width of the rounded rectangle as a percentage of the image width")
    parser.add_argument("--height_percentage", type=float, required=True, help="Height of the rounded rectangle as a percentage of the image height")
    parser.add_argument("--center_x_percentage", type=float, required=True, help="X center of the rectangle as a percentage of the image width")
    parser.add_argument("--center_y_percentage", type=float, required=True, help="Y center of the rectangle as a percentage of the image height")
    parser.add_argument("--rect_color", nargs=3, type=int, required=True, help="Color of the rectangle (R G B)")
    parser.add_argument("--opacity", type=int, required=True, help="Opacity of the rectangle (0-255)")
    parser.add_argument("--font_size", type=int, default=20, help="Font size for the text")

    args = parser.parse_args()
    add_text_with_rounded_rectangle(
        args.image_path,
        args.text_file,
        args.output_image,
        args.width_percentage,
        args.height_percentage,
        args.center_x_percentage,
        args.center_y_percentage,
        tuple(args.rect_color),
        args.opacity,
        args.font_size
    )
