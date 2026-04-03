---
layout: default
title: Harmonic Potential Energy
kicker: Bonus Material
lead: Additional notes on harmonic oscillators and the relationship between force and potential energy.
description: Harmonic potential energy notes.
permalink: /harmonic-potential-energy/
---

## Harmonic Motion

A very important model in physics is **harmonic motion**.
Here, the system moves back and forth around an equilibrium position.
The word *harmonic* means that the restoring force is linearly proportional to the displacement from equilibrium.

In other words, when the particle is displaced farther from equilibrium, the restoring force becomes proportionally larger.
Here, the restoring force is proportional to the displacement from equilibrium:

```math
F = -k(x-x_0) \tag{18}
```

where `k` is the spring constant and `x_0` is the equilibrium position.
The minus sign means the force always pulls the particle back toward equilibrium.

Using the relation between force and potential energy,

```math
F(x) = -\frac{dV}{dx} \tag{19}
```

we get:

```math
-\frac{dV}{dx} = -k(x-x_0) \tag{20}
```

so

```math
\frac{dV}{dx} = k(x-x_0) \tag{21}
```

Integrating with respect to `x`,

```math
V(x) = \frac{1}{2}k(x-x_0)^2 + C \tag{22}
```

where `C` is a constant.
Usually we choose the zero of energy so that `C=0`, giving:

<div style="border: 2px solid #c55a11; border-radius: 8px; padding: 10px 14px; margin: 12px 0; background: #fff9f4;">

```math
V(x) = \frac{1}{2}k(x-x_0)^2 \tag{23}
```

</div>

This is the **harmonic potential**.
It is a parabola centered at the equilibrium position `x_0`.

![Harmonic oscillator]({{ '/images/week1_bonus_harmonic_oscillator.png' | relative_url }})

## Second Approximation of Potential Energy of Harmonic Motion

For a general potential energy function `V(x)`, we often do not know the exact form.
However, near an equilibrium position `x_0`, we can expand it in a Taylor series:

```math
V(x) = V(x_0) + \left.\frac{dV}{dx}\right|_{x_0}(x-x_0)
+ \frac{1}{2}\left.\frac{d^2V}{dx^2}\right|_{x_0}(x-x_0)^2 + \cdots \tag{24}
```

At equilibrium,

```math
\left.\frac{dV}{dx}\right|_{x_0} = 0 \tag{25}
```

so the linear term disappears.
Then, close to equilibrium, the potential energy can be approximated as:

```math
V(x) \approx V(x_0) + \frac{1}{2}\left.\frac{d^2V}{dx^2}\right|_{x_0}(x-x_0)^2 \tag{26}
```

If we define

```math
k = \left.\frac{d^2V}{dx^2}\right|_{x_0} \tag{27}
```

then the approximation becomes:

```math
V(x) \approx V(x_0) + \frac{1}{2}k(x-x_0)^2 \tag{28}
```

If we further choose `V(x_0)=0`, then we recover the familiar harmonic form:

```math
V(x) \approx \frac{1}{2}k(x-x_0)^2 \tag{29}
```

This is why the harmonic oscillator is so important.
Even when the true potential is complicated, near equilibrium it can often be approximated by a harmonic potential.
This is the key idea behind normal mode analysis and elastic network models.

![Harmonic approximation]({{ '/images/week1_bonus_harmonic_approximation.png' | relative_url }})

Reference:
Tom W. B. Kibble and Frank H. Berkshire, *Classical Mechanics*, Chapter 2: Linear Motion, Sections 2.1 and 2.2.

## Solution of Harmonic Motion

To solve the motion, combine Newton's second law with the harmonic restoring force:

```math
\begin{aligned}
m\frac{d^2x}{dt^2} &= F \\
                   &= -k(x-x_0)
\end{aligned}
```

If we shift the coordinate so that the equilibrium position is at the origin, then $x_0 = 0$, and the equation becomes

```math
m\frac{d^2x}{dt^2} + kx = 0 \tag{30}
```

