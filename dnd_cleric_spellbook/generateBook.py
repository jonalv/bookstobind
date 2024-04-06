import json
import re

import json
import re

# Define the preamble and document setup for LaTeX
latex_preamble = r"""
\documentclass[12pt,showtrims]{memoir}
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

\setstocksize{210mm}{148mm}
\settrimmedsize{198mm}{142mm}{*}
\settrims{6mm}{6mm}

\chapterstyle{bianchi}
\semiisopage[10]
\makepagestyle{mypage}
\makeoddfoot{mypage}{}{}{\thepage}
\makeevenfoot{mypage}{\thepage}{}{}
\setulmargins{0.7in}{*}{*}

\checkandfixthelayout
\trimFrame

\renewcommand{\chapnumfont}{\HUGE}
\renewcommand{\chaptitlefont}{\HUGE\swshape\color{black}}
\setsecheadstyle{\Huge\scshape\memRTLraggedright}

\let\oldafterchapternum\afterchapternum
\let\oldafterchaptertitle\afterchaptertitle

\makeatletter
\makeatother

\setlength\fboxsep{0pt}
\hyphenation{Gryph-on}

\newfontfamily\RotundaFont{"rotunda.otf"}

% Custom command to apply Rotunda Venata font
\newcommand{\rotunda}[1]{{\RotundaFont#1}}

% Define a custom chapter style
\makechapterstyle{rotundaChapter}{%
  \chapterstyle{default} % Start with the default style
  \renewcommand*{\chapnamefont}{\RotundaFont\Large\bfseries} % Chapter name ("Chapter")
  \renewcommand*{\chapnumfont}{\RotundaFont\Large\bfseries} % Chapter number
  \renewcommand*{\chaptitlefont}{\RotundaFont\Huge\bfseries} % Chapter title
}

\chapterstyle{rotundaChapter}

\setsecheadstyle{\RotundaFont\Large\bfseries\centering}

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

  \resizebox{0.85\textwidth}{!}{\HUGE \qquad \rotunda{Cleric's Spellbook}} \hfill\hfill
    
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

def transform_to_subsection(description):
    # Regular expression pattern to match lines starting with ***<Word>.*** 
    # and capturing the <Word> for use in the subsection title
    pattern = r"\*\*\*(.*?)\.\*\*\*"

    # Replacement function to format matched patterns as LaTeX subsections
    def replace_with_subsection(match):
        # Extracting the first group (matched word) to use as a subsection title
        title = match.group(1).strip()
        # Returning the LaTeX subsection command with the title
        return f"\\paragraph{{{title}}}"

    # Using re.sub() to find all matches of the pattern and replace them
    # with the LaTeX subsection command
    transformed_description = re.sub(pattern, replace_with_subsection, description)

    return transformed_description


# Helper function to convert bullet lists to LaTeX itemize
def convert_bullet_list_to_latex(description):
    # Splitting the description at " - " to identify potential list items
    parts = description.split(" - ")
    if len(parts) > 1:  # Indicates there's at least one list item
        # The first part is the introduction to the list, kept as is
        latex_description = parts[0] + "\n\\begin{itemize}\n"
        # Process each subsequent part as a list item
        for item in parts[1:]:
            latex_description += "    \\item " + item + "\n"
        latex_description += "\\end{itemize}\n"
    else:
        # If there's no list, return the description unchanged
        latex_description = description
    
    return latex_description

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
                # Convert bullet lists in the description to LaTeX itemize
                description = convert_bullet_list_to_latex(description)
                # Transform ***Word.*** patterns to subsections
                description = transform_to_subsection(description)
                # Escape LaTeX special characters
                description = re.sub(r'([&$#_])', r'\\\1', description)
                # Bold markup for **text**
                description = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', description)



                components = ", ".join(spell["components"])
                if "M" in spell["components"]:
                    material = spell.get("material", "N/A")
                    material = re.sub(r'([&$#_])', r'\\\1', material)
                    components += f" ({material})"

                tableHeader = \
"""
{
\\small\\centering\\vspace{-6pt}
\\begin{tabular}{rlrl}
\\toprule
"""
                tableFooter = \
"""
\\bottomrule
\\end{tabular}
}
"""
                print(tableHeader, file=f)
                print(f"\\textbf{{Duration:}} & {spell['duration']} &", file=f)
                print(f"\\textbf{{Casting Time:}} & {spell['casting_time']} \\\\", file=f)
                print(f"\\textbf{{Concentration:}} & {spell['concentration']} &", file=f)
                print(f"\\textbf{{Range:}} & {spell['range']} \\\\", file=f)
                print(f"\\textbf{{School:}} & {spell['school']['name']} \\\\", file=f)
                print(f"\\textbf{{Components:}} & \\multicolumn{{3}}{{p{{0.7\\textwidth}}}}{{{components}}}\\\\", file=f)

                print(tableFooter, file=f)
                
                print("\\vspace{1\\baselineskip}\\noindent " + description + "\n", file=f)
                
                if "higher_level" in spell and spell["higher_level"]:
                    higher_level = ' '.join(spell["higher_level"])
                    higher_level = re.sub(r'([&$#_])', r'\\\1', higher_level)
                    print("\\vspace{8pt} \\noindent\\textbf{At Higher Levels:} " + higher_level, file=f)
                
                print("\\newpage", file=f)

# Write the end of the document
    f.write("\n\\end{document}")
