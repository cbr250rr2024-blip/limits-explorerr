import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Limits Explorer", layout="centered")

# Title
st.title("📘 Limits Explorer")
st.write("Learn limits step-by-step, visualize graphs, and understand function behavior.")

# Input
st.header("Enter a Function")
user_input = st.text_input("Enter a function in terms of x (e.g., (x**2-1)/(x-1), sin(x)/x):", "(x**2-1)/(x-1)")
point = st.number_input("Find the limit as x approaches:", value=1.0)

x = sp.symbols('x')

try:
    expr = sp.sympify(user_input)
    a = sp.sympify(point)

    left_limit = sp.limit(expr, x, a, '-')
    right_limit = sp.limit(expr, x, a, '+')
    general_limit = sp.limit(expr, x, a)

    # ── SECTION 1 ──────────────────────────────────────────
    st.header("1️⃣ The Function f(x)")
    st.write("First, we identify the **function being analyzed**.")
    st.write("A function *f* maps elements from a **domain** to a **range**. "
             "When discussing limits, we study how the function behaves **near a certain point**, "
             "even if the function may not be defined at that point.")
    st.write("**Example:**")
    st.latex(f"f(x) = {sp.latex(expr)}")
    st.write(f"Here we investigate how the function behaves **as x approaches {a}**, "
             f"even though the function may be undefined at x = {a}.")

    # ── SECTION 2 ──────────────────────────────────────────
    st.header("2️⃣ The Point of Approach a")
    st.write("The limit investigates what happens when the "
             "**independent variable approaches a specific value**.")
    st.latex(f"\\lim_{{x \\to a}} f(x)")
    st.write(f"The important idea is that x gets **arbitrarily close to {a}** "
             f"but does **not necessarily equal {a}**.")
    st.write("**Example:**")
    st.latex(f"\\lim_{{x \\to {a}}} {sp.latex(expr)}")
    st.write(f"We examine the behavior **near x = {a}**.")

    # ── SECTION 3 ──────────────────────────────────────────
    st.header("3️⃣ The Limit Value L")
    st.write("The limit value is the **number that f(x) approaches** as x gets closer to a.")
    st.write("Formally we say:")
    st.latex("\\lim_{x \\to a} f(x) = L")
    st.write("if the function values become **arbitrarily close to L** whenever x is sufficiently close to a.")

    st.write("**Left-hand limit:**")
    st.latex(f"\\lim_{{x \\to {a}^-}} f(x) = {sp.latex(left_limit)}")
    st.write("**Right-hand limit:**")
    st.latex(f"\\lim_{{x \\to {a}^+}} f(x) = {sp.latex(right_limit)}")

    if left_limit == right_limit:
        st.success(f"✅ Since both sides are equal, the limit EXISTS!")
        st.latex(f"\\lim_{{x \\to {a}}} {sp.latex(expr)} = {sp.latex(general_limit)}")
        st.write(f"Even though the function may be undefined at x = {a}, "
                 f"the values of f(x) approach **{general_limit}**.")
    else:
        st.error("❌ The limit DOES NOT EXIST — left-hand and right-hand limits are different.")

    # ── SECTION 4 ──────────────────────────────────────────
    st.header("4️⃣ The ε−δ (Epsilon-Delta) Condition")
    st.write("At the university level, limits are **formally defined** using the ε−δ definition.")
    st.latex(r"\lim_{x \to a} f(x) = L \iff \forall\varepsilon > 0,\ \exists\delta > 0 \text{ such that if } 0 < |x - a| < \delta,\ \text{then } |f(x) - L| < \varepsilon")
    st.write("**Meaning:**")
    st.markdown("- **ε (epsilon)** represents how close the function value must be to *L*.")
    st.markdown("- **δ (delta)** represents how close x must be to *a*.")
    st.markdown("- If we can always find such a δ for every ε, the **limit exists**.")

    # ── GRAPH ──────────────────────────────────────────────
    st.header("5️⃣ Graph")
    f_lambdified = sp.lambdify(x, expr, 'numpy')
    x_vals = np.linspace(float(a) - 5, float(a) + 5, 400)
    with np.errstate(divide='ignore', invalid='ignore'):
        y_vals = f_lambdified(x_vals)
        y_vals = np.where(np.abs(y_vals) > 100, np.nan, y_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label='f(x)', color='cyan')
    ax.axvline(float(a), color='red', linestyle='--', label=f'x = {a}')
    ax.axhline(0, color='white', linewidth=0.5)
    ax.axvline(0, color='white', linewidth=0.5)
    ax.legend()
    ax.set_title(f"Graph of f(x) near x = {a}")
    ax.set_facecolor('#0e1117')
    fig.patch.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    ax.title.set_color('white')
    st.pyplot(fig)

except Exception as e:
    st.error("Invalid function. Please try again.")
    st.text(str(e))

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit & SymPy")
