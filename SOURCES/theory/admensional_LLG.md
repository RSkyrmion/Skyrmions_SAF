# Processo de Adimensionalização da Equação Micromagnética de Landau-Lifshitz-Gilbert (LLG)

Este documento detalha passo a passo o processo de renormalização micromagnética e adimensionalização da equação dinâmica de Landau-Lifshitz-Gilbert (LLG) com inclusão de torque de transferência de spin (termos adiabático e não-adiabático), conforme descrito no texto fornecido.

---

## 1. Contexto e Motivação Micromagnética

Em uma nanofita magnética real, o número total de momentos magnéticos atômicos é extremamente elevado (da ordem de $\sim 10^7$), tornando a integração numérica direta computacionalmente inviável.

A **aproximação micromagnética** redefine o sistema em células de trabalho de volume $v_{\text{cel}} = a^3$, onde $a$ é o parâmetro de rede da nova célula de trabalho e $a_0$ é o parâmetro de rede atômico. O número de momentos magnéticos representados em cada célula é:

$$N_{\text{momentos}} = 4 \left( \frac{a^3}{a_0^3} \right)$$

O tamanho da célula $a$ deve satisfazer a condição $a \le \lambda_{\text{tr}}$, onde $\lambda_{\text{tr}}$ é o **comprimento de troca** (*exchange length*), definido por:

$$\lambda_{\text{tr}} = \sqrt{\frac{2A}{\mu_0 M_s^2}}$$

- $A$: constante de troca do material.
- $M_s$: magnetização de saturação.
- $\mu_0$: permeabilidade do vácuo.

Sob essa condição, a magnetização dentro de cada célula está saturada, permitindo escrever o momento magnético da célula como:

$$\vec{m}_i = m_i \hat{m}_i = v_{\text{cel}} M_s \hat{m}_i$$

sendo $\hat{m}_i$ o versor unitário na direção da magnetização ($|\hat{m}_i| = 1$) e $m_i = |\vec{m}_i| = v_{\text{cel}} M_s$.

---

## 2. Hamiltoniana Micromagnética e Adimensionalização da Energia

A energia total do sistema magnético discretizado inclui contribuições de troca e dipolar:

1. **Energia de Troca:**
   $$U^{\text{tr}} = -\frac{J_{\text{cel}}}{2} \sum_{\langle i,j \rangle} \hat{m}_i \cdot \hat{m}_j$$
   onde $J_{\text{cel}} = 2aA$ é a constante de acoplamento renormalizada entre células.

2. **Energia Dipolar:**
   $$U^{\text{dip}} = \frac{1}{2} D_{\text{cel}} \sum_{i=1}^N \sum_{j=1}^N \left[ \frac{\hat{m}_i \cdot \hat{m}_j - 3(\hat{m}_i \cdot \hat{r}_{ij})(\hat{m}_j \cdot \hat{r}_{ij})}{(r_{ij}/a)^3} \right]$$
   com o parâmetro dipolar de célula $D_{\text{cel}}$ dado por:
   $$D_{\text{cel}} = \frac{\mu_0 m_i^2}{4\pi a^3} = \frac{\mu_0 M_s^2 a^3}{4\pi} = \frac{1}{4\pi} \left( \frac{a}{\lambda_{\text{tr}}} \right)^2 J_{\text{cel}}$$

Colocando o fator $J_{\text{cel}}/2$ em evidência, a Hamiltoniana total pode ser fatorada em uma escala de energia e uma **Hamiltoniana adimensional** $U'$:

$$U = \frac{J_{\text{cel}}}{2} U'$$

com:

$$U' = -\sum_{\langle i,j \rangle} \hat{m}_i \cdot \hat{m}_j + \frac{1}{4\pi}\left( \frac{a}{\lambda_{\text{tr}}} \right)^2 \sum_{i=1}^N \sum_{j=1}^N \left[ \frac{\hat{m}_i \cdot \hat{m}_j - 3(\hat{m}_i \cdot \hat{r}_{ij})(\hat{m}_j \cdot \hat{r}_{ij})}{(r_{ij}/a)^3} \right]$$

---

## 3. Campo Efetivo Adimensional

O campo efetivo local $\vec{B}_i^{\text{eff}}$ (em Tesla) é obtido a partir da derivada funcional da Hamiltoniana:

