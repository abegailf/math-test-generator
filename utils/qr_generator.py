import io
import qrcode
from qrcode.image.svg import SvgImage

def generate_qr_code(data, as_image=False):
    """
    Generate a QR code from the given data.
    
    Args:
        data (str): The data to encode in the QR code (typically a URL)
        as_image (bool): If True, returns a PIL Image object; if False, returns SVG string
    
    Returns:
        Either a PIL Image object or SVG string depending on as_image parameter
    """
    # Set QR code parameters
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data
    qr.add_data(data)
    qr.make(fit=True)
    
    if as_image:
        # Create a PIL image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Return the image
        img_buffer = io.BytesIO()
        img.save(img_buffer)
        img_buffer.seek(0)
        return img_buffer
    else:
        # Generate SVG
        img = qr.make_image(image_factory=SvgImage)
        
        # Convert to SVG string
        svg_buffer = io.BytesIO()
        img.save(svg_buffer)
        svg_string = svg_buffer.getvalue().decode('utf-8')
        
        return svg_string
