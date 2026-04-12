---
layout: default
title: Harmonic Potential Energy
kicker: Bonus Material
lead: Additional notes on harmonic oscillators and the relationship between force and potential energy.
description: Harmonic potential energy notes.
permalink: /harmonic-potential-energy/
---
## Harmonic Oscillator

Consider a two-particle system moving in 1D. Let $r_1,r_2$ and $r_1^0,r_2^0$ the positions of the two particles be $r_1$ and $r_2$. So in this page, we define:

- $\Delta r=r_2-r_1$ is the instantaneous distance between the two particles
- $\Delta r^0=r_2^0-r_1^0$ is the equilibrium distance between the two particles
- $\Delta r - \Delta r^0$ is the displacement from equilibrium

If the particles are displaced only slightly from $\Delta r^0$, the interaction tends to pull the system back toward equilibrium. This kind of back-and-forth motion is called **harmonic motion**, and the corresponding model is the **harmonic oscillator**.

A two-particle system is in equilibrium when the net force on the relative coordinate vanishes. For a conservative force,

$$
F(\Delta r) = -\frac{dV}{d(\Delta r)} \tag{1}

$$

so at the equilibrium position $\Delta r = \Delta r^0$ we must have

$$
F(\Delta r^0) = -\left.\frac{dV}{d(\Delta r)}\right|_{\Delta r=\Delta r^0} = 0 \tag{2}

$$

This tells us that the potential energy curve is locally flat at equilibrium. In addition, the force depends only on the derivative of $V(\Delta r)$, not on its absolute value. If we replace $V(\Delta r)$ by

$$
\tilde V(\Delta r) = V(\Delta r) + C, \tag{3}

$$

then

$$
-\frac{d\tilde V}{d(\Delta r)} = -\frac{d}{d(\Delta r)}\bigl(V(\Delta r)+C\bigr) = -\frac{dV}{d(\Delta r)} = F(\Delta r). \tag{4}

$$

Therefore, adding a constant does not change the physics. For this reason, we are free to choose the zero of potential energy conveniently, so we set $V(\Delta r^0)=0$.

In general, we do not know the exact form of the potential energy $V(\Delta r)$. However, if we are interested only in small displacements from equilibrium, then we can describe the potential relative to $V(\Delta r^0)=0$ by expanding it in a Maclaurin-Taylor series around the equilibrium distance:

$$
V(\Delta r) = V(\Delta r^0) + (\Delta r-\Delta r^0)V'(\Delta r^0) + \frac{1}{2}(\Delta r-\Delta r^0)^2V''(\Delta r^0) + \cdots , \tag{5}

$$

where the primes denote differentiation with respect to $\Delta r$. Since we chose $V(\Delta r^0)=0$ and also know that $V'(\Delta r^0)=0$, the first two terms vanish. Thus, near the equilibrium distance $\Delta r^0$, we may write

$$
V(\Delta r) \approx \frac{1}{2}(\Delta r-\Delta r^0)^2V''(\Delta r^0) = \frac{1}{2}k(\Delta r-\Delta r^0)^2 \tag{6}

$$

,where $k=V''(\Delta r^0)$ is the curvature of the potential energy at the equilibrium distance, or the spring constant. If we choose the coordinate origin so that the equilibrium distance is at zero, that is, $\Delta r^0=0$, then the harmonic approximation simplifies to

$$
V(\Delta r) \approx \frac{1}{2}k(\Delta r)^2. \tag{7}

$$

In this shifted coordinate system, the displacement from equilibrium is simply $\Delta r$ itself, and the corresponding force becomes

$$
F(\Delta r) = -\frac{dV}{d(\Delta r)} \approx -k\Delta r. \tag{8}

$$

This is the standard form of Hooke's law: the force is proportional to the displacement and points in the opposite direction.

> Reference: Tom W. B. Kibble and Frank H. Berkshire, *Classical Mechanics*, Chapter 2: Linear Motion, Sections 2.1 and 2.2.

## At temperature T, what is the size of fluctuation? (Thermal fluctation)

Let us define the displacement from equilibritum is $x=\Delta r - \Delta r^0 $. Then, we have $V(x) = \frac{1}{2}kx^2$ (harmonic approximation of potential) and $P(x) = \frac{1}{Z} \exp(-\frac{V(x)}{k_B T})$ (Boltzmann distribution), where partition function $Z = \int_{-\infty}^{\infty} \exp(-\frac{kx^2}{2k_B T})\,dx$ and $k_B$ is Boltzmann constant.

The ensemble average of the fluctuation is

$$
\langle x \rangle
=
\int_{-\infty}^{\infty} x\,P(x)\,dx \tag{9}

$$

Because, at equilibrium, we have $\Delta r = \Delta r^0$ or $\langle\Delta r \rangle = \Delta r^0$. To measure the size of the fluctuation, we consider the mean-square fluctuation:

