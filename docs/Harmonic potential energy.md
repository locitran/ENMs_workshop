---
layout: default
title: Harmonic Potential Energy
kicker: Bonus Material
lead: Additional notes on harmonic oscillators and the relationship between force and potential energy.
description: Harmonic potential energy notes.
permalink: /harmonic-potential-energy/
---

## Harmonic Oscillator

Consider a two-particle system moving in one dimension. Let the positions of the two particles be $r_1$ and $r_2$. The quantity we care about is their distance,

$$
\Delta r = r_2 - r_1 \tag{1}

$$

So in this page, we define:

- $\Delta r$ is the instantaneous distance between the two particles
- $\Delta r^0$ is the equilibrium distance between the two particles
- $\Delta r - \Delta r^0$ is the displacement from equilibrium
- $V(\Delta r)$ is the potential energy as a function of distance
- $F(\Delta r)$ is the force associated with that potential
- $k$ is the local curvature of the potential near equilibrium, and later becomes the effective spring constant

If the particles are displaced only slightly from $\Delta r^0$, the interaction tends to pull the system back toward equilibrium. This kind of back-and-forth motion is called **harmonic motion**, and the corresponding model is the **harmonic oscillator**.

A two-particle system is in equilibrium when the net force on the relative coordinate vanishes. For a conservative force,

$$
F(\Delta r) = -\frac{dV}{d(\Delta r)} \tag{2}

$$

so at the equilibrium position $\Delta r = \Delta r^0$ we must have

$$
F(\Delta r^0) = -\left.\frac{dV}{d(\Delta r)}\right|_{\Delta r=\Delta r^0} = 0 \tag{3}

$$

This tells us that the potential energy curve is locally flat at equilibrium. In addition, the force depends only on the derivative of $V(\Delta r)$, not on its absolute value. If we replace $V(\Delta r)$ by

$$
\tilde V(\Delta r) = V(\Delta r) + C, \tag{4}

$$

then

$$
-\frac{d\tilde V}{d(\Delta r)} = -\frac{d}{d(\Delta r)}\bigl(V(\Delta r)+C\bigr) = -\frac{dV}{d(\Delta r)} = F(\Delta r). \tag{5}

$$

Therefore, adding a constant does not change the physics. For this reason, we are free to choose the zero of potential energy conveniently, so we set $V(\Delta r^0)=0$.

In general, we do not know the exact form of the potential energy $V(\Delta r)$. However, if we are interested only in small displacements from equilibrium, then we can describe the potential relative to $V(\Delta r^0)=0$ by expanding it in a Maclaurin-Taylor series around the equilibrium distance:

$$
V(\Delta r) = V(\Delta r^0) + (\Delta r-\Delta r^0)V'(\Delta r^0) + \frac{1}{2}(\Delta r-\Delta r^0)^2V''(\Delta r^0) + \cdots , \tag{6}

$$

where the primes denote differentiation with respect to $\Delta r$. Since we chose $V(\Delta r^0)=0$ and also know that $V'(\Delta r^0)=0$, the first two terms vanish. Thus, near the equilibrium distance $\Delta r^0$, we may write

$$
V(\Delta r) \approx \frac{1}{2}(\Delta r-\Delta r^0)^2V''(\Delta r^0) = \frac{1}{2}k(\Delta r-\Delta r^0)^2, \quad k=V''(\Delta r^0) \tag{7}

$$

If we choose the coordinate origin so that the equilibrium distance is at zero, that is, $\Delta r^0=0$, then the harmonic approximation simplifies to

$$
V(\Delta r) \approx \frac{1}{2}k(\Delta r)^2. \tag{8}

$$

In this shifted coordinate system, the displacement from equilibrium is simply $\Delta r$ itself, and the corresponding force becomes

$$
F(\Delta r) = -\frac{dV}{d(\Delta r)} \approx -k\Delta r. \tag{9}

$$

This is the standard form of Hooke's law: the force is proportional to the displacement and points in the opposite direction.

