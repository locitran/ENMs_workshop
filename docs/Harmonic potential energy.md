---
layout: default
title: Harmonic Potential Energy
kicker: Bonus Material
lead: Additional notes on harmonic oscillators and the relationship between force and potential energy.
description: Harmonic potential energy notes.
permalink: /harmonic-potential-energy/
---

<details>
    <summary>
        <span style="font-size: 18px;">
        <strong>Harmonic Oscillator</strong>
        </span>
    </summary>

A very important model in physics is the **harmonic oscillator**.
Here, **oscillator** means a system that moves back and forth around an equilibrium position. **Harmonic** means that the restoring force is linearly proportional to the displacement from equilibrium.

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

![Harmonic oscillator](<../images/week1_bonus_harmonic_oscillator.png>)

</details>

<details>
    <summary><span style="font-size: 18px;"><strong>Harmonic Approximation Near Equilibrium</strong></span></summary>

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

![Harmonic approximation](<../images/week1_bonus_harmonic_approximation.png>)

Reference:
Tom W. B. Kibble and Frank H. Berkshire, *Classical Mechanics*, Chapter 2: Linear Motion, Sections 2.1 and 2.2.

</details>

</details>

<details>
    <summary>
        <span style="font-size: 24px;">
            <strong>Mode, vibrational frequency, and vibrational mode</strong>
        </span>
    </summary>

<details>
    <summary>
        <span style="font-size: 18px;">
            <strong>Overview</strong>
        </span>
    </summary>

This section will summarize what a mode is, how vibrational frequency is defined, and what is meant by a vibrational mode.

</details>

</details>

<details>
    <summary>
        <span style="font-size: 24px;">
            <strong>Normal mode analysis</strong>
        </span>
    </summary>

<details>
    <summary>
        <span style="font-size: 18px;">
            <strong>Overview</strong>
        </span>
    </summary>

This section will introduce the basic idea of normal mode analysis and how it is used to describe collective motions.

</details>

</details>
