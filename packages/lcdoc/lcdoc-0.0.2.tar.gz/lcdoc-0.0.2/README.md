# lcdoc
LC documentation generator

### Markup Features
 - sub-documentation for each member
 - authomatic code blocks and inline code blocks highlighting using [highlightjs](https://highlightjs.org/)
   ````md
   ```cpp
   int i = 42
   ```
   ````
 - manual syntax highlighting support using user friendly `<code-*>` tags
   ```html
   <pre><code>
       <code-keyword>int</code-keyword> <code-var>i</code-var> = <code-number>42</code-number>;
   </code></pre>
   ```
  - LaTex equations rendering using [tex-math](https://www.npmjs.com/package/tex-math) package (based on [katex](https://www.npmjs.com/package/katex)) :
    ```html
    inline equation: <i-math>x^2</i-math>
    equation:
    <tex-math>
        i \hbar \frac{\partial}{\partial t} \psi = H \psi
    </tex-math>
    ```

## dependencies:

We use `libclang` [Python binding](https://pypi.org/project/libclang/), doc [here](https://libclang.readthedocs.io/en/latest/), [see also](https://sudonull.com/post/907-An-example-of-parsing-C-code-using-libclang-in-Python)