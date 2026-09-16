#!/usr/bin/env python3
"""Builds the Playhead reference site from Jinja templates into ../site/.
Run: python3 build/build.py   (from the framer-template-playhead folder)"""
import os, sys, shutil
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")
env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "build", "templates")), autoescape=False)

ARROW = '<svg class="arrow" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
TICK = '<svg viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2.5 6.2l2.3 2.3L9.5 3.8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PLUS = '<svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M7 2v10M2 7h10" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.5l2.9 6.2 6.8.8-5 4.7 1.3 6.8L12 17.6 6 21l1.3-6.8-5-4.7 6.8-.8z"/></svg>'
def icon(path):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'
ICONS = {
    "short": icon('<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M10.5 9.5v5l4-2.5z" fill="currentColor" stroke="none"/>'),
    "long": icon('<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M10 9.5v5l4.5-2.5z" fill="currentColor" stroke="none"/>'),
    "motion": icon('<path d="M4 17c4-8 6-8 8-2s4 4 8-6"/><circle cx="4" cy="17" r="1.6" fill="currentColor" stroke="none"/><circle cx="20" cy="9" r="1.6" fill="currentColor" stroke="none"/>'),
    "thumb": icon('<rect x="2.5" y="4" width="19" height="16" rx="2.5"/><path d="M3 16l5-5 4 4 3-3 6 6"/><circle cx="16.5" cy="8.5" r="1.5" fill="currentColor" stroke="none"/>'),
}

site = dict(
    brand="Noa Keller", persona="Noa Keller", first_name="Noa",
    availability="Booking Q4 2026", location="Berlin",
    email="hello@noakeller.example", phone="+49 30 000 0000", phone_raw="+49300000000",
    footer_word="Keep them watching.",
)
clients = ["Kestrel Labs", "Northwind Coffee", "Salt & Signal", "Volt Athletics", "Mono Supply", "Halo Audio", "Loop Records", "Arda Films", "Rooftop Sessions", "Wander"]
reels = [
    dict(img="reel-01.jpg", title="7 seconds to yes", client="Northwind Coffee", platform="Reels", views="2.4M", meta="61% avg. watch"),
    dict(img="reel-02.jpg", title="Hooks that hold", client="Kestrel Labs", platform="TikTok", views="1.8M", meta="hook-first cut"),
    dict(img="reel-03.jpg", title="Founder POV", client="Salt & Signal", platform="Shorts", views="940k", meta="talking head"),
    dict(img="reel-04.jpg", title="Gym reset", client="Volt Athletics", platform="Reels", views="3.1M", meta="fast cuts · SFX"),
    dict(img="reel-05.jpg", title="Street eats: Tokyo", client="Wander", platform="TikTok", views="5.6M", meta="travel · captions"),
    dict(img="reel-06.jpg", title="Desk setup 2026", client="Mono Supply", platform="Shorts", views="1.2M", meta="product · b-roll"),
]
projects = [
    dict(img="poster-4hour.jpg", title="The 4-hour cut", client="Arda Films", format="YouTube documentary", result="1.1M views", fmt="long"),
    dict(img="poster-studio.jpg", title="Inside the studio", client="Loop Records", format="Brand film · series", result="3.1× watch time", fmt="long"),
    dict(img="poster-built.jpg", title="How we built it", client="Kestrel Labs", format="Founder series · 12 ep.", result="+21k subs", fmt="long"),
    dict(img="poster-spring.jpg", title="Spring drop", client="Mono Supply", format="Paid social · 6 cuts", result="2.3× ROAS", fmt="ads"),
    dict(img="poster-launch.jpg", title="Launch film", client="Halo Audio", format="Product film · 90s", result="Site conv. +18%", fmt="ads"),
    dict(img="poster-titles.jpg", title="Title sequence", client="Rooftop Sessions", format="Motion design", result="Season 3", fmt="motion"),
    dict(img="poster-podcast.jpg", title="Signal & Noise", client="Salt & Signal", format="Podcast · clips", result="40 clips / month", fmt="podcast"),
]
work = []
for p in projects:
    work.append(dict(p, tall=False, platform="", views=""))