We may view Eq. 30 as a [linear differential equation]({{ '/linear-differential-equation/' | relative_url }}) of the general form
```math
a_2(t)x'' + a_1(t)x' + a_0(t)x = b(t),
```
where $a_2(t) = m$, $a_1(t) = 0$, $a_0(t) = k$, and $b(t) = 0$.

This is therefore a **second-order linear homogeneous differential equation**.

Instead of asking only how to manipulate Eq. 30, we can ask a more mathematical question: which function $x(t)$ makes the differential operator vanish?

The differential operator is $L[x] = m\frac{d^2x}{dt^2} + kx$. Then the equation of motion becomes
```math
L[x] = m\frac{d^2x}{dt^2} + kx = 0 \tag{31}
```

So the problem is to find all functions $x(t)$ that are sent to zero by the operator $L$.

A standard trial solution is to set $x(t) = e^{\lambda t}$. Then Eq. 31 becomes
 ```math
m \lambda^2 e^{\lambda t} + k e^{\lambda t} = 0 \tag{32}
```

Since $e^{\lambda t}$ is never zero, we can divide both sides by it and obtain
```math
\begin{aligned}
m\lambda^2 + k &= 0 \Leftrightarrow \lambda^2 = -\frac{k}{m} \\
\Rightarrow \lambda &= \pm i\sqrt{\frac{k}{m}} = \pm i \omega \qquad (\omega=\sqrt{\frac{k}{m}})
\end{aligned} \tag{33}
```

Therefore, the exponential solutions are
```math
x(t) = e^{i\omega t}  \qquad\text{and}\qquad x(t) = e^{-i\omega t} \tag{34}
```

Using [Euler's formula](https://en.wikipedia.org/wiki/Euler%27s_formula),

```math
\begin{aligned}
e^{i\omega t} &= \cos(\omega t) + i\sin(\omega t) \\
e^{-i\omega t} &= \cos(\omega t) - i\sin(\omega t)
\end{aligned}
```

we can rewrite the general real-valued solution as

```math
x(t) = a\cos(\omega t) + b\sin(\omega t) \tag{35}
```
, where $a$ and $b$ are constants determined by the initial conditions.

This is the standard 1D solution for harmonic motion.
It tells us that the particle oscillates with angular frequency

```math
\omega = \sqrt{\frac{k}{m}} \tag{36}
```

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Angularvelocity.svg/3840px-Angularvelocity.svg.png" alt="Angular frequency diagram" width="420">
</p>

*Figure source:* [Simple English Wikipedia: Angular frequency](https://simple.wikipedia.org/wiki/Angular_frequency##/media/File:Angularvelocity.svg)

In general physics, **angular frequency** $\omega$ measures how fast a system moves through an angle or phase.
For an object rotating around a circle, it is defined by

```math
\omega = \frac{d\theta}{dt}
```

where $\theta$ is the angle swept out in time $t$.
So a larger $\omega$ means the system moves through its cycle more quickly.

In the figure, the rotating radius sweeps out an angle $\theta$.
As time passes, the angle changes continuously, and $\omega$ tells us how rapidly that change happens.
This is why angular frequency is commonly associated with rotation.

For our **two-particle motion in 1D**, the particles do not literally move in a circle.
However, the solution

```math
x(t) = a\cos(\omega t) + b\sin(\omega t)
```

still contains the phase $\omega t$.
That phase plays the same mathematical role as an angle in circular motion.
So even though the motion is back-and-forth along one line, $\omega$ still measures how fast the oscillation goes through one cycle.

This is the connection:

- in circular motion, $\omega$ measures how fast the angle changes
- in harmonic motion, $\omega$ measures how fast the oscillation phase changes
- mathematically, both are described by sine and cosine functions

That is why the quantity

```math
\omega = \sqrt{\frac{k}{m}}
```

is called the **angular frequency** of the two-particle harmonic motion.

So:

- a larger spring constant $k$ gives a faster oscillation
- a larger mass $m$ gives a slower oscillation
