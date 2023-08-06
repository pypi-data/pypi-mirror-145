#!/usr/bin/env python
# coding: utf-8

# # VAE for the CelebA dataset
#
# > In this post, we will implement the variational AutoEncoder (VAE) for an image dataset of celebrity faces. This is the Programming Assignment of lecture "Probabilistic Deep Learning with Tensorflow 2" from Imperial College London.
#
# - toc: true
# - badges: true
# - comments: true
# - author: Chanseok Kang
# - categories: [Python, Coursera, Tensorflow_probability, ICL]
# - image: images/celeba-reconstruct.png

# ## Packages


from tensorflow.keras.layers import Conv2D, BatchNormalization, Flatten, Dense, UpSampling2D, Reshape
from tensorflow.keras.models import Model, Sequential
import tensorflow as tf
import tensorflow_probability as tfp

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# custom import
from .utils import *

tfd = tfp.distributions
tfpl = tfp.layers
tfb = tfp.bijectors

plt.rcParams['figure.figsize'] = (10, 6)


# ## Mixture of Gaussians distribution
#
# We will define a prior distribution that is a mixture of Gaussians. This is a more flexible distribution that is comprised of $K$ separate Gaussians, that are combined together with some weighting assigned to each.
#
# Recall that the probability density function for a multivariate Gaussian distribution with mean $\mu\in\mathbb{R}^D$ and covariance matrix $\Sigma\in\mathbb{R}^{D\times D}$ is given by
#
# $$
# \mathcal{N}(\mathbf{z}; \mathbf{\mu}, \Sigma) = \frac{1}{(2\pi)^{D/2}|\Sigma|^{1/2}}
# \exp\left(-\frac{1}{2}(\mathbf{z}-\mathbf{\mu})^T\Sigma^{-1}(\mathbf{z}-\mathbf{\mu})\right).
# $$
#
# A mixture of Gaussians with $K$ components defines $K$ Gaussians defined by means $\mathbf{\mu}_k$ and covariance matrices $\Sigma_k$, for $k=1,\ldots,K$. It also requires mixing coefficients $\pi_k$, $k=1,\ldots,K$ with $\sum_{k} \pi_k = 1$. These coefficients define a categorical distribution over the $K$ Gaussian components. To sample an event, we first sample from the categorical distribution, and then again from the corresponding Gaussian component.
#
# The probability density function of the mixture of Gaussians is simply the weighted sum of probability density functions for each Gaussian component:
#
# $$
# p(\mathbf{z}) = \sum_{k=1}^K \pi_k \mathcal{N}(\mathbf{z}; \mathbf{\mu}_k, \Sigma_k)
# $$

# ## Define the prior distribution
#
# We will define the mixture of Gaussians distribution for the prior, for a given number of components and latent space dimension. Each Gaussian component will have a diagonal covariance matrix. This distribution will have fixed mixing coefficients, but trainable means and standard deviations.


def get_prior(num_modes, latent_dim):
    """
    Creates a mixture of gaussian distribution.


    Args:
        num_modes (int): 
        latent_dim (int): latent dimension we want to encode the image in

    Returns:
        tfp.distributions.MixtureSameFamily : Mixture of gaussian distribution, with variable means and 
        standart deviations
    """
    prior = tfd.MixtureSameFamily(
        # The mixture distribution is a list of probability for the distributions. Here it is set to be
        # all equal
        mixture_distribution=tfd.Categorical(
            probs=[1 / num_modes, ] * num_modes),
        # The components distribution is made of two lists : loc represents the mean of the distribution,
        # or the "location" of the distribution.
        # scale_diag represents the
        components_distribution=tfd.MultivariateNormalDiag(
            loc=tf.Variable(tf.random.normal(shape=[num_modes, latent_dim])),
            scale_diag=tfp.util.TransformedVariable(tf.Variable(
                tf.ones(shape=[num_modes, latent_dim])), bijector=tfb.Softplus())
        )
    )
    return prior


# Define the encoder Network
#
# We will now define the encoder network as part of the VAE. First, we will define the `KLDivergenceRegularizer` to use in the encoder network to add the KL divergence part of the loss.


