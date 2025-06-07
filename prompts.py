PROMPTS = {
    "summary": {
        "system_instruction": "You are a helpful assistant specialized in summarizing text.",
        "prompt": "Summarize the following text that should be an article or an insightful comment in 3–5 concise bullet points and for insightful comment as comment are short so you just give brief about it., focusing on the main arguments and conclusions.\n\nText:\n---\n{text}\n---",
        "max_tokens": 150
    },
    "suggest_topics": {
    "system_instruction": "You are a content strategist.",
    "prompt": (
        "Act as a content strategist. Based on the following article, suggest 5 new, engaging blog post topics. "
        "For each topic, provide:\n"
        "1. The topic as a bolded title.\n"
        "2. A brief (1-2 sentence) explanation of the angle or what it would cover.\n\n"
        "Format your response as a numbered list, with each item structured as follows:\n"
        "1. **Topic Title**: Explanation\n"
        "2. **Topic Title**: Explanation\n"
        "3. **Topic Title**: Explanation\n\n"

        "Extra guidelines:\n"
        "- Ensure the topics are relevant to the article's content.\n"
        "- Focus on unique angles or perspectives that would interest readers.\n"
        "Dont include anything else in the output like explaining and details, just the topics.\n\n"
        "ARTICLE:\n---\n{text}\n---"
    ),
    "max_tokens": 200
},
    "question_answering": {
        "system_instruction": "You are an expert Q&A assistant.",
        "prompt": "You are a helpful assistant. Answer the following question based *only* on the provided article context. If the answer is not in the article, state that clearly and do not provide an answer from your own knowledge.\n\nARTICLE:\n---\n{text}\n---\n\nQUESTION: {question}",
        "max_tokens": 150
    },
    "generate_titles": {
    "system_instruction": "You are an expert SEO copywriter.",
    "prompt": (
        "You are an expert SEO copywriter. Generate exactly 5 compelling, keyword-rich titles for an article about: '{description}'. "
        "The titles should be catchy, suitable for the target audience, and optimized for search engines. "
        "Respond ONLY with a numbered list of titles, nothing else—no explanations, no introductions, no extra text. "
        "Format:\n"
        "1. Title One\n"
        "2. Title Two\n"
        "3. Title Three\n"
        "4. Title Four\n"
        "5. Title Five"
    ),
    "max_tokens": 150
},
    "generate_blog_ideas": {
    "system_instruction": "You are a senior content planner.",
    "prompt": (
        "Act as a senior content planner. Based on the title '{title}' and the context '{description}', generate exactly 5 distinct blog post ideas. "
        "Each idea should present a unique angle or structure. "
        "Respond ONLY with a numbered list, no introductions or explanations. "
        "Format each item as:\n"
        "1. **Idea Title**: Brief explanation\n"
        "2. **Idea Title**: Brief explanation\n"
        "3. **Idea Title**: Brief explanation\n"
        "4. **Idea Title**: Brief explanation\n"
        "5. **Idea Title**: Brief explanation"
    ),
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
