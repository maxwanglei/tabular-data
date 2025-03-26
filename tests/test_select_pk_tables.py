
import pytest

from components.table_utils import select_pk_tables

html_tables = [{
    'caption': 'Table 1. Individual characteristics of the parturients investigated (n\xa0=\xa010)', 'footnote': '', 
    'table': None, 
    'raw_tag': '<div class="tables frame-topbot rowsep-0 colsep-0" id="tbl1"><span class="captions text-s"><span><p><span class="label">Table 1</span>. Individual characteristics of the parturients investigated (<em>n</em>\xa0=\xa010)</p></span></span><div class="groups"><table><thead class="valign-top"><tr><th class="rowsep-1 align-left" scope="col">Parturient</th><th class="rowsep-1 align-left" scope="col">Fetal gestational age (weeks)</th><th class="rowsep-1 align-left" scope="col">Age (years)</th><th class="rowsep-1 align-left" scope="col">Weight before delivery (kg)</th><th class="rowsep-1 align-left" scope="col">Height (cm)</th><th class="rowsep-1 align-left" scope="col">Associated drugs</th></tr></thead><tbody><tr><td class="align-left">1</td><td class="align-left">36.0</td><td class="align-left">30</td><td class="align-left">80</td><td class="align-left">156</td><td class="align-left">Diclofenac, lidocaine, oxytocin</td></tr><tr><td class="align-left">2</td><td class="align-left">40.1</td><td class="align-left">18</td><td class="align-left">50</td><td class="align-left">150</td><td class="align-left">–</td></tr><tr><td class="align-left">3</td><td class="align-left">39.0</td><td class="align-left">37</td><td class="align-left">72</td><td class="align-left">163</td><td class="align-left">Bupivacaine, dipyrone, fentanyl, lidocaine, methyl ergometrine, oxytocin</td></tr><tr><td class="align-left">4</td><td class="align-left">38.2</td><td class="align-left">20</td><td class="align-left">75</td><td class="align-left">170</td><td class="align-left">Bupivacaine, fentanyl, oxytocin</td></tr><tr><td class="align-left">5</td><td class="align-left">37.0</td><td class="align-left">20</td><td class="align-left">72</td><td class="align-left">159</td><td class="align-left">Bupivacaine, diclofenac, fentanyl, oxytocin</td></tr><tr><td class="align-left">6</td><td class="align-left">38.2</td><td class="align-left">24</td><td class="align-left">65</td><td class="align-left">157</td><td class="align-left">Cefazolin, diclofenac, lidocaine, oxytocin, thionembutal</td></tr><tr><td class="align-left">7</td><td class="align-left">38.6</td><td class="align-left">24</td><td class="align-left">82</td><td class="align-left">171</td><td class="align-left">Bupivacaine, diclofenac, dipyrone, oxytocin</td></tr><tr><td class="align-left">8</td><td class="align-left">39.2</td><td class="align-left">21</td><td class="align-left">93</td><td class="align-left">166</td><td class="align-left">Bupivacaine, cefazolin, diclofenac, oxytocin</td></tr><tr><td class="align-left">9</td><td class="align-left">39.6</td><td class="align-left">21</td><td class="align-left">86</td><td class="align-left">163</td><td class="align-left">Bupivacaine, lidocaine, nifedipine, oxytocin, sufentanyl</td></tr><tr><td class="align-left">10</td><td class="align-left">38.2</td><td class="align-left">18</td><td class="align-left">93</td><td class="align-left">162</td><td class="align-left">Oxytocin, sufentanyl</td></tr><tr><td class="align-left" colspan="6"><br/></td></tr><tr><td class="align-left">Mean CI 95%</td><td class="align-left">38.41 37.54–39.28</td><td class="align-left">23.30 19.02–27.58</td><td class="align-left">76.80 67.40–86.20</td><td class="align-left">161.70 157.08–166.32</td><td></td></tr></tbody></table></div></div>'
}, {
    'caption': 'Table 2. Kinetic disposition of lorazepam and its metabolite glucuronide in parturients treated with a single oral dose of 2\xa0mg rac-lorazepam; mean (CI 95%)', 
    'footnote': '–, Not determined.', 
    'table': None, 
    'raw_tag': '<div class="tables frame-topbot rowsep-0 colsep-0" id="tbl2"><span class="captions text-s"><span><p><span class="label">Table 2</span>. Kinetic disposition of lorazepam and its metabolite glucuronide in parturients treated with a single oral dose of 2\xa0mg <em>rac-</em>lorazepam; mean (CI 95%)</p></span></span><div class="groups"><table><thead class="valign-top"><tr><td class="rowsep-1" scope="col"><span class="screen-reader-only">Empty Cell</span></td><th class="rowsep-1 align-left" scope="col">Lorazepam isomeric mixture</th><th class="rowsep-1 align-left" scope="col">Lorazepam-glucuronide isomeric mixture</th></tr></thead><tbody><tr><td class="align-left"><em>C</em><sub>max</sub> (ng/ml)</td><td class="align-left">12.96 (9.42–16.49)</td><td class="align-left">35.55 (8.27–62.83)</td></tr><tr><td class="align-left">t<sub>max</sub> (h)</td><td class="align-left">3.10 (2.57–3.63)</td><td class="align-left">4.33 (2.90–5.77)</td></tr><tr><td class="align-left"><em>t</em><sub>1/2a</sub> (h)</td><td class="align-left">3.16 (2.62–3.68)</td><td class="align-left">1.37 (1.15–1.58)</td></tr><tr><td class="align-left"><em>K</em><sub>a</sub> (h<sup>−1</sup>)</td><td class="align-left">0.23 (0.19–0.28)</td><td class="align-left">0.52 (0.44–0.59)</td></tr><tr><td class="align-left"><em>t</em><sub>1/2</sub><em>β</em> (h)</td><td class="align-left">10.35 (9.39–11.32)</td><td class="align-left">18.17 (14.10–22.23)</td></tr><tr><td class="align-left"><em>β</em> (h<sup>−1</sup>)</td><td class="align-left">0.068 (0.061–0.075)</td><td class="align-left">0.039 (0.032–0.047)</td></tr><tr><td class="align-left">AUC<sup>0–∞</sup> ((ng\xa0h)/ml)</td><td class="align-left">175.25 (145.74–204.75)</td><td class="align-left">481.19 (252.87–709.51)</td></tr><tr><td class="align-left">Cl<sub>T</sub>/F (ml/(min\xa0kg))</td><td class="align-left">2.61 (2.34–2.88)</td><td class="align-left">–</td></tr><tr><td class="align-left">Vd/F (l)</td><td class="align-left">178.78 (146.46–211.10)</td><td class="align-left">–</td></tr></tbody></table></div><div class="legend"><div class="u-margin-s-bottom">–, Not determined.</div></div></div>'
}, {
    'caption': 'Table 3. Urinary excretion of lorazepam and its metabolite glucuronide in parturients treated with a single oral dose of 2\xa0mg rac-lorazepam; mean (CI 95%)', 
    'footnote': '', 
    'table': None, 
    'raw_tag': '<div class="tables frame-topbot rowsep-0 colsep-0" id="tbl3"><span class="captions text-s"><span><p><span class="label">Table 3</span>. Urinary excretion of lorazepam and its metabolite glucuronide in parturients treated with a single oral dose of 2\xa0mg rac-lorazepam; mean (CI 95%)</p></span></span><div class="groups"><table><thead class="valign-top"><tr><td class="rowsep-1" scope="col"><span class="screen-reader-only">Empty Cell</span></td><th class="rowsep-1 align-left" scope="col">Lorazepam isomeric mixture</th><th class="rowsep-1 align-left" scope="col">Lorazepam-glucuronide isomeric mixture</th></tr></thead><tbody><tr><td class="align-left"><em>A</em><sub>e</sub> total (μg)</td><td class="align-left">8.18 (2.67–13.70)</td><td class="align-left">899.77 (534.58–1265.0)</td></tr><tr><td class="align-left">Fel (%)</td><td class="align-left">0.29 (0.12–0.45)</td><td class="align-left">44.97 (26.65–63.29)</td></tr><tr><td class="align-left">Cl<sub>R</sub> (ml/(min\xa0kg))</td><td class="align-left">0.0099 (0.0049–0.015)</td><td class="align-left">1.12 (0.69–1.55)</td></tr><tr><td class="align-left"><em>t</em><sub>1/2</sub> (h)</td><td class="align-left">12.75 (10.71–14.79)</td><td class="align-left">11.5 (6.14–16.86)</td></tr><tr><td class="align-left">Kel (h<sup>−1</sup>)</td><td class="align-left">0.057 (0.048–0.065)</td><td class="align-left">0.066 (0.040–0.093)</td></tr></tbody></table></div></div>'
}, {
    'caption': 'Table 4. Transplacental distribution of lorazepam as an enantiomeric mixture at delivery (n\xa0=\xa08)', 
    'footnote': 'Parturients were treated with a single oral dose of 2\xa0mg rac-lorazepam; mean (CI 95%).', 
    'table': None, 
    'raw_tag': '<div class="tables frame-topbot rowsep-0 colsep-0" id="tbl4"><span class="captions text-s"><span><p><span class="label">Table 4</span>. Transplacental distribution of lorazepam as an enantiomeric mixture at delivery (<em>n</em>\xa0=\xa08)</p></span></span><div class="groups"><table><thead class="valign-top"><tr><th class="rowsep-1 align-left" scope="col">Parturient</th><th class="rowsep-1 align-left" scope="col">Cord blood (ng/ml)</th><th class="rowsep-1 align-left" scope="col">Maternal blood (ng/ml)</th><th class="rowsep-1 align-left" scope="col">Collection time<a class="anchor anchor-primary" data-sd-ui-side-panel-opener="true" data-xocs-content-id="tbl4fn1" data-xocs-content-type="reference" href="#tbl4fn1" name="btbl4fn1"><span class="anchor-text-container"><span class="anchor-text"><sup>a</sup></span></span></a> (min)</th><th class="rowsep-1 align-left" scope="col">Cord blood/maternal blood</th></tr></thead><tbody><tr><td class="align-left">1</td><td class="align-left">5.77</td><td class="align-left">14.74</td><td class="align-left">135</td><td class="align-left">0.392</td></tr><tr><td class="align-left">2</td><td class="align-left">6.82</td><td class="align-left">7.95</td><td class="align-left">426</td><td class="align-left">0.858</td></tr><tr><td class="align-left">3</td><td class="align-left">4.38</td><td class="align-left">10.48</td><td class="align-left">153</td><td class="align-left">0.418</td></tr><tr><td class="align-left">4</td><td class="align-left">8.42</td><td class="align-left">9.60</td><td class="align-left">300</td><td class="align-left">0.878</td></tr><tr><td class="align-left">5</td><td class="align-left">5.87</td><td class="align-left">5.33</td><td class="align-left">390</td><td class="align-left">1.100</td></tr><tr><td class="align-left">6</td><td class="align-left">5.78</td><td class="align-left">9.87</td><td class="align-left">120</td><td class="align-left">0.586</td></tr><tr><td class="align-left">7</td><td class="align-left">7.75</td><td class="align-left">10.94</td><td class="align-left">552</td><td class="align-left">0.708</td></tr><tr><td class="align-left">8</td><td class="align-left">9.45</td><td class="align-left">10.35</td><td class="align-left">207</td><td class="align-left">0.913</td></tr><tr><td class="align-left" colspan="5"><br/></td></tr><tr><td class="align-left">Mean CI 95%</td><td class="align-left">6.78 (5.39–8.17)</td><td class="align-left">9.91 (7.68–12.14)</td><td class="align-left">293.4 (163.2–423)</td><td class="align-left">0.73 (0.52–0.94)</td></tr></tbody></table></div><div class="legend"><div class="u-margin-s-bottom">Parturients were treated with a single oral dose of 2\xa0mg rac-lorazepam; mean (CI 95%).</div></div><dl class="footnotes"><dt id="tbl4fn1">a</dt><dd><div class="u-margin-s-bottom">Time between drug intake and blood collection from the umbilical cord and maternal vein.</div></dd></dl></div>'
}]

def test_select_pk_tables(llm):
    tables, ixs, _ = select_pk_tables(html_tables, llm)
    assert tables is not None
    assert len(tables) > 0
    assert ixs is not None
    assert len(ixs) == len(tables)
    
