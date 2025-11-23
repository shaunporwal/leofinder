# Goal

Train models that can determine whether artworks are ascribable Leonardo Da Vinci. Specifically, train an encoder to represent features from a variety of pieces, and then fine-tune a head to distinguish between Da Vinci and non-Da Vinci works.

# Motivation

I am a big fan of Isaacson biographies, having read Steve Jobs and half of Einstein and Da Vinci. Currently I'm roughing it through Da Vinci as it is very dense but educational nonetheless. I find it fascinating that a couple works were attributed to Da Vinci several hundred years posthumously due to improper initial examination, leading to increbile arbitrage opportunities for those with proper discernment. The most prominent examples are `Salvatore Mundi` and `La Bella Principessa`.

Because I work in machine learning, I thought to leverage my skills and computer assistance to the task of attributing or disattributing artworks to the legendary Da Vinci, and later, to represent art works so finely that they can be attributed to various authors with statistical significance.

# Data Collection Methods

##### Pool general collection of artworks to train an encoder

Encoders can represent images as unique tensors, capturing the `features` or nuances that make each one unique. High encoder quality will allow for features imperceptible to the human eye to be captured and used for predictions. To train a powerful encoder, as diverse and high quality a dataset (does not mean a dataset without noise) needs to be curated.

Thankfully, there are plenty of images in the public domain to begin our training, and we can enrich our collection later on with more images if needed. Specifically, the MET Museum has `open sourced` ~448k images through a Kaggle challenge (https://www.kaggle.com/datasets/metmuseum/the-metropolitan-museum-of-art-open-access).

##### Pool collection of Da Vinci artworks to learn features specific to his style

Because the MET Museum collection does not have any Da Vinci pieces, it is necessary to enrich our data with his works so (1) the encoder can learn Da Vinci features along with those from many other works and (2) we can fine-tune a head to distinguish Da Vinci works from non-Da Vinci works. We are using all 331 pieces from: schttps://leonardoda-vinci.org.