for i, r in enumerate(reels):
    work.append(dict(img=r["img"], title=r["title"], client=r["client"], format="Short-form · " + r["platform"], result=r["views"] + " views", fmt="short", tall=True, platform=r["platform"], views=r["views"]))
# interleave tall cards for a masonry feel
order = [0, 7, 1, 8, 3, 2, 9, 4, 10, 5, 11, 6, 12]
work = [work[i] for i in order]

services = [
    dict(icon=ICONS["short"], title="Short-form editing", text="Hooks, captions, pacing and sound design for TikTok, Reels and Shorts. Delivered in batches so you can post daily.", from_="$90 / video", deliverables=["Hook-first structure and pacing", "Captions, SFX and music licensing", "Platform-native exports (9:16, 1:1)"]),
    dict(icon=ICONS["long"], title="Long-form YouTube", text="Story-first cuts for 8–25 minute videos: structure, b-roll, retention edits and chapters.", from_="$450 / video", deliverables=["Paper edit and structure pass", "B-roll, graphics and chapters", "Retention review after 7 days"]),
    dict(icon=ICONS["motion"], title="Motion & titles", text="Animated titles, lower thirds, explainer graphics and channel packages in After Effects.", from_="$600 / package", deliverables=["Title sequence and lower thirds", "Reusable MOGRT templates", "Channel intro / outro"]),
    dict(icon=ICONS["thumb"], title="Thumbnails & packaging", text="Thumbnail concepts, title testing and channel art that earns the click.", from_="$60 / thumbnail", deliverables=["3 concepts per video", "Title and thumbnail A/B notes", "Channel banner and end screens"]),
]
for s in services: s["from"] = s.pop("from_")
process = [
    dict(when="Day 0", title="Brief", text="Share footage, references and the goal for the video. We agree on format, length and deadline."),
    dict(when="Day 2", title="Rough cut", text="First cut with structure and pacing locked. You comment directly on the timeline via Frame.io."),
    dict(when="Day 3–4", title="Revisions", text="Two rounds included. Captions, sound design and color are finalized."),
    dict(when="Day 5", title="Delivery", text="Platform-ready exports, project files on request, and a thumbnail if booked."),
]
testimonials = [
    dict(quote="Noa turned 40 minutes of rambling into a 12-minute video that people actually finish. Our average view duration doubled.", name="Mara Lindqvist", role="Founder, Kestrel Labs", initials="ML", color="#2F5BFF"),
    dict(quote="Fast, sharp, and the hooks are unreal. We went from 20k to 400k views per Reel in three months.", name="Jonas Petrov", role="Head of Content, Volt Athletics", initials="JP", color="#FF4D1A"),
    dict(quote="Feels like having an in-house editor who also does motion. Zero hand-holding needed.", name="Amara Osei", role="Creator · 310k subscribers", initials="AO", color="#1B8F5A"),
]
packages = [
    dict(name="Starter", tag="Shorts only", price="$890", desc="For creators posting three to four times a week who need a reliable editor.", featured=False, features=["8 short-form edits per month", "Captions and sound design", "Two revision rounds", "48h turnaround"]),
    dict(name="Retainer", tag="Shorts + long-form", price="$1,900", desc="The full channel: shorts, two long-form videos and thumbnails, every month.", featured=True, features=["16 shorts + 2 long-form videos", "Thumbnails and titles included", "Priority queue, weekly call", "Frame.io review workflow"]),
    dict(name="Studio", tag="Unlimited", price="$3,400", desc="Unlimited requests, one at a time. Motion, packaging and 24h turnaround.", featured=False, features=["Unlimited requests, one active", "Motion graphics and channel package", "24h turnaround on shorts", "Slack access and monthly strategy call"]),
]
addons = [
    dict(title="Rush delivery", text="Shorts in 24h, long-form in 72h.", unit="per video", price="+50%"),
    dict(title="Extra revision round", text="Beyond the two included rounds.", unit="per round", price="$60"),
    dict(title="Vertical cutdowns", text="From an existing long-form edit.", unit="per clip", price="$45"),
    dict(title="Color grade", text="DaVinci grade for brand films.", unit="per minute", price="$120"),
    dict(title="Voice-over sourcing", text="Casting and direction, VO fee separate.", unit="per project", price="$150"),
    dict(title="Channel audit", text="Retention review of your last 10 videos.", unit="one-off", price="$390"),
]
faq = [
    dict(q="How do I send you footage?", a="Google Drive, Dropbox or Frame.io. For anything over 50 GB I set up a transfer link. Proxies are fine if the originals are on the way."),
    dict(q="What’s your turnaround?", a="Shorts: 48 hours. Long-form: five working days from full footage. Retainer clients get a priority queue and Studio gets 24 hours."),
    dict(q="Do you work with raw or already-scripted content?", a="Both. I can build a story from raw talking-head footage, or follow a script and shot list to the frame."),
    dict(q="Which tools do you use?", a="Premiere Pro and After Effects for editing and motion, DaVinci Resolve for color, Frame.io for review. Project files are yours on request."),
    dict(q="Can I cancel a retainer?", a="Yes, monthly. No long contracts — pause or cancel with seven days’ notice and unused videos roll over once."),
    dict(q="Do you offer thumbnails and titles too?", a="Yes. Packaging is included in Retainer and Studio, or bookable per video at $60 per thumbnail with three concepts."),
]
tools = ["Premiere Pro", "After Effects", "DaVinci Resolve", "CapCut", "Frame.io", "Figma", "Descript", "Notion"]
timeline = [
    dict(year="2018", title="First paid edit", text="Skate videos and local music clips. Learned pacing before I learned color."),
    dict(year="2020", title="Post house, Berlin", text="Two years of commercials and brand films. Learned the client side of the timeline."),
    dict(year="2022", title="Went independent", text="First creator clients. Built the short-form pipeline that still runs today."),
    dict(year="2024", title="Motion crew", text="Added a two-person motion team for title sequences and channel packages."),
    dict(year="2026", title="120M+ views", text="Across client channels. Four of them crossed one million subscribers."),
]

