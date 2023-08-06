# easyaug
A package to faster and easier preview, prepare and augment images. This includes 3 main components:
1. Preprocesser: Preprocess images before augmentation if needed.
2. Quickviewer: Quickly preview images before augmentation.
3. Augmenter: Augment images with different pre-made augmentation types.

## Installation

```bash
pip install easyaug
```

# Usage

View the documentation for a complete usage guide. The quick and dirty usage is shown below. 
When initalizing these packages, you can access their neat functions.

To use Quickviewer:

```python
from easyaug.quickview import Quickviewer
quickviewer = Quickviewer()
```

To use Preprocesser:

```python
from easyaug.preprocess import Preprocesser
preprocesser = Preprocesser()
```

To use Augmenter:

```python
from easyaug.augment import Augmenter
augmenter = Augmenter()
```

