# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tf_transformers',
 'tf_transformers.activations',
 'tf_transformers.callbacks',
 'tf_transformers.callbacks.metrics',
 'tf_transformers.core',
 'tf_transformers.data',
 'tf_transformers.data.callbacks',
 'tf_transformers.data.processors',
 'tf_transformers.layers',
 'tf_transformers.layers.attention',
 'tf_transformers.layers.mask',
 'tf_transformers.layers.transformer',
 'tf_transformers.losses',
 'tf_transformers.models',
 'tf_transformers.models.albert',
 'tf_transformers.models.bart',
 'tf_transformers.models.bert',
 'tf_transformers.models.bigbird',
 'tf_transformers.models.clip',
 'tf_transformers.models.distilbert',
 'tf_transformers.models.encoder_decoder',
 'tf_transformers.models.gpt2',
 'tf_transformers.models.minilm',
 'tf_transformers.models.model_configs',
 'tf_transformers.models.model_configs.albert',
 'tf_transformers.models.model_configs.bert',
 'tf_transformers.models.model_configs.gpt2',
 'tf_transformers.models.model_configs.mt5',
 'tf_transformers.models.model_configs.roberta',
 'tf_transformers.models.model_configs.t5',
 'tf_transformers.models.mt5',
 'tf_transformers.models.roberta',
 'tf_transformers.models.sentence_transformers',
 'tf_transformers.models.t5',
 'tf_transformers.models.tasks',
 'tf_transformers.models.vit',
 'tf_transformers.notebooks.experimental',
 'tf_transformers.notebooks.tutorials.albert_pretrain',
 'tf_transformers.optimization',
 'tf_transformers.pipeline',
 'tf_transformers.text',
 'tf_transformers.text.lm_tasks',
 'tf_transformers.utils']

package_data = \
{'': ['*'],
 'tf_transformers': ['notebooks/*',
                     'notebooks/conversion_scripts/*',
                     'notebooks/tutorials/*',
                     'notebooks/tutorials/joint_loss_experiments/*',
                     'notebooks/tutorials/joint_loss_experiments/glue/*'],
 'tf_transformers.models.model_configs': ['unilm_cnndm/*']}

install_requires = \
['absl-py>=1.0.0,<2.0.0',
 'sentencepiece>=0.1.96,<0.2.0',
 'tqdm>=4.62.3,<5.0.0',
 'transformers>=4.15.0,<5.0.0']

