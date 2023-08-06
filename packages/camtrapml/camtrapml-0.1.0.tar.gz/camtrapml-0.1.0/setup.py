# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camtrapml',
 'camtrapml.detection',
 'camtrapml.detection.models',
 'camtrapml.embedding',
 'camtrapml.image']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0',
 'PyExifTool>=0.4.13,<0.5.0',
 'font-fredoka-one>=0.0.4,<0.0.5',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.2,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'scikit-learn==1.0.1',
 'tensorflow-hub>=0.12.0,<0.13.0',
 'tensorflow>=2.8.0,<3.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'camtrapml',
    'version': '0.1.0',
    'description': 'CamTrapML is a Python library for Detecting, Classifying, and Analysing Wildlife Camera Trap Imagery.',
    'long_description': '# CamTrapML\n\n> CamTrapML is a Python library for Detecting, Classifying, and Analysing Wildlife [Camera Trap](https://en.wikipedia.org/wiki/Camera_trap) Imagery.\n\n## Installation\n\n    $ pip install camtrapml\n\n## Features\n\n### Loading Data\n\nSearch for images in a directory, load an image and create a thumbnail.\n\n\n```python\n%load_ext autoreload\n%autoreload\nfrom camtrapml.dataset import ImageDataset\nfrom camtrapml.image.utils import load_image, thumbnail\n\nena24 = ImageDataset(\n    name="ena24",\n    path="/pool0/datasets/ena24/ena24",\n)\n\nena24_image_paths = list(ena24.enumerate_images())\n\nthumbnail(load_image(ena24_image_paths[0]))\n```\n\n### EXIF Extraction\n\nEXIF extraction is a common task in gathering the metadata such as each image\'s timestamp, camera model, focal length, etc. Some researchers write labelling into the EXIF data. CamTrapML doesn\'t assist with writing to EXIF. However, there is functionality for extracting it for analysis and building datasets for training new models from previously labelled images.\n\nExifTool is required for this package to work. Installation instructions can be found [here](https://exiftool.org/install.html).\n\nThree methods are available for extracting EXIF data from images. Each with different performance characteristics.\n\n**Method 1: Individual Images**\n\n\n```python\nfrom camtrapml.image.exif import extract_exif\n\nexif = extract_exif(ena24_image_paths[0])\nexif\n```\n\n**Method 2: Multiple Images**\n\n`extract_multiple_exif` passes a list of image paths to ExifTool and returns a list of dictionaries containing the EXIF data. This is faster than `extract_exif` when multiple images are being processed as it only passes the list of image paths to ExifTool once, rather than spawning a new process for each image.\n\n\n```python\nfrom camtrapml.image.exif import extract_multiple_exif\n\nexif = extract_multiple_exif(ena24_image_paths)\nexif[0]\n```\n\n**Method 3: Multiple Images, Multiple Processes**\n\nWhen processing large datasets, it\'s apparent that the bottleneck in extracting the EXIF information tends to be the CPU. This method spawns multiple versions of ExifTool in parallel, each with a batch of image paths. This is faster than `extract_multiple_exif` when processing large datasets as it allows for multiple processes to be spawned and the data extracted in parallel.\n\n\n```python\nfrom camtrapml.image.exif import extract_multiple_exif_fast\n\nexif = extract_multiple_exif_fast(ena24_image_paths)\nexif[0]\n```\n\n### Detection\n\nVarious Detection models are available in the `camtrapml.detection` subpackage. These currently include MegaDetector (v4.1, v3 and v2) and support for loading in custom Tensorflow v1.x Object Detection Frozen models.\n\n#### Detection with MegaDetector v4.1\n\n\n```python\nfrom camtrapml.detection.models.megadetector import MegaDetectorV4_1\nfrom camtrapml.detection.utils import render_detections\n\nwith MegaDetectorV4_1() as detector:\n    detections = detector.detect(ena24_image_paths[0])\n\nthumbnail(\n    render_detections(ena24_image_paths[0], detections, class_map=detector.class_map)\n)\n```\n\n#### Detection with a custom Tensorflow v1.x Object Detection Frozen model\n\n\n```python\nfrom camtrapml.detection.models.tensorflow import TF1ODAPIFrozenModel\nfrom camtrapml.detection.utils import render_detections\nfrom pathlib import Path\n\nwith TF1ODAPIFrozenModel(\n    model_path=Path("~/Downloads/my-custom-model.pb").expanduser(),\n    model_image_tensor_name="image_tensor:0",\n    model_boxes_tensor_name="detection_boxes:0",\n    model_scores_tensor_name="detection_scores:0",\n    model_classes_tensor_name="detection_classes:0",\n    class_map={\n        1: "animal",\n    },\n) as detector:\n    detections = detector.detect(ena24_image_paths[1])\n\nthumbnail(\n    render_detections(ena24_image_paths[1], detections, class_map=detector.class_map)\n)\n```\n\n#### Extract Detections\n\n\n```python\nfrom camtrapml.detection.models.megadetector import MegaDetectorV4_1\nfrom camtrapml.detection.utils import extract_detections_from_image\n\nwith MegaDetectorV4_1() as detector:\n    detections = detector.detect(ena24_image_paths[0])\n\nlist(extract_detections_from_image(load_image(ena24_image_paths[0]), detections))[0]\n```\n\n#### Remove Humans from Images\n\nIn order to reduce the risks of identification of humans in line with GDPR, CamTrapML provides the ability to remove humans from images. This is achieved by using the MegaDetector v3+ models to detect humans in the image, and then replacing all pixels in each human detection.\n\n\n```python\nfrom camtrapml.detection.models.megadetector import MegaDetectorV4_1\nfrom camtrapml.detection.utils import remove_detections_from_image\nfrom camtrapml.image.utils import load_image, thumbnail\nfrom pathlib import Path\n\nct_image_with_humans = Path("/pool0/datasets/bens-day-at-zsl/IMG_0576.JPG").expanduser()\n\nwith MegaDetectorV4_1() as detector:\n    detections = detector.detect(ct_image_with_humans)\n\nhuman_class_id = 2\n\nthumbnail(\n    remove_detections_from_image(\n        load_image(ct_image_with_humans),\n        [\n            detection\n            for detection in detections\n            if detection["category"] == human_class_id and detection["conf"] > 0.5\n        ],\n    )\n)\n```\n',
    'author': 'Benjamin C. Evans',
    'author_email': 'Benjamin.Evans@brunel.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bencevans/camtrapml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
