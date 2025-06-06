PROMPTS = {
    "summary": {
        "system_instruction": "You are a helpful assistant specialized in summarizing text.",
        "prompt": "Summarize the following article in 3–5 concise bullet points, focusing on the main arguments and conclusions.\n\nARTICLE:\n---\n{text}\n---",
        "max_tokens": 150
    },
    "suggest_topics": {
        "system_instruction": "You are a content strategist.",
        "prompt": "Act as a content strategist. Based on the following article, suggest 3 new, engaging blog post topics. For each topic, provide a brief (1-2 sentence) explanation of the angle or what it would cover. Format the output as a numbered list.\n\nARTICLE:\n---\n{text}\n---",
        "max_tokens": 200
    },
    "question_answering": {
        "system_instruction": "You are an expert Q&A assistant.",
        "prompt": "You are a helpful assistant. Answer the following question based *only* on the provided article context. If the answer is not in the article, state that clearly and do not provide an answer from your own knowledge.\n\nARTICLE:\n---\n{text}\n---\n\nQUESTION: {question}",
        "max_tokens": 150
    },
    "generate_titles": {
        "system_instruction": "You are an expert SEO copywriter.",
        "prompt": "You are an expert SEO copywriter. Generate 5 compelling, keyword-rich titles for an article about: '{description}'. The titles should be catchy and suitable for the target audience.",
        "max_tokens": 150
    },
    "generate_blog_ideas": {
        "system_instruction": "You are a senior content planner.",
        "prompt": "Act as a senior content planner. Based on the title '{title}' and the context '{description}', generate 5 distinct blog post ideas. Each idea should present a unique angle or structure. Format as a numbered list.",
        "max_tokens": 500
    },
    "generate_article": {
        "system_instruction": "You are a professional blog writer.",
        "prompt": """Act as an expert blog writer with strong SEO knowledge. Your task is to write a complete, high-quality blog post.

Follow these instructions carefully:
1.  Use the provided Title and chosen Blog Idea as your primary guide.
2.  The target context is: {description}.
3.  Write in a clear, engaging, and professional tone.
4.  Structure the article with Markdown for formatting (e.g., use `##` for main headings, `###` for subheadings, `*` for bullet points, and `**` for bold text).
5.  Incorporate relevant keywords naturally throughout the text.
6.  Ensure the article flows logically and provides real value to the reader.

---
TITLE: {title}
CHOSEN BLOG IDEA: {blog_idea}
---

Begin writing the article now.""",
        "max_tokens": 2048 # Increased for full article generation
    }
}