$$
\langle x^2 \rangle
=
\int_{-\infty}^{\infty} x^2 P(x)\,dx = \frac{1}{Z} \int_{-\infty}^{\infty} x^2 e^{-kx^2/(2k_B T)} dx = \frac{1}{Z} \int_{-\infty}^{\infty} x^2 e^{-ax^2} dx  \tag{10}

$$

, where $a = \frac{k}{2k_B T}$. Using the Gaussian integral result ([ref](https://quantummechanics.ucsd.edu/ph130a/130_notes/node87.html)): $\int_{-\infty}^{\infty} x^2 e^{-ax^2} dx = \frac{1}{2a}\sqrt{\frac{\pi}{a}}$, we have

$$
\langle x^2 \rangle = \frac{1}{Z} \cdot \frac{1}{2a}\sqrt{\frac{\pi}{a}}

$$

Now, what is `Z`? The partition function is: $Z = \int_{-\infty}^{\infty} e^{-ax^2} dx = \sqrt{\frac{\pi}{a}}$. Therefore,

$$
\langle x^2 \rangle
= \frac{1}{\sqrt{\pi/a}} \cdot \frac{1}{2a}\sqrt{\frac{\pi}{a}}
= \frac{1}{2a}
= \frac{k_B T}{k}

$$

This is an important result.
It tells us that:

- the mean-square fluctuation increases with temperature
- the mean-square fluctuation decreases when the spring constant becomes larger

So a softer spring gives larger fluctuations, while a stiffer spring gives smaller fluctuations.
This is the physical idea behind why ENMs can connect network stiffness to molecular fluctuations.

## Solution of Harmonic Motion

To solve the motion, combine Newton's second law with the harmonic restoring force:

$$
F = ma = -k\Delta r \Rightarrow m\frac{d^2(\Delta r)}{dt^2} + k\Delta r = 0 \tag{11}

$$

We may view this equation as a [linear differential equation]({{ '/linear-differential-equation/' | relative_url }}) of the general form

$$
a_2(t)\Delta r'' + a_1(t)\Delta r' + a_0(t)\Delta r = b(t) \tag{12}

$$

, where $a_2(t)=m$, $a_1(t)=0$, $a_0(t)=k$, and $b(t)=0$. Therefore, the equation of motion for $\Delta r(t)$ is a **second-order linear differential equation**. In operator form, we may define the linear differential operator

$$
\mathcal{L}[\Delta r] = m\frac{d^2(\Delta r)}{dt^2} + k\Delta r, \tag{13}

$$

so that the equation of motion can be written compactly as

$$
\mathcal{L}[\Delta r] = 0. \tag{14}

$$

We now want to find a function $\Delta r(t)$ that is annihilated by this operator, that is, a function satisfying the differential equation above. For linear equations with constant coefficients, a standard approach is to try an exponential solution, because exponentials remain proportional to themselves when differentiated. We therefore assume a trial solution of the form

$$
\Delta r(t) = e^{\lambda t}, \tag{15}

$$

where $\lambda$ is a constant to be determined. Substituting this trial form into the equation of motion gives

$$
m \lambda^2 e^{\lambda t} + k e^{\lambda t} = 0. \tag{16}

$$

Since $e^{\lambda t}$ is never zero, we can divide both sides by it and obtain

$$
\begin{aligned}
m\lambda^2 + k &= 0 \Leftrightarrow \lambda^2 = -\frac{k}{m} \\
\Rightarrow \lambda &= \pm i\sqrt{\frac{k}{m}} = \pm i \omega \qquad (\omega=\sqrt{\frac{k}{m}})
\end{aligned} \tag{17}

$$

Thus there are two linearly independent exponential solutions $e^{i\omega t}$ and $e^{-i\omega t}$.

Because the differential equation is linear, any linear combination of these solutions is also a solution. Therefore,

$$
\Delta r(t) = A e^{i\omega t} + B e^{-i\omega t} \tag{18}

$$

, where A and B are arbitrary complex numbers. Although this expression is written in terms of complex exponentials, the physical displacement must be real. Using [Euler's formula](https://en.wikipedia.org/wiki/Euler%27s_formula),

$$
\begin{aligned}
e^{i\omega t} &= \cos(\omega t) + i\sin(\omega t) \\
e^{-i\omega t} &= \cos(\omega t) - i\sin(\omega t)
\end{aligned} \tag{19}

$$

we can rewrite the general real-valued solution in the equivalent form

$$
\Delta r(t) = a\cos(\omega t) + b\sin(\omega t), \tag{20}

$$

where $a$ and $b$ are real constants determined by the initial conditions. This shows that the motion is sinusoidal, with angular frequency $\omega=\sqrt{\frac{k}{m}}$ ($k=m\omega^2$, spring constant is proportional to frequency square).

> How can we determine the constants $a$ and $b$ from the initial position and initial velocity?

This is the standard 1D solution for harmonic motion.
It tells us that the particle oscillates with angular frequency

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Angularvelocity.svg/3840px-Angularvelocity.svg.png" alt="Angular frequency diagram" width="420">
</p>

*Figure source:* [Simple English Wikipedia: Angular frequency](https://simple.wikipedia.org/wiki/Angular_frequency##/media/File:Angularvelocity.svg)

In general physics, **angular frequency** $\omega$ measures how fast a system moves through an angle or phase.
For an object rotating around a circle, it is defined by $\omega = \frac{d\theta}{dt}$, where $\theta$ is the angle swept out in time $t$.
So a larger $\omega$ means the system moves through its cycle more quickly.

In the figure, the rotating radius sweeps out an angle $\theta$.
As time passes, the angle changes continuously, and $\omega$ tells us how rapidly that change happens.
This is why angular frequency is commonly associated with rotation.

For our **two-particle motion in 1D**, the particles do not literally move in a circle.
However, the solution

$$
\Delta r(t) = \Delta r^0 + a\cos(\omega t) + b\sin(\omega t) \tag{21}

$$

still contains the phase $\omega t$.
That phase plays the same mathematical role as an angle in circular motion.
So even though the motion is back-and-forth along one line, $\omega$ still measures how fast the oscillation goes through one cycle.

## Harmonic motion in 2D

We derive the same in 2D. So in this page, we define:

- $\mathbf{r}_1 = [x_1\ y_1]^T$ and $\mathbf{r}_2 = [x_2\ y_2]^T$ are the position vectors.
- $\mathbf{r}_1^0 = [x_1^0\ y_1^0]^T$ and $\mathbf{r}_2^0 = [x_2^0\ y_2^0]^T$ are the equilibrium position vectors.
- $\Delta \mathbf{r} = \mathbf{r}_2 - \mathbf{r}_1$ is the instantaneous separation vector.
- $\Delta \mathbf{r}^0 = \mathbf{r}_2^0 - \mathbf{r}_1^0$ is the equilibrium separation vector.
- $\Delta \mathbf{r} - \Delta \mathbf{r}^0$ is the displacement of the separation vector from equilibrium.

Remember, lowercase regular symbols denote scalars, while boldface symbols denote vectors or matrices.

Now we know that the force acting on the system has two components, one in the $x$-direction and one in the $y$-direction:

$$
\mathbf{F} =
\begin{pmatrix} F_x \\ F_y \end{pmatrix}
=
-
\begin{pmatrix}
\dfrac{\partial V}{\partial (\Delta x)} \\
\dfrac{\partial V}{\partial (\Delta y)}
\end{pmatrix}
= -\nabla_{\Delta \mathbf{r}} V. \tag{22}

$$

Here, $\nabla_{\Delta \mathbf{r}} V$ is the gradient of the potential $V$ with respect to the separation vector $\Delta \mathbf{r}$, so we may think of it as the first derivative of $V$ with respect to $\Delta \mathbf{r}$. In 2D, it becomes a $2\times 2$ matrix, called the **Hessian matrix**:

$$
\mathbf{H}(\Delta \mathbf{r}) = \nabla_{\Delta \mathbf{r}}\!\left(\nabla_{\Delta \mathbf{r}} V\right)
=
\nabla_{\Delta \mathbf{r}}
\begin{pmatrix}
\dfrac{\partial V}{\partial (\Delta x)} \\
\dfrac{\partial V}{\partial (\Delta y)}
\end{pmatrix}
=
\begin{pmatrix}
\dfrac{\partial^2 V}{\partial (\Delta x)^2} &
\dfrac{\partial^2 V}{\partial (\Delta x)\partial (\Delta y)} \\
\dfrac{\partial^2 V}{\partial (\Delta y)\partial (\Delta x)} &
\dfrac{\partial^2 V}{\partial (\Delta y)^2}
\end{pmatrix}. \tag{23}

$$

The matrix $\mathbf{H}$ tells us how strongly the system resists displacement in each direction and whether motions in different directions are coupled. If this resistance is the same in every direction, then the motion is called **isotropic**; otherwise, it is **anisotropic**. In the **isotropic** case, the Hessian matrix is proportional to the identity matrix,

$$
\mathbf{H} = k I, \tag{24}

$$

where $k=\dfrac{\partial^2 V}{\partial (\Delta x)^2}=\dfrac{\partial^2 V}{\partial (\Delta x)\partial (\Delta y)}=\dfrac{\partial^2 V}{\partial (\Delta y)^2}$ is the uniform spring constant and $I$ is the identity matrix. Then the restoring force has the same strength in every direction.

Similar to Eq. 6, when the system is only slightly displaced from equilibrium, we expand $V$ using a Taylor series:

$$
V(\Delta \mathbf{r}) =
V(\Delta \mathbf{r}^0)
+ (\Delta \mathbf{r}-\Delta \mathbf{r}^0)^T
\left.\nabla_{\Delta \mathbf{r}} V\right|_{\Delta \mathbf{r}=\Delta \mathbf{r}^0}
+ \frac{1}{2}
(\Delta \mathbf{r}-\Delta \mathbf{r}^0)^T
\mathbf{H}
(\Delta \mathbf{r}-\Delta \mathbf{r}^0)
+ \cdots, \tag{25}

$$

where $\mathbf{H}$ is the Hessian matrix of second derivatives of the potential evaluated at $\Delta \mathbf{r}^0$. Since $\Delta \mathbf{r}^0$ is the equilibrium separation vector, the first derivative vanishes $\nabla_{\Delta \mathbf{r}} V|_{\Delta \mathbf{r}=\Delta \mathbf{r}^0} = \mathbf{0}$. If we also choose the zero of potential energy so that $V(\Delta \mathbf{r}^0)=0$, then the expansion reduces to

$$
V(\Delta \mathbf{r})
\approx
\frac{1}{2}
(\Delta \mathbf{r}-\Delta \mathbf{r}^0)^T
\mathbf{H}
(\Delta \mathbf{r}-\Delta \mathbf{r}^0). \tag{26}

$$

And again, if we choose the coordinate system so that $\Delta \mathbf{r}^0 = \mathbf{0}$, then we have

$$
V(\Delta \mathbf{r}) \approx
\frac{1}{2} \Delta \mathbf{r}^T \mathbf{H} \Delta \mathbf{r}. \tag{27}

$$

How can we calculate the force, now?

$$
\mathbf{F} = 
-\nabla_{\Delta \mathbf{r}} V(\Delta \mathbf{r}) =
-\nabla_{\Delta \mathbf{r}} (\frac{1}{2} \Delta \mathbf{r}^T \mathbf{H} \Delta \mathbf{r}) =
- \mathbf{H} \Delta \mathbf{r} \tag{28}

$$

We now combine Eq. 26 with Newton's second law. For the relative coordinate, the equation of motion becomes

$$
\mathbf{F} = m \frac{d^2 \Delta \mathbf{r}}{dt^2} = - \mathbf{H} \Delta \mathbf{r} \Leftrightarrow m \frac{d^2 \Delta \mathbf{r}}{dt^2} + \mathbf{H} \Delta \mathbf{r} = \mathbf{0}. \tag{29}

$$

## Thermal fluctation in 2D

Let us define the displacement from equilibrium as $\mathbf{x} = \Delta \mathbf{r} - \Delta \mathbf{r}^0$. Using Eq. 24, the harmonic potential can be written as

$$
V(\mathbf{x}) = \frac{1}{2}\mathbf{x}^T \mathbf{H} \mathbf{x}. \tag{30}

$$

At thermal equilibrium, the probability density of the displacement vector is given by the Boltzmann distribution:

$$
P(\mathbf{x}) = \frac{1}{Z}\exp\!\left(-\frac{V(\mathbf{x})}{k_B T}\right)
=
\frac{1}{Z}\exp\!\left(-\frac{1}{2k_B T}\mathbf{x}^T \mathbf{H} \mathbf{x}\right) \tag{31}

$$

, where the partition function is $Z=\int \exp(-\frac{1}{2k_B T}\mathbf{x}^T \mathbf{H} \mathbf{x})\,d\mathbf{x}$. To describe the size of the fluctuation, we consider the covariance matrix

$$
\langle \mathbf{x}\mathbf{x}^T \rangle =
\int \mathbf{x}\mathbf{x}^T P(\mathbf{x})\,d\mathbf{x}
= k_B T\,\mathbf{H}^{-1} \tag{32}

$$

This is the 2D analogue of the 1D result $\langle x^2 \rangle = k_B T/k$. In 1D, the spring constant is the scalar $k$; in 2D, it is replaced by the Hessian matrix $\mathbf{H}$, so the fluctuation is controlled by the inverse Hessian.

The mean-square size of the fluctuation is the ensemble average of the squared magnitude:

$$
\left\langle |\mathbf{x}|^2 \right\rangle
=
\left\langle \mathbf{x}^T\mathbf{x} \right\rangle
=
\mathrm{Tr}\!\left(\langle \mathbf{x}\mathbf{x}^T \rangle\right)
=
k_B T\,\mathrm{Tr}(\mathbf{H}^{-1}). \tag{33}

$$

Therefore, the root-mean-square fluctuation is

$$
\sqrt{\left\langle |\mathbf{x}|^2 \right\rangle}
=
\sqrt{k_B T\,\mathrm{Tr}(\mathbf{H}^{-1})}. \tag{34}

$$

These equations show that the fluctuations are larger at higher temperature and smaller when the Hessian has larger eigenvalues, that is, when the system is stiffer. This same idea is generalized further in Gaussian network models, where fluctuation amplitudes and correlations are obtained from the inverse of a network matrix.

## Solution of Harmonic Motion in 2D

To solve Eq. 27, we again try an exponential form. Since the displacement is now a vector, we assume

$$
\Delta \mathbf{r}(t) = \mathbf{u} e^{\lambda t}, \tag{35}

$$

where $\mathbf{u}$ is a constant vector and $\lambda$ is a constant to be determined. Substituting this trial solution into Eq. 27 gives

$$
m \lambda^2 \mathbf{u} e^{\lambda t} + \mathbf{H} \mathbf{u} e^{\lambda t} = \mathbf{0}. \tag{36}

$$

Since $e^{\lambda t} \neq 0$, we can divide by it and obtain

$$
\mathbf{H} \mathbf{u} = -m \lambda^2 \mathbf{u}. \tag{37}

$$

Therefore, $\mathbf{u}$ must be an eigenvector of $\mathbf{H}$, and the corresponding eigenvalue is $\mu = -m \lambda^2$. Since $\mathbf{H}$ is a $2\times 2$ matrix, it has two eigenvalues, which we denote by $\mu_1$ and $\mu_2$, with corresponding eigenvectors $\mathbf{u}_1$ and $\mathbf{u}_2$.

Let us define the angular frequencies $\omega^2 = \mu / m = -\lambda^2$ ($\mu=m\omega^2$, eigenvalue is proportional to frequency square), then we obtain $\lambda = \pm i\omega_1$, $\lambda = \pm i\omega_2$. Therefore, the exponential solutions are

$$
\Delta \mathbf{r}(t) = \mathbf{u}_1 e^{i\omega_1 t},
\qquad
\Delta \mathbf{r}(t) = \mathbf{u}_1 e^{-i\omega_1 t},
\qquad
\Delta \mathbf{r}(t) = \mathbf{u}_2 e^{i\omega_2 t},
\qquad
\Delta \mathbf{r}(t) = \mathbf{u}_2 e^{-i\omega_2 t}. \tag{38}

$$

Using Euler's formula, we can rewrite the general real-valued solution as

$$
\Delta \mathbf{r}(t)
=
a_1 \mathbf{u}_1 \cos(\omega_1 t)
+ b_1 \mathbf{u}_1 \sin(\omega_1 t)
+ a_2 \mathbf{u}_2 \cos(\omega_2 t)
+ b_2 \mathbf{u}_2 \sin(\omega_2 t)
=
\sum_{i=1}^{2}
\mathbf{u}_i \left[ a_i \cos(\omega_i t) + b_i \sin(\omega_i t) \right]
, \tag{39}

$$

where $a_1$, $b_1$, $a_2$, and $b_2$ are constants determined by the initial conditions.

In this form, the meaning becomes clearer. The total motion is the sum of two independent oscillations, one along the direction of $\mathbf{u}_1$ and the other along the direction of $\mathbf{u}_2$.

Each of these oscillations is called a **normal mode**. A normal mode is a pattern of motion in which all coordinates oscillate with the same single frequency and keep a fixed direction pattern determined by the eigenvector. In our 2D case:

- $\mathbf{u}_1$ gives the first normal mode, with frequency $\omega_1$
- $\mathbf{u}_2$ gives the second normal mode, with frequency $\omega_2$

Therefore, although the motion may look complicated in the original $x$-$y$ coordinates, it becomes simple when expressed in the basis of eigenvectors of the Hessian matrix. In that basis, the coupled 2D motion is decomposed into a superposition of two independent harmonic oscillators.

## N-particle system in 3D

We now generalize the discussion from a two-particle system to an $n$-particle system in three dimensions. A convenient picture is a mass-spring network, where each particle is represented by a node and each interaction is represented by a spring.

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/5/58/MassSpringNetwork.jpg" alt="Mass-spring network model" width="900">
</p>

*Figure source:* [Wikipedia: Gaussian network model, MassSpringNetwork.jpg](https://en.wikipedia.org/wiki/Gaussian_network_model#/media/File:MassSpringNetwork.jpg)

In this model, particle $i$ has position vector $\mathbf{R}_i = \begin{pmatrix} x_i \\ y_i \\ z_i \end{pmatrix}$, and equilibrium position vector $\mathbf{R}_i^0 = \begin{pmatrix} x_i^0 \\ y_i^0 \\ z_i^0 \end{pmatrix}$. Its displacement from equilibrium is

$$
\Delta \mathbf{R}_i = \mathbf{R}_i - \mathbf{R}_i^0. \tag{40}

$$

For the whole system, the instantaneous position vectors, equilibrium position vectors, and displacement vectors are

$$
\mathbf{R} =
\begin{pmatrix}
\mathbf{R}_1 \\
\mathbf{R}_2 \\
\vdots \\
\mathbf{R}_n
\end{pmatrix},
\qquad
\mathbf{R}^0 =
\begin{pmatrix}
\mathbf{R}_1^0 \\
\mathbf{R}_2^0 \\
\vdots \\
\mathbf{R}_n^0
\end{pmatrix},
\qquad
\Delta \mathbf{R} =
\begin{pmatrix}
\Delta \mathbf{R}_1 \\
\Delta \mathbf{R}_2 \\
\vdots \\
\Delta \mathbf{R}_n
\end{pmatrix}. \tag{41}

$$

The relation between these quantities is shown in the figure: $\mathbf{R}_i^0$ and $\mathbf{R}_j^0$ are the equilibrium position vectors, $\Delta \mathbf{R}_i$ and $\Delta \mathbf{R}_j$ are the displacements from equilibrium, and $\mathbf{R}_{ij}^0$ is the equilibrium separation vector between particles $i$ and $j$.

For the whole system, we define:

- $n$ is the number of particles in the system.
- $\mathbf{R}_i$ is the instantaneous position vector of particle $i$.
- $\mathbf{R}_i^0$ is the equilibrium position vector of particle $i$.
- $\Delta \mathbf{R}_i = \mathbf{R}_i - \mathbf{R}_i^0$ is the displacement vector of particle $i$ from equilibrium.
- $\mathbf{R}_{ij} = \mathbf{R}_j - \mathbf{R}_i$ is the instantaneous separation vector between particles $i$ and $j$.
- $\mathbf{R}_{ij}^0 = \mathbf{R}_j^0 - \mathbf{R}_i^0$ is the equilibrium separation vector between particles $i$ and $j$.
- $\mathbf{R}_{ij}-\mathbf{R}_{ij}^0 = (\mathbf{R}_j - \mathbf{R}_i) - (\mathbf{R}_j^0 - \mathbf{R}_i^0)=\Delta \mathbf{R}_j $

The change in separation vector from equilibrium is

$$
\Delta \mathbf{R}_{ij}=\mathbf{R}_{ij}-\mathbf{R}_{ij}^0 = (\mathbf{R}_j - \mathbf{R}_i) - (\mathbf{R}_j^0 - \mathbf{R}_i^0)=\Delta \mathbf{R}_j - \Delta \mathbf{R}_i

$$

It means that the change in separation vector is just the difference of the two particle displacement vectors. For one interacting pair $(i,j)$, the harmonic potential energy is

$$
V_{ij} \approx \frac{1}{2}
\left( \mathbf{R}_{ij} - \mathbf{R}_{ij}^0 \right)^T
\mathbf{H}_{ij}
\left( \mathbf{R}_{ij} - \mathbf{R}_{ij}^0 \right)
= 
\frac{1}{2} 
\left(\Delta \mathbf{R}_{j} - \Delta \mathbf{R}_{i} \right)^T
\mathbf{H}_{ij}
\left(\Delta \mathbf{R}_{j} - \Delta \mathbf{R}_{i} \right) \tag{42}

$$

, where $\mathbf{H}_{ij}$ is the $3\times 3$ Hessian matrix for the interaction between particles $i$ and $j$, evaluated at the equilibrium separation vector $\mathbf{R}_{ij}^0$

$$
\mathbf{H}_{ij}
=
\left.
\nabla_{\mathbf{R}_{ij}}
\left(
\nabla_{\mathbf{R}_{ij}} V_{ij}
\right)
\right|_{\mathbf{R}_{ij}=\mathbf{R}_{ij}^0}
=
\left.
\frac{\partial^2 V_{ij}}
{\partial \mathbf{R}_{ij}\,\partial \mathbf{R}_{ij}^T}
\right|_{\mathbf{R}_{ij}=\mathbf{R}_{ij}^0}

$$

As a concrete example, consider a tri-peptide-like system with three particles, labeled $1$, $2$, and $3$, as shown below. Suppose that particles $1$ and $2$ are in contact, particles $2$ and $3$ are in contact, but particles $1$ and $3$ are not in contact for the chosen cutoff distance $R_c$.

<p align="center">
  <img src="{{ '/images/The elastic potential of a tri-peptide molecule.png' | relative_url }}" alt="Tri-peptide contact example" width="720">
</p>

In this case, the connectivity matrix is

$$
A =
\begin{pmatrix}
0 & 1 & 0 \\
1 & 0 & 1 \\
0 & 1 & 0
\end{pmatrix}. \tag{43}

$$

Therefore, only two pair interactions contribute to the total potential:

$$
V_{\text{total}} = V_{12} + V_{23}. \tag{44}

$$

Using Eq. 46, this becomes

$$
\begin{aligned}
V_{\text{total}}
&\approx
\frac{1}{2}
\left( \mathbf{R}_{12} - \mathbf{R}_{12}^0 \right)^T
\mathbf{H}_{12}
\left( \mathbf{R}_{12} - \mathbf{R}_{12}^0 \right) \\
&\qquad +
\frac{1}{2}
\left( \mathbf{R}_{23} - \mathbf{R}_{23}^0 \right)^T
\mathbf{H}_{23}
\left( \mathbf{R}_{23} - \mathbf{R}_{23}^0 \right).
\end{aligned} \tag{45}

$$

Since $\mathbf{R}_{ij} - \mathbf{R}_{ij}^0 = \Delta \mathbf{R}_j - \Delta \mathbf{R}_i$, we may rewrite the total potential in terms of the particle displacements:

$$
\begin{aligned}
V_{\text{total}}
&\approx
\frac{1}{2}
\left( \Delta \mathbf{R}_2 - \Delta \mathbf{R}_1 \right)^T
\mathbf{H}_{12}
\left( \Delta \mathbf{R}_2 - \Delta \mathbf{R}_1 \right) \\
&\qquad +
\frac{1}{2}
\left( \Delta \mathbf{R}_3 - \Delta \mathbf{R}_2 \right)^T
\mathbf{H}_{23}
\left( \Delta \mathbf{R}_3 - \Delta \mathbf{R}_2 \right).
\end{aligned} \tag{46}

$$

Now collect the displacements into the stacked vector

$$
\Delta \mathbf{R} =
\begin{pmatrix}
\Delta \mathbf{R}_1 \\
\Delta \mathbf{R}_2 \\
\Delta \mathbf{R}_3
\end{pmatrix}. \tag{47}

$$

Then the same potential can be written in quadratic form,

$$
V_{\text{total}} = \frac{1}{2}\Delta \mathbf{R}^T \mathbf{H}_{\text{tri}} \Delta \mathbf{R}, \tag{48}

$$

where the tri-peptide system Hessian is the $9\times 9$ block matrix

$$
\mathbf{H}_{\text{tri}} =
\begin{pmatrix}
\mathbf{H}_{12} & -\mathbf{H}_{12} & \mathbf{0} \\
-\mathbf{H}_{12} & \mathbf{H}_{12}+\mathbf{H}_{23} & -\mathbf{H}_{23} \\
\mathbf{0} & -\mathbf{H}_{23} & \mathbf{H}_{23}
\end{pmatrix}. \tag{49}

$$

> Prove equation 48 and equation 49?

In the isotropic GNM approximation with a uniform spring constant $\gamma$, we take

$$
\mathbf{H}_{12} = \mathbf{H}_{23} = \gamma \mathbf{I}_3,
\qquad
\mathbf{H}_{13} = \mathbf{0}. \tag{50}

$$

Then Eq. 46h becomes

$$
\mathbf{H}_{\text{tri}}
=
\gamma
\begin{pmatrix}
\mathbf{I}_3 & -\mathbf{I}_3 & \mathbf{0} \\
-\mathbf{I}_3 & 2\mathbf{I}_3 & -\mathbf{I}_3 \\
\mathbf{0} & -\mathbf{I}_3 & \mathbf{I}_3
\end{pmatrix}
=
\gamma\,\Gamma \otimes \mathbf{I}_3, \tag{51}

$$

with

$$
\Gamma =
\begin{pmatrix}
1 & -1 & 0 \\
-1 & 2 & -1 \\
0 & -1 & 1
\end{pmatrix}. \tag{52}

$$

This is the simplest explicit example of how the full system Hessian is assembled from pair interactions and how, under the GNM approximation, it reduces to a Kirchhoff matrix times the $3\times 3$ identity.

The total harmonic potential energy of the system is obtained by summing over all connected pairs:

$$
V_{\text{total}}
=
\sum_{i=1}^{n}\sum_{j=1}^{n}
\frac{1}{2}
(\mathbf{R}_{ij} - \mathbf{R}_{ij}^0)^T
\mathbf{H}_{ij}
(\mathbf{R}_{ij} - \mathbf{R}_{ij}^0)
= 
\frac{1}{2} \Delta \mathbf{R}^T \mathbf{H} \Delta \mathbf{R} \tag{53}

$$

, where $\mathbf{H}$ is the full $3n \times 3n$ system Hessian, built from all the pair blocks $\mathbf{H}_{ij}$

$$
\mathbf{H}
=
\left.
\nabla_{\Delta \mathbf{R}}
\left(
\nabla_{\Delta \mathbf{R}} V_{\text{total}}
\right)
\right|_{\Delta \mathbf{R}=\mathbf{0}}
=
\left.
\frac{\partial^2 V_{\text{total}}}
{\partial (\Delta \mathbf{R})\,\partial (\Delta \mathbf{R})^T}
\right|_{\Delta \mathbf{R}=\mathbf{0}}

$$

Then $\mathbf{H}^{(g)}_{ij}$ is the $(i,j)$ block of this full matrix

$$
\mathbf{H}^{(g)}_{ij}
=
\left.
\frac{\partial^2 V_{\text{total}}}
{\partial (\Delta \mathbf{R}_i)\,\partial (\Delta \mathbf{R}_j)^T}
\right|_{\Delta \mathbf{R}=\mathbf{0}}.

$$

$$
A_{ij}
=
\begin{cases}
1, & \text{if particles } i \text{ and } j \text{ are connected}, \\
0, & \text{otherwise}.
\end{cases} \tag{54}

$$

The factor of $\frac{1}{2}$ avoids counting each pair twice.

In Gaussian network-type models, the connectivity is usually determined by a cutoff distance $r_c$: particles $i$ and $j$ are connected if

$$
R_{ij}^0 < r_c. \tag{55}

$$

If all connected pairs are assigned the same spring constant $\gamma$, then the total potential simplifies to

$$
V_{\text{total}}
=
\frac{\gamma}{2}
\sum_{i<j}
A_{ij}\left(R_{ij}-R_{ij}^0\right)^2. \tag{56}

$$

This isotropic, uniform-spring approximation is the key simplification behind the Gaussian network model (GNM).

The force acting on particle $i$ is obtained from the total potential by

$$
\mathbf{F}_i = -\nabla_{\mathbf{R}_i} V_{\text{total}}. \tag{57}

$$

Applying Newton's second law to every particle gives a set of $n$ coupled vector equations:

$$
m_i \frac{d^2 \mathbf{R}_i}{dt^2}
=
\mathbf{F}_i
=
-\nabla_{\mathbf{R}_i} V_{\text{total}},
\qquad i=1,\dots,n. \tag{58}

$$

Collecting all particle displacements into the stacked vector $\Delta \mathbf{R}$, the linearized equation of motion near equilibrium can be written compactly as

$$
M \frac{d^2 \Delta \mathbf{R}}{dt^2} + \mathbf{H} \Delta \mathbf{R} = \mathbf{0}, \tag{59}

$$

where $M$ is the mass matrix and $\mathbf{H}$ is now the full $3n\times 3n$ Hessian matrix of the system.

## Solution of Harmonic Motion for an N-particle System in 3D

To solve Eq. 53, we again try an exponential solution, now for the full $3n$-dimensional displacement vector:

$$
\Delta \mathbf{R}(t) = \mathbf{U} e^{\lambda t}, \tag{60}

$$

where $\mathbf{U}$ is a constant $3n$-dimensional vector.

Substituting Eq. 54 into Eq. 53 gives

$$
M \lambda^2 \mathbf{U} e^{\lambda t} + \mathbf{H} \mathbf{U} e^{\lambda t} = \mathbf{0}. \tag{61}

$$

Since $e^{\lambda t} \neq 0$, we obtain

$$
\mathbf{H} \mathbf{U} = - M \lambda^2 \mathbf{U}. \tag{62}

$$

This is the matrix generalization of the eigenvalue equation we saw in 2D. If all particles have the same mass $m$, then $M = mI$, and Eq. 56 becomes

$$
\mathbf{H} \mathbf{U} = - m \lambda^2 \mathbf{U}. \tag{63}

$$

Therefore, $\mathbf{U}$ must be an eigenvector of the full Hessian matrix $\mathbf{H}$, and the corresponding eigenvalue $\mu$ satisfies

$$
\mu = -m\lambda^2. \tag{64}

$$

If the eigenvalues of $\mathbf{H}$ are $\mu_1,\mu_2,\dots,\mu_{3n}$, then the corresponding angular frequencies are

$$
\omega_k = \sqrt{\frac{\mu_k}{m}},
\qquad
k=1,2,\dots,3n. \tag{65}

$$

Each eigenvector $\mathbf{U}_k$ gives one normal mode of the entire system. The general real-valued solution can therefore be written as

$$
\Delta \mathbf{R}(t)
=
\sum_{k=1}^{3n}
\mathbf{U}_k \left[ a_k \cos(\omega_k t) + b_k \sin(\omega_k t) \right]. \tag{66}

$$

Here $a_k$ and $b_k$ are constants determined by the initial conditions.

This expression has exactly the same structure as the 2D two-particle case, except that the sum now runs over all $3n$ normal modes. Each mode describes a collective pattern of motion involving all particles in the system.

In practice, some of these modes correspond to rigid-body translations and rotations, which do not deform the structure and therefore have zero or near-zero frequency. The remaining nonzero-frequency modes describe the internal vibrations of the network and are the main objects of interest in elastic network models.

In the language of GNM, we usually do not follow the full time-dependent vector solution in Eq. 60. Instead, we use the isotropic network assumption to study fluctuation amplitudes and correlations from the inverse of the Kirchhoff matrix $\Gamma$. Thus, Eq. 60 is best viewed as the more detailed directional analogue, while GNM keeps the same network idea but focuses on scalar fluctuation statistics rather than explicit vector-valued motion.
