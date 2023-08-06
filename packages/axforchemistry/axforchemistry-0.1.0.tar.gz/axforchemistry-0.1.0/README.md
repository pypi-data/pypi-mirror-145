# Adaptive Experimentation (Ax) Platform for Chemistry

AxForChemistry is an unofficial wrapper for the [Ax platform](ax.dev) geared towards materials
science/[materials informatics](https://citrine.io/what-is-materials-informatics/) and chemistry/[cheminformatics](https://en.wikipedia.org/wiki/Cheminformatics) optimization tasks where the datasets are often characterized as:

<p align="center"><i>small</i>, <i>sparse</i>, <i>noisy</i>, <i>multiscale</i>, <i>heterogeneous</i>, <i>high-dimensional</i> <sup><a href=https://dx.doi.org/10.1021/acs.chemmater.9b04078>1</a></sup>,<br><i>nonlinearly correlated</i>, <i>discontinuous</i>, and <i>nonlinearly constrained</i></p>

The goal of this codebase is to expose state-of-the-art Bayesian optimization techniques to the materials informatics and cheminformatics communities for both experts and non-experts with minimal barriers to usage/modification while retaining advanced features. This is done through classes and scripts primarily based on real experimental and computational research within the [Sparks group](https://my.eng.utah.edu/~sparks/) across a range of subjects in both industry and academia. While we are not affiliated with Ax, [Ax developers have contributed extensively to development and troubleshooting](https://github.com/facebook/Ax/issues?q=is%3Aissue+is%3Aopen+commenter%3Asgbaird) that led to this codebase.

## Why another materials adaptive design platform?
There are many existing domain- and non-domain-specific adaptive design packages. A nonexhaustive list of materials discovery resources is given as follows:
- [Open Citrine Platform](https://citrination.com/search/simple) by [Citrine Informatics](https://citrine.io/) ([learn-citrination](https://github.com/CitrineInformatics/learn-citrination))
- [Computational Autonomy for Materials Discovery (CAMD)](https://github.com/TRI-AMDD/CAMD)
- [Sequential Learning App for Materials Discovery (SLAMD)](https://github.com/BAMresearch/SequentialLearningApp)
- [Chemically Novel Materials Discovery via `mat_discover`](https://github.com/sparks-baird/mat_discover)
- [Co-Optimization of Composition in CrabNet (CoCoCrab)](https://github.com/AndrewFalkowski/CoCoCrab)

A nonexhaustive list of general optimization resources is given as follows:
- [Adaptive Experimentation (Ax) Platform](ax.dev)
- [Dragonfly: scalable Bayesian optimization](https://github.com/dragonfly/dragonfly)
- [IBM Bayesian Optimization Accelerator](https://www.ibm.com/products/bayesian-optimization-accelerator)
- [Google Vizier: A Service for Black-Box Optimization](https://cloud.google.com/ai-platform/optimizer/docs/overview) ([open-source implementation](https://github.com/tobegit3hub/advisor)) <!-- ([paper](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/46180.pdf)) -->
- [Modular Active Learning framework (ModAL)](https://github.com/modAL-python/modAL)
- [Rocketsled: a black-box optimization framework "on rails" for high-throughput computation](https://github.com/hackingmaterials/rocketsled)
- [COMmon Bayesian Optimization Library for Python 3 (COMBO3)](https://github.com/tsudalab/combo3)
- [Gryffin for categorical variables and mixed categorical-continuous parameter domains](https://github.com/aspuru-guzik-group/gryffin)

[RayTune](https://docs.ray.io/en/latest/tune/index.html), while geared primarily towards hyperparameter optimization, supports a [wide variety of search algorithms](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html) including Ax and Dragonfly. We recommend looking through the descriptions to see which ones stand out to you.

So, why another platform? The answer lies in the features of the Adaptive Experimentation (Ax) platform. It is relatively easy-to-use, modular, well-documented, open-source, actively maintained and expanding, and importantly, contains state-of-the-art models for a wide variety of tasks. For example, Ax supports noisy, high-dimensional, multi-objective, nonlinearly constrained optimization.. all at once! However, simultaneously implementing these features for a single materials design problem is non-trivial; this is the motivation for our implementation, **AxForChemistry**. As mentioned before, our goal is to:

> expose state-of-the-art Bayesian optimization techniques to the materials informatics and cheminformatics communities for both experts and non-experts with minimal barriers to usage/modification while retaining advanced features.

## What are AxForChemistry's use-cases?

Inline with the course of development for this codebase, perhaps the best way to introduce its features is by describing the materials informatics tasks that brought it about. Each of the following tasks links to a tutorial. We encourage you to focus on the tutorials most relevant to your priorities. As an outline:

- Neural Network Hyperparameter Optimization (`crabnet_hyperopt.ipynb`, Colab)
- Industry: Multi-objective Optimization of Dental Resin Formulations (`dental_bayesopt.ipynb`, Colab)
- ARPA-E: High-temperature Multi-Principal Element Alloy (MPEA) discovery using domain knowledge and predefined candidates (`mpea_predefined.ipynb`, Colab)
- Industry: Maximize packing fraction for solid rocket fuel particle packing simulations under compositional constraints (`particle_packing.ipynb`, Colab)
- CrabNet as a pseudo-materials discovery benchmark problem with fake compositional constraints (`pseudo_discovery_validation.ipynb`, Colab)
- Experimental validation of materials discovery via Open Citrine Platform, DiSCoVeR, and AxForChemistry (`expt_validation_comparison.ipynb`, Colab)
- Vickers Hardness adaptive design - let's consult the literature, again and again (`hardness_literature.ipynb`, Colab)
- Sparse, multi-objective, heterogeneous, heteroskedastic, multi-fidelity Bayesian optimization (`sparse_moo.ipynb`, Colab)
- Optimizing in a latent space: discovering high-performing crystal structures using VAEs (`crystal_bayesopt_vae.ipynb`, Colab)

### Neural Network Hyperparameter Optimization

Let's begin with the first publication related to this work, a high-dimensional hyperparameter optimization study of 23 neural network hyperparameters, including both numerical and categorical parameters. We used a recently introduced high-dimensional Bayesian optimization scheme within the Ax platform called Sparse Axis-Aligned Subspaces Bayesian Optimization ([SAASBO](https://ax.dev/tutorials/saasbo.html)) to set a new state-of-the-art benchmark on a Matbench task ([`matbench_expt_gap`](https://matbench.materialsproject.org/Leaderboards%20Per-Task/matbench_v0.1_matbench_expt_gap/)) with no prior knowledge other than (generous) bounds on the search space. See the [submission](https://matbench.materialsproject.org/Full%20Benchmark%20Data/matbench_v0.1_Ax_SAASBO_CrabNet_v1.2.7/), [notebook](https://github.com/materialsproject/matbench/blob/main/benchmarks/matbench_v0.1_Ax_SAASBO_CrabNet_v1.2.7/notebook.ipynb), and [paper](https://doi.org/10.48550/arXiv.2203.12597) for additional details.

> Baird, S. G.; Liu, M.; Sparks, T. D. High-Dimensional Bayesian Optimization of Hyperparameters for an Attention-Based Network to Predict Materials Property: A Case Study on CrabNet Using Ax and SAASBO. [arXiv:2203.12597](https://doi.org/10.48550/arXiv.2203.12597) [cond-mat] 2022.

### Multi-objective Optimization of Dental Resin Formulations (Industry)
Dental resins are made up of monomer resins, fillers, dyes, and inhibitors.

#### Monomer optimization, without `max_components` constraint
We fix filler, dye, and inhibitor contributions and optimize over 16 distinct monomers in a continuous sense.

#### Monomer optimization, with `max_components` constraint
We apply the same optimization, except with the constraint that suggested candidates may contain no more than `n` components out of `k` monomers. This reframes the problem as an nchoosek problem where each of the `k` parameters is a continuous variable.

#### Multiple compositional constraints
Each of the categories (resins, fillers, dyes, and inhibitors) can be restricted to total contribution ranges as well as maximum allowable number of components. For example, we can restrict the total resin contribution to 15-30% and the total filler contribution to 50-70% while also constraining the total contribution of all components to 100%.

### High-temperature Multi-Principal Element Alloy (MPEA) discovery using domain knowledge and predefined candidates (ARPA-E)
Discovering new, high-temperature multi-principal element alloys can help unlock a new generation of efficient turbine engines. We limit the search to a max of `n` elements out of `k` possible elements (nchoosek) where the individual component contributions vary continuously from 0 to 1.

### Maximize packing fraction for solid rocket fuel particle packing simulations under compositional constraints (Industry)
Particle packing fraction of solid rocket fuel affects the combustion process through properties such as density, reactivity, surface area, and mechanical properties.

#### Concurrent optimization for a large, initial training set (15000)
To reduce memory consumption, an exact (as opposed to noisy) acquisition function is applied during the search for candidates with high packing fractions. [RayTune's integrations with Ax](https://ax.dev/tutorials/raytune_pytorch_cnn.html) are used to perform task scheduling. Out of a pool of CPUs, as soon as one CPU becomes inactive, it is assigned a new task based on all available data (including recently generated data). This maximization of resource efficiency is especially important since simulation times can range from 20 min to over 20 hours. A CPU that completes a 20 minute simulation can run additional, adaptively suggested tasks while another CPU continues to run a 20 hour simulation.

#### SAASBO, training from scratch
We test the performance of SAASBO on the particle packing simulations by hiding all training data, allowing SAASBO to search from scratch (SAASBO is limited to small datasets).

#### Multi-fidelity
Dragonfly is used to perform multi-fidelity optimization of the particle packing simulations. Multi-fidelity in this context refers to the fact that simulation results tend to converge when a larger number of particles is used (slow, high-fidelity) and tends to have more noise when a smaller number of particles is used (fast, low-fidelity). Dragonfly interprets number of particles as the fidelity parameter and seeks to maximize search efficiency by leveraging both (fast) low-fidelity and (slow) high-fidelity simulations running concurrently.

### Maximize (qualitative) coating quality of metal coated polymers (Industry)
Electroless deposition of metals on polymers requires careful recipe generation to produce adhesive, uniform coatings. Researchers assign qualitative rankings of the coatings as the optimization objective.

### CrabNet as a pseudo-materials discovery benchmark problem with fake compositional constraints
Here, we compare Ax models to other state-of-the-art techniques on a fake materials discovery validation problem.

### Experimental validation of materials discovery via Open Citrine Platform, DiSCoVeR, and AxForChemistry

### Vickers Hardness adaptive design - let's consult the literature, again and again
Rather than immediately venture to the laboratory upon obtaining suggested candidates, we implement a loop where we consult the literature for the top `k` suggested compounds and update the model/suggestions until `n` of the `k` compounds do not contain data within the literature.

### Sparse, multi-objective, heterogeneous, heteroskedastic, multi-fidelity Bayesian optimization
Not implemented yet. How to deal with sparsity in the Ax framework? (open an issue).

### Optimizing in a latent space: discovering high-performing crystal structures using VAEs
Not implemented yet. Consider using https://github.com/PV-Lab/FTCP.

<!-- _nonlinear correlations_ between variables, _discontinuity_ in the feature spaces, and nonlinear constraints_. -->

<!-- - small
- sparse
- noisy
- multiscale
- heterogeneous
- high-dimensional
 -->
<!-- <table>
<tbody>
  <tr>
    <td><li>small</li></td>
    <td>multiscale</td>
  </tr>
  <tr>
    <td>sparse</td>
    <td>heterogeneous</td>
  </tr>
  <tr>
    <td>noisy</td>
    <td>high-dimensional</td>
  </tr>
</tbody>
</table> -->
