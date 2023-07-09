import ImageReward as RM
import numpy as np
from PIL import Image

class ImageRewardLoader:
    CATEGORY = "ImageReward"

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("STRING", {
                    "multiline": False,
                    "default": "ImageReward-v1.0"
                }),
            },
        }

    RETURN_TYPES = ("IMAGEREWARD_MODEL",)
    RETURN_NAMES = ("IMAGEREWARD_MODEL",)
    OUTPUT_NODE = False

    FUNCTION = "load_model"

    def load_model(self, model):
        model = RM.load(model)
        return (model,)

class ImageRewardScore:
    CATEGORY = "ImageReward"

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("IMAGEREWARD_MODEL",),
                "prompt": ("STRING", {
                    "multiline": True
                }),
                "images": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("FLOAT","STRING")
    RETURN_NAMES = ("SCORE_FLOAT","SCORE_STRING")
    OUTPUT_NODE = False

    FUNCTION = "score_images"

    def score_images(self, model, prompt, images):
        score = 0.0
        for image in images:
          # convert to PIL image
          i = 255.0 * image.cpu().numpy()
          img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
          score += model.score(prompt, [img])
        score /= len(images)
        return (score,str(score))


NODE_CLASS_MAPPINGS = {
    "ImageRewardLoader": ImageRewardLoader,
    "ImageRewardScore": ImageRewardScore
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageRewardLoader": "ImageReward Loader",
    "ImageRewardScore": "ImageReward Score"
}
