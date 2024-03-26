import json
import re

import json
import re

# Define the preamble and document setup for LaTeX
latex_preamble = r"""
\documentclass[a5paper, 12pt]{memoir}
\usepackage[T1]{fontenc}
\usepackage{microtype}
\usepackage{lettrine}
\usepackage{xcolor}
\usepackage{fontspec}
\usepackage[english]{babel}
\usepackage{graphicx}
\usepackage{eso-pic}% www.ctan.org/pkg/eso-pic
\usepackage{letltxmacro}
\usepackage{rotating}
\usepackage{caption}
\usepackage{alltt}
\usepackage{eso-pic}
%\usepackage{imfellEnglish}
\usepackage{ebgaramond}

\setlength{\parskip}{0pt}

\chapterstyle{bianchi}
\semiisopage[10]
\makepagestyle{mypage}
\makeoddfoot{mypage}{}{}{\thepage}
\makeevenfoot{mypage}{\thepage}{}{}
\setulmargins{0.7in}{*}{*}

\checkandfixthelayout

\renewcommand{\chapnumfont}{\HUGE}
\renewcommand{\chaptitlefont}{\HUGE\swshape\color{black}}
\setsecheadstyle{\Huge\scshape\memRTLraggedright}

\let\oldafterchapternum\afterchapternum
\let\oldafterchaptertitle\afterchaptertitle

\makeatletter
\makeatother

\setlength\fboxsep{0pt}
\hyphenation{Gryph-on}

\begin{document}
\pagestyle{empty}
\setcounter{secnumdepth}{0}
\frontmatter
\makeevenhead{ruled}{\scshape\leftmark}{}{}
\makeoddhead{ruled}{}{}{\scshape\rightmark}
\renewcommand{\chaptermark}[1]{\markboth{#1}{}}

\clearpage \null
  \vfill
  \hfill 

  \resizebox{0.85\textwidth}{!}{\HUGE \swshape \qquad Cleric's spellbook} \hfill\hfill
    
    \vspace{1\baselineskip}
  \hfill
  {\color{white}\swshape }
  \hfill\hfill
  \vfill\vfill

\cleartooddpage

\mainmatter
\counterwithout{figure}{chapter}
\pagestyle{ruled}
"""

# Load spells data
with open('cleric_spells.json') as file:
    data = json.load(file)

with open('clericSpells.tex', 'w') as f:
    f.write(latex_preamble)  # Write the preamble to the LaTeX file

    for lvl in range(0, 10):  # Assuming 0 for Cantrips and 1-9 for spell levels
        if lvl == 0:
            chapter = "\\chapter*{Cantrips} \\markboth{Cantrips}{Cantrips}"
        else:
            chapter = f"\\chapter*{{Level {lvl}}} \\markboth{{Level {lvl}}}{{Level {lvl}}}"
        print(chapter, file=f)

        for spell in data:
            spell_level = 0 if spell["level"] == "Cantrip" else int(spell["level"])
            if spell_level == lvl:
                print("\\section*{" + spell['name'], file=f, end='')
                if spell.get("ritual", "no") == "yes":
                    print("\\hfill (Ritual)", file=f, end='')
                print("}", file=f)

                # Join the description list into a single string
                description = ' '.join(spell["desc"])
                # Escape LaTeX special characters
                description = re.sub(r'([&$#_])', r'\\\1', description)
                # Bold markup for **text**
                description = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', description)

                print(description + "\n", file=f)

                if "higher_level" in spell and spell["higher_level"]:
                    higher_level = ' '.join(spell["higher_level"])
                    higher_level = re.sub(r'([&$#_])', r'\\\1', higher_level)
                    print("\\vspace{8pt} \\noindent\\textbf{At Higher Levels:} " + higher_level, file=f)

                components = ", ".join(spell["components"])
                if "M" in spell["components"]:
                    material = spell.get("material", "N/A")
                    material = re.sub(r'([&$#_])', r'\\\1', material)
                    components += f" ({material})"

                tableHeader = \
"""
{
\\begin{center}
\\small
\\begin{tabular}{rlrl}
\\toprule
"""
                tableFooter = \
"""
\\bottomrule
\\end{tabular}
\\end{center}
}
"""
                print(tableHeader, file=f)
                print(f"\\textbf{{Duration:}} & {spell['duration']} &", file=f)
                print(f"\\textbf{{Casting Time:}} & {spell['casting_time']} \\\\", file=f)
                print(f"\\textbf{{Concentration:}} & {spell['concentration']} &", file=f)
                print(f"\\textbf{{Range:}} & {spell['range']} \\\\", file=f)
                print(f"\\textbf{{Components:}} & {components} &", file=f)
                print(f"\\textbf{{School:}} & {spell['school']['name']} \\\\", file=f)

                if "material" in spell and spell["material"]:
                    material = spell["material"]
                    material = re.sub(r'([&$#_])', r'\\\1', material)
                    print(f"\\textbf{{Material:}} & \\multicolumn{{3}}{{p{{0.7\\textwidth}}}}{{{material}}}\\\\", file=f)

                print(tableFooter, file=f)
                print("\\newpage", file=f)

# Write the end of the document
    f.write("\n\\end{document}")