$$\vec{B}_i^{\text{eff}} = -\frac{\partial U}{\partial \vec{m}_i} = -\frac{J_{\text{cel}}}{m_i} \frac{\partial U'}{\partial \hat{m}_i} = \frac{J_{\text{cel}}}{m_i} \vec{b}_i^{\text{eff}}$$

onde $\vec{b}_i^{\text{eff}}$ é o **campo efetivo local adimensional**:

$$\vec{b}_i^{\text{eff}} = \sum_{j \ne i}^N C_{ij} \hat{m}_j - \frac{1}{4\pi}\left( \frac{a}{\lambda_{\text{tr}}} \right)^2 \sum_{j \ne i}^N \left[ \frac{\hat{m}_j - 3\hat{r}_{ij}(\hat{m}_j \cdot \hat{r}_{ij})}{(r_{ij}/a)^3} \right]$$

sendo $C_{ij} = 1$ para primeiros vizinhos e $0$ para os demais casos.

---

## 4. Equação Dinâmica com Torque de Transferência de Spin (STT)

A dinâmica do momento magnético $\vec{m}_i$ sob ação de campo magnético e corrente elétrica polarizada em spin (com velocidade de deriva $v_j$ e coeficiente não-adiabático $\xi$, onde $c_j = \xi v_j$) é descrita originalmente por:

$$\frac{d\vec{m}_i}{dt} = -\gamma \vec{m}_i \times \vec{B}_i^{\text{eff}} + \frac{\alpha}{m_i} \vec{m}_i \times \frac{d\vec{m}_i}{dt} - \frac{v_j}{m_i^2} \vec{m}_i \times \left( \vec{m}_i \times \frac{d\vec{m}_i}{dx} \right) - \frac{c_j}{m_i} \vec{m}_i \times \frac{d\vec{m}_i}{dx}$$

### Passo 1: Eliminação do termo implícito de amortecimento
Calculando o produto vetorial de $\frac{\alpha}{m_i} \vec{m}_i$ com a própria equação e usando a identidade vetorial $\vec{m}_i \times (\vec{m}_i \times \frac{d\vec{m}_i}{dt}) = -m_i^2 \frac{d\vec{m}_i}{dt}$, obtém-se:

$$(1+\alpha^2) \frac{d\vec{m}_i}{dt} = -\gamma \vec{m}_i \times \vec{B}_i^{\text{eff}} - \frac{\alpha\gamma}{m_i} \vec{m}_i \times (\vec{m}_i \times \vec{B}_i^{\text{eff}}) - \frac{\alpha v_j}{m_i^3} \vec{m}_i \times \left[ \vec{m}_i \times \left( \vec{m}_i \times \frac{d\vec{m}_i}{dx} \right) \right] - \left[ \left( \frac{\alpha c_j + v_j}{m_i^2} \right) \vec{m}_i \times \left( \vec{m}_i \times \frac{d\vec{m}_i}{dx} \right) \right] - \frac{c_j}{m_i} \vec{m}_i \times \frac{d\vec{m}_i}{dx}$$

### Passo 2: Introdução do campo adimensional e frequência característica
Substituindo $\vec{B}_i^{\text{eff}} = \frac{J_{\text{cel}}}{m_i} \vec{b}_i^{\text{eff}}$ e definindo a frequência angular característica de precessão:

$$\omega_0 = \frac{\gamma J_{\text{cel}}}{m_i}$$

A equação passa a ser:

$$(1+\alpha^2) \frac{d\vec{m}_i}{dt} = -\omega_0 \vec{m}_i \times \vec{b}_i^{\text{eff}} - \frac{\omega_0 \alpha}{m_i} \vec{m}_i \times (\vec{m}_i \times \vec{b}_i^{\text{eff}}) - \frac{\alpha v_j}{m_i^3} \vec{m}_i \times \left[ \vec{m}_i \times \left( \vec{m}_i \times \frac{d\vec{m}_i}{dx} \right) \right] - \left[ \left( \frac{\alpha c_j + v_j}{m_i^2} \right) \vec{m}_i \times \left( \vec{m}_i \times \frac{d\vec{m}_i}{dx} \right) \right] - \frac{c_j}{m_i} \vec{m}_i \times \frac{d\vec{m}_i}{dx}$$

### Passo 3: Normalização dos momentos e introdução de $c_j = \xi v_j$
Dividindo ambos os lados por $\omega_0$ e substituindo $\vec{m}_i = m_i \hat{m}_i$ (com $m_i$ constante no tempo e no espaço celular):

$$\frac{1+\alpha^2}{\omega_0} \frac{d\hat{m}_i}{dt} = -\hat{m}_i \times \vec{b}_i^{\text{eff}} - \alpha \hat{m}_i \times (\hat{m}_i \times \vec{b}_i^{\text{eff}}) - \frac{\alpha v_j}{\omega_0} \hat{m}_i \times \left[ \hat{m}_i \times \left( \hat{m}_i \times \frac{d\hat{m}_i}{dx} \right) \right] - \left[ \left( \frac{\xi \alpha + 1}{\omega_0} \right) v_j \hat{m}_i \times \left( \hat{m}_i \times \frac{d\hat{m}_i}{dx} \right) \right] - \frac{\xi v_j}{\omega_0} \hat{m}_i \times \frac{d\hat{m}_i}{dx}$$

### Passo 4: Variáveis Adimensionais de Tempo e Espaço
Definem-se as variáveis adimensionais:
- **Tempo adimensional:** $d\tau = \omega_0 dt \implies \tau = \omega_0 t$
- **Espaço adimensional:** $dx' = \frac{dx}{a} \implies \frac{\partial}{\partial x} = \frac{1}{a} \frac{\partial}{\partial x'}$
- **Parâmetro de velocidade adimensional:** $\tilde{v} = \frac{v_j}{\omega_0 a}$