def get_kl_regularizer(prior_distribution):
    """The kl regularizer is a part of the loss function. It takes the prior distribution as an
    input will be used as the activity_regularizer of the tfpl.MultivariateNormalTriL layer of the encoder.

    Args:
        prior_distribution (tfp.distributions.MixtureSameFamily): 

    Returns:
        tensorflow_probability.python.layers.distribution_layer.KLDivergenceRegularizer :
    """
    divergence_regularizer = tfpl.KLDivergenceRegularizer(
        prior_distribution,
        use_exact_kl=False,
        weight=1.0,
        test_points_fn=lambda q: q.sample(3),
        test_points_reduce_axis=(0, 1)
    )
    return divergence_regularizer


def get_encoder(latent_dim, kl_regularizer):
    """generates an encoder with a given latent dimension and a kl regularizer

    Args:
        latent_dim (int): dimension of the latent space we want to encode the image to
        kl_regularizer (tensorflow_probability.python.layers.distribution_layer.KLDivergenceRegularizer): kl regularizer

    Returns:
        keras.engine.sequential.Sequential : encoder with all the layers we want
    """
    encoder = Sequential([
        Conv2D(32, (4, 4), activation='relu', strides=2,
               padding='SAME', input_shape=(64, 64, 3)),
        BatchNormalization(),
        Conv2D(64, (4, 4), activation='relu', strides=2, padding='SAME'),
        BatchNormalization(),
        Conv2D(128, (4, 4), activation='relu', strides=2, padding='SAME'),
        BatchNormalization(),
        Conv2D(256, (4, 4), activation='relu', strides=2, padding='SAME'),
        BatchNormalization(),
        Flatten(),
        Dense(tfpl.MultivariateNormalTriL.params_size(latent_dim)),
        tfpl.MultivariateNormalTriL(
            latent_dim, activity_regularizer=kl_regularizer)
    ])
    return encoder


# ## Define the decoder network
#
# We'll define the decoder network for the VAE, which return IndependentBernoulli
# distribution of `event_shape=(64, 64, 3)`

def get_decoder(latent_dim):
    """generates the decoder of the vae, with a given latent dimension

    Args:
        latent_dim (int): latent dimension the image is encoded into

    Returns:
        keras.engine.sequential.Sequential: decoder of the vae model
    """
    decoder = Sequential([
        Dense(4096, activation='relu', input_shape=(latent_dim, )),
        Reshape((4, 4, 256)),
        UpSampling2D(size=(2, 2)),
        Conv2D(128, (3, 3), activation='relu', padding='SAME'),
        UpSampling2D(size=(2, 2)),
        Conv2D(64, (3, 3), activation='relu', padding='SAME'),
        UpSampling2D(size=(2, 2)),
        Conv2D(32, (3, 3), activation='relu', padding='SAME'),
        UpSampling2D(size=(2, 2)),
        Conv2D(128, (3, 3), activation='relu', padding='SAME'),
        Conv2D(3, (3, 3), padding='SAME'),
        Flatten(),
        tfpl.IndependentBernoulli(event_shape=(64, 64, 3))
    ])
    return decoder


# #### Define the average reconstruction loss
#
# You should now define the reconstruction loss that forms the remaining part of the negative ELBO objective. This function should take a batch of images of shape `(batch_size, 64, 64, 3)` in the first argument, and the output of the decoder after passing the batch of images through `vae` in the second argument.
#
# The loss should be defined so that it returns
# $$
#     -\frac{1}{n}\sum_{i=1}^n \log p(x_i|z_i)
# $$
# where $n$ is the batch size and $z_i$ is sampled from $q(z|x_i)$, the encoding distribution a.k.a. the approximate posterior. The value of this expression is always a scalar.
#
# Expression (1) is, as you know, is an estimate of the (negative of the) batch's average expected reconstruction loss:
#
# $$
#     -\frac{1}{n}\sum_{i=1}^n \mathrm{E}_{Z\sim q(z|x_i)}\big[\log p(x_i|Z)\big]
# $$