Reference:
Tom W. B. Kibble and Frank H. Berkshire, *Classical Mechanics*, Chapter 2: Linear Motion, Sections 2.1 and 2.2.

## Solution of Harmonic Motion

To solve the motion, combine Newton's second law with the harmonic restoring force:

$$
F = ma = -k\Delta r \Rightarrow m\frac{d^2(\Delta r)}{dt^2} + k\Delta r = 0 \tag{10}

$$

We may view this equation as a [linear differential equation]({{ '/linear-differential-equation/' | relative_url }}) of the general form

$$
a_2(t)\Delta r'' + a_1(t)\Delta r' + a_0(t)\Delta r = b(t) \tag{11}

$$

, where $a_2(t)=m$, $a_1(t)=0$, $a_0(t)=k$, and $b(t)=0$. Therefore, the equation of motion for $\Delta r(t)$ is a **second-order linear differential equation**. In operator form, we may define the linear differential operator

$$
\mathcal{L}[\Delta r] = m\frac{d^2(\Delta r)}{dt^2} + k\Delta r, \tag{12}

$$

so that the equation of motion can be written compactly as

$$
\mathcal{L}[\Delta r] = 0. \tag{13}

$$

We now want to find a function $\Delta r(t)$ that is annihilated by this operator, that is, a function satisfying the differential equation above. For linear equations with constant coefficients, a standard approach is to try an exponential solution, because exponentials remain proportional to themselves when differentiated. We therefore assume a trial solution of the form

$$
\Delta r(t) = e^{\lambda t}, \tag{14}

$$

where $\lambda$ is a constant to be determined. Substituting this trial form into the equation of motion gives

$$
m \lambda^2 e^{\lambda t} + k e^{\lambda t} = 0. \tag{15}

$$

Since $e^{\lambda t}$ is never zero, we can divide both sides by it and obtain

$$
\begin{aligned}
m\lambda^2 + k &= 0 \Leftrightarrow \lambda^2 = -\frac{k}{m} \\
\Rightarrow \lambda &= \pm i\sqrt{\frac{k}{m}} = \pm i \omega \qquad (\omega=\sqrt{\frac{k}{m}})
\end{aligned} \tag{16}

$$

Thus there are two linearly independent exponential solutions $e^{i\omega t}$ and $e^{-i\omega t}$.

Because the differential equation is linear, any linear combination of these solutions is also a solution. Therefore,

$$
\Delta r(t) = A e^{i\omega t} + B e^{-i\omega t} \tag{17}

$$