pages = [
    ("index.html", "index.html", dict(page_id="home", title="Video editor for creators & brands", description="Noa Keller — video editor and motion designer for creators and brands. Short-form that hooks, long-form that holds. Book a call.")),
    ("work.html", "work.html", dict(page_id="work", title="Work", description="Short-form, long-form, ads and motion work by Noa Keller, filterable by format.")),
    ("project.html", "project.html", dict(page_id="project", title="The 4-hour cut — case study", description="How a 4-hour founder interview became a 14-minute documentary that 1.1 million people watched.")),
    ("services.html", "services.html", dict(page_id="services", title="Services & packages", description="Short-form editing, long-form YouTube, motion & titles, thumbnails. Public pricing and monthly packages.")),
    ("about.html", "about.html", dict(page_id="about", title="About", description="Eight years in the timeline: how Noa Keller works, tools, clients and story.")),
    ("contact.html", "contact.html", dict(page_id="contact", title="Contact", description="Send a brief and get a plan and price within one working day. Or book a 20-minute call.")),
    ("404.html", "404.html", dict(page_id="notfound", title="Page not found", description="This clip got cut in the edit.")),
    ("legal.html", "legal.html", dict(page_id="legal", title="Privacy & imprint", description="Legal information for this website.")),
    ("start-here.html", "start-here.html", dict(page_id="start", title="Start here — template guide", description="Customization guide shipped with the Playhead template.")),
    ("lite.html", "lite.html", dict(page_id="lite", title="Playhead Lite — free one-page portfolio", description="Free one-page version of the Playhead template for video editors.")),
]
ctx = dict(site=site, clients=clients, reels=reels, projects=projects, work=work, services=services, process=process,
           testimonials=testimonials, packages=packages, addons=addons, faq=faq, tools=tools, timeline=timeline,
           arrow=ARROW, tick=TICK, plus=PLUS, star=STAR)
for tpl, out, extra in pages:
    html = env.get_template(tpl).render(**ctx, **extra)
    with open(os.path.join(OUT, out), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", out, len(html))
