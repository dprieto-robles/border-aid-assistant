# 🌎 Border Aid Assistant

An AI chatbot built with LangChain and Groq that raises awareness about the
humanitarian crisis at the U.S.-Mexico border.

**[Try the Live Chatbot Here](https://huggingface.co/spaces/dprieto-robles/border-aid-assistant)**

---

## Overview

The Border Aid Assistant is a conversational AI chatbot that provides factual,
compassionate information about humanitarian aid organizations, border crossing
corridors, and migrant death statistics along the U.S.-Mexico border. It is
designed for students, journalists, researchers, and anyone interested in
understanding the scale of the border humanitarian crisis.

---

## The Problem

Earlier this year I visited the Kino Border Initiative in Nogales, Arizona and
learned firsthand about the humanitarian crisis unfolding along the U.S.-Mexico
border. Information about aid organizations, crossing corridor dangers, and
migrant death statistics is scattered across dozens of websites, datasets, and
news sources. People who want to learn, volunteer, or report on this crisis
often struggle to find clear consolidated information in one place. This
chatbot brings that information together in a conversational format that is
easy to access and understand.

---

## How It Works

The chatbot uses a LangChain-powered routing system that directs user questions
to one of three specialized tools based on the topic of the question.

**Tool 1: Organization Info**
Answers questions about Kino Border Initiative, No More Deaths, Humane Borders,
and Border Angels including their founding, location, focus, and programs.

**Tool 2: Corridor Risk Info**
Answers questions about six major border crossing corridors including their
risk level, primary causes of death, and humanitarian organizations active in
each area.

**Tool 3: Migrant Death Data**
Answers questions about migrant death statistics sourced from the Humane Borders
Arizona OpenGIS Initiative and the No More Deaths Border Death Database,
including yearly trends, causes of death, body conditions, and identification
rates.

---

## Key Findings and What I Learned

Building this chatbot taught me how powerful LangChain's tool routing is for
creating focused domain-specific AI assistants. Rather than trying to cram all
the information into a single prompt, separating the data into three distinct
tools made the bot faster, more accurate, and easier to maintain. Working with
the data also reinforced how sparse and sobering the information about migrant
deaths really is — 93 percent of 2025 deaths in Pima County involved skeletal
remains or undetermined causes, meaning most of these people died anonymously
and were found long after the fact.

What was harder than expected was navigating version conflicts between different
LangChain packages and model API rate limits. I originally attempted to use
Google Gemini but hit free tier exhaustion almost immediately, which led me to
switch to Groq and the Llama 3.3 model — a change that ultimately made the app
faster and more reliable.

---

## Sample Conversations

**Conversation 1: Organization Info Tool**

> **User**: What does the Kino Border Initiative do?
>
> **Bot**: The Kino Border Initiative's mission is to provide humanitarian aid
> and advocacy for migrants and deportees. Their activities include operating
> a comedor (dining hall) to provide meals, offering shelter support, running
> a legal aid clinic, conducting medical outreach, and hosting specialized
> volunteering opportunities for students in social work, medicine, and law.

**Conversation 2: Corridor Risk Tool**

> **User**: How dangerous is the Tucson corridor?
>
> **Bot**: The Tucson corridor has an Extreme danger level. It is considered
> one of the deadliest crossing corridors in the United States, with migrants
> facing extreme heat, dehydration, and rough terrain in the Sonoran Desert.

**Conversation 3: Migrant Death Data Tool**

> **User**: How many migrants died in 2025?
>
> **Bot**: According to the data, there were 28 recorded migrant deaths along
> the U.S.-Mexico border from January through April 2025.

---

## How to Run Locally

**1. Clone the repository:**

    git clone https://github.com/dprieto-robles/border-aid-assistant.git
    cd border-aid-assistant

**2. Install dependencies:**

    pip install -r requirements.txt

**3. Set your Groq API key as an environment variable:**

    export GROQ_API_KEY="your_key_here"

**4. Run the app:**

    python app.py
