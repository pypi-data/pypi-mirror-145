# table from: https://github.com/marhop/pandoc-unicode-math/blob/master/src/Symbols.hs
unicode_to_latex =\
    { '¬': "\\neg"
    , '±': "\\pm"
    , '×': "\\times"
    , '÷': "\\div"
    , '…': "\\dots"
    , 'ℕ': "\\mathbb{N}"
    , 'ℚ': "\\mathbb{Q}"
    , 'ℝ': "\\mathbb{R}"
    , 'ℤ': "\\mathbb{Z}"
    , 'ℂ': "\\mathbb{C}"
    , '←': "\\leftarrow"
    , '↑': "\\uparrow"
    , '→': "\\rightarrow"
    , '↓': "\\downarrow"
    , '↔': "\\leftrightarrow"
    , '⇐': "\\Leftarrow"
    , '⇒': "\\Rightarrow"
    , '⇔': "\\Leftrightarrow"
    , '↦': "\\mapsto"
    , '∀': "\\forall"
    , '∃': "\\exists"
    , '∅': "\\emptyset"
    , '∈': "\\in"
    , '∉': "\\notin"
    , '∋': "\\ni"
    , '∎': "\\blacksquare"
    , '∫': "\\int"
    , '∑': "\\sum"
    , '√': "\\sqrt"
    , '∂': "\\partial"
    , '∓': "\\mp"
    , '∗': "\\ast"
    , '∘': "\\circ"
    , '∙': "\\bullet"
    , '∝': "\\propto"
    , '∞': "\\infty"
    , '∥': "\\parallel"
    , '∡': "\\measuredangle"
    , '∧': "\\land"
    , '∨': "\\lor"
    , '∩': "\\cap"
    , '∪': "\\cup"
    , '⟨': "\\langle"
    , '⟩': "\\rangle"
    , '∴': "\\therefore"
    , '∵': "\\because"
    , '≈': "\\approx"
    , '≠': "\\neq"
    , '≡': "\\equiv"
    , '≤': "\\leq"
    , '≥': "\\geq"
    , '⊂': "\\subset"
    , '⊃': "\\supset"
    , '⊆': "\\subseteq"
    , '⊇': "\\supseteq"
    , '⊢': "\\vdash"
    , '⊤': "\\top"
    , '⊥': "\\bot"
    , '⊨': "\\vDash"
    , '⋅': "\\cdot"
    , '⋮': "\\vdots"
    , '⋯': "\\cdots"
    , 'ℵ': "\\aleph"
    , 'α': "\\alpha"
    , 'Α': "A"
    , 'β': "\\beta"
    , 'Β': "B"
    , 'γ': "\\gamma"
    , 'Γ': "\\Gamma"
    , 'δ': "\\delta"
    , 'Δ': "\\Delta"
    , 'ε': "\\varepsilon"
    , 'ϵ': "\\epsilon"
    , 'Ε': "E"
    , 'ζ': "\\zeta"
    , 'Ζ': "Z"
    , 'η': "\\eta"
    , 'Η': "H"
    , 'θ': "\\theta"
    , 'ϑ': "\\vartheta"
    , 'Θ': "\\Theta"
    , 'ι': "\\iota"
    , 'Ι': "I"
    , 'κ': "\\kappa"
    , 'ϰ': "\\varkappa"
    , 'Κ': "K"
    , 'λ': "\\lambda"
    , 'Λ': "\\Lambda"
    , 'μ': "\\mu"
    , 'Μ': "M"
    , '∇': "\\nabla"
    , 'ν': "\\nu"
    , 'Ν': "N"
    , 'ξ': "\\xi"
    , 'Ξ': "\\Xi"
    , 'ο': "o"
    , 'Ο': "O"
    , 'π': "\\pi"
    , 'Π': "\\Pi"
    , 'ρ': "\\rho"
    , 'ϱ': "\\varrho"
    , 'Ρ': "P"
    , 'σ': "\\sigma"
    , 'ς': "\\varsigma"
    , 'Σ': "\\Sigma"
    , 'τ': "\\tau"
    , 'Τ': "T"
    , 'υ': "\\upsilon"
    , 'Υ': "\\Upsilon"
    , 'φ': "\\varphi"
    , 'ϕ': "\\phi"
    , 'Φ': "\\Phi"
    , 'χ': "\\chi"
    , 'Χ': "X"
    , 'ψ': "\\psi"
    , 'Ψ': "\\Psi"
    , 'ω': "\\omega"
    # - D: not switch order of the two "\\Omega" entries! The /last/ one is use
    # - i: latexToUnicodeMap, which is what we want
    , 'Ω': "\\Omega"
    , 'Ω': "\\Omega"}

#%%
latex_to_unicode = {v:k for k,v in unicode_to_latex.items()}


def unicode_to_latex_file(fnin,fnout=None,is_verbose=False):
    if fnout is None:
        fnout = fnin
    with open(fnin,'r+') as f:
        txt = f.read()

        for U,L in unicode_to_latex.items():
            newtxt = txt.replace(U,L)
            if txt != newtxt:
                if is_verbose: print(f'replaced {U} with {L}')
                txt = newtxt
    
    with open(fnout,'w') as f:
        f.write(txt)
        
if __name__ == '__main__':
    unicode_to_latex_file('../tests/simple_file.md','../tests/simple_file_out.md')


# # Test script:
# import markdown_manuscript_filters as mmf 
# mmf.unicode_to_latex_file('tests/simple_file.md','tests/simple_file_out.md')
# python -c "import markdown_manuscript_filters as mmf; mmf.unicode_to_latex_file('tests/simple_file.md','tests/simple_file_out.md',is_verbose=True)"