Substituindo essas relações, obtém-se a **Equação de Landau-Lifshitz-Gilbert Adimensionalizada**:

$$\frac{d\hat{m}_i}{d\tau} = \frac{1}{1+\alpha^2} \left\{ -\hat{m}_i \times \vec{b}_i^{\text{eff}} - \alpha \hat{m}_i \times (\hat{m}_i \times \vec{b}_i^{\text{eff}}) - \alpha \left( \frac{v_j}{\omega_0 a} \right) \hat{m}_i \times \left[ \hat{m}_i \times \left( \hat{m}_i \times \frac{d\hat{m}_i}{dx'} \right) \right] - (\xi \alpha + 1) \left( \frac{v_j}{\omega_0 a} \right) \hat{m}_i \times \left( \hat{m}_i \times \frac{d\hat{m}_i}{dx'} \right) - \xi \left( \frac{v_j}{\omega_0 a} \right) \hat{m}_i \times \frac{d\hat{m}_i}{dx'} \right\}$$

---

## 5. Resumo das Grandezas Adimensionais e Relações de Escala

| Grandeza Original | Grandeza Adimensional | Fator de Escala / Definição |
| :--- | :--- | :--- |
| Momento Magnético $\vec{m}_i$ | Versor $\hat{m}_i$ | $\hat{m}_i = \vec{m}_i / (v_{\text{cel}} M_s)$ |
| Energia Total $U$ | Energia Adimensional $U'$ | $U' = \frac{2}{J_{\text{cel}}} U$, com $J_{\text{cel}} = 2aA$ |
| Campo Efetivo $\vec{B}_i^{\text{eff}}$ (Tesla) | Campo Adimensional $\vec{b}_i^{\text{eff}}$ | $\vec{b}_i^{\text{eff}} = \frac{m_i}{J_{\text{cel}}} \vec{B}_i^{\text{eff}}$ |
| Tempo $t$ (segundos) | Tempo Adimensional $\tau$ | $\tau = \omega_0 t$, com $\omega_0 = \frac{\gamma J_{\text{cel}}}{m_i}$ |
| Posição $x$ (metros) | Posição Adimensional $x'$ | $x' = x / a$ |
| Velocidade de Spin $v_j$ | Velocidade Adimensional | $\frac{v_j}{\omega_0 a}$ |
| Razão Dipolar / Troca | Peso da interação dipolar | $\frac{D_{\text{cel}}}{J_{\text{cel}}} = \frac{1}{4\pi} \left( \frac{a}{\lambda_{\text{tr}}} \right)^2$ |
