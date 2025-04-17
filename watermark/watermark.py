from PIL import Image


def apply_watermark(base_img: Image.Image,
                    watermark_img: Image.Image,
                    position: str = "bottom-right",
                    margin: int = 10) -> Image.Image:
    base = base_img.convert("RGBA")
    mark = watermark_img.convert("RGBA")

    # Resize watermark if too big
    if mark.width > base.width or mark.height > base.height or mark.width < base.width or mark.height < base.height:
        ratio = min(base.width / mark.width,
                    base.height / mark.height) * 0.1
        new_size = (int(mark.width * ratio),
                    int(mark.height * ratio))
        # Use high-quality resampling filter
        mark = mark.resize(new_size, resample=Image.Resampling.LANCZOS)

    # Determine position
    if position == "top-left":
        x = margin
        y = margin
    elif position == "top-right":
        x = base.width - mark.width - margin
        y = margin
    elif position == "bottom-left":
        x = margin
        y = base.height - mark.height - margin
    else:  # bottom-right
        x = base.width - mark.width - margin
        y = base.height - mark.height - margin

    # Composite images
    layer = Image.new("RGBA", base.size)
    layer.paste(mark, (x, y), mark)
    combined = Image.alpha_composite(base, layer)
    return combined.convert("RGB")