, where A and B are arbitrary complex numbers. Although this expression is written in terms of complex exponentials, the physical displacement must be real. Using [Euler's formula](https://en.wikipedia.org/wiki/Euler%27s_formula),

$$
\begin{aligned}
e^{i\omega t} &= \cos(\omega t) + i\sin(\omega t) \\
e^{-i\omega t} &= \cos(\omega t) - i\sin(\omega t)
\end{aligned} \tag{18}

$$

we can rewrite the general real-valued solution in the equivalent form

$$
\Delta r(t) = a\cos(\omega t) + b\sin(\omega t), \tag{19}

$$

where $a$ and $b$ are real constants determined by the initial conditions. This shows that the motion is sinusoidal, with angular frequency $\omega=\sqrt{\frac{k}{m}}$.

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
\Delta r(t) = \Delta r^0 + a\cos(\omega t) + b\sin(\omega t) \tag{20}

$$

still contains the phase $\omega t$.
That phase plays the same mathematical role as an angle in circular motion.
So even though the motion is back-and-forth along one line, $\omega$ still measures how fast the oscillation goes through one cycle.

## Harmonic motion in 2D

We derive the same in 2D.
So in this page, we define:

- $\mathbf{r}_1 = [x_1\ y_1]^T$ and $\mathbf{r}_2 = [x_2\ y_2]^T$ are the position vectors.
- $\mathbf{r}_1^0 = [x_1^0\ y_1^0]^T$ and $\mathbf{r}_2^0 = [x_2^0\ y_2^0]^T$ are the equilibrium position vectors.
- $\Delta \mathbf{r} = \mathbf{r}_2 - \mathbf{r}_1$ is the instantaneous separation vector.
- $\Delta \mathbf{r}^0 = \mathbf{r}_2^0 - \mathbf{r}_1^0$ is the equilibrium separation vector.
- $\Delta \mathbf{r} - \Delta \mathbf{r}^0$ is the displacement of the separation vector from equilibrium.
- $\Delta r = |\Delta \mathbf{r}|$ is the instantaneous distance between the two particles.
- $\Delta r^0 = |\Delta \mathbf{r}^0|$ is the equilibrium distance between the two particles.
- $V(\Delta r)$ is the potential energy as a function of the scalar distance $\Delta r$.
- $\mathbf{F}$ is the force associated with that potential.
- $k$ is the local curvature of the potential near equilibrium, and later becomes the effective spring constant.

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
= -\nabla_{\Delta \mathbf{r}} V. \tag{21}

$$

Here, $\nabla_{\Delta \mathbf{r}} V$ is the gradient of the potential $V$ with respect to the separation vector $\Delta \mathbf{r}$, so we may think of it as the first derivative of $V$ with respect to $\Delta \mathbf{r}$. The second derivative is no longer a scalar. In two dimensions, it becomes a $2\times 2$ matrix, called the **Hessian matrix**:

$$
H(\Delta \mathbf{r}) = \nabla_{\Delta \mathbf{r}}\!\left(\nabla_{\Delta \mathbf{r}} V\right)
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
\end{pmatrix}. \tag{22}

$$

The Hessian matrix $H$ plays the role of a generalized spring constant in more than one dimension. In 1D, the second derivative of the potential is just the scalar spring constant $k$. In 2D, that scalar is replaced by the matrix $H$, which tells us how strongly the system resists displacement in each direction and whether motions in different directions are coupled.

If the interaction has the same curvature in every direction, then the system is called **isotropic**. In that case, the Hessian matrix is proportional to the identity matrix,

$$
H = k I, \tag{22a}

$$

where $k$ is the ordinary spring constant and $I$ is the identity matrix. Then the restoring force has the same strength in every direction.

If the curvature depends on direction, or if motion in one coordinate affects the force in another coordinate, then the system is called **anisotropic**. In that case, the diagonal elements of $H$ need not be equal, and the off-diagonal elements need not vanish.

Similar to Eq. 6, when the system is only slightly displaced from equilibrium, we expand $V$ using a Taylor series:

$$
V(\Delta \mathbf{r}) =
V(\Delta \mathbf{r}^0)
+ (\Delta \mathbf{r}-\Delta \mathbf{r}^0)^T
\left.\nabla_{\Delta \mathbf{r}} V\right|_{\Delta \mathbf{r}=\Delta \mathbf{r}^0}
+ \frac{1}{2}
(\Delta \mathbf{r}-\Delta \mathbf{r}^0)^T
H
(\Delta \mathbf{r}-\Delta \mathbf{r}^0)
+ \cdots, \tag{23}

$$

where $H$ is the Hessian matrix of second derivatives of the potential evaluated at $\Delta \mathbf{r}^0$. Since $\Delta \mathbf{r}^0$ is the equilibrium separation vector, the first derivative vanishes $\nabla_{\Delta \mathbf{r}} V|_{\Delta \mathbf{r}=\Delta \mathbf{r}^0} = \mathbf{0}$. If we also choose the zero of potential energy so that $V(\Delta \mathbf{r}^0)=0$, then the expansion reduces to

$$
V(\Delta \mathbf{r})
\approx
\frac{1}{2}
(\Delta \mathbf{r}-\Delta \mathbf{r}^0)^T
H
(\Delta \mathbf{r}-\Delta \mathbf{r}^0). \tag{24}

$$

And again, if we choose the coordinate system so that $\Delta \mathbf{r}^0 = \mathbf{0}$, then we have

$$
V(\Delta \mathbf{r}) \approx
\frac{1}{2} \Delta \mathbf{r}^T H \Delta \mathbf{r}. \tag{25}

$$

How can we calculate the force, now?

$$
\mathbf{F} = 
-\nabla_{\Delta \mathbf{r}} V(\Delta \mathbf{r}) =
-\nabla_{\Delta \mathbf{r}} (\frac{1}{2} \Delta \mathbf{r}^T H \Delta \mathbf{r}) =
- H \Delta \mathbf{r} \tag{26}

$$

We now combine Eq. 26 with Newton's second law. For the relative coordinate, the equation of motion becomes

$$
\mathbf{F} = m \frac{d^2 \Delta \mathbf{r}}{dt^2} = - H \Delta \mathbf{r} \Leftrightarrow m \frac{d^2 \Delta \mathbf{r}}{dt^2} + H \Delta \mathbf{r} = \mathbf{0}. \tag{27}

$$

## Solution of Harmonic Motion in 2D

To solve Eq. 27, we again try an exponential form. Since the displacement is now a vector, we assume

$$
\Delta \mathbf{r}(t) = \mathbf{u} e^{\lambda t}, \tag{28}

$$

where $\mathbf{u}$ is a constant vector and $\lambda$ is a constant to be determined. Substituting this trial solution into Eq. 27 gives

$$
m \lambda^2 \mathbf{u} e^{\lambda t} + H \mathbf{u} e^{\lambda t} = \mathbf{0}. \tag{29}

$$

Since $e^{\lambda t} \neq 0$, we can divide by it and obtain

$$
H \mathbf{u} = -m \lambda^2 \mathbf{u}. \tag{30}

$$

Therefore, $\mathbf{u}$ must be an eigenvector of $H$, and the corresponding eigenvalue is $\mu = -m \lambda^2$. Since $H$ is a $2\times 2$ matrix, it has two eigenvalues, which we denote by $\mu_1$ and $\mu_2$, with corresponding eigenvectors $\mathbf{u}_1$ and $\mathbf{u}_2$.

Let us define the angular frequencies by

$$
\omega_1^2 = \frac{\mu_1}{m},
\qquad
\omega_2^2 = \frac{\mu_2}{m}. \tag{31}

$$

Then, from $\lambda^2 = -\mu/m$, we obtain

$$
\lambda = \pm i\omega_1,
\qquad
\lambda = \pm i\omega_2. \tag{32}

$$

Therefore, the exponential solutions are

$$
\Delta \mathbf{r}(t) = \mathbf{u}_1 e^{i\omega_1 t},
\qquad
\Delta \mathbf{r}(t) = \mathbf{u}_1 e^{-i\omega_1 t},
\qquad
\Delta \mathbf{r}(t) = \mathbf{u}_2 e^{i\omega_2 t},
\qquad
\Delta \mathbf{r}(t) = \mathbf{u}_2 e^{-i\omega_2 t}. \tag{33}

$$

Using Euler's formula, we can rewrite the general real-valued solution as

$$
\Delta \mathbf{r}(t)
=
a_1 \mathbf{u}_1 \cos(\omega_1 t)
+ b_1 \mathbf{u}_1 \sin(\omega_1 t)
+ a_2 \mathbf{u}_2 \cos(\omega_2 t)
+ b_2 \mathbf{u}_2 \sin(\omega_2 t), \tag{34}

$$

where $a_1$, $b_1$, $a_2$, and $b_2$ are constants determined by the initial conditions.

It is useful to rewrite Eq. 34 as a sum of two terms:

$$
\Delta \mathbf{r}(t) = \Delta \mathbf{r}_1(t) + \Delta \mathbf{r}_2(t), \tag{35}

$$

where

$$
\Delta \mathbf{r}_1(t) = a_1 \mathbf{u}_1 \cos(\omega_1 t) + b_1 \mathbf{u}_1 \sin(\omega_1 t), \tag{36}

$$

and

$$
\Delta \mathbf{r}_2(t) = a_2 \mathbf{u}_2 \cos(\omega_2 t) + b_2 \mathbf{u}_2 \sin(\omega_2 t). \tag{37}

$$

In this form, the meaning becomes clearer. The total motion is the sum of two independent oscillations, one along the direction of $\mathbf{u}_1$ and the other along the direction of $\mathbf{u}_2$.

Each of these oscillations is called a **normal mode**. A normal mode is a pattern of motion in which all coordinates oscillate with the same single frequency and keep a fixed direction pattern determined by the eigenvector. In our 2D case:

- $\mathbf{u}_1$ gives the first normal mode, with frequency $\omega_1$
- $\mathbf{u}_2$ gives the second normal mode, with frequency $\omega_2$

Therefore, although the motion may look complicated in the original $x$-$y$ coordinates, it becomes simple when expressed in the basis of eigenvectors of the Hessian matrix. In that basis, the coupled 2D motion is decomposed into a superposition of two independent harmonic oscillators.

Finally, Eq. 34 may be written more compactly in summation form as

$$
\Delta \mathbf{r}(t)
=
\sum_{i=1}^{2}
\mathbf{u}_i \left[ a_i \cos(\omega_i t) + b_i \sin(\omega_i t) \right]. \tag{38}

$$

## N-particle system in 3D

We now generalize the discussion from a two-particle system to an $n$-particle system in three dimensions. A convenient picture is a mass-spring network, where each particle is represented by a node and each interaction is represented by a spring.

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/5/58/MassSpringNetwork.jpg" alt="Mass-spring network model" width="900">
</p>

*Figure source:* [Wikipedia: Gaussian network model, MassSpringNetwork.jpg](https://en.wikipedia.org/wiki/Gaussian_network_model#/media/File:MassSpringNetwork.jpg)

In this model, particle $i$ has position vector

$$
\mathbf{R}_i =
\begin{pmatrix}
x_i \\
y_i \\
z_i
\end{pmatrix}, \tag{39}

$$

and equilibrium position vector

$$
\mathbf{R}_i^0 =
\begin{pmatrix}
x_i^0 \\
y_i^0 \\
z_i^0
\end{pmatrix}. \tag{40}

$$

Its displacement from equilibrium is

$$
\Delta \mathbf{R}_i = \mathbf{R}_i - \mathbf{R}_i^0. \tag{41}

$$

For a pair of particles $i$ and $j$, the instantaneous separation vector is

$$
\mathbf{R}_{ij} = \mathbf{R}_j - \mathbf{R}_i, \tag{42}

$$

and the equilibrium separation vector is

$$
\mathbf{R}_{ij}^0 = \mathbf{R}_j^0 - \mathbf{R}_i^0. \tag{43}

$$

The corresponding instantaneous distance and equilibrium distance are

$$
R_{ij} = |\mathbf{R}_{ij}|, \qquad R_{ij}^0 = |\mathbf{R}_{ij}^0|. \tag{44}

$$

The relation between these quantities is shown in the figure: $\mathbf{R}_i^0$ and $\mathbf{R}_j^0$ are the equilibrium position vectors, $\Delta \mathbf{R}_i$ and $\Delta \mathbf{R}_j$ are the displacements from equilibrium, and $\mathbf{R}_{ij}^0$ is the equilibrium separation vector between particles $i$ and $j$.

For the whole system, we define:

- $n$ is the number of particles in the system.
- $\mathbf{R}_i$ is the instantaneous position vector of particle $i$.
- $\mathbf{R}_i^0$ is the equilibrium position vector of particle $i$.
- $\Delta \mathbf{R}_i = \mathbf{R}_i - \mathbf{R}_i^0$ is the displacement vector of particle $i$ from equilibrium.
- $\mathbf{R}_{ij} = \mathbf{R}_j - \mathbf{R}_i$ is the instantaneous separation vector between particles $i$ and $j$.
- $\mathbf{R}_{ij}^0 = \mathbf{R}_j^0 - \mathbf{R}_i^0$ is the equilibrium separation vector between particles $i$ and $j$.
- $R_{ij} = |\mathbf{R}_{ij}|$ is the instantaneous distance between particles $i$ and $j$.
- $R_{ij}^0 = |\mathbf{R}_{ij}^0|$ is the equilibrium distance between particles $i$ and $j$.
- $\gamma$ is the uniform spring constant of the network, meaning that all connected pairs are assigned the same spring constant: $k_{ij}=\gamma$.

As before, lowercase regular symbols denote scalars, while boldface symbols denote vectors or matrices. The main difference from the two-particle case is that we now have many interacting pairs, so the total potential energy of the system is obtained by summing the contributions from all connected pairs.

For one interacting pair $(i,j)$, the harmonic potential energy is

$$
V_{ij} \approx \frac{1}{2}
\left( \mathbf{R}_{ij} - \mathbf{R}_{ij}^0 \right)^T
H_{ij}
\left( \mathbf{R}_{ij} - \mathbf{R}_{ij}^0 \right), \tag{45}

$$

where $H_{ij}$ is the $3\times 3$ Hessian matrix for the interaction between particles $i$ and $j$, evaluated at the equilibrium separation vector $\mathbf{R}_{ij}^0$.


If the interaction is isotropic and has the same curvature in every Cartesian direction, then $H_{ij}$ is proportional to the identity matrix, and Eq. 45 reduces to the simpler scalar-spring form

$$
V_{ij} = \frac{1}{2} k_{ij} \left( R_{ij} - R_{ij}^0 \right)^2. \tag{46}

$$

To write the total potential energy of the system, we sum over all interacting pairs:

$$
V_{\text{total}} =
\frac{1}{2}
\sum_{i=1}^{n}
\sum_{j=1}^{n}
A_{ij}\,
V_{ij}. \tag{47}

$$

Here $A_{ij}$ is the connectivity matrix:

$$
A_{ij} =
\begin{cases}
1, & \text{if particles } i \text{ and } j \text{ are connected}, \\
0, & \text{otherwise}.
\end{cases} \tag{48}

$$

In Gaussian network-type models, the connectivity is usually determined by a cutoff distance $r_c$: particles $i$ and $j$ are connected if their equilibrium distance satisfies $R_{ij}^0 < r_c$, and otherwise they are not connected. In that case, $A_{ij}$ encodes the network topology of the structure.

The factor of $\frac{1}{2}$ in front of the double sum avoids counting each pair twice, because the pair $(i,j)$ is the same as the pair $(j,i)$.

If all connected pairs are assigned the same spring constant $\gamma$, then Eq. 46 simplifies to

$$
V_{\text{total}} =
\frac{\gamma}{2}
\sum_{i<j}
A_{ij}\left( R_{ij} - R_{ij}^0 \right)^2. \tag{49}

$$

This is the standard harmonic potential used in many elastic network models.

This isotropic, uniform-spring approximation is the key simplification behind the Gaussian network model (GNM). In GNM, the precise direction of motion is not tracked at this stage; instead, only the network connectivity and the amplitudes of fluctuations are retained.

The force on particle $i$ is obtained from the total potential by taking the gradient with respect to $\mathbf{R}_i$:

$$
\mathbf{F}_i = -\nabla_{\mathbf{R}_i} V_{\text{total}}. \tag{50}

$$

Applying Newton's second law to each particle gives

$$
m_i \frac{d^2 \mathbf{R}_i}{dt^2} = \mathbf{F}_i = -\nabla_{\mathbf{R}_i} V_{\text{total}}, \qquad i=1,\dots,n. \tag{51}

$$

Thus, instead of one equation for a single displacement, we now have $n$ coupled vector equations, one for each particle. Since each particle has three Cartesian coordinates, the whole system has $3n$ degrees of freedom.

It is convenient to collect all particle displacements into one column vector:

$$
\Delta \mathbf{R} =
\begin{pmatrix}
\Delta \mathbf{R}_1 \\
\Delta \mathbf{R}_2 \\
\vdots \\
\Delta \mathbf{R}_n
\end{pmatrix}. \tag{52}

$$

Near equilibrium, the equations of motion can be linearized and written in matrix form as

$$
M \frac{d^2 \Delta \mathbf{R}}{dt^2} + H \Delta \mathbf{R} = \mathbf{0}, \tag{53}

$$

where $M$ is the mass matrix and $H$ is now the full $3n \times 3n$ Hessian matrix of the system.

This is the direct generalization of the 2D two-particle result. The scalar spring constant in 1D and the $2\times 2$ Hessian in 2D are both replaced by a large Hessian matrix that encodes all couplings between all Cartesian coordinates of all particles.

At this point it is helpful to distinguish two closely related models:

- In the **Gaussian network model (GNM)**, the interactions are isotropic and the main object is the connectivity, or **Kirchhoff**, matrix $\Gamma$, which captures which particles are connected to which others.
- In the **anisotropic network model (ANM)**, one keeps the full directional $3n \times 3n$ Hessian matrix $H$ and therefore obtains vector-valued normal modes.

So the present 3D derivation is the more general directional framework. GNM can be viewed as the isotropic simplification in which the direction dependence is averaged out and the network is described by $\Gamma$ rather than the full Hessian.

## Solution of Harmonic Motion for an N-particle System in 3D

To solve Eq. 53, we again try an exponential solution, now for the full $3n$-dimensional displacement vector:

$$
\Delta \mathbf{R}(t) = \mathbf{U} e^{\lambda t}, \tag{54}
$$

where $\mathbf{U}$ is a constant $3n$-dimensional vector.

Substituting Eq. 54 into Eq. 53 gives

$$
M \lambda^2 \mathbf{U} e^{\lambda t} + H \mathbf{U} e^{\lambda t} = \mathbf{0}. \tag{55}
$$

Since $e^{\lambda t} \neq 0$, we obtain

$$
H \mathbf{U} = - M \lambda^2 \mathbf{U}. \tag{56}
$$

This is the matrix generalization of the eigenvalue equation we saw in 2D. If all particles have the same mass $m$, then $M = mI$, and Eq. 56 becomes

$$
H \mathbf{U} = - m \lambda^2 \mathbf{U}. \tag{57}
$$

Therefore, $\mathbf{U}$ must be an eigenvector of the full Hessian matrix $H$, and the corresponding eigenvalue $\mu$ satisfies

$$
\mu = -m\lambda^2. \tag{58}
$$

If the eigenvalues of $H$ are $\mu_1,\mu_2,\dots,\mu_{3n}$, then the corresponding angular frequencies are

$$
\omega_k = \sqrt{\frac{\mu_k}{m}},
\qquad
k=1,2,\dots,3n. \tag{59}
$$

Each eigenvector $\mathbf{U}_k$ gives one normal mode of the entire system. The general real-valued solution can therefore be written as

$$
\Delta \mathbf{R}(t)
=
\sum_{k=1}^{3n}
\mathbf{U}_k \left[ a_k \cos(\omega_k t) + b_k \sin(\omega_k t) \right]. \tag{60}
$$

Here $a_k$ and $b_k$ are constants determined by the initial conditions.

This expression has exactly the same structure as the 2D two-particle case, except that the sum now runs over all $3n$ normal modes. Each mode describes a collective pattern of motion involving all particles in the system.

In practice, some of these modes correspond to rigid-body translations and rotations, which do not deform the structure and therefore have zero or near-zero frequency. The remaining nonzero-frequency modes describe the internal vibrations of the network and are the main objects of interest in elastic network models.

In the language of GNM, we usually do not follow the full time-dependent vector solution in Eq. 60. Instead, we use the isotropic network assumption to study fluctuation amplitudes and correlations from the inverse of the Kirchhoff matrix $\Gamma$. Thus, Eq. 60 is best viewed as the more detailed directional analogue, while GNM keeps the same network idea but focuses on scalar fluctuation statistics rather than explicit vector-valued motion.
