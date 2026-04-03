---
layout: default
title: Newton's laws of motion.
kicker: Bonus Material
lead: Optional background notes on Newton's laws, kinetic energy, and harmonic potentials for students who want more theory.
description: Newton's laws of motion.
permalink: /newton-law-of-motion/
---

## Newton's Second Law of Motion

Motion in classical mechanics starts from **Newton's second law of motion**:
```math
F = ma \tag{1}
```

where $F$ is force, $m$ is mass, and $a$ is acceleration.
This tells us that when a force acts on a particle, the particle changes its motion.

To describe motion, we first define **position** $x(t)$ as a function of time.
From position, we define **velocity** as the rate of change of position:
```math
v = \frac{dx}{dt} \tag{2}
```

and **acceleration** as the rate of change of velocity:
```math
\begin{aligned}
a &= \frac{dv}{dt} \\
  &= \frac{d^2x}{dt^2}
\end{aligned} \tag{3}
```

<p align="center"><img src="{{ '/images/week1_bonus_newtons_second_law.png' | relative_url }}" alt="Newton's second law" width="420"></p>

## Kinetic Energy

When a particle moves, it has **kinetic energy** (how fast it is moving):
```math
K = \frac{1}{2}mv^2 \tag{4}
```

<details markdown="1">
<summary><strong>Why does kinetic energy have this form?</strong></summary>

It can be written as $K=\frac{1}{2}mv^2$.

We can derive this from the definition of **work**.
If a force moves a particle by a small distance $dx$, then the small amount of work done is:

```math
dW = F \, dx \tag{5}
```

Using Newton's second law, $F = ma$, we get:
```math
dW = ma \, dx \tag{6}
```

Now use the definitions of acceleration and velocity, so that
```math
\begin{aligned}
a &= \frac{dv}{dt} \\
  &= \frac{dv}{dx}\frac{dx}{dt} \\
  &= v\frac{dv}{dx}
\end{aligned} \tag{7}
```

Substitute this into the work expression:
```math
\begin{aligned}
dW &= m\left(v\frac{dv}{dx}\right)dx \\
   &= mv \, dv
\end{aligned} \tag{8}
```

Integrating both sides gives:
```math
\begin{aligned}
W &= \int mv \, dv \\
  &= \frac{1}{2}mv^2 + C
\end{aligned} \tag{9}
```

If we choose the kinetic energy to be zero when the particle is at rest, then $C = 0$, and we obtain:
```math
K = \frac{1}{2}mv^2 \tag{10}
```

So the familiar expression for kinetic energy comes from the work done by a force in changing the speed of a particle.

</details>


Differentiating, we find for its rate of change:
```math
\begin{aligned}
\frac{dK}{dt}
&= \frac{d}{dt}\left(\frac{1}{2}mv^2\right) \\
&= \frac{d (\frac{1}{2} mv^2)}{dv} \frac{dv}{dt} \\
&= mva \\
&= ma\frac{dx}{dt} \\
&= F\frac{dx}{dt}
\end{aligned} \tag{11}
```

Therefore,
```math
dK = F\,dx \tag{12}
```

So the infinitesimal change in kinetic energy is directly connected to the force acting on the particle through an infinitesimal displacement.

Integrating with respect to time, we find
```math
\begin{aligned}
K &= \int F\,dx \\
  &= \frac{1}{2}mv^2 + C
\end{aligned} \tag{13}
```

## From Total Energy to Potential Energy

The **first law of thermodynamics** tells us that energy is neither created nor destroyed.
For a closed system, the total mechanical energy is constant, so we write

```math
E = K + V \tag{14}
```

If the total energy does not change, then its differential must satisfy
```math
dE = dK + dV = 0 \tag{15}
```
Rearranging gives

```math
dV = -dK = -F\,dx \tag{16}
```

This is the differential relation between force and potential energy. It tells us that when the force increases the kinetic energy, the potential energy must decrease by the same amount.
For a **conservative force**, this relation allows us to define the force from the potential energy function. In one dimension,
```math
F(x) = -\frac{dV(x)}{dx} \tag{17}
```

This means that the force is the negative rate of change of the potential energy with respect to position. In other words, the force points toward decreasing potential energy.

Combining Eq. 1 and Eq.3 with Eq. 17, and assuming the system follows [harmonic motion]({{ '/harmonic-potential-energy/' | relative_url }}), we obtain equation of motion
```math
\begin{aligned}
m\frac{d^2x}{dt^2} &= -\frac{dV(x)}{dx} = -kx \\
\Leftrightarrow \quad m\frac{d^2x}{dt^2} + kx &= 0
\end{aligned} \tag{18}
```

To better understand how to solve this equation, we need:
- Ordinary differential equations (ODEs)
- Euler's formula
- complex numbers and their relation to $\sin x$ and $\cos x$
