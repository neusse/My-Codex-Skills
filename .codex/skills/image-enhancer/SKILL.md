---
name: image-enhancer
description: Improve screenshots and images for documentation, presentations, or publishing by enhancing clarity, sharpness, resolution, and export quality.
---

# Image Enhancer

Use this skill when a user asks to improve, upscale, sharpen, clean up, or prepare image files for a specific use.

## Workflow

1. Identify the source image path(s), intended output use, and requested changes.
2. Inspect image dimensions, format, file size, and obvious quality issues.
3. Preserve originals. Write enhanced output to a new deterministic filename unless the user requests overwrite.
4. Apply only changes that fit the request, such as upscaling, sharpening, denoising, contrast correction, crop cleanup, or export optimization.
5. Report the output path, original dimensions, final dimensions, and any files that could not be processed.

## Defaults

- Use PNG for screenshots and UI text unless the user asks for another format.
- Use JPEG/WebP only when smaller file size matters more than lossless fidelity.
- For batch jobs, keep outputs beside the originals in an `enhanced/` folder.
- If quality cannot be improved reliably, say why instead of fabricating an enhancement result.

## Common Requests

- "Improve this screenshot for docs"
- "Upscale these images for a presentation"
- "Sharpen this blurry UI capture"
- "Reduce compression artifacts in these PNGs"
- "Prepare this image for LinkedIn/Twitter/print"