def reconstruction_loss(batch_of_images, decoding_dist):
    """
    The function takes batch_of_images (Tensor containing a batch of input images to
    the encoder) and decoding_dist (output distribution of decoder after passing the 
    image batch through the encoder and decoder) as arguments.
    The function should return the scalar average expected reconstruction loss.

    Returns:
        tf.Tensor : scalar average expected reconstruction loss
    """
    return -tf.reduce_mean(decoding_dist.log_prob(batch_of_images), axis=0)


# ## Compute reconstructions of test images
#
# We will now take a look at some image reconstructions from the encoder-decoder architecture.
#
# You should complete the following function, that uses `encoder` and `decoder` to reconstruct images from the test dataset. This function takes the encoder, decoder and a Tensor batch of test images as arguments. The function should be completed according to the following specification:
#
# * Get the mean of the encoding distributions from passing the batch of images into the encoder
# * Pass these latent vectors through the decoder to get the output distribution
#
# Your function should then return the mean of the output distribution, which will be a Tensor of shape `(batch_size, 64, 64, 3)`.


def reconstruct(encoder, decoder, batch_of_images):
    """
    The function takes the encoder, decoder and batch_of_images as inputs, which
    should be used to compute the reconstructions.
    The function should then return the reconstructions Tensor.

    Args:
        encoder (Sequential): encoder of the model
        decoder (Sequential): decoder of the model
        batch_of_images (ndarray): list of images we want to reconstruct

    Returns:
        tf.Tensor : reconstruction tensor
    """
    approx_posterior = encoder(batch_of_images)
    decoding_dist = decoder(approx_posterior.mean())
    return decoding_dist.mean()


