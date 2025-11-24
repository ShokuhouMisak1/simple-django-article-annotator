# simple-django-article-annotator
LifelongLearningLab-Fall25-Task
A Django-based web application for reading articles, highlighting text, and taking smart notes. This project features an interactive UI for text annotation and integrates with Hugging Face's BART model for AI-powered summarization.

## Features

### Core Functionality
* **Dual-Pane Interface:** A clean layout displaying the article text on one side and a dedicated note-taking area on the other.
* **Interactive Highlighting:** Select any text within the article to highlight it instantly.
* **Contextual Notes:** Add notes specifically linked to highlighted text.
    * *Format:* Automatically saves as `"[selected text]: [note]"` to retain context.
* **Visual Connection:** Clicking on a highlighted section in the text automatically brings the corresponding note into focus.
* **Flexible Management:** Create, read, edit, and delete notes seamlessly.
* **Persistence:** All articles, highlights, and notes are stored in the database and retrieved upon page reload.

### Features
* **Multi-Article Support:** Dynamic routing allows multiple articles to be stored and accessed via unique URLs.
* **AI-Powered Summarization:** Integrated with the **Facebook BART Large CNN** model (via Hugging Face). When selecting text to add a note, the AI automatically generates a summary suggestion for the selected content.
