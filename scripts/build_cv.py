"""
Generates the CV PDF(s) for the site.

This is the source of truth for cv.pdf — edit the content below, then run:

    python3 scripts/build_cv.py

from the project root. It builds two files:
  - assets/cv.pdf              the PUBLIC version (no email), linked from the site, tracked in git
  - source-docs/cv-full.pdf    the PRIVATE version (with email), gitignored, stays local only

Requires reportlab: pip install reportlab
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACCENT = colors.HexColor("#7a3b2e")
TEXT = colors.HexColor("#26241f")
MUTED = colors.HexColor("#6b675c")

styles = {
    "name": ParagraphStyle("name", fontName="Times-Bold", fontSize=20, textColor=TEXT, alignment=TA_CENTER, spaceAfter=8, leading=24),
    "contact": ParagraphStyle("contact", fontName="Times-Roman", fontSize=10, textColor=MUTED, alignment=TA_CENTER, spaceAfter=14, spaceBefore=2),
    "section": ParagraphStyle("section", fontName="Times-Bold", fontSize=12, textColor=ACCENT, spaceBefore=14, spaceAfter=6, letterSpacing=1),
    "entry_title": ParagraphStyle("entry_title", fontName="Times-Bold", fontSize=10.5, textColor=TEXT, spaceBefore=6, spaceAfter=1, leading=13),
    "job_title": ParagraphStyle("job_title", fontName="Times-Bold", fontSize=9.5, textColor=TEXT, spaceBefore=6, spaceAfter=1, leading=11.5),
    "job_date": ParagraphStyle("job_date", fontName="Times-Bold", fontSize=9.5, textColor=TEXT, spaceBefore=6, spaceAfter=1, leading=11.5, alignment=2),
    "entry_mixed": ParagraphStyle("entry_mixed", fontName="Times-Roman", fontSize=10.5, textColor=TEXT, spaceBefore=6, spaceAfter=1, leading=13),
    "entry_sub": ParagraphStyle("entry_sub", fontName="Times-Italic", fontSize=10, textColor=MUTED, spaceAfter=3, leading=12),
    "bullet": ParagraphStyle("bullet", fontName="Times-Roman", fontSize=9.8, textColor=TEXT, leftIndent=14, firstLineIndent=-14, spaceAfter=2, leading=13),
    "plain": ParagraphStyle("plain", fontName="Times-Roman", fontSize=9.8, textColor=TEXT, spaceAfter=3, leading=13),
}

def rule():
    return HRFlowable(width="100%", thickness=0.75, color=ACCENT, spaceBefore=0, spaceAfter=8)

def section(title):
    return [Paragraph(title.upper(), styles["section"]), rule()]

def entry(title_left, title_right, sub=None, bullets=None):
    flow = []
    t = Table([[Paragraph(title_left, styles["job_title"]), Paragraph(title_right, styles["job_date"])]],
              colWidths=[5.25*inch, 1.40*inch])
    t.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING",(0,0),(-1,-1),0), ("RIGHTPADDING",(0,0),(-1,-1),0), ("TOPPADDING",(0,0),(-1,-1),0), ("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    flow.append(t)
    if sub:
        flow.append(Paragraph(sub, styles["entry_sub"]))
    if bullets:
        for b in bullets:
            flow.append(Paragraph("&bull;&nbsp;&nbsp;" + b, styles["bullet"]))
    return flow

def edu_entry(degree, program_institution, year, sub_lines=None):
    degree_para = Paragraph(degree, styles["entry_title"])
    main_line = f"<b>{program_institution}</b>, {year}"
    right_content = [Paragraph(main_line, styles["entry_mixed"])]
    if sub_lines:
        for s in sub_lines:
            right_content.append(Paragraph(s, styles["entry_sub"]))
    t = Table([[degree_para, right_content]], colWidths=[0.65*inch, 6.0*inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return [t, Spacer(1, 8)]

def entry_rev(date_left, title_right, sub=None, bullets=None):
    left = Paragraph(date_left, styles["entry_mixed"])
    right_content = [Paragraph(title_right, styles["entry_title"])]
    if sub:
        right_content.append(Paragraph(sub, styles["entry_sub"]))
    t = Table([[left, right_content]], colWidths=[1.2*inch, 5.45*inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    flow = [t]
    if bullets:
        for b in bullets:
            flow.append(Paragraph("&bull;&nbsp;&nbsp;" + b, styles["bullet"]))
    flow.append(Spacer(1, 8))
    return flow

def award_line(year, text):
    left = Paragraph(year, styles["plain"])
    right = Paragraph(text, styles["plain"])
    t = Table([[left, right]], colWidths=[1.2*inch, 5.45*inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return [t]


def build_story(include_email):
    story = []
    story.append(Paragraph("Saada Amadu", styles["name"]))
    contact_line = "Berkeley, CA &nbsp;&bull;&nbsp; saadaamadu@gmail.com" if include_email else "Berkeley, CA"
    story.append(Paragraph(contact_line, styles["contact"]))

    # EDUCATION
    story += section("Education")
    story += edu_entry("Ph.D.", "City and Regional Planning, University of California, Berkeley", "2024&ndash;Present",
                        ["Concentration: Food Systems and Applied Data Science", "Designated Emphasis in Political Economy"])
    story += edu_entry("M.S.", "Environmental Sciences &amp; Policy, Central European University, Budapest, Hungary", "2017",
                        ["Thesis: <i>From Land Grabbing to Sustainable Land Investments: Effects of Large-Scale Land Transactions on the Environment and Rural Livelihoods in Ghana</i>"])
    story += edu_entry("B.A.", "International Studies, College of Staten Island, New York, NY", "2016",
                        ["Honors Thesis: <i>State and Non-Governmental Organization Influences on Sustainable Agricultural Practices in Senegal</i>",
                         "Study abroad: Universit&eacute; Paris Ouest Nanterre La D&eacute;fense (2015), City University of Hong Kong (2016)"])

    # PROFESSIONAL EXPERIENCE
    story += section("Professional Experience")

    jobs = [
        ("Export Trading Group &mdash; Agribusiness Intern, Malawi", "May 2025 &ndash; Aug. 2025", [
            "Conducted technical due diligence and sustainability assessments on agroforestry carbon-credit projects for 2,000+ smallholder farmers, modeling carbon sequestration potentials and designing revenue-share frameworks to attract impact investors.",
            "Designed a Climate Desk toolkit and accompanying visuals for smallholder farmers on carbon credits, soil-health benefits, and revenue projections.",
        ]),
        ("Resilient Cities Network &mdash; Program Manager, Climate Resilience &amp; Equity, New York", "Jun. 2022 &ndash; May 2024", [
            "Collaborated with city officials, community-based organizations, and stakeholders to identify and scale community-centric resilience solutions addressing climate risks and socioeconomic inequities.",
            "Designed and conducted household surveys and key informant interviews across 250+ households, informing tailored interventions for extreme heat and flooding in four frontline environmental justice communities.",
            "Conducted pre-feasibility studies and identified 10 viable climate resilience projects, leading to the selection and initiation of 5 projects with a combined budget of $500,000, benefiting over 10,000 urban residents.",
            "Led the Urban Eats campaign to inspire cities to adopt circular and resilient food systems and attract funding support.",
            "Spearheaded the technical development and global deployment of the Resilient Infrastructure for Diversity and Equity (RIDE) Scorecard across 10 cities, with potential to impact over 2 million urban residents.",
        ]),
        ("Matriark Foods &mdash; Project Consultant, New York", "Oct. 2021 &ndash; Mar. 2022", [
            "Researched and recommended vegetables and producers in line with sustainable sourcing criteria, and conducted upcycled foods market research to inform go-to-market strategy.",
            "Designed and implemented company-wide environmental, social, and governance (ESG) reporting processes.",
        ]),
        ("Sky High Farm &mdash; Food Access Program Consultant, New York", "May 2021 &ndash; Oct. 2021", [
            "Utilized sustainable agriculture practices to produce food for distribution to the food-insecure.",
            "Conducted needs assessments and collaborated with community organizations on food security initiatives.",
        ]),
        ("Rethink Food &mdash; Policy Researcher, New York", "Feb. 2020 &ndash; Apr. 2021", [
            "Co-led strategic development and execution of Rethink Food's food policy strategy, legislative agenda, and revenue goals.",
            "Facilitated 30+ strategic partnerships with restaurants, directing funding and resources to combat food insecurity.",
            "Led targeted lobbying and advocacy campaigns, liaising with elected officials and community leaders.",
            "Identified viable government funding opportunities and prepared grant applications and contract proposals.",
        ]),
        ("Spaces &mdash; Community Manager, New York", "Dec. 2018 &ndash; Jan. 2020", [
            "Co-managed a seven-floor co-working space with over 100 companies.",
            "Built an active community through client programming; partnered with intergovernmental agencies on pitch competitions and coordinated logistics across five events with 300+ attendees.",
        ]),
        ("Schneider Electric &mdash; Sustainability Analyst, Budapest", "Jan. 2018 &ndash; Aug. 2018", [
            "Oversaw sustainability reporting for 15 companies, achieving a 10% reduction in energy consumption and 15% reduction in carbon emissions.",
            "Managed 20+ electricity and gas utility vendors and researched climate policy and compliance strategies for clients.",
        ]),
        ("Impact Hub Budapest &mdash; Community Host, Budapest, Hungary", "Feb. 2017 &ndash; Jul. 2017", [
            "Welcomed co-working members and space guests; fostered connections between community members to support innovation.",
        ]),
    ]

    for title, dates, bullets in jobs:
        story += entry(title, dates, bullets=bullets)
        story.append(Spacer(1, 8))

    # TEACHING
    story += section("Teaching Experience")
    story += entry_rev("Fall 2025", "University of California, Berkeley &mdash; Graduate Student Instructor",
                        sub="Planning for Sustainability")

    # AWARDS AND FELLOWSHIPS
    story += section("Awards and Fellowships")
    awards = [
        ("2026", "Mentored Research Award (Full Tuition and Stipend), UC Berkeley"),
        ("2026", "Center for African Studies Rocca Pre-dissertation Research Award, UC Berkeley"),
        ("2026", "Berkeley Economy and Society Initiative Award"),
        ("2024", "Chancellor&rsquo;s Fellowship (Full Tuition and Stipend), UC Berkeley"),
        ("2017", "Central European University Research Travel Grant"),
        ("2016", "Central European University Master&rsquo;s Excellence Scholarship (Full Tuition and Stipend)"),
        ("2016", "Benjamin A. Gilman International Scholarship"),
        ("2015", "Benjamin Franklin Travel Grant"),
        ("", "Dean&rsquo;s List, College of Staten Island"),
    ]
    for year, text in awards:
        story += award_line(year, text)

    # CONFERENCE PRESENTATIONS
    story += section("Conference Presentations")
    story += entry_rev("2026", "Association of American Geographers Annual Meeting",
                        sub="&ldquo;What Do You Mean You Have No Forex?&rdquo;: Foreign Exchange Shortages, Food Security, and Economic Development in Landlocked Malawi &mdash; Accepted and Presented")
    story += entry_rev("2026", "Oxford Food Symposium",
                        sub="&ldquo;From Poverty Food to Global Superfood: Can Fonio Escape the Quinoa Trap?&rdquo; &mdash; Accepted and Presented")
    story += entry_rev("2026", "Society for the Advancement of Socio-Economics",
                        sub="&ldquo;Quinoa and Teff Ran so Fonio Could Walk: Beyond the Superfood Cycle and Toward a Proactive Political Economy of Fonio and Underutilized Species&rdquo; &mdash; Accepted")

    # INVITED TALKS AND PANELS
    story += section("Invited Talks and Panels")
    story += entry_rev("April 2026", "Guest Speaker &mdash; Food Systems Minor", sub="UC Berkeley")
    story += entry_rev("March 2024", "Monthly Forum: Sustainable Food Systems", sub="GreenHomeNYC &mdash; Panelist")
    story += entry_rev("May 2023", "Resilient Infrastructure Diversity and Equity (RIDE) Scorecard", sub="Cocreating a Resilient Future &mdash; Presenter")
    story += entry_rev("May 2023", "Bridging the Gap Between Local Governments and the Public", sub="Cocreating a Resilient Future &mdash; Panelist")
    story += entry_rev("July 2021", "Reconnecting with the Land: A Conversation with Saada Amadu, Michelle Jackson, &amp; Qiana Mickie", sub="A Meal &mdash; Panelist")
    story += entry_rev("February 2021", "Shifting from Response to Resiliency, Rethinking Food Systems in NYC", sub="Food System Forum &mdash; Panelist")
    story += entry_rev("October 2020", "Local Innovations, SDGs &amp; COVID-19", sub="UN-Habitat New York World Cities Day &mdash; Panelist")
    story += entry_rev("September 2020", "Tackling Food Loss and Waste and Supporting Food Security During the COVID-19 Pandemic", sub="UN FAO &mdash; Organizer and Moderator")

    # SKILLS
    story += section("Skills")
    story.append(Paragraph("<b>Languages:</b> English (Native), Dagbanli (Native), Twi (Proficient), Hausa (Proficient), French (Elementary)", styles["plain"]))
    story.append(Paragraph("<b>Research Methods:</b> Household Surveys, Focus Groups, Key Informant Interviews, Participant Observation", styles["plain"]))
    story.append(Paragraph("<b>Technology:</b> Microsoft Office, G Suite, ArcGIS, SPSS, Python, R", styles["plain"]))
    story.append(Paragraph("<b>Project Management:</b> Asana, Miro, Airtable", styles["plain"]))

    return story


def build(output_path, include_email):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=0.55*inch, bottomMargin=0.55*inch, leftMargin=0.75*inch, rightMargin=0.75*inch,
    )
    doc.build(build_story(include_email))


if __name__ == "__main__":
    build(os.path.join(ROOT, "assets", "cv.pdf"), include_email=False)
    build(os.path.join(ROOT, "source-docs", "cv-full.pdf"), include_email=True)
    print("Built assets/cv.pdf (public, no email) and source-docs/cv-full.pdf (private, with email)")