def plot_reconstructions_test_ds(encoder, decoder):
    """
    plots the reconstruction of the images versus the initial images

    Args:
        encoder (Sequential): encoder of the vae
        decoder (Sequential): decoder of the vae
    """
    n_reconstructions = 7
    num_test_files = np.load('./img_align_celeba/dataset_test.npy').shape[0]
    test_ds_for_reconstructions = load_dataset('dataset_test')
    # Run your function to compute reconstructions of random samples from the test dataset
    for all_test_images, _ in test_ds_for_reconstructions.batch(num_test_files).take(1):
        all_test_images_np = all_test_images.numpy()
    example_images = all_test_images_np[np.random.choice(
        num_test_files, n_reconstructions, replace=False)]

    reconstructions = reconstruct(encoder, decoder, example_images).numpy()

    # Plot the reconstructions

    f, axs = plt.subplots(2, n_reconstructions, figsize=(16, 6))
    axs[0, n_reconstructions // 2].set_title("Original test images")
    axs[1, n_reconstructions // 2].set_title("Reconstructed images")
    for j in range(n_reconstructions):
        axs[0, j].imshow(example_images[j])
        axs[1, j].imshow(reconstructions[j])
        axs[0, j].axis('off')
        axs[1, j].axis('off')

    plt.tight_layout()
    plt.show()

    return None


# ## Sample new images from the generative model
#
# Now we will sample from the generative model; that is, first sample latent vectors from the prior, and then decode those latent vectors with the decoder.
#
# You should complete the following function to generate new images. This function takes the prior distribution and decoder network as arguments, as well as the number of samples to generate. This function should be completed according to the following:
#
# * Sample a batch of `n_samples` images from the prior distribution, to obtain a latent vector Tensor of shape `(n_samples, 50)`
# * Pass this batch of latent vectors through the decoder, to obtain an Independent Bernoulli distribution with batch shape equal to `[n_samples]` and event shape equal to `[64, 64, 3]`.
#
# The function should then return the mean of the Bernoulli distribution, which will be a Tensor of shape `(n_samples, 64, 64, 3)`.


def generate_images(prior, decoder, n_samples):
    """
    The function takes the prior distribution, decoder and number of samples as inputs, which
    should be used to generate the images.
    The function should then return the batch of generated images.

    Args:
        prior (MixtureSameFamily): prior distribution
        decoder (Sequential): trained decoder of the vae
        n_samples (int): targeted number of samples

    Returns:
        tf.Tensor : images generated
    """
    z = prior.sample(n_samples)
    sampled_images = decoder(z).mean()
    for count, value in enumerate(sampled_images):
        image = Image.fromarray((value.numpy()*255).astype('uint8'), 'RGB')
        image.save('gen'+str(count)+'.png')
    return sampled_images


def generate_latent_vectors(prior, n_samples):
    ''''''
    Z = prior.sample(n_samples)
    Z2 = Z.numpy()
    '''if n_samples == 1:
        Z3 = []
        for element in Z2[0]:
            Z3.append(element)
        Z2 = np.array(Z3)'''
    return Z2


def reconstruct_image_from_latent_vectors(decoder, Z):
    ''''''
    return decoder(Z).mean()


def plot_recontructed_images(X):
    ''''''
    n_samples = len(X)
    f, axs = plt.subplots(1, n_samples, figsize=(16, 6))
    if n_samples == 1:
        plt.imshow(X[0])
    else:
        for j in range(n_samples):
            axs[j].imshow(X[j])
            axs[j].axis('off')
    plt.show()


# Run your function to generate new images

def plot_generate_images(prior, decoder):
    n_samples = 10
    sampled_images = generate_images(prior, decoder, n_samples)

    f, axs = plt.subplots(1, n_samples, figsize=(16, 6))

    for j in range(n_samples):
        axs[j].imshow(sampled_images[j])
        axs[j].axis('off')

    plt.tight_layout()
    plt.show()
    plt.savefig('image_generation.png')

# ## Modify generations with attribute vector
#
# We will see how the latent space encodes high-level information about the images, even though it has not been trained with any information apart from the images themselves.
#
# As mentioned in the introduction, each image in the CelebA dataset is labelled according to the attributes of the person pictured.


# Function to load labels and images as a numpy array

def load_labels_and_image_arrays(split):
    dataset = load_dataset(split)
    num_files = np.load('./img_align_celeba/{}.npy'.format(split)).shape[0]

    for all_images, _ in dataset.batch(num_files).take(1):
        all_images_np = all_images.numpy()

    labels = pd.read_csv(
        './img_align_celeba/list_attr_celeba.txt', delimiter=r"\s+", header=1)
    #labels = labels[labels['image_id'].isin(files)]
    return labels[:num_files], all_images_np


def train(vae, train_ds, val_ds, epochs):
    vae.fit(train_ds, validation_data=val_ds, epochs=epochs)
    return None

##========================= MAIN =======================##


if __name__ == "__main__":
    print("Tensorflow Version: ", tf.__version__)
    print("Tensorflow Probability Version: ", tfp.__version__)

    #train_ds, val_ds, test_ds = load_datasets()

    # Run your function to get the prior distribution with 2 components and latent_dim = 50
    prior = get_prior(num_modes=2, latent_dim=50)

    # Run your function to get the encoder
    encoder = get_encoder(
        latent_dim=50, kl_regularizer=get_kl_regularizer(prior))

    # Run your function to get the decoder
    decoder = get_decoder(latent_dim=50)

    # ## Link the encoder and decoder together
    #
    # Connects `encoder` and `decoder` to form the end-to-end architecture.
    vae = Model(inputs=encoder.inputs, outputs=decoder(encoder.outputs))

    # ## Compile and fit the model
    #
    # It's now time to compile and train the model. Note that, it is recommand to use Hardware accelerator while training.

    # Compile the model
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0005)
    vae.compile(optimizer=optimizer, loss=reconstruction_loss)

    # Train the model
    #vae.fit(train_ds, validation_data=val_ds, epochs=1)
    # Or just load the weights
    encoder.load_weights("./model_vae/encoder/saved_encoder")
    decoder.load_weights("./model_vae/decoder/saved_decoder")

    #vae.fit(train_ds, validation_data=val_ds, epochs=1)

    # encoder.save_weights("./model_vae/encoder/saved_encoder")
    # decoder.save_weights("./model_vae/decoder/saved_decoder")

    # Evaluate the model on the test set
    #test_loss = vae.evaluate(test_ds)
    #print("Test loss: {}".format(test_loss))

    #plot_reconstructions_test_ds(encoder, decoder)

    plot_generate_images(prior, decoder)