setup_kwargs = {
    'name': 'tf-transformers',
    'version': '1.0.20',
    'description': 'NLP with Transformer based models on Tensorflow 2.0',
    'long_description': '<!---\nCopyright 2021 The LegacyAI Team. All rights reserved.\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n-->\n\n<p align="center">\n    <br>\n    <img src="src/transformers_blue.png" width="400"/>\n    <br>\n</p>\n\n<p align="center">\n<a href="https://github.com/legacyai/tf-transformers/actions?workflow=Tests">\n        <img alt="Tests" src="https://github.com/legacyai/tf-transformers/workflows/Tests/badge.svg">\n</a>\n\n<a href="https://codecov.io/gh/legacyai/tf-transformers">\n        <img alt="Coverage" src="https://codecov.io/gh/legacyai/tf-transformers/branch/main/graph/badge.svg?token=9TZ10G9GL6">\n</a>\n\n<a href="https://opensource.org/licenses/Apache-2.0">\n        <img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg">\n</a>\n</p>\n\n<h1 align="center">\n<b>Tensorflow Transformers</b>\n</h1>\n\n<h5 align="center">\n<p>Website: https://legacyai.github.io/tf-transformers</p>\n</h5>\n\n<h3 align="center">\n<p>tf-transformers: faster and easier state-of-the-art Transformer in TensorFlow 2.0\n</h3>\n\nImagine auto-regressive generation to be **90x** faster.\ntf-transformers (Tensorflow Transformers) is designed to harness the full power of Tensorflow 2, designed specifically for Transformer based architecture.\n\nThese models can be applied on:\n\n* 📝 Text, for tasks like text classification, information extraction, question answering, summarization, translation, text generation, in over 100 languages.\n* 🖼️ Images, for tasks like image classification, object detection, and segmentation.\n* 🗣️ Audio, for tasks like speech recognition and audio classification. (Coming Soon)\n## Version\nversion: v1.0.8\n## Unique Features\n- **Faster AutoReggressive Decoding**\n- **TFlite** support\n- **Creating TFRecords is simple**.\n- **Auto-Batching tf.data.dataset** or **tf.ragged** tensors\n- **Everything is dictionary (inputs and outputs)**\n- Multiple mask modes like **causal**, **user-defined**, **prefix**.\n- **tensorflow-text tokenizer** support\n- **Supports GPU, TPU, multi-GPU trainer with wandb, multiple callbacks, auto tensorboard**\n\n\n## Benchmark on GPT2 text generation\n\nGPT2 text generation with ```max_length=64```, ```num_beams=3``` .\n\n```\ntf_transformers : 31 minutes\nhuggingface_tf  : 83 minutes\nhuggingface_pt  : 36 minutes\nhuggingface_jax : 35 minutes\n```\n\nFrom ```83 minutes``` to ```31 minutes``` is a significant speedup. ```167 %1``` speedup.\nOn an average, **tf-transformers** is **80-90 times** faster than **HuggingFace** **Tensorflow** implementation and in most cases it is **comparable** or **faster** than **PyTorch**.\n\nMore benchmarks can be found in [benchmark](https://github.com/legacyai/tf-transformers/tree/main/benchmarks)\n\n## Installation\n### With pip\n\nThis repository is tested on Python 3.7+ and TensorFlow 2.7.\n\n#### Recommended prerequistes\n\n```bash\npip install sentencepiece\npip install tensorflow-text >= 2.7.3\npip install tqdm\n```\nInstall ```tensorflow >= 2.7.0 [CPU or GPU]``` as per your machine.\nYou should install tf-transformers in a [virtual environment](https://docs.python.org/3/library/venv.html). If you\'re unfamiliar with Python virtual environments, check out the [user guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).\n\nFirst, create a virtual environment with the version of Python you\'re going to use and activate it.\n\nThen, you will need to install at least one of TensorFlow.\nPlease refer to [TensorFlow installation page](https://www.tensorflow.org/install/), installation pages regarding the specific install command for your platform. We highly recommend to install [tensorflow-text]\n(https://www.tensorflow.org/text).\n\nWhen one of those backends has been installed, tf-transformers can be installed using pip as follows:\n\n```bash\npip install tf-transformers\n```\n\n### From source\n```bash\ngit clone https://github.com/legacyai/tf-transformers.git\npip install poetry\ncd tf-transformers\npoetry install\n```\n\n## Quick tour\n\ntf-transformers API is very simple and minimalistic.\n\n```python\n>>> from tf_transformers.models import GPT2Model\n>>> model = GPT2Model.from_pretrained(\'gpt2\')\n>>> model.save_checkpoint("/tmp/gpt2_model/") # Save Model\n\n```\nFor text-generation, it is very important to add :obj:`use_auto_regressive=True`. This is required for all the models.\n```python\n\n>>> from tf_transformers.models import GPT2Model\n>>> model = GPT2Model.from_pretrained(\'gpt2\', use_auto_regressive=True)\n```\nTo serialize save and load model\n\n```python\n>>> from tf_transformers.models import GPT2Model\n>>> model = GPT2Model.from_pretrained(\'gpt2\')\n>>> model.save_transformers_serialized("/tmp/gpt2_serialized/")\n\n# To load a serialized models for inference in prodcution:\n\n>>> import tensorflow as tf\n>>> loaded = tf.saved_model.load("/tmp/gpt2_serialized/")\n>>> model  = loaded.signatures[\'serving_default\']\n```\n## Tutorials\n\nWe have covered tutorials covering pre-training, finetuning, classfication, QA, NER so much more.\n\n\n- [Read and Write TFRecords using tft](https://github.com/legacyai/tf-transformers/blob/main/tutorials/1_read_write_tfrecords.ipynb)\n- [Text Classification using Albert](https://github.com/legacyai/tf-transformers/blob/main/tutorials/2_text_classification_imdb_albert.ipynb)\n- [Dynamic MLM (on the fly pre-processing using tf-text) in TPU](https://github.com/legacyai/tf-transformers/blob/main/tutorials/3_masked_lm_tpu.ipynb)\n- [Image Classification ViT multi GPU mirrored](https://github.com/legacyai/tf-transformers/blob/main/tutorials/4_image_classification_vit_multi_gpu.ipynb)\n- [Sentence Embedding train from scratch using Quoara on Roberta + Zeroshot STS-B](https://github.com/legacyai/tf-transformers/blob/main/tutorials/5_sentence_embedding_roberta_quora_zeroshot.ipynb)\n\n## Model usage\n- [Text Generation using GPT2](https://github.com/legacyai/tf-transformers/blob/main/docs/source/model_usage/text_generation_using_gpt2.ipynb)\n- [Text Generation using T5](https://github.com/legacyai/tf-transformers/blob/main/docs/source/model_usage/text_generation_using_t5.ipynb)\n- [Sentence Transformers](https://github.com/legacyai/tf-transformers/blob/main/docs/source/model_usage/sentence_transformers.ipynb)\n## TFlite Tutorials\n- [Albert TFlite](https://github.com/legacyai/tf-transformers/blob/main/docs/source/tflite_tutorials/albert_tflite.ipynb)\n- [Bert TFlite](https://github.com/legacyai/tf-transformers/blob/main/docs/source/tflite_tutorials/bert_tflite.ipynb)\n- [Roberta TFlite](https://github.com/legacyai/tf-transformers/blob/main/docs/source/tflite_tutorials/roberta_tflite.ipynb)\n\n## Why should I use tf-transformers?\n\n1. Use state-of-the-art models in Production, with less than 10 lines of code.\n    - High performance models, better than all official Tensorflow based models\n    - Very simple classes for all downstream tasks\n    - Complete TFlite support for all tasks.\n\n2. Make industry based experience to avaliable to students and community with clear tutorials\n\n3. Train any model on **GPU**, **multi-GPU**, **TPU** with amazing ```tf.keras.Model.fit```\n    - Train state-of-the-art models in few lines of code.\n    - All models are completely serializable.\n\n4. Customize any models or pipelines with minimal or no code change.\n\n## Research\n\nThe [Research](https://github.com/legacyai/tf-transformers/tree/main/research) section has codes\nfor pre-training different models ranging from **MLM, T5, CLIP etc **. All these scripts are designed\nto harness full power of tensorflow-io pipeline and tested on TPU V2 and TPU V3. Bugs are expected in\nthose, but it serves as a purpose for practioners to start or modifying what we have already done.\n\n## Contributions\n\n### **Joint Albert** *(Smallest and best Transformer based model ever) on GLUE*.\nWe have conducted few experiments to squeeze the power of **Albert base** models ( concept is applicable to any models and in tf-transformers, it is out of the box.)\n\nThe idea is minimize the loss for specified task in each layer of your model and check predictions at each layer. as per our experiments, we are able to get the best smaller model (thanks to **Albert**), and from **layer 4** onwards we beat all the smaller model in **GLUE** benchmark. By **layer 6**, we got a **GLUE** score of **81.0**, which is **4** points ahead of **Distillbert** with GLUE score of **77** and **MobileBert** GLUE score of **78**.\n\nThe **Albert** model has **14 million** parameters, and by using **layer 6**, we were able to speed up the compuation by 50% .\n\nThe concept is applicable to all the models and tasks.\n\n[Codes + Read More](https://legacyai.github.io/tf-transformers/build/html/research/glue.html)\n\n### **Long Block Sequence Transformer**\nBy splitting input sequence into block attention and merge using FFN layer we have shown that, smaller machines will be able to perform sequence processing up to 4096 tokens in a single V100 GPU machine.\nThe model has outperforms ```Pegasus Base (128 million)``` in ```PubMed``` summarisation despite being ```60 million``` parameter.\n\n<p align="centre">\n    <br>\n    <img src="docs/source/imgs/long_block_sequencer.gif" width="900"/>\n    <br>\n<p>\n\n[Codes + Read More](https://legacyai.github.io/tf-transformers/build/html/research/long_block_sequencer.html)\n\n## Supported Models architectures\n\ntf-transformers currently provides the following architectures .\n1. **[ALBERT](https://huggingface.co/transformers/model_doc/albert.html)** (from Google Research and the Toyota Technological Institute at Chicago) released with the paper [ALBERT: A Lite BERT for Self-supervised Learning of Language Representations](https://arxiv.org/abs/1909.11942), by Zhenzhong Lan, Mingda Chen, Sebastian Goodman, Kevin Gimpel, Piyush Sharma, Radu Soricut.\n2. **[BERT](https://huggingface.co/transformers/model_doc/bert.html)** (from Google) released with the paper [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805) by Jacob Devlin, Ming-Wei Chang, Kenton Lee and Kristina Toutanova.\n3. **[BERT For Sequence Generation](https://huggingface.co/transformers/model_doc/bertgeneration.html)** (from Google) released with the paper [Leveraging Pre-trained Checkpoints for Sequence Generation Tasks](https://arxiv.org/abs/1907.12461) by Sascha Rothe, Shashi Narayan, Aliaksei Severyn.\n4. **[ELECTRA](https://huggingface.co/transformers/model_doc/electra.html)** (from Google Research/Stanford University) released with the paper [ELECTRA: Pre-training text encoders as discriminators rather than generators](https://arxiv.org/abs/2003.10555) by Kevin Clark, Minh-Thang Luong, Quoc V. Le, Christopher D. Manning.\n5. **[GPT-2](https://huggingface.co/transformers/model_doc/gpt2.html)** (from OpenAI) released with the paper [Language Models are Unsupervised Multitask Learners](https://blog.openai.com/better-language-models/) by Alec Radford*, Jeffrey Wu*, Rewon Child, David Luan, Dario Amodei** and Ilya Sutskever**.\n6. **[MT5](https://huggingface.co/transformers/model_doc/mt5.html)** (from Google AI) released with the paper [mT5: A massively multilingual pre-trained text-to-text transformer](https://arxiv.org/abs/2010.11934) by Linting Xue, Noah Constant, Adam Roberts, Mihir Kale, Rami Al-Rfou, Aditya Siddhant, Aditya Barua, Colin Raffel.\n7. **[RoBERTa](https://huggingface.co/transformers/model_doc/roberta.html)** (from Facebook), released together with the paper a [Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692) by Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, Veselin Stoyanov.\n8. **[T5](https://huggingface.co/transformers/model_doc/t5.html)** (from Google AI) released with the paper [Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683) by Colin Raffel and Noam Shazeer and Adam Roberts and Katherine Lee and Sharan Narang and Michael Matena and Yanqi Zhou and Wei Li and Peter J. Liu.\n9. **[Vision Transformer (ViT)](https://huggingface.co/docs/transformers/model_doc/vit)** (from Google AI) released with the paper [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929) by Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, Neil Houlsby.\n10 **[CLIP](https://huggingface.co/docs/transformers/model_doc/clip)** (from OpenAI) released with the paper [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020) by Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, Ilya Sutskever.\n\n## Citation\n\nWe now have a [page](https://legacyai.github.io/tf-transformers/build/html/index.html) you can cite for the tf-transformers library.\n',
    'author': 'Sarath R Nair',
    'author_email': 's4sarath@gmail.com',
    'maintainer': 'Sarath R Nair',
    'maintainer_email': 's4sarath@gmail.com',
    'url': '',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
