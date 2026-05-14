import numpy as np
import torch
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget


def compute_gradcam(model: torch.nn.Module,
                    input_tensor: torch.Tensor,
                    target_layer,
                    target_category: int | None = None,
                    use_cuda: bool = False):
    device = torch.device("cuda" if use_cuda and torch.cuda.is_available() else "cpu")
    model = model.to(device)
    input_tensor = input_tensor.to(device)
    target = None
    if target_category is not None:
        target = [ClassifierOutputTarget(target_category)]
    cam = GradCAM(model=model, target_layers=[target_layer])
    grayscale_cam = cam(input_tensor=input_tensor, targets=target)
    return grayscale_cam[0]


def overlay_gradcam(image: np.ndarray, grayscale_cam: np.ndarray, colormap="jet") -> np.ndarray:
    if image.ndim == 2:
        image = np.stack([image, image, image], axis=-1)
    image = image.astype(np.float32)
    if image.max() > 1.0:
        image = image / np.max(image)
    overlay = show_cam_on_image(image, grayscale_cam, use_rgb=True)
    return overlay


def gradcam_for_batch(model: torch.nn.Module,
                      images: torch.Tensor,
                      target_layer,
                      target_class: int | None = None,
                      use_cuda: bool = False):
    images = images.to("cpu")
    cams = []
    overlays = []
    for image_tensor in images:
        input_tensor = image_tensor.unsqueeze(0)
        grayscale_cam = compute_gradcam(model, input_tensor, target_layer, target_category=target_class, use_cuda=use_cuda)
        image_np = image_tensor.squeeze(0).cpu().numpy()
        overlay = overlay_gradcam(image_np, grayscale_cam)
        cams.append(grayscale_cam)
        overlays.append(overlay)
    return np.stack(cams), np.stack(overlays)
