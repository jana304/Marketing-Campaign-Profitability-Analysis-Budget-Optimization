
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ==========================================
# 1. PROJECT PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
VISUAL_DIR = PROJECT_DIR / "05_Visualizations"
OUTPUT_DIR = PROJECT_DIR / "07_Presentation"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "Marketing_Profitability_Project_Presentation.pptx"

# ==========================================
# 2. PRESENTATION SETTINGS
# ==========================================

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

NAVY = RGBColor(18, 34, 59)
BLUE = RGBColor(33, 105, 190)
WHITE = RGBColor(255, 255, 255)
DARK = RGBColor(38, 48, 62)
GRAY = RGBColor(103, 115, 130)
LIGHT = RGBColor(238, 244, 250)
GREEN = RGBColor(25, 135, 95)


def add_text(slide, text, x, y, w, h,
             size=20, color=DARK, bold=False,
             align=PP_ALIGN.LEFT):

    box = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h)
    )

    tf = box.text_frame
    tf.word_wrap = True

    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.name = "Aptos"
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.alignment = align
        p.space_after = Pt(12)

    return box


def add_background(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = WHITE

    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0, 0, prs.slide_width, Inches(0.12)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()


def add_title(slide, title, subtitle=None):
    add_background(slide)
    add_text(slide, title, 0.65, 0.4, 12, 0.65,
             size=29, color=NAVY, bold=True)

    if subtitle:
        add_text(slide, subtitle, 0.67, 1.12, 12, 0.5,
                 size=14, color=GRAY)


def add_footer(slide):
    number = len(prs.slides)
    add_text(
        slide,
        f"MARKETING_PROFITABILITY  |  {number}",
        0.65, 7.05, 12, 0.25,
        size=10, color=GRAY
    )


def new_slide(title, subtitle=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, title, subtitle)
    add_footer(slide)
    return slide


def add_bullets(slide, items, x=0.85, y=1.85,
                w=11.6, size=21, gap=0.72):

    for i, item in enumerate(items):
        add_text(
            slide,
            "\u2022 " + item,
            x, y + i * gap, w, gap,
            size=size
        )


def add_chart(slide, filename, x=1.1, y=1.65,
              max_w=11.1, max_h=4.95):

    path = VISUAL_DIR / filename

    if not path.exists():
        add_text(
            slide,
            f"Chart not found: {filename}",
            1.0, 2.6, 11, 1,
            size=20, color=GRAY
        )
        print(f"WARNING: Missing chart: {path}")
        return

    from PIL import Image

    with Image.open(path) as img:
        img_w, img_h = img.size

    ratio = min(max_w / img_w, max_h / img_h)
    w = img_w * ratio
    h = img_h * ratio

    left = x + (max_w - w) / 2
    top = y + (max_h - h) / 2

    slide.shapes.add_picture(
        str(path),
        Inches(left), Inches(top),
        width=Inches(w),
        height=Inches(h)
    )


# ==========================================
# SLIDE 1: TITLE
# ==========================================

slide = prs.slides.add_slide(prs.slide_layouts[6])

slide.background.fill.solid()
slide.background.fill.fore_color.rgb = NAVY

add_text(
    slide,
    "MARKETING PROFITABILITY",
    0.9, 1.55, 11.5, 0.8,
    size=39, color=WHITE, bold=True
)

add_text(
    slide,
    "Marketing Campaign Profitability Analysis\n"
    "& Budget Optimization",
    0.95, 2.65, 11.3, 1.4,
    size=28, color=WHITE
)

add_text(
    slide,
    "Data Analyst Portfolio Project  |  Excel • SQL • Python",
    0.95, 5.65, 11.3, 0.5,
    size=17, color=WHITE
)


# ==========================================
# SLIDE 2: BUSINESS PROBLEM
# ==========================================

slide = new_slide("Business Problem")

add_bullets(slide, [
    "Marketing budgets are distributed across multiple channels.",
    "Higher advertising spend does not guarantee higher returns.",
    "Acquisition efficiency varies between channels.",
    "Businesses need reliable performance and profitability metrics.",
    "Data-driven analysis can inform budget allocation decisions."
])


# ==========================================
# SLIDE 3: PROJECT OBJECTIVES
# ==========================================

slide = new_slide("Project Objectives")

add_bullets(slide, [
    "Analyze advertising spend and campaign engagement.",
    "Measure lead generation and conversion efficiency.",
    "Evaluate attributed revenue, ROAS, and marketing profit.",
    "Compare performance across five advertising channels.",
    "Develop an illustrative budget optimization scenario."
])


# ==========================================
# SLIDE 4: DATASET OVERVIEW
# ==========================================

slide = new_slide("Dataset Overview")

add_bullets(slide, [
    "Campaigns: 120 records",
    "Daily Spend: 11,240 records",
    "Leads: 261,684 records",
    "Conversions: 39,696 records",
    "Relational analysis using campaign IDs and lead IDs."
], size=22)


# ==========================================
# SLIDE 5: TOOLS & METHODOLOGY
# ==========================================

slide = new_slide("Tools & Analytical Methodology")

add_bullets(slide, [
    "Excel: KPI analysis and financial calculations.",
    "MySQL: Data validation, joins, and performance queries.",
    "Python and Pandas: Data cleaning and automated analysis.",
    "Matplotlib and Seaborn: Marketing visualizations.",
    "Scenario modeling: Evaluate alternative budget allocations."
], size=20)


# ==========================================
# SLIDE 6: EXECUTIVE KPIs
# ==========================================

slide = new_slide("Executive Marketing KPIs")

add_bullets(slide, [
    "Advertising Spend: 4,523,050.02",
    "Attributed Revenue: 21,561,839.01",
    "Marketing Profit: 17,038,788.99",
    "Return on Ad Spend: 4.77x",
    "Marketing ROI: 376.71%",
    "Lead Conversion Rate: 15.17%"
], size=22, gap=0.66)


# ==========================================
# SLIDE 7: REVENUE BY CHANNEL
# ==========================================

slide = new_slide(
    "Revenue by Marketing Channel",
    "Historical attributed revenue comparison"
)

add_chart(slide, "01_revenue_by_channel.png")


# ==========================================
# SLIDE 8: ROAS COMPARISON
# ==========================================

slide = new_slide(
    "Return on Ad Spend by Channel",
    "Affiliate and Paid Search achieved the strongest ROAS"
)

add_chart(slide, "02_roas_by_channel.png")


# ==========================================
# SLIDE 9: CUSTOMER ACQUISITION
# ==========================================

slide = new_slide(
    "Customer Acquisition Efficiency",
    "Advertising cost per conversion by channel"
)

add_chart(slide, "04_cost_per_conversion.png")


# ==========================================
# SLIDE 10: MARKETING PROFITABILITY
# ==========================================

slide = new_slide(
    "Marketing Profit by Channel",
    "Attributed revenue minus advertising spend"
)

add_chart(slide, "06_marketing_profit_by_channel.png")


# ==========================================
# SLIDE 11: BUDGET OPTIMIZATION
# ==========================================

slide = new_slide(
    "Budget Optimization Scenario",
    "Illustrative fixed-ROAS model; not a guaranteed forecast"
)

add_chart(slide, "08_budget_optimization_comparison.png")


# ==========================================
# SLIDE 12: BUSINESS RECOMMENDATIONS
# ==========================================

slide = new_slide("Strategic Business Recommendations")

add_bullets(slide, [
    "Evaluate controlled expansion of Affiliate campaigns.",
    "Test additional Paid Search investment.",
    "Optimize Paid Social targeting and creatives.",
    "Review Display and Video advertising efficiency.",
    "Measure incremental returns before reallocating budgets."
], size=20)


# ==========================================
# SLIDE 13: CONCLUSION
# ==========================================

slide = new_slide("Project Conclusion")

add_bullets(slide, [
    "Affiliate delivered the highest historical ROAS: 6.54x.",
    "Paid Search achieved strong engagement and acquisition efficiency.",
    "Video recorded the lowest direct-response ROAS: 2.52x.",
    "Budget scenarios support hypothesis-driven investment decisions.",
    "Excel, SQL, and Python provide an integrated analytics workflow."
], size=19)

add_text(
    slide,
    "Note: Marketing profit excludes non-advertising business costs.",
    0.85, 6.25, 11.7, 0.4,
    size=13, color=GRAY
)


# ==========================================
# SAVE PRESENTATION
# ==========================================

prs.save(OUTPUT_FILE)

print("=" * 60)
print("PRESENTATION GENERATED SUCCESSFULLY")
print("=" * 60)
print(f"Output: {OUTPUT_FILE}")
print(f"Total slides: {len(prs.slides)}")
print("=" * 60)
