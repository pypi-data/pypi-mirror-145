

def TransformNormalizedRect(rect, 
                            input_image_width,
                            input_image_height,
                            square_long = True,
                            scale_x=1.5,
                            scale_y=1.5):
    width = rect.width
    height = rect.height
    
    if square_long:
        long_side = max(width*input_image_width, height*input_image_height)
        width = long_side / input_image_width
        height = long_side / input_image_height
    
    rect.width = width*scale_x
    rect.height = height*scale_y
        