# Goal

Train models that can determine whether artworks are ascribable Leonardo Da Vinci (DV). Specifically, train an encoder to represent features from a variety of pieces, and then fine-tune a head to distinguish between DV and non-DV works.

# Motivation

I am a big fan of Isaacson biographies, having read Steve Jobs and half of Einstein and DV Currently I'm roughing it through DV as it is very dense but educational nonetheless. I find it fascinating that a couple works were attributed to DV several hundred years posthumously due to improper initial examination, leading to increbile arbitrage opportunities for those with proper discernment. The most prominent examples are `Salvatore Mundi` and `La Bella Principessa`.

Because I work in machine learning, I thought to leverage my skills and computer assistance to the task of attributing or disattributing artworks to the legendary DV, and later, to represent art works so finely that they can be attributed to various authors with statistical significance.

# Methods: Data Collection

##### 1. Pool general collection of artworks to train an encoder

Encoders can represent images as unique tensors, capturing the `features` or nuances that make each one unique. High encoder quality will allow for features imperceptible to the human eye to be captured and used for predictions. To train a powerful encoder, as diverse and high quality a dataset (does not mean a dataset without noise) needs to be curated.

Thankfully, there are plenty of images in the public domain to begin our training, and we can enrich our collection later on with more images if needed. Specifically, the MET Museum has `open sourced` ~448k images through a Kaggle challenge (https://www.kaggle.com/datasets/metmuseum/the-metropolitan-museum-of-art-open-access).

##### 2. Pool collection of DV artworks to learn features specific to his style

Because the MET Museum collection does not have any DV pieces, it is necessary to enrich our data with his works so (1) the encoder can learn DV features along with those from many other works and (2) we can fine-tune a head to distinguish DV works from non-DV works. We are using all 331 pieces from: schttps://leonardoda-vinci.org.

##### 3. Mix Da Vinci works into the MET collection so encoder learns DV

Because the MET collection does not have any DV pieces, we will add in the 331 images to the MET collection

# Methods: Experiments

Tests of increasing size will be performed to determine efficacy and estimate costs. Earlier tests will be run on my local computer (M2 MacBook Air) with 500GB disk space and 16GB RAM. Once methods are validated, later experiments will be run on RunPod servers with powerful GPUs.

1. Use rudimentary methods from https://course.fast.ai/ to do image classification
2. Train an encoder using 20 DV and 20 MET works. Use embeddings to train the head to distinguish DV works
